import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from atlascloud_backend import AtlasCloudImageBackend  # noqa: E402


class Response:
    def __init__(self, payload=None, content=b""):
        self._payload = payload or {}
        self.content = content

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class AtlasCloudImageBackendTests(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {"ATLASCLOUD_API_KEY": "secret", "ATLASCLOUD_POLL_INTERVAL": "0"}, clear=False)
        self.env.start()

    def tearDown(self):
        self.env.stop()

    def test_generates_and_downloads_image(self):
        backend = AtlasCloudImageBackend()
        responses = [
            Response({"data": {"status": "processing"}}),
            Response({"data": {"status": "completed", "outputs": ["https://cdn.example/slide.png"]}}),
            Response(content=b"png"),
        ]
        with tempfile.TemporaryDirectory() as directory, mock.patch("atlascloud_backend.requests.post", return_value=Response({"data": {"id": "p1"}})) as post, mock.patch("atlascloud_backend.requests.get", side_effect=responses) as get:
            output = Path(directory) / "slide.png"
            backend.generate_scene_image({"image_prompt": "A title slide"}, str(output))
            self.assertEqual(output.read_bytes(), b"png")
        self.assertEqual(post.call_args.kwargs["json"]["model"], "google/nano-banana-2-lite/text-to-image")
        self.assertEqual(post.call_args.kwargs["json"]["aspect_ratio"], "16:9")
        self.assertEqual(get.call_count, 3)

    def test_reference_image_uses_edit_model(self):
        backend = AtlasCloudImageBackend()
        with mock.patch.object(backend, "_upload", return_value="https://cdn.example/source.png"), mock.patch("atlascloud_backend.requests.post", return_value=Response({"data": {"id": "p1"}})) as post, mock.patch.object(backend, "_poll", return_value={"data": {"status": "completed", "outputs": ["https://cdn.example/out.png"]}}), mock.patch("atlascloud_backend.requests.get", return_value=Response(content=b"png")):
            with tempfile.TemporaryDirectory() as directory:
                backend.generate_scene_image({"image_prompt": "Edit"}, str(Path(directory) / "out.png"), reference_image_path="source.png")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "google/nano-banana-2-lite/edit")
        self.assertEqual(payload["image_urls"], ["https://cdn.example/source.png"])


if __name__ == "__main__":
    unittest.main()
