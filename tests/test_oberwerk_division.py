import unittest
from pathlib import Path

from src.codm.goerlitz_paths import default_goerlitz_extract_root
from src.codm.oberwerk_division import build_oberwerk_division

GOERLITZ_EXTRACT_ROOT = default_goerlitz_extract_root()
WASSELONNE_ROOT = Path(
    "/Volumes/Samsung T7/Orgulje/Silbermann Wasselonne/OrganInstallationPackages/000802"
)


@unittest.skipUnless(GOERLITZ_EXTRACT_ROOT.is_dir(), "Görlitz scratch extraction not present")
class TestOberwerkDivision(unittest.TestCase):
    def test_build_oberwerk_division_has_13_stops_wired_correctly(self):
        division, ranks, stops, stopranks, packages = build_oberwerk_division(
            GOERLITZ_EXTRACT_ROOT, WASSELONNE_ROOT
        )

        self.assertEqual(division.division_code, 3)
        self.assertEqual(len(ranks), 13)
        self.assertEqual(len(stops), 13)
        self.assertEqual(len(stopranks), 13)

        stop_codes = [s.stop_code for s in stops]
        self.assertEqual(len(set(stop_codes)), 13)
        for code in stop_codes:
            self.assertTrue(2200 <= code <= 2299, f"StopCode {code} outside 2200-2299")

        harmonics = {r.name: r.pitch_harmonic_num for r in ranks}
        expected_harmonics = {
            "Quintaden 16'": 4,
            "Principal 8'": 8,
            "Gedackt 8'": 8,
            "Quintaden 8'": 8,
            "Octava 4'": 16,
            "Spitzflöte 4'": 16,
            "Super-Oktava 2'": 32,
            "Flaschlöt 1'": 64,
            "Mixtur 3f": 24,
            "Cimbeln 2f": 32,
            "Krumbhorn 8'": 8,
            "Echo 5f": 8,
            "Vox humana 8'": 8,
        }
        self.assertEqual(harmonics, expected_harmonics)

        echo = next(r for r in ranks if r.name == "Echo 5f")
        self.assertEqual(echo.first_midi_note, 60)
        self.assertEqual(echo.num_pipes, 25)
        self.assertEqual(echo.package_id, 802)
        # Review Focus #4: "long" (the only tier with cue+loop points,
        # measured separately) must be the MAIN folder, not short/medium.
        self.assertEqual(echo.main_folder, "EchoCornet/long")
        self.assertEqual(echo.short_release_folder, "EchoCornet/short")
        self.assertEqual(echo.medium_release_folder, "EchoCornet/medium")

        vox = next(r for r in ranks if r.name == "Vox humana 8'")
        self.assertEqual(vox.first_midi_note, 36)
        self.assertEqual(vox.num_pipes, 49)
        self.assertEqual(vox.main_folder, "GoVoixHumaine8/long")
        self.assertEqual(vox.short_release_folder, "GoVoixHumaine8/short")
        self.assertEqual(vox.medium_release_folder, "GoVoixHumaine8/medium")

        package_ids = {p[0] for p in packages}
        self.assertEqual(package_ids, {1, 1812, 1813, 802})

    def test_wasselonne_ranks_need_no_pitch_correction(self):
        # Measured directly from smpl chunks: Wasselonne's EchoCornet and
        # GoVoixHumaine8 (note 060) are within 0.004 semitones of Görlitz's
        # 440Hz reference - measurement noise, not a real pitch-standard
        # difference. Deliberately left uncorrected (tuning_adjust=0), unlike
        # Zöblitz/Waltershausen - this is a documented finding, not an
        # oversight someone should "fix" later.
        _, ranks, _, _, _ = build_oberwerk_division(GOERLITZ_EXTRACT_ROOT, WASSELONNE_ROOT)
        for name in ["Echo 5f", "Vox humana 8'"]:
            r = next(r for r in ranks if r.name == name)
            self.assertEqual(r.tuning_adjust_cents_036, 0)
            self.assertEqual(r.tuning_adjust_cents_096, 0)


if __name__ == "__main__":
    unittest.main()
