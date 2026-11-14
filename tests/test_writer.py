import re
import unittest
from pathlib import Path

from src.codm.model import Coupler, Division, Rank, Stop, StopRank, Tremulant
from src.codm.local_paths import zoblitz_root
from src.codm.writer import render_custom_organ

ZOBLITZ_PACKAGE_458 = zoblitz_root()


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

    def test_disabled_wind_model_has_zero_parameters(self):
        # Hauptwerk error 5603: wind model params only if the wind model is enabled.
        d = Division(division_code=1, name="PEDAL", short_name="Pedal",
                     number_of_keys=32, first_key_midi_note=36)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[d], stops=[],
                                   ranks=[], stopranks=[], required_packages=[])
        self.assertIn("<WindModel_EnableWindModel>N</WindModel_EnableWindModel>", xml)
        params = re.findall(r"<WindModel_(?!EnableWindModel)\w+>([^<]*)</", xml)
        self.assertEqual(params, ["0", "0", "0", "0"])

    def test_every_stoprank_has_a_name(self):
        # Hauptwerk error 0801: StopRank 'Name' is mandatory.
        def rank(rid, name):
            return Rank(rank_id=rid, name=name, num_pipes=32, first_midi_note=36,
                        package_id=1811, main_folder="x", short_release_folder="x",
                        pitch_harmonic_num=8, windchest_division_code=1)
        stops = [Stop(stop_code=1001, name="Subbass 16'", display_name="SUBBASS 16"),
                 Stop(stop_code=1002, name="Untersatz 32'+16'", display_name="UNTERSATZ")]
        ranks = [rank(1, "Subbass 16'"), rank(2, "Gross Principal-Bass 32'"), rank(3, "Contra-Bass 16'")]
        stopranks = [StopRank(stop_code=1001, rank_id=1, first_mapped_key=36, num_mapped_keys=32),
                     StopRank(stop_code=1002, rank_id=2, first_mapped_key=36, num_mapped_keys=32),
                     StopRank(stop_code=1002, rank_id=3, first_mapped_key=36, num_mapped_keys=32)]
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=stops,
                                   ranks=ranks, stopranks=stopranks, required_packages=[])
        block = re.search(r'<ObjectList ObjectType="stoprank">(.*?)</ObjectList>', xml, re.DOTALL).group(1)
        names = re.findall(r"<Name>([^<]*)</Name>", block)
        self.assertEqual(names, ["Subbass 16'", "Gross Principal-Bass 32'", "Contra-Bass 16'"])

    def test_required_package_short_name_capped_at_32_chars(self):
        # Hauptwerk error 0806: RequiredInstallationPackage ShortName > 32 chars.
        pkg = (255, "OrganART 1730 Trost Package-000255-PatchV3.2", 15, "OrganArt Media", None)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[pkg])
        short_names = re.findall(r"<ShortName>([^<]*)</ShortName>", xml)
        self.assertIn("OrganART1730TrostPackage000255Pa", short_names)
        self.assertTrue(all(len(s) <= 32 for s in short_names))

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
                    tuning_adjust_cents_036=-11.8, tuning_adjust_cents_096=-11.8)
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertIn(
            "<Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>-11.8"
            "</Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones>",
            xml,
        )

    def test_render_rank_with_separate_rel_and_medium_release_folders(self):
        rank = Rank(rank_id=1, name="Grossoctava 8'", num_pipes=58, first_midi_note=36,
                    package_id=1811, main_folder="pipes/HW/01-AB_grossoct8",
                    short_release_folder="pipes/HW/01-AB_grossoct8/rel00200",
                    pitch_harmonic_num=8, windchest_division_code=2,
                    short_release_max_ms=200,
                    medium_release_folder="pipes/HW/01-AB_grossoct8/rel00450",
                    medium_release_max_ms=450,
                    rel_release_folder="pipes/HW/01-AB_grossoct8/rel99999")
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertIn(
            "<Samples_RelSampleFileFolderIfRelSamplesStoredInSeparateFiles>"
            "pipes/HW/01-AB_grossoct8/rel99999"
            "</Samples_RelSampleFileFolderIfRelSamplesStoredInSeparateFiles>",
            xml,
        )
        self.assertIn(
            "<Samples_MediumNoteReleaseSampleFileFolderIfAny>pipes/HW/01-AB_grossoct8/rel00450"
            "</Samples_MediumNoteReleaseSampleFileFolderIfAny>",
            xml,
        )
        self.assertIn(
            "<Samples_MaxNoteTimeMsForMediumNoteReleaseSamplesIfAny>450"
            "</Samples_MaxNoteTimeMsForMediumNoteReleaseSamplesIfAny>",
            xml,
        )
        self.assertIn(
            "<Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny>200"
            "</Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny>",
            xml,
        )

    def test_render_includes_given_couplers_and_tremulants(self):
        coupler = Coupler(coupler_code=1111, name="Coupler: Sw to Gt", display_name="SW TO GT")
        tremulant = Tremulant(tremulant_code=1720, name="Tremulant: Oberwerk", display_name="TREMULANT")
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   couplers=[coupler], tremulants=[tremulant])
        self.assertIn("<CouplerCode>1111</CouplerCode>", xml)
        self.assertIn("<TremulantCode>1720</TremulantCode>", xml)

    def test_render_rank_with_tremulant_waveform_fields(self):
        rank = Rank(rank_id=1, name="Octava 2'", num_pipes=58, first_midi_note=36,
                    package_id=1812, main_folder="pipes/OW/01-AB_octava4",
                    short_release_folder=None, pitch_harmonic_num=16, windchest_division_code=3,
                    trem_code=1720, trem_package_id=1812, trem_waveform_folder="pipes/OW/01-AB_octava4/trem")
        xml = render_custom_organ(organ_id=800100, name="Test", divisions=[], stops=[],
                                   ranks=[rank], stopranks=[], required_packages=[])
        self.assertIn("<Trem_TremulantCode>1720</Trem_TremulantCode>", xml)
        self.assertIn("<Trem_SampleInstallationPackageID>1812</Trem_SampleInstallationPackageID>", xml)
        self.assertIn(
            "<Trem_WaveformSampleFileFolder>pipes/OW/01-AB_octava4/trem</Trem_WaveformSampleFileFolder>", xml
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
