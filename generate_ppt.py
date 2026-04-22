#!/usr/bin/env python3
"""
PPT Generator - Generate PPT slide images using OpenAI gpt-image-2 (Images API).

This script generates PPT slide images based on a slide plan and style template,
then creates an HTML viewer for playback.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


# =============================================================================
# Constants
# =============================================================================

DEFAULT_TEMPLATE_PATH = "templates/viewer.html"
OUTPUT_BASE_DIR = "outputs"

SCRIPT_DIR = Path(__file__).parent


# =============================================================================
# Environment Configuration
# =============================================================================

def find_and_load_env() -> bool:
    """
    Find and load .env file from multiple locations.

    Search priority:
    1. Current script directory
    2. Parent directories up to project root (containing .git or .env)
    3. Claude ​Code skill standard location (~/.claude/skills/gpt-image2-ppt-skills/)
    """
    current_dir = SCRIPT_DIR
    env_locations = [
        current_dir / ".env",
        *[parent / ".env" for parent in current_dir.parents],
        Path.home() / ".claude" / "skills" / "gpt-image2-ppt-skills" / ".env",
    ]

    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from: {env_path}")
            return True

        if env_path.parent != current_dir and (env_path.parent / ".git").exists():
            break

    load_dotenv(override=True)
    print("Warning: No .env file found, using system environment variables")
    return False


# =============================================================================
# Style Template
# =============================================================================

def load_style_template(style_path: str) -> str:
    """Extract the '## 基础提示词模板' section from a style markdown file."""
    with open(style_path, "r", encoding="utf-8") as f:
        content = f.read()

    base_prompt_marker = "## 基础提示词模板"
    start_idx = content.find(base_prompt_marker)

    if start_idx == -1:
        print("Warning: '## 基础提示词模板' section not found, using fallback extraction")
        start_idx = content.find("## ")
        end_idx = content.find("## ", start_idx + 3)
        if start_idx == -1 or end_idx == -1:
            return content
        return content[start_idx + 3:end_idx].strip()

    section_start = start_idx + len(base_prompt_marker)
    next_section_idx = content.find("\n## ", section_start)

    if next_section_idx == -1:
        extracted = content[section_start:]
    else:
        extracted = content[section_start:next_section_idx]

    return extracted.strip()


# =============================================================================
# Prompt Generation
# =============================================================================

LANGUAGE_FONT_RULE = """

【强制语言与字体要求】
1. 幻灯片上所有文字必须使用简体中文，严禁出现任何英文单词或句子（产品名称等专有名词可保留英文，其余一律用中文）。
2. 中文字体使用思源黑体（Source Han Sans）或苹方（PingFang SC），字形清晰、笔画规整，严禁使用草书、艺术字或变形字体。
3. 标题字体粗体，正文字体常规，字号对比清晰，确保在演示场景下可读性极高。
"""


def generate_prompt(
    style_template: str,
    page_type: str,
    content_text: str,
    slide_number: int,
    total_slides: int,
) -> str:
    """Generate a complete prompt for a single slide."""
    prompt_parts = [style_template, "\n\n"]

    is_cover = page_type == "cover" or slide_number == 1
    is_data = page_type == "data" or slide_number == total_slides

    if is_cover:
        prompt_parts.append(
            f"""请根据视觉平衡美学，生成封面页。在中心放置一个巨大的复杂3D玻璃物体，并覆盖粗体大字：

{content_text}

背景有延伸的极光波浪。"""
        )
    elif is_data:
        prompt_parts.append(
            f"""请生成数据页或总结页。使用分屏设计，左侧排版以下文字，右侧悬浮巨大的发光3D数据可视化图表：

{content_text}"""
        )
    else:
        prompt_parts.append(
            f"""请生成内容页。使用Bento网格布局，将以下内容组织在模块化的圆角矩形容器中，容器材质必须是带有模糊效果的磨砂玻璃：

{content_text}"""
        )

    prompt_parts.append(LANGUAGE_FONT_RULE)
    return "".join(prompt_parts)


# =============================================================================
# Image Generation
# =============================================================================

def generate_slide(
    prompt: str,
    slide_number: int,
    output_dir: str,
) -> Optional[str]:
    """Generate a single PPT slide image using gpt-image-2."""
    sys.path.insert(0, str(SCRIPT_DIR))
    from image_generator import GptImage2Generator

    print(f"  Generating slide {slide_number} via gpt-image-2 ...")

    try:
        generator = GptImage2Generator(aspect_ratio="16:9")
        image_path = os.path.join(output_dir, "images", f"slide-{slide_number:02d}.png")

        scene_data = {
            "index": slide_number,
            "image_prompt": prompt,
        }
        generator.generate_scene_image(scene_data=scene_data, output_path=image_path)
        print(f"  Slide {slide_number} saved: {image_path}")
        return image_path

    except Exception as e:
        print(f"  Slide {slide_number} failed: {e}")
        return None


# =============================================================================
# Output Generation
# =============================================================================

def generate_viewer_html(
    output_dir: str,
    slide_count: int,
    template_path: str,
) -> str:
    """Generate HTML viewer for slides playback."""
    if not os.path.isabs(template_path):
        template_path = str(SCRIPT_DIR / template_path)

    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    slides_list = [f"'images/slide-{i:02d}.png'" for i in range(1, slide_count + 1)]

    html_content = html_template.replace(
        "/* IMAGE_LIST_PLACEHOLDER */",
        ",\n            ".join(slides_list),
    )

    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  Viewer HTML generated: {html_path}")
    return html_path


def save_prompts(output_dir: str, prompts_data: Dict[str, Any]) -> str:
    """Save all prompts to JSON file."""
    prompts_path = os.path.join(output_dir, "prompts.json")
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)
    print(f"  Prompts saved: {prompts_path}")
    return prompts_path


# =============================================================================
# Main Entry Point
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PPT Generator - Generate PPT images using OpenAI gpt-image-2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md
  python generate_ppt.py --plan slides_plan.json --style styles/clean-tech-blue.md --slides 1,3,5

Environment variables (set in .env file):
  OPENAI_BASE_URL:        Images API base URL (default: https://api.openai.com)
  OPENAI_API_KEY:         API key (required)
  GPT_IMAGE_MODEL_NAME:   Model name (default: gpt-image-2)
  GPT_IMAGE_QUALITY:      low / medium / high / auto (default: high)
""",
    )

    parser.add_argument("--plan", required=True, help="Path to slides plan JSON file")
    parser.add_argument("--style", required=True, help="Path to style template file")
    parser.add_argument("--output", help="Output directory path (default: outputs/TIMESTAMP)")
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help=f"HTML template path (default: {DEFAULT_TEMPLATE_PATH})",
    )
    parser.add_argument(
        "--slides",
        help="Only generate specific slides, e.g. '1,3,5'",
    )

    return parser


def main() -> None:
    find_and_load_env()

    parser = create_argument_parser()
    args = parser.parse_args()

    style_path = args.style
    if not os.path.isabs(style_path):
        candidate = SCRIPT_DIR / style_path
        if candidate.exists():
            style_path = str(candidate)

    with open(args.plan, "r", encoding="utf-8") as f:
        slides_plan = json.load(f)

    style_template = load_style_template(style_path)

    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = str(SCRIPT_DIR / OUTPUT_BASE_DIR / timestamp)

    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    slides = slides_plan["slides"]
    total_slides = len(slides)

    if args.slides:
        target_nums = set(int(x.strip()) for x in args.slides.split(","))
        slides = [s for s in slides if s.get("slide_number") in target_nums]

    print("=" * 60)
    print("PPT Generator (gpt-image-2) Started")
    print("=" * 60)
    print(f"Style: {style_path}")
    print(f"Slides: {len(slides)} / {total_slides}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    prompts_data: Dict[str, Any] = {
        "metadata": {
            "title": slides_plan.get("title", "Untitled Presentation"),
            "total_slides": total_slides,
            "model": os.getenv("GPT_IMAGE_MODEL_NAME", "gpt-image-2"),
            "style": style_path,
            "generated_at": datetime.now().isoformat(),
        },
        "slides": [],
    }

    for slide_info in slides:
        slide_number = slide_info["slide_number"]
        page_type = slide_info.get("page_type", "content")
        content_text = slide_info["content"]

        existing = os.path.join(output_dir, "images", f"slide-{slide_number:02d}.png")
        if os.path.exists(existing):
            print(f"Slide {slide_number}: already exists, skipping.")
            prompts_data["slides"].append({
                "slide_number": slide_number,
                "page_type": page_type,
                "content": content_text,
                "prompt": "(skipped - already exists)",
                "image_path": existing,
            })
            continue

        prompt = generate_prompt(
            style_template, page_type, content_text, slide_number, total_slides
        )

        print(f"Generating slide {slide_number} ({page_type})...")
        image_path = generate_slide(prompt, slide_number, output_dir)

        prompts_data["slides"].append({
            "slide_number": slide_number,
            "page_type": page_type,
            "content": content_text,
            "prompt": prompt,
            "image_path": image_path,
        })

        print()

    save_prompts(output_dir, prompts_data)
    generate_viewer_html(output_dir, total_slides, args.template)

    print()
    print("=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Viewer HTML: {os.path.join(output_dir, 'index.html')}")
    print()
    print("Open viewer in browser:")
    print(f"  open {os.path.join(output_dir, 'index.html')}")
    print()


if __name__ == "__main__":
    main()
