import importlib.util
import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "render_docs.py"
SPEC = importlib.util.spec_from_file_location("render_docs", MODULE_PATH)
assert SPEC and SPEC.loader
render_docs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_docs)


class RenderDocsTests(unittest.TestCase):
    def test_major_minor_version_is_derived(self):
        self.assertEqual(render_docs.major_minor("1.18.x"), "1.18")
        self.assertEqual(render_docs.major_minor("1.19.2"), "1.19")

    def test_render_replaces_all_supported_tokens(self):
        rendered = render_docs.render(
            "version={{WESNOTH_VERSION}}, path={{WESNOTH_MAJOR_MINOR}}, "
            "date={{PO_LAST_MODIFIED_DATE}}",
            "1.19.x",
            "20260925",
        )
        self.assertEqual(
            rendered,
            "version=1.19.x, path=1.19, date=20260925",
        )
        self.assertNotIn("{{", rendered)
        self.assertNotIn("}}", rendered)

    def test_render_rejects_unresolved_tokens(self):
        with self.assertRaises(ValueError):
            render_docs.render("{{UNKNOWN}}", "1.18.x")

    def test_latest_po_date_extracts_date_from_timestamp_metadata(self):
        self.assertEqual(
            render_docs.latest_po_date("1.18.x"),
            "20260926",
        )

    def test_environment_version_has_priority(self):
        previous = os.environ.get("WESNOTH_VERSION")
        try:
            os.environ["WESNOTH_VERSION"] = "1.19.x"
            self.assertEqual(render_docs.read_version(), "1.19.x")
        finally:
            if previous is None:
                os.environ.pop("WESNOTH_VERSION", None)
            else:
                os.environ["WESNOTH_VERSION"] = previous


if __name__ == "__main__":
    unittest.main()
