from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
import time
import uuid
import zipfile
from pathlib import Path
from typing import Any, Dict
from xml.sax.saxutils import escape

from flask import Flask, abort, jsonify, request, send_file


APP_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = APP_ROOT / "engine"
JOBS_ROOT = Path(os.getenv("JOBS_ROOT", "/tmp/gpt-image2-ppt-jobs"))
JOBS_ROOT.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
jobs: Dict[str, Dict[str, Any]] = {}


STYLE_OPTIONS = [
    "clean-tech-blue",
    "gradient-glass",
    "dark-aurora",
    "editorial-mono",
    "vector-illustration",
    "risograph",
    "japanese-wabi",
    "swiss-grid",
    "hand-sketch",
    "y2k-chrome",
]


def _safe_title(value: str) -> str:
    clean = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", value).strip()
    return clean[:80] or "GPT Image2 PPT"


def _default_plan(topic: str, slide_count: int) -> str:
    topic = _safe_title(topic)
    slide_count = max(1, min(int(slide_count or 5), 12))
    sections = [
        f"## 1. [cover] {topic}\n副标题：由 gpt-image-2 生成的视觉演示\n日期：2026\n",
    ]
    templates = [
        ("content", "背景与机会", ["行业变化", "用户痛点", "为什么现在值得做"]),
        ("content", "核心方案", ["产品定位", "关键能力", "差异化体验"]),
        ("data", "关键指标", ["效率提升：3 倍", "成本下降：40%", "交付周期：从天到小时"]),
        ("content", "落地路径", ["第一阶段：验证", "第二阶段：规模化", "第三阶段：生态扩展"]),
        ("data", "总结与下一步", ["一句话结论", "优先行动", "预期收益"]),
        ("content", "目标用户", ["核心人群", "使用场景", "决策因素"]),
        ("content", "竞争优势", ["速度", "质量", "自动化"]),
        ("data", "投入产出", ["时间节省", "费用节省", "复用价值"]),
        ("content", "风险与应对", ["质量校验", "合规边界", "流程兜底"]),
        ("content", "路线图", ["近期", "中期", "长期"]),
        ("data", "最终结论", ["值得投入", "快速试点", "持续迭代"]),
    ]
    for idx in range(2, slide_count + 1):
        page_type, title, bullets = templates[(idx - 2) % len(templates)]
        body = "\n".join(f"- {item}" for item in bullets)
        sections.append(f"## {idx}. [{page_type}] {title}\n{body}\n")
    return f"---\ntitle: {topic}\n---\n\n" + "\n".join(sections)


def _write_zip(output_dir: Path) -> Path:
    zip_path = output_dir / "gpt-image2-ppt-output.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in output_dir.rglob("*"):
            if path == zip_path or not path.is_file():
                continue
            zf.write(path, path.relative_to(output_dir))
    return zip_path


def _rels_xml(items: list[tuple[str, str, str]]) -> str:
    rels = "\n".join(
        f'  <Relationship Id="{rid}" Type="{rtype}" Target="{escape(target)}"/>'
        for rid, rtype, target in items
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        f"{rels}\n"
        "</Relationships>"
    )


def _build_simple_pptx(output_dir: Path, title: str) -> Path:
    """Create a valid image-only 16:9 PPTX without python-pptx."""
    images = sorted((output_dir / "images").glob("slide-*.png"))
    if not images:
        raise RuntimeError("No slide images found for PPTX generation")

    safe_title = re.sub(r"[^A-Za-z0-9_\-\u4e00-\u9fff]+", "_", title).strip("_") or "gpt-image2-ppt"
    pptx_path = output_dir / f"{safe_title}.pptx"
    cx, cy = 12192000, 6858000

    content_overrides = "\n".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, len(images) + 1)
    )
    slide_ids = "\n".join(
        f'    <p:sldId id="{255 + i}" r:id="rId{i + 1}"/>'
        for i in range(1, len(images) + 1)
    )
    presentation_rels = [
        (
            "rId1",
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster",
            "slideMasters/slideMaster1.xml",
        )
    ] + [
        (
            f"rId{i + 1}",
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide",
            f"slides/slide{i}.xml",
        )
        for i in range(1, len(images) + 1)
    ]

    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Image2">
  <a:themeElements>
    <a:clrScheme name="Image2">
      <a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F2937"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="1155CC"/></a:accent1><a:accent2><a:srgbClr val="059669"/></a:accent2>
      <a:accent3><a:srgbClr val="D97706"/></a:accent3><a:accent4><a:srgbClr val="7C3AED"/></a:accent4>
      <a:accent5><a:srgbClr val="DC2626"/></a:accent5><a:accent6><a:srgbClr val="0891B2"/></a:accent6>
      <a:hlink><a:srgbClr val="1155CC"/></a:hlink><a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Image2"><a:majorFont><a:latin typeface="Arial"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="Image2">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/><a:extraClrSchemeLst/>
</a:theme>"""

    def group_shape_xml() -> str:
        return (
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        )

    with zipfile.ZipFile(pptx_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
{content_overrides}
</Types>""",
        )
        zf.writestr(
            "_rels/.rels",
            _rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                    ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
                ]
            ),
        )
        zf.writestr(
            "docProps/core.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>{escape(title)}</dc:title>
</cp:coreProperties>""",
        )
        zf.writestr(
            "docProps/app.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>GPT Image2 PPT App</Application><Slides>{len(images)}</Slides>
</Properties>""",
        )
        zf.writestr(
            "ppt/presentation.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>
{slide_ids}
  </p:sldIdLst>
  <p:sldSz cx="{cx}" cy="{cy}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>""",
        )
        zf.writestr("ppt/_rels/presentation.xml.rels", _rels_xml(presentation_rels))
        zf.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>{group_shape_xml()}</p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>""",
        )
        zf.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            _rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
                ]
            ),
        )
        zf.writestr(
            "ppt/slideLayouts/slideLayout1.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree>{group_shape_xml()}</p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>""",
        )
        zf.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            _rels_xml([("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml")]),
        )
        zf.writestr("ppt/theme/theme1.xml", theme_xml)

        for i, image_path in enumerate(images, start=1):
            media_name = f"image{i}.png"
            zf.write(image_path, f"ppt/media/{media_name}")
            zf.writestr(
                f"ppt/slides/slide{i}.xml",
                f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>{group_shape_xml()}<p:pic><p:nvPicPr><p:cNvPr id="4" name="{escape(image_path.name)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>""",
            )
            zf.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                _rels_xml(
                    [
                        ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", f"../media/{media_name}"),
                        ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                    ]
                ),
            )
    return pptx_path


def _run_job(job_id: str, payload: Dict[str, Any]) -> None:
    job = jobs[job_id]
    work_dir = JOBS_ROOT / job_id
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        job["status"] = "running"
        job["message"] = "Preparing slide plan"

        topic = _safe_title(payload.get("topic") or "GPT Image2 PPT")
        slide_count = int(payload.get("slideCount") or 5)
        style = payload.get("style") if payload.get("style") in STYLE_OPTIONS else "clean-tech-blue"
        plan_md = (payload.get("slidesMarkdown") or "").strip() or _default_plan(topic, slide_count)

        plan_md_path = work_dir / "slides_plan.md"
        plan_json_path = work_dir / "slides_plan.json"
        output_dir = work_dir / "output"
        plan_md_path.write_text(plan_md, encoding="utf-8")

        env = os.environ.copy()
        env.setdefault("OPENAI_BASE_URL", "https://apihk.unifyllm.top")
        env["GPT_IMAGE_MODEL_NAME"] = "gpt-image-2"
        env["GPT_IMAGE_ENDPOINT"] = "images"
        env["GPT_IMAGE_QUALITY"] = payload.get("quality") or env.get("GPT_IMAGE_QUALITY", "high")
        env["GPT_IMAGE_CONCURRENCY"] = str(max(1, min(int(payload.get("concurrency") or env.get("GPT_IMAGE_CONCURRENCY", 2)), 4)))
        if not env.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not configured in the app runtime")

        job["message"] = "Converting Markdown to JSON"
        subprocess.run(
            ["python", str(ENGINE_ROOT / "scripts" / "md_to_plan.py"), str(plan_md_path), "-o", str(plan_json_path)],
            cwd=work_dir,
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )

        job["message"] = "Generating slide images with gpt-image-2"
        cmd = [
            "python",
            str(ENGINE_ROOT / "scripts" / "generate_ppt.py"),
            "--plan",
            str(plan_json_path),
            "--style",
            str(ENGINE_ROOT / "styles" / f"{style}.md"),
            "--output",
            str(output_dir),
            "--concurrency",
            env["GPT_IMAGE_CONCURRENCY"],
        ]
        proc = subprocess.run(cmd, cwd=work_dir, env=env, text=True, capture_output=True, timeout=3600)
        job["log"] = (proc.stdout or "")[-12000:] + ("\n" + (proc.stderr or "")[-4000:] if proc.stderr else "")
        if proc.returncode != 0:
            raise RuntimeError(f"generate_ppt.py failed with code {proc.returncode}")

        prompts = json.loads((output_dir / "prompts.json").read_text(encoding="utf-8"))
        meta = prompts.get("metadata", {})
        if meta.get("model") != "gpt-image-2":
            raise RuntimeError(f"Unexpected model in prompts.json: {meta.get('model')}")

        pptx_files = sorted(output_dir.glob("*.pptx"))
        if not pptx_files:
            pptx_files = [_build_simple_pptx(output_dir, topic)]
        zip_path = _write_zip(output_dir)
        job.update(
            status="done",
            message="Done",
            outputDir=str(output_dir),
            html=str(output_dir / "index.html"),
            pptx=str(pptx_files[0]) if pptx_files else None,
            zip=str(zip_path),
            model=meta.get("model"),
            endpoint=meta.get("endpoint"),
            baseUrlHost=meta.get("base_url_host"),
        )
    except Exception as exc:
        job["status"] = "failed"
        job["message"] = str(exc)


@app.get("/health")
def health():
    return {"ok": True, "model": "gpt-image-2"}


@app.get("/")
def index():
    return """<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GPT Image2 PPT App</title>
  <style>
    body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fb;color:#0f172a}
    main{max-width:1040px;margin:0 auto;padding:32px 20px 48px}
    h1{font-size:34px;margin:0 0 8px}
    p{color:#526071;line-height:1.6}
    section{background:white;border:1px solid #e2e8f0;border-radius:8px;padding:20px;margin-top:18px}
    label{display:block;font-weight:700;margin:14px 0 6px}
    input,select,textarea{width:100%;box-sizing:border-box;border:1px solid #cbd5e1;border-radius:6px;padding:10px;font:inherit}
    textarea{min-height:220px}
    button{margin-top:16px;background:#1155cc;color:white;border:0;border-radius:6px;padding:12px 16px;font-weight:700;cursor:pointer}
    button:disabled{opacity:.55;cursor:not-allowed}
    .row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}
    .status{white-space:pre-wrap;background:#0f172a;color:#dbeafe;border-radius:8px;padding:14px;min-height:96px}
    a{color:#1155cc;font-weight:700}
  </style>
</head>
<body>
<main>
  <h1>GPT Image2 PPT App</h1>
  <p>确定性后端直接调用 <code>gpt-image-2</code>，生成 16:9 PNG、HTML viewer 和 PPTX。不会调用 Profy 聊天框架的 image tool。</p>
  <section>
    <label>主题</label>
    <input id="topic" value="AI 产品发布演示" />
    <div class="row">
      <div><label>页数</label><input id="slideCount" type="number" min="1" max="12" value="5" /></div>
      <div><label>风格</label><select id="style"></select></div>
      <div><label>质量</label><select id="quality"><option>high</option><option>medium</option><option>low</option></select></div>
    </div>
    <label>可选：直接粘贴 slides_plan.md</label>
    <textarea id="slidesMarkdown" placeholder="留空则按主题自动生成一个结构化草稿"></textarea>
    <button id="start">生成 PPT</button>
  </section>
  <section>
    <h2>状态</h2>
    <div class="status" id="status">等待开始</div>
    <div id="links"></div>
  </section>
</main>
<script>
const styles = """ + json.dumps(STYLE_OPTIONS) + """;
const styleSelect = document.getElementById('style');
styles.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; styleSelect.appendChild(o); });
async function poll(id){
  const res = await fetch('/api/jobs/'+id);
  const job = await res.json();
  document.getElementById('status').textContent = JSON.stringify(job, null, 2);
  if(job.status === 'done'){
    document.getElementById('links').innerHTML =
      '<p><a href="/api/jobs/'+id+'/file?kind=html" target="_blank">打开 HTML viewer</a></p>' +
      '<p><a href="/api/jobs/'+id+'/file?kind=pptx">下载 PPTX</a></p>' +
      '<p><a href="/api/jobs/'+id+'/file?kind=zip">下载完整 ZIP</a></p>';
    document.getElementById('start').disabled = false;
  } else if(job.status === 'failed'){
    document.getElementById('start').disabled = false;
  } else {
    setTimeout(() => poll(id), 3000);
  }
}
document.getElementById('start').onclick = async () => {
  document.getElementById('start').disabled = true;
  document.getElementById('links').innerHTML = '';
  const payload = {
    topic: document.getElementById('topic').value,
    slideCount: document.getElementById('slideCount').value,
    style: document.getElementById('style').value,
    quality: document.getElementById('quality').value,
    slidesMarkdown: document.getElementById('slidesMarkdown').value
  };
  const res = await fetch('/api/jobs', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  const data = await res.json();
  poll(data.jobId);
};
</script>
</body>
</html>"""


@app.post("/api/jobs")
def create_job():
    payload = request.get_json(force=True, silent=True) or {}
    job_id = uuid.uuid4().hex[:12]
    jobs[job_id] = {"id": job_id, "status": "queued", "message": "Queued", "createdAt": time.time()}
    thread = threading.Thread(target=_run_job, args=(job_id, payload), daemon=True)
    thread.start()
    return jsonify({"jobId": job_id})


@app.get("/api/jobs/<job_id>")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        abort(404)
    public = {k: v for k, v in job.items() if k not in {"outputDir", "html", "pptx", "zip"}}
    return jsonify(public)


@app.get("/api/jobs/<job_id>/file")
def get_file(job_id: str):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        abort(404)
    kind = request.args.get("kind", "zip")
    key = {"html": "html", "pptx": "pptx", "zip": "zip"}.get(kind)
    if not key or not job.get(key):
        abort(404)
    path = Path(job[key])
    if not path.exists():
        abort(404)
    return send_file(path, as_attachment=(kind != "html"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
