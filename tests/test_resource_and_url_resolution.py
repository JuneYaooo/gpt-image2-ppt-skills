import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImageGeneratorUrlTests(TestCase):
    def setUp(self):
        self.image_generator = load_module("image_generator_under_test", SCRIPTS_DIR / "image_generator.py")

    def test_api_url_accepts_root_base_url(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "OPENAI_BASE_URL": "https://relay.example"}, clear=False):
            gen = self.image_generator.GptImage2Generator()

        self.assertEqual(
            gen._api_url("/v1/images/generations"),
            "https://relay.example/v1/images/generations",
        )

    def test_api_url_accepts_v1_base_url(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "OPENAI_BASE_URL": "https://relay.example/v1"}, clear=False):
            gen = self.image_generator.GptImage2Generator()

        self.assertEqual(
            gen._api_url("/v1/chat/completions"),
            "https://relay.example/v1/chat/completions",
        )

    def test_crop_to_aspect_normalizes_three_by_two_image(self):
        image_generator = self.image_generator
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slide.png"
            try:
                from PIL import Image
            except ImportError:
                self.skipTest("Pillow is required for aspect normalization")
            Image.new("RGB", (1536, 1024), "white").save(path)

            width, height = image_generator.crop_to_aspect(str(path), "16:9")

        self.assertEqual((width, height), (1536, 864))
        self.assertTrue(image_generator.aspect_acceptable(width, height, "16:9"))

    def test_remote_end_closed_error_is_retriable(self):
        self.assertTrue(
            self.image_generator.is_transient_generation_error(
                RuntimeError("Remote end closed connection without response")
            )
        )


class ResourceResolutionTests(TestCase):
    def setUp(self):
        self.generate_ppt = load_module("generate_ppt_under_test", SCRIPTS_DIR / "generate_ppt.py")

    def test_resolves_packaged_reference_by_basename(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            scripts_dir = skill_root / "scripts"
            references_dir = skill_root / "references"
            references_dir.mkdir(parents=True)
            scripts_dir.mkdir()
            expected = references_dir / "clean-tech-blue.md"
            expected.write_text("## 基础提示词模板\nexample", encoding="utf-8")

            with patch.object(self.generate_ppt, "SCRIPT_DIR", scripts_dir), patch.object(self.generate_ppt, "CWD", Path(tmp) / "work"):
                resolved = self.generate_ppt.resolve_resource_path("styles/clean-tech-blue.md", default_subdir="styles")

        self.assertEqual(Path(resolved), expected)


class StdlibServerAssetTests(TestCase):
    def setUp(self):
        app_root = REPO_ROOT / "profy_image2_app"
        sys.path.insert(0, str(app_root))
        try:
            self.server_stdlib = load_module(
                "server_stdlib_under_test",
                app_root / "app" / "server_stdlib.py",
            )
        finally:
            sys.path.remove(str(app_root))

    def test_html_preview_gets_job_asset_base(self):
        html = "<html><head><title>x</title></head><body><script>const slides = ['images/slide-01.png'];</script></body></html>"

        rewritten = self.server_stdlib.html_with_asset_base(html, "abc123")

        self.assertIn('<base href="/api/jobs/abc123/assets/">', rewritten)
        self.assertIn("images/slide-01.png", rewritten)
