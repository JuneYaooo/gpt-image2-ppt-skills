#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性脚本：把 styles/ 下 10 个风格各出一张 16:9 封面图，

主题统一为「如何用 gpt-image-2 做 PPT」，然后拼成 2x5 画廊。

    python3 scripts/generate_style_gallery.py

产物：
    docs/assets/gallery/<style-id>.png       ---- 10 张单图
    docs/assets/style-gallery.png            ---- 2 行 x 5 列拼图
"""

from __future__ import annotations

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_ppt import find_and_load_env  # noqa: E402
from image_generator import GptImage2Generator  # noqa: E402


STYLES_DIR = ROOT / "styles"
OUT_DIR = ROOT / "docs" / "assets" / "gallery"
GRID_PATH = ROOT / "docs" / "assets" / "style-gallery.jpg"
GRID_MAX_WIDTH = 3000  # 拼图最终宽度上限，超过会等比缩放

# 画廊排布：2 行 x 5 列（按风格分组，每行 5 个）
GRID_ORDER = [
    "gradient-glass",
    "clean-tech-blue",
    "editorial-mono",
    "dark-aurora",
    "risograph",
    "japanese-wabi",
    "swiss-grid",
    "hand-sketch",
    "y2k-chrome",
    "vector-illustration",
]

# 每张图统一的"内容"：一张封面页，主题 = 如何用 gpt-image-2 做 PPT
SHARED_COVER_BRIEF = """
【这张图的内容 ---- 所有风格统一】
这是一页"演示封面"，需要在画面里清晰呈现文字，按下方层级排布：

- 主标题（最大字号）：如何用 gpt-image-2 做 PPT
- 副标题（中等字号）：从一句话 Prompt 到 16:9 幻灯片
- 角标 / 页脚（小字号）：gpt-image2-ppt-skills · 2026

要求：
1. 主标题必须是中文，大且清晰，占画面视觉中心或左侧主体。
2. 副标题用中文，字号明显小于主标题。
3. 页脚那一行英文可保留。
4. 不要出现除以上三行外的其它大段说明文字。
5. 严格按本风格的配色、版式、装饰元素、留白节奏生成；不要混入别的风格元素。
6. 16:9 横版宽屏，宽明显大于高。
"""


def load_style_prompt(style_id: str) -> str:
    path = STYLES_DIR / f"{style_id}.md"
    text = path.read_text(encoding="utf-8")
    # 取 "## 基础提示词模板" 到下一个 "## " 之间的内容
    m = re.search(r"## 基础提示词模板\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"没在 {path} 里找到 '## 基础提示词模板' 段落")
    return m.group(1).strip()


def build_prompt(style_id: str) -> str:
    base = load_style_prompt(style_id)
    return (
        base
        + "\n\n"
        + "【当前任务：生成封面页】\n"
        + "请严格按上方该风格的『封面页构图』章节布局。\n"
        + SHARED_COVER_BRIEF.strip()
    )


def generate_one(style_id: str, generator: GptImage2Generator) -> Path:
    out_path = OUT_DIR / f"{style_id}.png"
    if out_path.exists() and out_path.stat().st_size > 10_000:
        print(f"[skip] {style_id} 已存在 -> {out_path}")
        return out_path
    prompt = build_prompt(style_id)
    print(f"\n=== 生成 {style_id} ===")
    generator.generate_scene_image(
        {"index": style_id, "image_prompt": prompt},
        str(out_path),
    )
    return out_path


def stitch_grid(image_paths: list[Path], cols: int = 5, cell_w: int = 960) -> Path:
    """把 N 张图缩放到统一宽度后按 cols 列拼成网格。"""
    imgs = [Image.open(p).convert("RGB") for p in image_paths]
    # 统一等比缩放到 cell_w
    resized = []
    for im in imgs:
        ratio = cell_w / im.width
        resized.append(im.resize((cell_w, int(im.height * ratio)), Image.LANCZOS))
    cell_h = max(im.height for im in resized)
    rows = (len(resized) + cols - 1) // cols
    gap = 16
    W = cell_w * cols + gap * (cols + 1)
    H = cell_h * rows + gap * (rows + 1)
    canvas = Image.new("RGB", (W, H), (250, 250, 252))
    for i, im in enumerate(resized):
        r, c = divmod(i, cols)
        x = gap + c * (cell_w + gap)
        y = gap + r * (cell_h + gap)
        canvas.paste(im, (x, y))
    if canvas.width > GRID_MAX_WIDTH:
        ratio = GRID_MAX_WIDTH / canvas.width
        canvas = canvas.resize(
            (GRID_MAX_WIDTH, int(canvas.height * ratio)), Image.LANCZOS
        )
    GRID_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(GRID_PATH, format="JPEG", quality=88, optimize=True, progressive=True)
    return GRID_PATH


def main() -> int:
    find_and_load_env()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    generator = GptImage2Generator(aspect_ratio="16:9")

    # 并发生成：10 个并行，和默认 skill 的 10 路并发一致
    max_workers = int(os.getenv("GALLERY_CONCURRENCY", "10"))
    results: dict[str, Path] = {}
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(generate_one, sid, generator): sid for sid in GRID_ORDER}
        for fut in as_completed(futures):
            sid = futures[fut]
            try:
                results[sid] = fut.result()
            except Exception as e:
                errors[sid] = str(e)[:300]
                print(f"[FAIL] {sid}: {e}")

    if errors:
        print("\n失败清单：")
        for sid, msg in errors.items():
            print(f"  - {sid}: {msg}")

    ok_paths = [results[sid] for sid in GRID_ORDER if sid in results]
    if len(ok_paths) < len(GRID_ORDER):
        print(f"\n(!) 只有 {len(ok_paths)}/{len(GRID_ORDER)} 张成功，仍尝试拼图")

    if not ok_paths:
        print("没有可用图片，放弃拼图")
        return 1

    grid = stitch_grid(ok_paths, cols=5)
    print(f"\n[OK] 拼图已保存: {grid}")
    print(f"[OK] 单图目录:   {OUT_DIR}")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
