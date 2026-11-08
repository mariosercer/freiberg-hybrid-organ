import re
import unittest
from pathlib import Path

from src.codm.console_layout import console_size
from src.codm.full_organ import build_full_organ
from src.codm.goerlitz_paths import default_goerlitz_extract_root
from src.codm.model import Division

GOERLITZ_EXTRACT_ROOT = default_goerlitz_extract_root()


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
        # 9 Zöblitz Brustwerk ranks (all 9 have confirmed trem templates,
        # including Gedackt 8' - tremulantTemplates/ow/gedackt8/haupt exists)
        self.assertEqual(len(wired), 19)

    def test_rank_ids_globally_unique_across_all_four_divisions(self):
        xml = build_full_organ()
        rank_block = re.search(r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        rank_ids = [int(c) for c in re.findall(r"<RankID>(\d+)</RankID>", rank_block)]
        self.assertEqual(len(rank_ids), 45)
        self.assertEqual(len(set(rank_ids)), 45, "RankID collision across divisions")

        stoprank_block = re.search(r'<ObjectList ObjectType="stoprank">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        stoprank_rank_ids = [int(c) for c in re.findall(r"<RankID>(\d+)</RankID>", stoprank_block)]
        self.assertEqual(len(stoprank_rank_ids), 45)
        for rid in stoprank_rank_ids:
            self.assertIn(rid, rank_ids, f"stoprank references RankID {rid} not present in rank table")

    def test_tuning_corrections_survive_the_merge(self):
        xml = build_full_organ()
        rank_block = re.search(r'<ObjectList ObjectType="rank">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        values = [
            float(v) for v in re.findall(
                r"<Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>([-\d.]+)"
                r"</Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>",
                rank_block,
            )
        ]
        self.assertEqual(len(values), 45)
        chorton = [v for v in values if abs(v - (-111.45)) < 0.1]
        waltershausen = [v for v in values if abs(v - (-102.36)) < 0.1]
        zero = [v for v in values if v == 0]
        self.assertEqual(len(chorton), 9, "all 9 Brustwerk ranks must carry the Chorton correction")
        self.assertEqual(len(waltershausen), 1, "Bordun 16' must carry the Waltershausen correction")
        self.assertEqual(len(zero), 35, "every Görlitz and Wasselonne rank must stay uncorrected")

    def test_console_graphics_wired_for_all_elements(self):
        xml = build_full_organ()

        stop_block = re.search(r'<ObjectList ObjectType="stop">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        coupler_block = re.search(r'<ObjectList ObjectType="coupler">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        tremulant_block = re.search(r'<ObjectList ObjectType="tremulant">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        division_block = re.search(r'<ObjectList ObjectType="division">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        general_block = re.search(r'<ObjectList ObjectType="_general">(.*?)</ObjectList>', xml, re.DOTALL).group(1)

        control_positions = {}
        for block, count, prefix, code_tag in [
            (stop_block, 44, "stop", "StopCode"),
            (coupler_block, 6, "coupler", "CouplerCode"),
            (tremulant_block, 2, "tremulant", "TremulantCode"),
        ]:
            objs = re.findall(r"<(?:stop|coupler|tremulant)>(.*?)</(?:stop|coupler|tremulant)>", block, re.DOTALL)
            self.assertEqual(len(objs), count, f"expected {count} {prefix} objects")
            for obj in objs:
                code = re.search(rf"<{code_tag}>(\d+)</{code_tag}>", obj).group(1)
                page_id = re.search(r"<CustomDisplay1_DisplayPageID>(\d*)</CustomDisplay1_DisplayPageID>", obj).group(1)
                style_id = re.search(r"<CustomDisplay1_ControlStyleID>(\d*)</CustomDisplay1_ControlStyleID>", obj).group(1)
                x = re.search(r"<CustomDisplay1_PosPixels_X>(\d*)</CustomDisplay1_PosPixels_X>", obj).group(1)
                y = re.search(r"<CustomDisplay1_PosPixels_Y>(\d*)</CustomDisplay1_PosPixels_Y>", obj).group(1)
                self.assertEqual(page_id, "1", f"{prefix}:{code} missing CustomDisplay1_DisplayPageID")
                self.assertEqual(style_id, "1", f"{prefix}:{code} missing CustomDisplay1_ControlStyleID")
                control_positions[f"{prefix}:{code}"] = (int(x), int(y))

        division_objs = re.findall(r"<division>(.*?)</division>", division_block, re.DOTALL)
        self.assertEqual(len(division_objs), 4)

        divisions = []
        keyboard_anchors = {}
        for obj in division_objs:
            division_code = int(re.search(r"<DivisionCode>(\d+)</DivisionCode>", obj).group(1))
            number_of_keys = int(re.search(r"<NumberOfKeys>(\d+)</NumberOfKeys>", obj).group(1))
            first_key = int(re.search(r"<MIDINoteNumOfFirstKey>(\d+)</MIDINoteNumOfFirstKey>", obj).group(1))
            keyboard_page_id = re.search(
                r"<CustomDisplay1_Keyboard_DisplayPageID>(\d*)</CustomDisplay1_Keyboard_DisplayPageID>", obj
            ).group(1)
            keyboard_style_id = re.search(
                r"<CustomDisplay1_Keyboard_KeyboardStyleID>(\d*)</CustomDisplay1_Keyboard_KeyboardStyleID>", obj
            ).group(1)
            keyboard_x = int(
                re.search(r"<CustomDisplay1_Keyboard_PosPixels_X>(\d*)</CustomDisplay1_Keyboard_PosPixels_X>", obj).group(1)
            )
            keyboard_y = int(
                re.search(r"<CustomDisplay1_Keyboard_PosPixels_Y>(\d*)</CustomDisplay1_Keyboard_PosPixels_Y>", obj).group(1)
            )

            self.assertEqual(keyboard_page_id, "1", f"division {division_code} missing keyboard DisplayPageID")
            expected_style = "2" if division_code == 1 else "1"
            self.assertEqual(keyboard_style_id, expected_style, f"division {division_code} wrong KeyboardStyleID")

            divisions.append(Division(
                division_code=division_code, name="x", short_name="x",
                number_of_keys=number_of_keys, first_key_midi_note=first_key,
            ))
            keyboard_anchors[division_code] = (keyboard_x, keyboard_y)

        declared_width = int(
            re.search(r"<CustomDisplay_ConsoleWidthPixels>(\d+)</CustomDisplay_ConsoleWidthPixels>", general_block).group(1)
        )
        declared_height = int(
            re.search(r"<CustomDisplay_ConsoleHeightPixels>(\d+)</CustomDisplay_ConsoleHeightPixels>", general_block).group(1)
        )
        declared_default_page = re.search(
            r"<CustomDisplay_DefaultDisplayPageID>(\d*)</CustomDisplay_DefaultDisplayPageID>", general_block
        ).group(1)
        self.assertEqual(declared_default_page, "1")

        expected_width, expected_height = console_size(control_positions, keyboard_anchors, divisions)
        self.assertGreaterEqual(
            declared_width, expected_width,
            "declared console width smaller than the actual laid-out content",
        )
        self.assertGreaterEqual(
            declared_height, expected_height,
            "declared console height smaller than the actual laid-out content",
        )


if __name__ == "__main__":
    unittest.main()
