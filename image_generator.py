#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt-image-2 图片生成器

调用 OpenAI 官方 Images API（POST /v1/images/generations）。
也兼容大多数 OpenAI 兼容中转站（base_url 替换成中转站地址即可）。
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv


load_dotenv()


# 16:9 横版用 1536x1024，竖版 9:16 用 1024x1536，方图用 1024x1024
ASPECT_TO_SIZE = {
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}


class GptImage2Generator:
    """gpt-image-2 图片生成器（OpenAI 官方 Images API）"""

    def __init__(self, aspect_ratio: str = "16:9") -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("GPT_IMAGE_MODEL_NAME", "gpt-image-2")
        self.quality = os.getenv("GPT_IMAGE_QUALITY", "high")

        if not self.api_key:
            raise ValueError("缺少 OPENAI_API_KEY，请在 .env 中配置")

        self.aspect_ratio = aspect_ratio
        self.default_size = ASPECT_TO_SIZE.get(aspect_ratio, "1536x1024")

        print(
            f"🎨 初始化 gpt-image-2 生成器 "
            f"(model={self.model_name}, size={self.default_size}, quality={self.quality})"
        )

    def _save_b64(self, b64: str, output_path: str) -> None:
        # 容忍 data:image/png;base64,xxx 这种带前缀的形式
        if "," in b64 and b64.startswith("data:"):
            b64 = b64.split(",", 1)[1]
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64))

    def _download_url(self, url: str, output_path: str) -> None:
        print(f"📥 下载图片: {url}")
        resp = requests.get(url, stream=True, timeout=120)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

    def _request_image(self, prompt: str, size: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/images/generations"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": self.quality,
            "response_format": "b64_json",
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        print(f"🔗 POST {url}  size={size}  quality={self.quality}")
        print(f"📝 prompt[:100]: {prompt[:100].replace(chr(10), ' ')}{'...' if len(prompt) > 100 else ''}")

        resp = requests.post(url, headers=headers, json=payload, timeout=600)
        print(f"📥 status={resp.status_code}")

        if resp.status_code != 200:
            body = resp.text[:500]
            raise RuntimeError(
                f"gpt-image-2 API 调用失败 (status={resp.status_code}): {body}"
            )

        return resp.json()

    def generate_scene_image(
        self,
        scene_data: Dict[str, Any],
        output_path: str,
        size: str = "auto",
    ) -> str:
        """根据场景数据生成单张图片，写入 output_path 后返回该路径。"""
        scene_index = scene_data.get("index", 0)
        prompt = scene_data.get("image_prompt", "")
        if not prompt:
            raise ValueError(f"场景 {scene_index} 缺少 image_prompt")

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        target_size = self.default_size if size == "auto" else size

        print(f"🎨 [gpt-image-2] 生成场景 {scene_index}")
        result = self._request_image(prompt=prompt, size=target_size)

        data_list = result.get("data") or []
        if not data_list:
            raise RuntimeError(f"响应中没有 data 字段: {str(result)[:300]}")

        first = data_list[0]
        b64 = first.get("b64_json")
        url = first.get("url")

        if b64:
            self._save_b64(b64, output_path)
        elif url:
            self._download_url(url, output_path)
        else:
            raise RuntimeError(f"data[0] 既没有 b64_json 也没有 url: {str(first)[:300]}")

        print(f"✅ 已保存: {output_path}")
        return output_path


if __name__ == "__main__":
    # 简易自检：直接跑一次封面图
    import sys

    gen = GptImage2Generator(aspect_ratio="16:9")
    out = "test_output.png"
    gen.generate_scene_image(
        {
            "index": 0,
            "image_prompt": "A clean blue gradient background with the bold white text 'gpt-image-2 Test'",
        },
        out,
    )
    print(f"自检完成: {Path(out).resolve()}")
    sys.exit(0)
