"""Atlas Cloud asynchronous image backend."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests


API_BASE = "https://api.atlascloud.ai/api/v1"
DEFAULT_MODEL = "google/nano-banana-2-lite/text-to-image"
EDIT_MODEL = "google/nano-banana-2-lite/edit"
SUCCESS_STATES = {"completed", "succeeded", "success"}
FAILURE_STATES = {"failed", "canceled", "cancelled"}


class AtlasCloudImageBackend:
    """Generate PPT slide images through Atlas Cloud's media API."""

    def __init__(self, aspect_ratio: str = "16:9") -> None:
        self.api_key = os.getenv("ATLASCLOUD_API_KEY", "").strip()
        if not self.api_key:
            raise ValueError("Missing ATLASCLOUD_API_KEY")
        self.base_url = os.getenv("ATLASCLOUD_MEDIA_BASE_URL", API_BASE).rstrip("/")
        self.model = os.getenv("ATLASCLOUD_IMAGE_MODEL", DEFAULT_MODEL)
        self.edit_model = os.getenv("ATLASCLOUD_IMAGE_EDIT_MODEL", EDIT_MODEL)
        self.aspect_ratio = aspect_ratio
        self.poll_interval = float(os.getenv("ATLASCLOUD_POLL_INTERVAL", "3"))
        self.timeout = float(os.getenv("ATLASCLOUD_TIMEOUT", "600"))
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _upload(self, path: str) -> str:
        with open(path, "rb") as handle:
            response = requests.post(
                f"{self.base_url}/model/uploadMedia",
                headers=self.headers,
                files={"file": (Path(path).name, handle)},
                timeout=120,
            )
        response.raise_for_status()
        result = response.json()
        url = result.get("data", {}).get("download_url")
        if not url:
            raise RuntimeError(f"Atlas Cloud upload returned no download_url: {result}")
        return url

    @staticmethod
    def _references(value: Optional[Union[str, List[str]]]) -> List[str]:
        if not value:
            return []
        values = value if isinstance(value, (list, tuple)) else [value]
        return [str(item) for item in values if item]

    @staticmethod
    def _prediction_id(result: Dict[str, Any]) -> str:
        identifier = result.get("data", {}).get("id") or result.get("id")
        if not identifier:
            raise RuntimeError(f"Atlas Cloud returned no prediction id: {result}")
        return str(identifier)

    @staticmethod
    def _output_url(result: Dict[str, Any]) -> str:
        data = result.get("data", result)
        outputs = data.get("outputs") or data.get("output") or []
        if isinstance(outputs, str):
            outputs = [outputs]
        for output in outputs:
            if isinstance(output, str) and output.startswith(("http://", "https://")):
                return output
        raise RuntimeError(f"Atlas Cloud completed without an output URL: {result}")

    def _poll(self, identifier: str) -> Dict[str, Any]:
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            response = requests.get(
                f"{self.base_url}/model/prediction/{identifier}",
                headers=self.headers,
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            status = str(result.get("data", result).get("status", "")).lower()
            if status in SUCCESS_STATES:
                return result
            if status in FAILURE_STATES:
                raise RuntimeError(f"Atlas Cloud prediction {status}: {result}")
            time.sleep(self.poll_interval)
        raise TimeoutError(f"Atlas Cloud prediction timed out after {self.timeout:g}s")

    def generate_scene_image(
        self,
        scene_data: Dict[str, Any],
        output_path: str,
        size: str = "auto",
        reference_image_path: Optional[Union[str, List[str]]] = None,
    ) -> str:
        del size
        prompt = scene_data.get("image_prompt", "")
        if not prompt:
            raise ValueError("scene_data is missing image_prompt")

        references = self._references(reference_image_path)
        uploaded = [self._upload(path) if not path.startswith(("http://", "https://")) else path for path in references]
        payload: Dict[str, Any] = {
            "model": self.edit_model if uploaded else self.model,
            "prompt": prompt,
            "aspect_ratio": self.aspect_ratio,
        }
        if uploaded:
            payload["image_urls"] = uploaded

        response = requests.post(
            f"{self.base_url}/model/generateImage",
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        result = self._poll(self._prediction_id(response.json()))
        image = requests.get(self._output_url(result), timeout=120)
        image.raise_for_status()
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(image.content)
        return str(destination)
