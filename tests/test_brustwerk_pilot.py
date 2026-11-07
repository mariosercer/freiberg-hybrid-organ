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


if __name__ == "__main__":
    unittest.main()
