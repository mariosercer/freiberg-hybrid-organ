import re
import unittest
from pathlib import Path

from src.codm.brustwerk_pilot import build_brustwerk_pilot, build_brustwerk_division

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

    def test_pitch_harmonic_numbers_match_measured_sample_pitch_ratios(self):
        # Measured directly from the smpl chunks of 060-C.wav across all 9
        # rank folders (ratio to Gedackt 8' x8): 8, 16, 16, 24, 32, 40, 48,
        # 64, 64. Nasat 3' is acoustically a 2-2/3' mutation (harmonic 24,
        # not 64/3=21.33), Quinta 1 1/2' is acoustically 1-1/3' (harmonic
        # 48, not 64/1.5=42.67), and Mixtur 3f (Cimbel II) sounds a full
        # octave above the 1' Sifflöt (harmonic 64, not 32).
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        rank_block = re.search(
            r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        harmonics = [
            (name, float(harm))
            for name, harm in re.findall(
                r"<Name>([^<]*)</Name>.*?<Pitch_RankBaseOutputPitch64ftHarmonicNum>"
                r"([\d.]+)</Pitch_RankBaseOutputPitch64ftHarmonicNum>",
                rank_block,
                re.DOTALL,
            )
        ]
        expected = {
            "Gedackt 8'": 8,
            "Principal 4'": 16,
            "Rohrflöte 4'": 16,
            "Nasat 3'": 24,
            "Octava 2'": 32,
            "Tertia 1 3/5'": 40,
            "Quinta 1 1/2'": 48,
            "Sifflöt 1'": 64,
            "Mixtur 3f": 64,
        }
        actual = dict(harmonics)
        self.assertEqual(actual, expected)

    def test_stops_wired_to_a_manual_division_not_pedal(self):
        # DivisionCode is a fixed Hauptwerk identity, not a free label:
        # 1=PEDAL, 2=GREAT (confirmed against Hauptwerk's own
        # ExampleCustomOrgan1/2). A single-manual pilot must use division 2,
        # and its StopCodes must fall in the 2100-2199 range reserved for
        # that division's stops (2000 + (division-1)*100 + index) - not the
        # 1xxx range, which Hauptwerk reserves for couplers.
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        division_code = re.search(r"<DivisionCode>(\d+)</DivisionCode>", xml).group(1)
        self.assertEqual(division_code, "2")

        stop_block = re.search(
            r'<ObjectList ObjectType="stop">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        stop_codes = [int(c) for c in re.findall(r"<StopCode>(\d+)</StopCode>", stop_block)]
        self.assertEqual(len(stop_codes), 9)
        for code in stop_codes:
            self.assertTrue(2100 <= code <= 2199, f"StopCode {code} outside GREAT's 2100-2199 range")

    def test_rank_ids_unique_and_stoprank_references_resolve(self):
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        rank_block = re.search(
            r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        rank_ids = [int(x) for x in re.findall(r"<RankID>(\d+)</RankID>", rank_block)]
        self.assertEqual(len(rank_ids), 9)
        self.assertEqual(len(set(rank_ids)), len(rank_ids))

        stop_block = re.search(
            r'<ObjectList ObjectType="stop">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        stop_codes = {int(x) for x in re.findall(r"<StopCode>(\d+)</StopCode>", stop_block)}

        stoprank_block = re.search(
            r'<ObjectList ObjectType="stoprank">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        stopranks = re.findall(
            r"<StopCode>(\d+)</StopCode>\s*<RankTypeCode>\d+</RankTypeCode>\s*<RankID>(\d+)</RankID>",
            stoprank_block,
        )
        self.assertEqual(len(stopranks), 9)
        for stop_code_str, rank_id_str in stopranks:
            self.assertIn(int(stop_code_str), stop_codes)
            self.assertIn(int(rank_id_str), rank_ids)

    def test_short_release_max_ms_still_set_after_model_extension(self):
        # Regression guard: writer.py used to hardcode 200ms whenever a
        # short_release_folder was set; that was replaced by an explicit
        # Rank.short_release_max_ms field (needed for Görlitz, whose
        # short-release thresholds vary per rank). Brustwerk must keep
        # passing 200 explicitly or this value silently drops to 0.
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        rank_block = re.search(
            r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL
        ).group(1)
        values = re.findall(
            r"<Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny>(\d+)"
            r"</Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny>",
            rank_block,
        )
        self.assertEqual(len(values), 9)
        self.assertTrue(all(v == "200" for v in values))


    def test_build_brustwerk_division_uses_given_division_code(self):
        # When Brustwerk is merged with the other 3 divisions (Task 5), it
        # can no longer sit on DivisionCode 2 (GREAT) - that collides with
        # Hauptwerk. build_brustwerk_division must accept the division
        # code as a parameter and derive StopCodes from it, same formula
        # as every other division module (2000 + (division_code-1)*100 + i).
        division, ranks, stops, stopranks, packages = build_brustwerk_division(
            ZOBLITZ_ROOT, division_code=4
        )
        self.assertEqual(division.division_code, 4)
        stop_codes = [s.stop_code for s in stops]
        self.assertEqual(len(stop_codes), 9)
        for code in stop_codes:
            self.assertTrue(2300 <= code <= 2399, f"StopCode {code} outside 2300-2399")
        for r in ranks:
            self.assertEqual(r.windchest_division_code, 4)

    def test_all_ranks_corrected_from_chorton_to_440hz(self):
        # Measured directly from smpl chunks: Zöblitz's Gedackt 8' (note 060)
        # sounds at 279.08 Hz vs Görlitz's reference 261.68 Hz for the "same"
        # key - a +1.1145 semitone Chorton offset. TuningAdjustPercentSemitones
        # is read as hundredths of a semitone (cents), so the correction is
        # -1.1145 * 100 = -111.45, applied flat across the compass (same value
        # at note 036 and 096, since the whole set is one consistent pressing).
        # tuning_adjust_cents must be passed explicitly - it is NOT automatic,
        # because the standalone pilot organ (build_brustwerk_pilot) has
        # nothing to harmonize against and must stay uncorrected (see
        # test_build_brustwerk_pilot_stays_uncorrected below).
        expected = -111.45
        _, ranks, _, _, _ = build_brustwerk_division(ZOBLITZ_ROOT, division_code=4,
                                                       tuning_adjust_cents=expected)
        for r in ranks:
            self.assertAlmostEqual(r.tuning_adjust_cents_036, expected, places=1)
            self.assertAlmostEqual(r.tuning_adjust_cents_096, expected, places=1)

    def test_build_brustwerk_pilot_stays_uncorrected(self):
        # The standalone pilot organ (not merged with anything) must NOT
        # inherit the hybrid's Chorton correction - there is nothing for it
        # to harmonize against, so it should keep playing at its own native
        # pitch, same as when it was first built and reviewed.
        xml = build_brustwerk_pilot(ZOBLITZ_ROOT)
        self.assertIn(
            "<Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>0.0</Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>",
            xml,
        )
        self.assertNotIn("-111.45", xml)


if __name__ == "__main__":
    unittest.main()
