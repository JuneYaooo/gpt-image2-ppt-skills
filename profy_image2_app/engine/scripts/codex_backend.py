#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Codex CLI backend for image generation.

Instead of calling OpenAI Images API directly (which requires OPENAI_API_KEY),
shell out to `codex exec` and let codex — authenticated via the user's ChatGPT
login or its own configured API key — generate the image and write the PNG.

Interface is intentionally identical to `image_generator.GptImage2Generator`
so `generate_ppt.py` can swap between them with a single flag.

Tradeoffs vs direct API (documented in SKILL.md):
- Pro: no OPENAI_API_KEY needed in this skill's .env; reuses codex auth.
- Con: slower per image (agent overhead), less reliable parallelism, harder to
  control quality/size precisely — codex interprets the natural-language spec.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CODEX_CMD = "codex exec --full-auto"
DEFAULT_TIMEOUT_SECS = 900  # codex agent loop can be slow per image


class CodexImageBackend:
    """Generate PPT slide PNGs via `codex exec`.

    Env:
      CODEX_CMD    override the codex invocation (default: `codex exec --full-auto`)
                   must be a shell-quoted string; the instruction is appended as
                   a single argv element.
      CODEX_IMAGE_MODEL  model to request codex to use (default: gpt-image-2)
      CODEX_TIMEOUT_SECS per-image timeout (default: 900)
    """

    def __init__(self, aspect_ratio: str = "16:9") -> None:
        self.aspect_ratio = aspect_ratio
        self.codex_cmd = os.getenv("CODEX_CMD", DEFAULT_CODEX_CMD)
        self.model = os.getenv("CODEX_IMAGE_MODEL", "gpt-image-2")
        self.timeout = int(os.getenv("CODEX_TIMEOUT_SECS", str(DEFAULT_TIMEOUT_SECS)))
        self.size = {
            "16:9": "1536x1024",
            "9:16": "1024x1536",
            "1:1": "1024x1024",
        }.get(aspect_ratio, "1536x1024")

        # Sanity check: codex binary reachable?
        exe = shlex.split(self.codex_cmd)[0]
        from shutil import which
        if which(exe) is None:
            raise RuntimeError(
                f"codex backend 选中但找不到 `{exe}` 可执行文件。\n"
                f"请先安装 codex CLI（https://github.com/openai/codex）并完成登录，"
                f"或通过 CODEX_CMD 指定完整路径。"
            )

        print(
            f"🎨 初始化 codex backend "
            f"(cmd={self.codex_cmd!r}, model={self.model}, size={self.size}, "
            f"timeout={self.timeout}s)"
        )

    def _build_instruction(
        self,
        prompt: str,
        output_path: str,
        reference_image_path: Optional[str],
    ) -> str:
        abs_out = str(Path(output_path).resolve())
        ref_line = ""
        if reference_image_path and os.path.exists(reference_image_path):
            abs_ref = str(Path(reference_image_path).resolve())
            ref_line = (
                f"- 把这张图作为视觉风格参考（配色 / 字体 / 装饰元素 / 布局氛围），"
                f"不要复制其中文字：{abs_ref}\n"
            )

        aspect_rule = {
            "16:9": "16:9 横版宽屏（landscape, widescreen, 宽度明显大于高度）",
            "9:16": "9:16 竖版手机屏幕（portrait, vertical）",
            "1:1": "1:1 方图（square）",
        }.get(self.aspect_ratio, "16:9 横版宽屏")

        return (
            f"帮我用 OpenAI Images API 生成一张 PPT 幻灯片图片，并写到磁盘上。\n\n"
            f"要求：\n"
            f"- 模型：{self.model}\n"
            f"- 尺寸：{self.size}（{aspect_rule}）\n"
            f"- 质量：high\n"
            f"- 输出路径（绝对路径）：{abs_out}\n"
            f"{ref_line}"
            f"- 保存后确认文件存在且体积 > 10KB；若失败请报错退出非零。\n"
            f"- 不要向我解释或改写 prompt，直接出图。\n\n"
            f"图片 prompt：\n"
            f"-----BEGIN PROMPT-----\n"
            f"{prompt}\n"
            f"-----END PROMPT-----\n"
        )

    def generate_scene_image(
        self,
        scene_data: Dict[str, Any],
        output_path: str,
        size: str = "auto",
        reference_image_path: Optional[str] = None,
    ) -> str:
        scene_index = scene_data.get("index", 0)
        prompt = scene_data.get("image_prompt", "")
        if not prompt:
            raise ValueError(f"场景 {scene_index} 缺少 image_prompt")

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        instruction = self._build_instruction(prompt, output_path, reference_image_path)
        argv = shlex.split(self.codex_cmd) + [instruction]

        print(f"🔗 [scene {scene_index}] dispatching to codex ({len(instruction)} chars)")
        try:
            result = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"codex exec 超时（{self.timeout}s）: {e}") from e

        # Codex writes progress to stderr; log tail for debugging without spamming.
        stderr_tail = (result.stderr or "").strip().splitlines()[-5:]
        if stderr_tail:
            for line in stderr_tail:
                print(f"  ↳ {line[:200]}")

        if result.returncode != 0:
            raise RuntimeError(
                f"codex exec 非零退出 (code={result.returncode}): "
                f"{(result.stderr or result.stdout or '')[-500:]}"
            )

        if not os.path.exists(output_path):
            raise RuntimeError(
                f"codex 声称成功但文件不存在: {output_path}\n"
                f"stdout tail: {(result.stdout or '')[-300:]}"
            )

        size_bytes = os.path.getsize(output_path)
        if size_bytes < 10 * 1024:
            raise RuntimeError(
                f"codex 产出的文件过小 ({size_bytes} bytes)，可能是错误页/空文件：{output_path}"
            )

        print(f"[OK] 已保存: {output_path}  ({size_bytes // 1024} KB)")
        return output_path


if __name__ == "__main__":
    import sys
    gen = CodexImageBackend(aspect_ratio="16:9")
    gen.generate_scene_image(
        {"index": 0, "image_prompt": "A clean blue gradient background with the bold white text 'codex backend test'"},
        "test_codex_output.png",
    )
    print(f"自检完成: {Path('test_codex_output.png').resolve()}")
    sys.exit(0)
