import re
import unittest
from pathlib import Path

from src.codm.goerlitz_paths import default_goerlitz_extract_root
from src.codm.hauptwerk_division import build_hauptwerk_division

GOERLITZ_EXTRACT_ROOT = default_goerlitz_extract_root()
WALTERSHAUSEN_ROOT = Path(
    "/Volumes/Samsung T7/Orgulje/Trost Waltershausen/OrganInstallationPackages"
)


@unittest.skipUnless(GOERLITZ_EXTRACT_ROOT.is_dir(), "Görlitz scratch extraction not present")
class TestHauptwerkDivision(unittest.TestCase):
    def test_build_hauptwerk_division_has_13_stops_wired_correctly(self):
        division, ranks, stops, stopranks, packages = build_hauptwerk_division(
            GOERLITZ_EXTRACT_ROOT, WALTERSHAUSEN_ROOT
        )

        self.assertEqual(division.division_code, 2)
        self.assertEqual(len(ranks), 13)
        self.assertEqual(len(stops), 13)
        self.assertEqual(len(stopranks), 13)

        stop_codes = [s.stop_code for s in stops]
        self.assertEqual(len(set(stop_codes)), 13)
        for code in stop_codes:
            self.assertTrue(2100 <= code <= 2199, f"StopCode {code} outside 2100-2199")

        rank_ids = [r.rank_id for r in ranks]
        self.assertEqual(len(set(rank_ids)), 13)

        harmonics = {r.name: r.pitch_harmonic_num for r in ranks}
        expected_harmonics = {
            "Principal 8'": 8,
            "Viol di Gamba 8'": 8,
            "Rohrflöte 8'": 8,
            "Octava 4'": 16,
            "Quinta 3'": 24,
            "Super-Octava 2'": 32,
            "Tertia 1 3/5'": 40,
            "Mixtur 4f": 24,
            "Cimbeln 3f": 32,
            "Cornet 5f": 8,
            "Trompet 8'": 8,
            "Clarin 4'": 16,
            "Bordun 16'": 4,
        }
        self.assertEqual(harmonics, expected_harmonics)

        # Cornet 5f is treble-only (measured 053-093 on disk)
        cornet = next(r for r in ranks if r.name == "Cornet 5f")
        self.assertEqual(cornet.first_midi_note, 53)
        self.assertEqual(cornet.num_pipes, 41)

        # Bordun 16' (Waltershausen) is shorter than the 58-key Görlitz compass
        bordun = next(r for r in ranks if r.name == "Bordun 16'")
        self.assertEqual(bordun.first_midi_note, 36)
        self.assertEqual(bordun.num_pipes, 54)
        self.assertEqual(bordun.package_id, 255)
        # Waltershausen is documented at 466.8 Hz (spec-stated, not measured -
        # its samples are encrypted); correction = -12*log2(466.8/440)*100 cents
        self.assertAlmostEqual(bordun.tuning_adjust_cents_036, -102.36, places=1)
        self.assertAlmostEqual(bordun.tuning_adjust_cents_096, -102.36, places=1)

        # Görlitz's own ranks need no correction - they ARE the 440Hz reference
        principal = next(r for r in ranks if r.name == "Principal 8'")
        self.assertEqual(principal.tuning_adjust_cents_036, 0)

        package_ids = {p[0] for p in packages}
        self.assertEqual(package_ids, {1, 1811, 1812, 1813, 255})


if __name__ == "__main__":
    unittest.main()
