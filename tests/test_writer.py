import re
import unittest
from pathlib import Path

from src.codm.model import Rank
from src.codm.writer import render_custom_organ

ZOBLITZ_PACKAGE_458 = Path(
    "/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458"
)


class TestWriter(unittest.TestCase):
    def test_render_rank_has_no_self_closing_tags_and_escapes_apostrophe(self):
        rank = Rank(rank_id=1, name="Sifflöt 1'", num_pipes=56, first_midi_note=36,
                    package_id=458, main_folder="samples/ow/07_sufflet1/lang/haupt",
                    short_release_folder="samples/ow/07_sufflet1/kurz/haupt",
                    pitch_harmonic_num=64, windchest_division_code=2)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertNotIn("/>", xml)
        # apostrophe is NOT one of the 4 CODM escape characters (& < > "),
        # so it must appear raw, same as in Hauptwerk's own "St. Anne's" examples
        self.assertIn("<Name>Sifflöt 1'</Name>", xml)
        self.assertIn(
            "<Samples_ShortNoteReleaseSampleFileFolderIfAny>samples/ow/07_sufflet1/kurz/haupt"
            "</Samples_ShortNoteReleaseSampleFileFolderIfAny>",
            xml,
        )
        self.assertEqual(xml.count("WindSupply_DivisionCodeOfWindchest>2<"), 1)

    def test_render_escapes_the_four_xml_special_characters_in_names(self):
        rank = Rank(rank_id=1, name='A & B <C> "D"', num_pipes=56, first_midi_note=36,
                    package_id=458, main_folder="x", short_release_folder=None,
                    pitch_harmonic_num=8, windchest_division_code=2)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertIn("<Name>A &amp; B &lt;C&gt; &quot;D&quot;</Name>", xml)
        self.assertNotIn("<Name>A & B <C> \"D\"</Name>", xml)

    def test_render_applies_tuning_adjust_from_rank(self):
        rank = Rank(rank_id=1, name="Test", num_pipes=56, first_midi_note=36,
                    package_id=1, main_folder="x", short_release_folder=None,
                    pitch_harmonic_num=8, windchest_division_code=2,
                    tuning_adjust_semitones_036=-11.8, tuning_adjust_semitones_096=-11.8)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertIn(
            "<Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>-11.8"
            "</Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>",
            xml,
        )

    def test_rendered_sample_folder_matches_case_sensitive_folder_on_disk(self):
        rank = Rank(rank_id=1, name="Sifflöt 1'", num_pipes=56, first_midi_note=36,
                    package_id=458, main_folder="samples/ow/07_sufflet1/lang/haupt",
                    short_release_folder="samples/ow/07_sufflet1/kurz/haupt",
                    pitch_harmonic_num=64, windchest_division_code=2)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        main_folder = re.search(
            r"<Samples_MainSampleFileFolder>(.*?)</Samples_MainSampleFileFolder>", xml
        ).group(1)

        on_disk = ZOBLITZ_PACKAGE_458
        for part in main_folder.split("/"):
            entries = {p.name for p in on_disk.iterdir()}
            self.assertIn(
                part, entries,
                f"'{part}' (exact case) not found on disk under {on_disk}; "
                f"available: {sorted(entries)}",
            )
            on_disk = on_disk / part


if __name__ == "__main__":
    unittest.main()
