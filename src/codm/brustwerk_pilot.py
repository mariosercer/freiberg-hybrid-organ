from pathlib import Path

from src.codm.model import Division, Rank, Stop, StopRank
from src.codm.writer import render_custom_organ

ORGAN_ID = 800100
PACKAGE_ID = 458
FIRST_MIDI_NOTE = 36
NUM_PIPES = 56

REQUIRED_PACKAGES = [
    (1, "Hauptwerk Standard Components", 1, "Milan Digital Audio", "4"),
    (PACKAGE_ID, "Stadtkirche Zöblitz standard", 11, "PROSPECTUM", "2.01"),
]

# (stop name, source rank folder relative to the package root, pitch_harmonic_num)
# pitch_harmonic_num = 64 / footage_in_feet. Nasat 3' (21.33) and Quinta 1 1/2'
# (42.67) are not whole numbers for this footage - rounded here to the nearest
# integer (21 and 43) as a placeholder. MUST be confirmed against Hauptwerk's
# own "Other | Design tools | View Custom Organ Design Module ... format
# documentation" before this file is treated as final - Claude has no tool to
# drive that desktop app, so a human needs to check this.
BRUSTWERK_STOPS = [
    ("Gedackt 8'", "samples/ow/01_gedackt8", 8),
    ("Principal 4'", "samples/ma/04_octava4", 16),
    ("Rohrflöte 4'", "samples/ow/02_rohrfloethe4", 16),
    ("Nasat 3'", "samples/ow/03_nasat3", 21),
    ("Octava 2'", "samples/ow/04_octava2", 32),
    ("Tertia 1 3/5'", "samples/ow/05_tertia135", 40),
    ("Quinta 1 1/2'", "samples/ow/06_quinta112", 43),
    ("Sifflöt 1'", "samples/ow/07_sufflet1", 64),
    ("Mixtur 3f", "samples/ow/08_cimbel2f", 32),
]


def build_brustwerk_pilot(zoblitz_root: Path) -> str:
    division = Division(
        division_code=1,
        name="BRUSTWERK",
        short_name="Brustwerk",
        number_of_keys=NUM_PIPES,
        first_key_midi_note=FIRST_MIDI_NOTE,
    )

    ranks = []
    stops = []
    stopranks = []
    for i, (name, folder, pitch_harmonic_num) in enumerate(BRUSTWERK_STOPS, start=1):
        rank_id = i
        stop_code = 1000 + i
        main_folder = f"{folder}/lang/haupt"
        short_release_folder = f"{folder}/kurz/haupt"

        main_dir = zoblitz_root / main_folder
        num_on_disk = len(list(main_dir.glob("*.wav"))) if main_dir.is_dir() else 0
        if num_on_disk != NUM_PIPES:
            raise ValueError(
                f"{name}: expected {NUM_PIPES} samples in {main_dir}, found {num_on_disk}"
            )

        ranks.append(
            Rank(
                rank_id=rank_id,
                name=name,
                num_pipes=NUM_PIPES,
                first_midi_note=FIRST_MIDI_NOTE,
                package_id=PACKAGE_ID,
                main_folder=main_folder,
                short_release_folder=short_release_folder,
                pitch_harmonic_num=pitch_harmonic_num,
            )
        )
        stops.append(
            Stop(stop_code=stop_code, name=name, display_name=name.upper())
        )
        stopranks.append(
            StopRank(
                stop_code=stop_code,
                rank_id=rank_id,
                first_mapped_key=FIRST_MIDI_NOTE,
                num_mapped_keys=NUM_PIPES,
            )
        )

    return render_custom_organ(
        organ_id=ORGAN_ID,
        name="Brustwerk Zoblitz Pilot",
        divisions=[division],
        stops=stops,
        ranks=ranks,
        stopranks=stopranks,
        required_packages=REQUIRED_PACKAGES,
    )


def main():
    zoblitz_root = Path(
        "/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458"
    )
    xml = build_brustwerk_pilot(zoblitz_root)
    out_path = Path(
        "/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/"
        "BrustwerkZoblitzPilot.CustomOrgan_Hauptwerk_xml"
    )
    out_path.write_text(xml, encoding="utf-8")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
