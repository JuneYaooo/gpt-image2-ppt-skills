#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt-image-2 图片生成器

调用 OpenAI 兼容的 /v1/chat/completions 端点，model 设为 gpt-image-2
（聚灵等中转站把图片模型挂在 chat completions 上，多模态返回）。

如果 base_url 是 OpenAI 官方或支持 Images API 的中转站，
也可以走 /v1/images/generations ---- 由 GPT_IMAGE_ENDPOINT 切换。
"""

from __future__ import annotations

import base64
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import requests

# .env 加载由顶层入口（generate_ppt.py 的 find_and_load_env）统一负责。
# 本模块不调 load_dotenv()，避免 import 时无意识加载父目录 / cwd 的 .env，
# 与 SKILL.md 声明的"scoped .env loading"保持一致。


# 16:9 横版用 1536x1024，竖版 9:16 用 1024x1536，方图用 1024x1024
ASPECT_TO_SIZE = {
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}

REQUEST_TIMEOUT_SECS = 600  # 图片生成可能需要 1-3 分钟
MAX_RETRIES = 3  # 524/超时/连接断开等瞬态错误的重试次数
RETRY_DELAY_SECS = 5
MAX_ASPECT_RETRIES = 2  # 比例不合格自动重生次数
ASPECT_TOLERANCE = 0.15  # 比例偏差容忍度（±15%）

# 期望的宽高比（width / height）
ASPECT_RATIO_VALUES = {
    "16:9": 16 / 9,
    "9:16": 9 / 16,
    "1:1": 1.0,
}


def read_png_dimensions(path: str) -> tuple:
    """从 PNG header 读宽高，不依赖 PIL。失败返回 (0, 0)。"""
    import struct
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return 0, 0
        # IHDR chunk: 16 字节偏移开始 width(4) + height(4) big-endian
        width, height = struct.unpack(">II", head[16:24])
        return width, height
    except Exception:
        return 0, 0


def aspect_acceptable(width: int, height: int, target: str, tolerance: float = ASPECT_TOLERANCE) -> bool:
    """检查实际宽高比是否在目标比例的容差范围内。"""
    if not (width and height):
        return True  # 读不到就放过，不阻塞流程
    expected = ASPECT_RATIO_VALUES.get(target)
    if expected is None:
        return True
    actual = width / height
    deviation = abs(actual - expected) / expected
    return deviation <= tolerance


class GptImage2Generator:
    """gpt-image-2 图片生成器"""

    def __init__(self, aspect_ratio: str = "16:9") -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("GPT_IMAGE_MODEL_NAME", "gpt-image-2")
        self.quality = os.getenv("GPT_IMAGE_QUALITY", "high")
        # endpoint: chat | images | auto（auto 先 images 不行再 chat）
        self.endpoint = os.getenv("GPT_IMAGE_ENDPOINT", "chat").lower()

        if not self.api_key:
            raise ValueError("缺少 OPENAI_API_KEY，请在 .env 中配置")

        self.aspect_ratio = aspect_ratio
        self.default_size = ASPECT_TO_SIZE.get(aspect_ratio, "1536x1024")

        print(
            f"🎨 初始化 gpt-image-2 生成器 "
            f"(model={self.model_name}, size={self.default_size}, "
            f"quality={self.quality}, endpoint={self.endpoint})"
        )

    # ---------- 通用工具 ----------

    def _save_b64(self, b64: str, output_path: str) -> None:
        if "," in b64 and b64.startswith("data:"):
            b64 = b64.split(",", 1)[1]
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64))

    def _download_url(self, url: str, output_path: str) -> None:
        # 安全提示：只接受 http/https；下载前打印 host，便于用户识别异常域；
        # 设最大 50MB 上限避免恶意大文件；非 image/* Content-Type 警告但仍写盘。
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"拒绝下载非 http(s) 协议的 URL: {parsed.scheme}")
        print(f"📥 下载图片 host={parsed.netloc} path={parsed.path[:80]}")
        resp = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT_SECS)
        resp.raise_for_status()
        ctype = resp.headers.get("content-type", "")
        if ctype and not ctype.startswith("image/"):
            print(f"(!)  非 image Content-Type: {ctype}（仍尝试写盘，请人工核对）")
        MAX_BYTES = 50 * 1024 * 1024
        written = 0
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                written += len(chunk)
                if written > MAX_BYTES:
                    f.close()
                    os.remove(output_path)
                    raise ValueError(f"下载超过 {MAX_BYTES} 字节上限，已丢弃 {url[:80]}")
                f.write(chunk)

    def _save_payload(self, payload: str, output_path: str) -> None:
        """根据 payload 形态（b64 / data url / 普通 url）落盘。"""
        if payload.startswith("data:image/") or (len(payload) > 200 and "/" in payload[:200] is False):
            # data:image/...;base64,xxxxx 或裸 base64
            self._save_b64(payload, output_path)
        elif payload.startswith("http"):
            self._download_url(payload, output_path)
        else:
            # 兜底当 base64
            self._save_b64(payload, output_path)

    # ---------- 多模态响应解析（chat completions 走这里）----------

    def _extract_image(self, content: Any) -> str:
        """从 chat completions 的 content 中提取图片 payload（b64 或 URL）。"""
        if isinstance(content, list):
            for part in content:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "image_url":
                    img_url = part.get("image_url", {}).get("url", "")
                    if img_url:
                        return img_url
                if part.get("type") == "text":
                    text = part.get("text", "")
                    found = self._extract_from_text(text)
                    if found:
                        return found
            raise RuntimeError(f"multimodal parts 里没找到图片：{str(content)[:300]}")

        if isinstance(content, str):
            found = self._extract_from_text(content)
            if found:
                return found
            raise RuntimeError(f"text content 里没找到图片：{content[:300]}")

        raise RuntimeError(f"未知 content 类型：{type(content)}")

    def _extract_from_text(self, text: str) -> Optional[str]:
        # 1) data:image/xxx;base64,YYY
        m = re.search(r"data:image/[\w]+;base64,[A-Za-z0-9+/=]+", text)
        if m:
            return m.group(0)
        # 2) markdown 图片 ![](url)
        m = re.search(r"!\[.*?\]\((https?://[^\)\s]+)\)", text)
        if m:
            return m.group(1)
        # 3) 裸图片 URL
        m = re.search(r"(https?://[^\s\)]+\.(?:png|jpg|jpeg|webp|gif))", text, re.IGNORECASE)
        if m:
            return m.group(1)
        # 4) 任意 http 链接（最后兜底）
        m = re.search(r"(https?://[^\s\)]+)", text)
        if m:
            return m.group(1)
        return None

    # ---------- 端点 1: /v1/chat/completions ----------

    def _request_via_chat(self, prompt: str, size: str, reference_image_path: Optional[str] = None) -> str:
        """流式请求 chat completions，从增量文本中拼接出图片 URL / b64。

        中转站（如聚灵）把图片模型挂在 chat completions 上时，通常要求 stream=True。
        响应里会先推送进度文本（"> 进度：25%"），最后吐 markdown 图片
        （"![image](http://...png)"）或 base64。

        reference_image_path 不为空时，把该图片作为多模态 input 一并塞进 messages，
        让 gpt-image-2 按它的视觉风格出新图（高保真 / 模板克隆模式）。
        """
        url = f"{self.base_url}/v1/chat/completions"
        # 用比例描述而不是具体像素 ---- gpt-image 类模型更听自然语言 "宽屏 16:9"，
        # 写具体像素值反而被忽略。
        if self.aspect_ratio == "9:16":
            aspect_hint = (
                "\n\n【画面比例 -- 强制】严格按 9:16 竖版手机屏幕生成 "
                "(portrait, vertical 9:16, height much taller than width). "
                "绝对不要方图。"
            )
        elif self.aspect_ratio == "1:1":
            aspect_hint = "\n\n【画面比例 -- 强制】1:1 方图。"
        else:
            aspect_hint = (
                "\n\n【画面比例 -- 强制要求】生成图片必须是 16:9 横版宽屏 "
                "(landscape orientation, widescreen 16:9 aspect ratio, "
                "ultrawide horizontal banner format). "
                "宽度必须明显大于高度，宽高比约 1.78:1。"
                "绝对不要生成方图(square)、近方图(near-square)或竖图(portrait)。"
                "Output MUST be 16:9 landscape widescreen, NEVER square or portrait."
            )

        full_prompt = f"{prompt}{aspect_hint}"
        if reference_image_path and os.path.exists(reference_image_path):
            with open(reference_image_path, "rb") as f:
                ref_b64 = base64.b64encode(f.read()).decode("ascii")
            ref_data_url = f"data:image/png;base64,{ref_b64}"
            user_content: Any = [
                {"type": "image_url", "image_url": {"url": ref_data_url}},
                {"type": "text", "text": (
                    "请以上面这张图作为视觉风格参考（配色 / 字体 / 装饰元素 / 布局氛围），"
                    "按下方新内容生成一张全新的 PPT 页，不要复制原图的文字内容。\n\n"
                    + full_prompt
                )},
            ]
        else:
            user_content = full_prompt

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": user_content}
            ],
            "stream": True,
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        print(f"🔗 POST {url}  size={size}  stream=True")
        resp = requests.post(
            url, headers=headers, json=payload,
            stream=True, timeout=REQUEST_TIMEOUT_SECS,
        )
        print(f"📥 status={resp.status_code}")
        if resp.status_code != 200:
            raise RuntimeError(
                f"chat 调用失败 (status={resp.status_code}): {resp.text[:500]}"
            )

        full_text = []
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                import json as _json
                chunk = _json.loads(data_str)
            except Exception:
                continue
            choices = chunk.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            content = delta.get("content")
            if content:
                full_text.append(content)
                # 实时打印进度（截短）
                snippet = content.replace("\n", " ").strip()
                if snippet:
                    print(f"  ↳ {snippet[:80]}")

        merged = "".join(full_text)
        found = self._extract_from_text(merged)
        if not found:
            raise RuntimeError(
                f"流式响应里没找到图片 URL/base64。完整文本：{merged[:500]}"
            )
        return found

    # ---------- 端点 2: /v1/images/generations ----------

    def _request_via_images(self, prompt: str, size: str) -> str:
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
        resp = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT_SECS)
        print(f"📥 status={resp.status_code}")

        if resp.status_code != 200:
            raise RuntimeError(
                f"images 调用失败 (status={resp.status_code}): {resp.text[:500]}"
            )

        result = resp.json()
        data = result.get("data") or []
        if not data:
            raise RuntimeError(f"响应没有 data: {str(result)[:300]}")
        first = data[0]
        b64 = first.get("b64_json")
        url_field = first.get("url")
        if b64:
            return f"data:image/png;base64,{b64}"
        if url_field:
            return url_field
        raise RuntimeError(f"data[0] 既没 b64_json 也没 url: {str(first)[:300]}")

    # ---------- 对外入口 ----------

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

        target_size = self.default_size if size == "auto" else size
        print(f"📝 prompt[:100]: {prompt[:100].replace(chr(10), ' ')}{'...' if len(prompt) > 100 else ''}")

        import time as _time

        # 外层：比例不合格重生（最多 MAX_ASPECT_RETRIES 次）
        for ratio_attempt in range(MAX_ASPECT_RETRIES + 1):
            last_err = None
            # 内层：瞬态错误重试（524 / 超时等）
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    if self.endpoint == "images":
                        # images endpoint 暂不支持 reference image，自动 fallback 到 chat
                        if reference_image_path:
                            payload = self._request_via_chat(prompt, target_size, reference_image_path)
                        else:
                            payload = self._request_via_images(prompt, target_size)
                    elif self.endpoint == "chat":
                        payload = self._request_via_chat(prompt, target_size, reference_image_path)
                    else:  # auto
                        try:
                            if reference_image_path:
                                payload = self._request_via_chat(prompt, target_size, reference_image_path)
                            else:
                                payload = self._request_via_images(prompt, target_size)
                        except Exception as e:
                            print(f"(!) images 失败，回退到 chat: {str(e)[:120]}")
                            payload = self._request_via_chat(prompt, target_size, reference_image_path)

                    self._save_payload(payload, output_path)
                    break  # 成功落盘，跳出瞬态重试循环
                except Exception as e:
                    last_err = e
                    msg = str(e)[:200]
                    transient = any(s in msg for s in ("524", "502", "503", "504", "timeout", "Read timed out",
                                                        "Connection aborted", "RemoteDisconnected"))
                    if attempt < MAX_RETRIES and transient:
                        print(f"(!) [scene {scene_index}] 第 {attempt} 次失败({msg})，{RETRY_DELAY_SECS}s 后重试")
                        _time.sleep(RETRY_DELAY_SECS)
                        continue
                    raise
            else:
                raise RuntimeError(f"重试 {MAX_RETRIES} 次仍失败: {last_err}")

            # 比例校验
            w, h = read_png_dimensions(output_path)
            if aspect_acceptable(w, h, self.aspect_ratio):
                print(f"[OK] 已保存: {output_path}  ({w}x{h}, 比例 {w/h:.3f}, 目标 {self.aspect_ratio})")
                return output_path

            # 比例偏离
            actual_ratio = w / h if h else 0
            expected = ASPECT_RATIO_VALUES.get(self.aspect_ratio, 16/9)
            dev_pct = abs(actual_ratio - expected) / expected * 100 if expected else 0
            if ratio_attempt < MAX_ASPECT_RETRIES:
                print(f"📐 [scene {scene_index}] 尺寸 {w}x{h} (比例 {actual_ratio:.3f}) "
                      f"偏离目标 {self.aspect_ratio} {dev_pct:.0f}%，重生 ({ratio_attempt+1}/{MAX_ASPECT_RETRIES})")
                try:
                    os.remove(output_path)
                except OSError:
                    pass
                continue
            else:
                print(f"(!) [scene {scene_index}] 尺寸 {w}x{h} 仍偏离 {dev_pct:.0f}%，已达比例重试上限，保留")
                return output_path

        return output_path


if __name__ == "__main__":
    import sys
    gen = GptImage2Generator(aspect_ratio="16:9")
    gen.generate_scene_image(
        {"index": 0, "image_prompt": "A clean blue gradient background with the bold white text 'gpt-image-2 Test'"},
        "test_output.png",
    )
    print(f"自检完成: {Path('test_output.png').resolve()}")
    sys.exit(0)
