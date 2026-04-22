#!/usr/bin/env python3
"""Render a .pptx template to per-page PNGs.

Backends, in priority order:
  PPTX → PDF: native LibreOffice CLI > docker linuxserver/libreoffice
  PDF → PNG:  pymupdf > pdf2image (needs poppler)

Default output: <cwd>/template_renders/<pptx_stem>/page-NN.png
Intermediate PDF goes to <out_dir>/_source.pdf and is left in place
for inspection (gitignored under template_renders/).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional


DEFAULT_RENDERS_DIR_NAME = "template_renders"
DOCKER_IMAGE = "linuxserver/libreoffice:latest"


def _safe_stem(name: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", name).strip("_")
    return cleaned[:80] or "template"


def default_out_dir(pptx_path: Path) -> Path:
    return Path.cwd() / DEFAULT_RENDERS_DIR_NAME / _safe_stem(pptx_path.stem)


def render_pptx_to_pngs(
    pptx_path: str | Path,
    out_dir: Optional[Path] = None,
    dpi: int = 144,
    force: bool = False,
) -> Path:
    """Render every slide of pptx to PNGs. Returns the directory containing PNGs."""
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    if out_dir is None:
        out_dir = default_out_dir(pptx_path)
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not force:
        existing = sorted(out_dir.glob("page-*.png"))
        if existing:
            print(f"📦 已渲染 {len(existing)} 页 → {out_dir}（用 --force 强制重渲）")
            return out_dir

    pdf_path = out_dir / "_source.pdf"
    print(f"🖨️  PPTX → PDF：{pptx_path.name}")
    _convert_pptx_to_pdf(pptx_path, pdf_path)

    print(f"🖼️  PDF → PNG（dpi={dpi}）...")
    n = _rasterize_pdf(pdf_path, out_dir, dpi=dpi)
    print(f"✅ 渲染 {n} 页 → {out_dir}")
    return out_dir


def _convert_pptx_to_pdf(pptx_path: Path, out_pdf: Path) -> None:
    cli = shutil.which("libreoffice") or shutil.which("soffice")
    if cli:
        subprocess.run(
            [cli, "--headless", "--convert-to", "pdf",
             "--outdir", str(out_pdf.parent), str(pptx_path)],
            check=True, capture_output=True, text=True,
        )
        produced = out_pdf.parent / f"{pptx_path.stem}.pdf"
        if not produced.exists():
            raise RuntimeError(f"LibreOffice 未产出 PDF：{produced}")
        produced.replace(out_pdf)
        return

    if shutil.which("docker"):
        inspect = subprocess.run(
            ["docker", "image", "inspect", DOCKER_IMAGE], capture_output=True
        )
        if inspect.returncode != 0:
            raise RuntimeError(
                f"docker 镜像 {DOCKER_IMAGE} 不在本地。\n"
                f"  先拉一次：docker pull {DOCKER_IMAGE}\n"
                "  或装本机 libreoffice：sudo apt-get install -y libreoffice"
            )
        out_dir = out_pdf.parent
        staging = out_dir / pptx_path.name
        copied_for_run = False
        if not staging.exists() or not staging.samefile(pptx_path):
            shutil.copy2(pptx_path, staging)
            copied_for_run = True
        try:
            subprocess.run(
                ["docker", "run", "--rm",
                 "-v", f"{out_dir}:/work",
                 "--entrypoint", "soffice",
                 DOCKER_IMAGE,
                 "--headless", "--convert-to", "pdf",
                 "--outdir", "/work", f"/work/{pptx_path.name}"],
                check=True, capture_output=True, text=True,
            )
            produced = out_dir / f"{pptx_path.stem}.pdf"
            if not produced.exists():
                raise RuntimeError(f"docker LibreOffice 未产出 PDF：{produced}")
            produced.replace(out_pdf)
        finally:
            if copied_for_run and staging.exists():
                staging.unlink()
        return

    raise RuntimeError(
        "没找到可用的 LibreOffice。任选一种装：\n"
        "  - 本机：sudo apt-get install -y libreoffice\n"
        f"  - Docker：docker pull {DOCKER_IMAGE}\n"
        "或者自己手动从 PowerPoint/Keynote 把每页导出 PNG，"
        "命名 page-01.png 起按字典序对应页码。"
    )


def _rasterize_pdf(pdf_path: Path, out_dir: Path, dpi: int = 144) -> int:
    pymupdf = None
    try:
        import pymupdf as _m  # type: ignore
        pymupdf = _m
    except ImportError:
        try:
            import fitz as _m  # type: ignore
            pymupdf = _m
        except ImportError:
            pass

    if pymupdf is not None:
        zoom = dpi / 72.0
        mat = pymupdf.Matrix(zoom, zoom)
        doc = pymupdf.open(str(pdf_path))
        n = len(doc)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=mat)
            pix.save(str(out_dir / f"page-{i+1:02d}.png"))
        doc.close()
        return n

    try:
        from pdf2image import convert_from_path  # type: ignore
    except ImportError:
        raise RuntimeError(
            "PDF → PNG 缺依赖。任选一种装：\n"
            "  - pip install pymupdf  （推荐，单装即可）\n"
            "  - pip install pdf2image && sudo apt-get install -y poppler-utils"
        )
    images = convert_from_path(str(pdf_path), dpi=dpi)
    for i, img in enumerate(images):
        img.save(str(out_dir / f"page-{i+1:02d}.png"), "PNG")
    return len(images)


def _cli() -> None:
    p = argparse.ArgumentParser(description="Render .pptx → per-page PNGs")
    p.add_argument("pptx", help="path to .pptx file")
    p.add_argument("-o", "--out", help="output directory (default: <cwd>/template_renders/<stem>/)")
    p.add_argument("--dpi", type=int, default=144, help="PNG dpi (default: 144)")
    p.add_argument("--force", action="store_true", help="re-render even if PNGs exist")
    args = p.parse_args()
    out_dir = render_pptx_to_pngs(
        args.pptx, Path(args.out) if args.out else None,
        dpi=args.dpi, force=args.force,
    )
    print()
    print(f"模板渲染目录：{out_dir}")
    print(f"喂给 generate_ppt.py：")
    print(f"  --template-pptx {args.pptx} \\")
    print(f"  --template-images {out_dir}")


if __name__ == "__main__":
    _cli()
