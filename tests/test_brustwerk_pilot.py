import re
import unittest
from pathlib import Path

from src.codm.brustwerk_pilot import build_brustwerk_pilot

ZOBLITZ_ROOT = Path(
    "/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458"
)


class TestBrustwerkPilot(unittest.TestCase):
    def test_build_brustwerk_pilot_has_nine_unique_stops(self):
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        # <StopCode> legitimately appears twice per stop (once in the `stop`
        # table, once in the `stoprank` table referencing it) - scope the
        # uniqueness check to the `stop` table alone, which is what "each
        # stop has a unique code" actually means (Review Focus #3).
        stop_block = re.search(
            r'<ObjectList ObjectType="stop">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        stop_codes = re.findall(r"<StopCode>(\d+)</StopCode>", stop_block)
        self.assertGreaterEqual(len(stop_codes), 9)
        self.assertEqual(len(set(stop_codes)), len(stop_codes))
        organ_id = re.search(r"<UniqueOrganID>(\d+)</UniqueOrganID>", xml).group(1)
        self.assertTrue(800000 <= int(organ_id) <= 899999)


if __name__ == "__main__":
    unittest.main()
