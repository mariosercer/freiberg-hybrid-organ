import os
import unittest
from pathlib import Path

from src.codm.goerlitz_paths import default_goerlitz_extract_root, goerlitz_package_root


class TestGoerlitzPaths(unittest.TestCase):
    def test_default_extract_root_without_env_override(self):
        os.environ.pop("GOERLITZ_EXTRACT_ROOT", None)
        root = default_goerlitz_extract_root()
        self.assertTrue(str(root).endswith("goerlitz-extract"))

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
