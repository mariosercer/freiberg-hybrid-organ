import re
import unittest
from pathlib import Path

from src.codm.pedal_division import build_pedal_division

GOERLITZ_EXTRACT_ROOT = Path(
    "/private/tmp/claude-501/-Users-pilepale-Documents-3D-metal-printing/"
    "fc14fe8b-9442-46d1-bef9-2a24ff20ea02/scratchpad/goerlitz-extract"
)


@unittest.skipUnless(GOERLITZ_EXTRACT_ROOT.is_dir(), "Görlitz scratch extraction not present")
class TestPedalDivision(unittest.TestCase):
    def test_build_pedal_division_has_9_stops_untersatz_as_dual_rank(self):
        division, ranks, stops, stopranks, packages = build_pedal_division(GOERLITZ_EXTRACT_ROOT)

        self.assertEqual(division.division_code, 1)
        self.assertEqual(len(stops), 9)
        self.assertEqual(len(ranks), 10)
        self.assertEqual(len(stopranks), 10)

        stop_codes = [s.stop_code for s in stops]
        self.assertEqual(len(set(stop_codes)), 9)
        for code in stop_codes:
            self.assertTrue(2000 <= code <= 2099, f"StopCode {code} outside 2000-2099")

        untersatz_stop = next(s for s in stops if s.name == "Untersatz 32'+16'")
        untersatz_links = [sr for sr in stopranks if sr.stop_code == untersatz_stop.stop_code]
        self.assertEqual(len(untersatz_links), 2)
        linked_rank_ids = {sr.rank_id for sr in untersatz_links}
        untersatz_rank_names = {r.name for r in ranks if r.rank_id in linked_rank_ids}
        self.assertEqual(untersatz_rank_names, {"Gross Principal-Bass 32'", "Contra-Bass 16'"})

        harmonics = {r.name: r.pitch_harmonic_num for r in ranks}
        expected_harmonics = {
            "Gross Principal-Bass 32'": 2,
            "Contra-Bass 16'": 4,
            "Principalbaß 16'": 4,
            "Subbaß 16'": 4,
            "Octavbaß 8'": 8,
            "Octavbaß 4'": 16,
            "Pedalmixtur 6f": 24,
            "Posaunenbaß 16'": 4,
            "Trompetenbaß 8'": 8,
            "Clarinbaß 4'": 16,
        }
        self.assertEqual(harmonics, expected_harmonics)

        for r in ranks:
            self.assertEqual(r.first_midi_note, 36)
            self.assertEqual(r.num_pipes, 32)

        package_ids = {p[0] for p in packages}
        self.assertEqual(package_ids, {1, 1811, 1812, 1813, 1814})


if __name__ == "__main__":
    unittest.main()
