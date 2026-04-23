#!/usr/bin/env python3
"""Convert a human-authored slides_plan.md into the machine-readable slides_plan.json.

Markdown schema (see SKILL.md for full spec):

    ---
    title: <presentation title>
    ---

    ## 1. [cover] Slide Title Line
    <body lines ... until next ## heading>

    ## 2. [content, layout=layout-05] Another Slide
    <body>

Rules:
- Frontmatter: YAML-ish, only `title` is required; unknown keys are preserved into
  the output JSON under top-level fields.
- Each `##` heading starts a new slide. The optional `N.` prefix is respected if
  present; otherwise slides are numbered by order of appearance.
- Optional `[page_type]` or `[page_type, layout=<id>]` directive immediately
  after the number. `page_type` defaults to `content`. Known values: cover /
  content / data.
- The remaining text of the heading line (after directive) is the slide's title
  line and becomes the FIRST line of the output `content` field. A blank line
  plus body lines follow, matching the existing JSON convention.
- Trailing/leading blank lines inside a slide body are trimmed.

Usage:
    python3 md_to_plan.py slides_plan.md                     # -> slides_plan.json next to it
    python3 md_to_plan.py slides_plan.md -o my_plan.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VALID_PAGE_TYPES = {"cover", "content", "data"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

HEADING_RE = re.compile(
    r"^##\s+"
    r"(?:(?P<num>\d+)\s*[.)]\s*)?"
    r"(?:\[(?P<directive>[^\]]*)\]\s*)?"
    r"(?P<title>.*?)\s*$"
)


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_block = m.group(1)
    rest = text[m.end():]
    fm: Dict[str, Any] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, rest


def parse_directive(directive: str) -> Tuple[str, Optional[str]]:
    page_type = "content"
    layout_id: Optional[str] = None
    if not directive:
        return page_type, layout_id
    parts = [p.strip() for p in directive.split(",") if p.strip()]
    for part in parts:
        if "=" in part:
            k, _, v = part.partition("=")
            if k.strip().lower() == "layout":
                layout_id = v.strip() or None
        else:
            candidate = part.lower()
            if candidate in VALID_PAGE_TYPES:
                page_type = candidate
            else:
                layout_id = part
    return page_type, layout_id


def parse_slides(body: str) -> List[Dict[str, Any]]:
    lines = body.splitlines()
    slides: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    buffer: List[str] = []

    def flush() -> None:
        if current is None:
            return
        body_lines = buffer[:]
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()

        title_line = current.pop("_title_line", "").strip()
        body_text = "\n".join(body_lines).rstrip()
        if title_line and body_text:
            current["content"] = f"{title_line}\n\n{body_text}"
        elif title_line:
            current["content"] = title_line
        else:
            current["content"] = body_text
        slides.append(current)

    for raw in lines:
        if raw.startswith("## "):
            flush()
            m = HEADING_RE.match(raw)
            if not m:
                title = raw[3:].strip()
                num = None
                directive = ""
            else:
                title = m.group("title") or ""
                num = m.group("num")
                directive = m.group("directive") or ""
            page_type, layout_id = parse_directive(directive)
            current = {
                "slide_number": int(num) if num else len(slides) + 1,
                "page_type": page_type,
                "_title_line": title,
            }
            if layout_id:
                current["layout_id"] = layout_id
            buffer = []
        else:
            if current is not None:
                buffer.append(raw)

    flush()

    seen = set()
    for i, s in enumerate(slides, start=1):
        n = s.get("slide_number")
        if n in seen or n is None:
            n = i
        seen.add(n)
        s["slide_number"] = n

    return slides


def md_to_plan(md_text: str) -> Dict[str, Any]:
    fm, body = parse_frontmatter(md_text)
    slides = parse_slides(body)
    plan: Dict[str, Any] = {
        "title": fm.get("title", "Untitled Presentation"),
        "total_slides": len(slides),
        "slides": slides,
    }
    for k, v in fm.items():
        if k not in {"title"} and k not in plan:
            plan[k] = v
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert slides_plan.md -> slides_plan.json")
    parser.add_argument("input", help="Path to the markdown plan")
    parser.add_argument("-o", "--output", help="Output JSON path (default: input with .json suffix)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"Error: {src} not found", file=sys.stderr)
        sys.exit(1)

    dst = Path(args.output) if args.output else src.with_suffix(".json")
    plan = md_to_plan(src.read_text(encoding="utf-8"))
    dst.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {src} -> {dst}  ({plan['total_slides']} slides)")


if __name__ == "__main__":
    main()
