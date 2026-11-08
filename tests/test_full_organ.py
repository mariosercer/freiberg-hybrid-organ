import re
import unittest
from pathlib import Path

from src.codm.full_organ import build_full_organ

GOERLITZ_EXTRACT_ROOT = Path(
    "/private/tmp/claude-501/-Users-pilepale-Documents-3D-metal-printing/"
    "fc14fe8b-9442-46d1-bef9-2a24ff20ea02/scratchpad/goerlitz-extract"
)


@unittest.skipUnless(GOERLITZ_EXTRACT_ROOT.is_dir(), "Görlitz scratch extraction not present")
class TestFullOrgan(unittest.TestCase):
    def test_build_full_organ_has_44_stops_no_division_or_stopcode_overlap(self):
        xml = build_full_organ()

        division_codes = sorted(set(int(c) for c in re.findall(r"<DivisionCode>(\d+)</DivisionCode>", xml)))
        self.assertEqual(division_codes, [1, 2, 3, 4])

        stop_block = re.search(r'<ObjectList ObjectType="stop">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        stop_codes = [int(c) for c in re.findall(r"<StopCode>(\d+)</StopCode>", stop_block)]
        self.assertEqual(len(stop_codes), 44)
        self.assertEqual(len(set(stop_codes)), 44, "StopCode collision across divisions")

        ranges = {1: (2000, 2099), 2: (2100, 2199), 3: (2200, 2299), 4: (2300, 2399)}
        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for code in stop_codes:
            for div, (lo, hi) in ranges.items():
                if lo <= code <= hi:
                    counts[div] += 1
                    break
            else:
                self.fail(f"StopCode {code} outside any division's reserved range")
        self.assertEqual(counts, {1: 9, 2: 13, 3: 13, 4: 9})

        coupler_block = re.search(r'<ObjectList ObjectType="coupler">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        coupler_codes = sorted(int(c) for c in re.findall(r"<CouplerCode>(\d+)</CouplerCode>", coupler_block))
        self.assertEqual(coupler_codes, [1006, 1011, 1016, 1111, 1116, 1216])

        tremulant_block = re.search(r'<ObjectList ObjectType="tremulant">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        tremulant_codes = sorted(int(c) for c in re.findall(r"<TremulantCode>(\d+)</TremulantCode>", tremulant_block))
        self.assertEqual(tremulant_codes, [1720, 1730])

        rank_block = re.search(r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        trem_codes_on_ranks = re.findall(r"<Trem_TremulantCode>(\d*)</Trem_TremulantCode>", rank_block)
        wired = [c for c in trem_codes_on_ranks if c]
        # 10 Görlitz Oberwerk ranks (Spitzflöte excluded, no trem data) +
        # 8 Zöblitz Brustwerk ranks (Gedackt excluded, no trem data)
        self.assertEqual(len(wired), 18)


if __name__ == "__main__":
    unittest.main()
