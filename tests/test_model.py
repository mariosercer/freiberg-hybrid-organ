import unittest

from src.codm.model import Rank, Stop, StopRank, Division


class TestModel(unittest.TestCase):
    def test_rank_holds_expected_fields(self):
        r = Rank(rank_id=1, name="Gedackt 8'", num_pipes=56, first_midi_note=36,
                  package_id=458, main_folder="samples/ow/01_gedackt8/lang/haupt",
                  short_release_folder="samples/ow/01_gedackt8/kurz/haupt",
                  pitch_harmonic_num=8, windchest_division_code=2)
        self.assertEqual(r.rank_id, 1)
        self.assertEqual(r.num_pipes, 56)
        self.assertEqual(r.pitch_harmonic_num, 8)
        self.assertEqual(r.windchest_division_code, 2)

    def test_stop_holds_expected_fields(self):
        s = Stop(stop_code=2001, name="Gedackt 8'", display_name="GEDACKT 8")
        self.assertEqual(s.stop_code, 2001)
        self.assertEqual(s.display_name, "GEDACKT 8")

    def test_stoprank_holds_expected_fields(self):
        sr = StopRank(stop_code=2001, rank_id=1, first_mapped_key=36, num_mapped_keys=56)
        self.assertEqual(sr.rank_id, 1)
        self.assertEqual(sr.num_mapped_keys, 56)

    def test_division_holds_expected_fields(self):
        d = Division(division_code=3, name="Brustwerk", short_name="BW",
                      number_of_keys=56, first_key_midi_note=36)
        self.assertEqual(d.division_code, 3)
        self.assertEqual(d.number_of_keys, 56)


if __name__ == "__main__":
    unittest.main()
