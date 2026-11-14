import os
import sys
import tempfile
import unittest
from pathlib import Path

from src.codm.goerlitz_paths import default_goerlitz_extract_root, goerlitz_package_root
from src.codm.local_paths import installed_packages_root


class TestGoerlitzPaths(unittest.TestCase):
    def test_default_extract_root_without_env_override(self):
        os.environ.pop("GOERLITZ_EXTRACT_ROOT", None)
        root = default_goerlitz_extract_root()
        if sys.platform == "darwin":
            self.assertTrue(str(root).endswith("goerlitz-extract"))
        else:
            self.assertEqual(root, installed_packages_root())

    def test_package_root_prefers_installed_package_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "001812").mkdir()
            self.assertEqual(goerlitz_package_root(Path(tmp), 1812), Path(tmp) / "001812")

    def test_env_var_overrides_default_extract_root(self):
        os.environ["GOERLITZ_EXTRACT_ROOT"] = "/tmp/some-other-location"
        try:
            root = default_goerlitz_extract_root()
            self.assertEqual(root, Path("/tmp/some-other-location"))
        finally:
            del os.environ["GOERLITZ_EXTRACT_ROOT"]

    def test_package_root_picks_the_right_zip_part(self):
        # Just checks the formula resolves to a plausible path shape, not
        # that the (large, external-drive) data actually exists.
        root = goerlitz_package_root(Path("/some/extract/root"), 1813)
        self.assertIn("Part 3", str(root))
        self.assertIn("001813", str(root))


if __name__ == "__main__":
    unittest.main()
