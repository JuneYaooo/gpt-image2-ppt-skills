from __future__ import annotations

import json
import mimetypes
import os
import re
import sys
import threading
import time
import types
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


class _DummyFlask:
    def __init__(self, *_args, **_kwargs):
        pass

    def get(self, *_args, **_kwargs):
        return lambda fn: fn

    def post(self, *_args, **_kwargs):
        return lambda fn: fn

    def run(self, *_args, **_kwargs):
        raise RuntimeError("Flask runtime is not available in stdlib mode")


def _abort(code: int):
    raise FileNotFoundError(code)


_fake_flask = types.ModuleType("flask")
_fake_flask.Flask = _DummyFlask
_fake_flask.abort = _abort
_fake_flask.jsonify = lambda value: value
_fake_flask.request = types.SimpleNamespace(args={}, get_json=lambda **_kwargs: {})
_fake_flask.send_file = lambda path, **_kwargs: path
sys.modules.setdefault("flask", _fake_flask)

from app import server as core  # noqa: E402


def html_with_asset_base(html: str, job_id: str) -> str:
    base_tag = f'<base href="/api/jobs/{job_id}/assets/">'
    if "<base " in html.lower():
        return html
    rewritten, count = re.subn(r"(<head[^>]*>)", rf"\1\n{base_tag}", html, count=1, flags=re.IGNORECASE)
    if count:
        return rewritten
    return f"{base_tag}\n{html}"


def resolve_job_asset(output_dir: str | Path, asset_path: str) -> Path | None:
    root = Path(output_dir).resolve()
    target = (root / asset_path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return None
    if not target.exists() or not target.is_file():
        return None
    return target


class Handler(BaseHTTPRequestHandler):
    server_version = "GPTImage2PPT/1.0"

    def _send_json(self, value: dict, status: int = 200) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, value: str, status: int = 200, content_type: str = "text/html; charset=utf-8") -> None:
        body = value.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, *, inline: bool) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "not found"}, 404)
            return
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(path.stat().st_size))
        disposition = "inline" if inline else "attachment"
        ascii_name = re.sub(r"[^A-Za-z0-9._-]+", "_", path.name).strip("_") or "download"
        self.send_header("Content-Disposition", f'{disposition}; filename="{ascii_name}"')
        self.end_headers()
        with path.open("rb") as f:
            while True:
                chunk = f.read(1024 * 128)
                if not chunk:
                    break
                self.wfile.write(chunk)

    def _send_html_file(self, path: Path, job_id: str) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "not found"}, 404)
            return
        body = html_with_asset_base(path.read_text(encoding="utf-8", errors="replace"), job_id).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        ascii_name = re.sub(r"[^A-Za-z0-9._-]+", "_", path.name).strip("_") or "index.html"
        self.send_header("Content-Disposition", f'inline; filename="{ascii_name}"')
        self.end_headers()
        self.wfile.write(body)

    def _public_base_url(self) -> str:
        proto = self.headers.get("X-Forwarded-Proto") or "https"
        host = self.headers.get("X-Forwarded-Host") or self.headers.get("Host") or ""
        if not host:
            return ""
        return f"{proto}://{host}"

    def _run_sync(self, payload: dict) -> None:
        job_id = uuid.uuid4().hex[:12]
        core.jobs[job_id] = {"id": job_id, "status": "queued", "message": "Queued", "createdAt": time.time()}
        core._run_job(job_id, payload)
        job = core.jobs[job_id]
        base = self._public_base_url()
        if job.get("status") != "done":
            self._send_json(
                {
                    "status": "failed",
                    "message": job.get("message"),
                    "log": job.get("log", ""),
                },
                500,
            )
            return

        links = {
            "html": f"{base}/api/jobs/{job_id}/file?kind=html",
            "pptx": f"{base}/api/jobs/{job_id}/file?kind=pptx",
            "zip": f"{base}/api/jobs/{job_id}/file?kind=zip",
        }
        self._send_json(
            {
                "status": "done",
                "jobId": job_id,
                "model": job.get("model"),
                "endpoint": job.get("endpoint"),
                "baseUrlHost": job.get("baseUrlHost"),
                "links": links,
                "message": "Generated with gpt-image-2. Use links.pptx for PowerPoint, links.html for browser preview, links.zip for all assets.",
            }
        )

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if parsed.path == "/health":
            self._send_json({"ok": True, "model": "gpt-image-2"})
            return

        if parsed.path == "/":
            self._send_text(core.index())
            return

        if len(parts) == 3 and parts[:2] == ["api", "jobs"]:
            job = core.jobs.get(parts[2])
            if not job:
                self._send_json({"error": "not found"}, 404)
                return
            public = {k: v for k, v in job.items() if k not in {"outputDir", "html", "pptx", "zip"}}
            self._send_json(public)
            return

        if len(parts) == 4 and parts[:2] == ["api", "jobs"] and parts[3] == "file":
            job = core.jobs.get(parts[2])
            if not job or job.get("status") != "done":
                self._send_json({"error": "not found"}, 404)
                return
            kind = parse_qs(parsed.query).get("kind", ["zip"])[0]
            key = {"html": "html", "pptx": "pptx", "zip": "zip"}.get(kind)
            if not key or not job.get(key):
                self._send_json({"error": "not found"}, 404)
                return
            if kind == "html":
                self._send_html_file(Path(job[key]), parts[2])
                return
            self._send_file(Path(job[key]), inline=(kind == "html"))
            return

        if len(parts) >= 5 and parts[:2] == ["api", "jobs"] and parts[3] == "assets":
            job = core.jobs.get(parts[2])
            if not job or job.get("status") != "done" or not job.get("outputDir"):
                self._send_json({"error": "not found"}, 404)
                return
            target = resolve_job_asset(job["outputDir"], "/".join(parts[4:]))
            if not target:
                self._send_json({"error": "not found"}, 404)
                return
            self._send_file(target, inline=True)
            return

        self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path not in {"/api/jobs", "/api/run"}:
            self._send_json({"error": "not found"}, 404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json({"error": "invalid json"}, 400)
            return

        if parsed.path == "/api/run":
            self._run_sync(payload)
            return

        job_id = uuid.uuid4().hex[:12]
        core.jobs[job_id] = {"id": job_id, "status": "queued", "message": "Queued", "createdAt": time.time()}
        thread = threading.Thread(target=core._run_job, args=(job_id, payload), daemon=True)
        thread.start()
        self._send_json({"jobId": job_id})

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    port = int(os.getenv("PORT", "3000"))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving GPT Image2 PPT App on 0.0.0.0:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
