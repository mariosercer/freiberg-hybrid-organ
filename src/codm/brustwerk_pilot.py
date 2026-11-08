import re
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
#
# pitch_harmonic_num is NOT simply 64/footage_in_feet - mutation stops are
# named after a traditional nominal footage that does not always match their
# true acoustic pitch (e.g. a historic "Nasat 3'" is often really a 2-2/3'
# mutation). The values below are measured directly from the `smpl` chunk of
# each rank's 060-C.wav, as the frequency ratio to Gedackt 8' (reference
# harmonic 8), confirmed against Hauptwerk's own ExampleCustomOrgan2 (which
# uses harmonic 24 for "Nazard 2 2/3'" and 40 for "Tierce 1 3/5'" - the same
# convention):
#   Gedackt 8'=8, Principal 4'/Rohrfloete 4'=16, Nasat 3'=24, Octava 2'=32,
#   Tertia 1 3/5'=40, Quinta 1 1/2'=48, Sifflöt 1'=64, Mixtur 3f (Cimbel II)=64
# (Cimbel II sounds a full octave above Sifflöt 1', not the same pitch as
# Octava 2' that 64/footage would suggest.)
BRUSTWERK_STOPS = [
    ("Gedackt 8'", "samples/ow/01_gedackt8", 8),
    ("Principal 4'", "samples/ma/04_octava4", 16),
    ("Rohrflöte 4'", "samples/ow/02_rohrfloethe4", 16),
    ("Nasat 3'", "samples/ow/03_nasat3", 24),
    ("Octava 2'", "samples/ow/04_octava2", 32),
    ("Tertia 1 3/5'", "samples/ow/05_tertia135", 40),
    ("Quinta 1 1/2'", "samples/ow/06_quinta112", 48),
    ("Sifflöt 1'", "samples/ow/07_sufflet1", 64),
    ("Mixtur 3f", "samples/ow/08_cimbel2f", 64),
]

# Hauptwerk's division/stop codes are fixed identities, not free labels:
# DivisionCode 1=PEDAL, 2=GREAT (confirmed against the locally installed
# ExampleCustomOrgan1/2). A single-manual pilot must be wired to GREAT (2),
# not PEDAL (1). StopCode for a division's own stops follows
# 2000 + (division_code-1)*100 + index (confirmed: GREAT's own example
# stops are 2101-2106) - the 1xxx range is reserved for couplers.
DIVISION_CODE = 2

# Zöblitz is pitched at Chorton, measured +1.1145 semitones above Görlitz's
# ~440 Hz reference (smpl chunk, Gedackt 8' note 060: 279.08 Hz vs Görlitz's
# 261.68 Hz for "the same" key). Pitch_PipeMIDINoteNum036/096_TuningAdjust-
# PercentSemitones is read as hundredths of a semitone (cents) - "a percent
# of a semitone" is the standard definition of a cent - so the correction
# is -1.1145 * 100 cents, applied flat across the whole compass since the
# whole set is one consistent recording/pressing, not a per-note drift.
# UNVERIFIED: whether Hauptwerk really expects cents here rather than raw
# semitones could not be confirmed without opening Hauptwerk's own in-app
# CODM format documentation (Other | Design tools | View ... format
# documentation) - a human needs to check this before treating it as final.
CHORTON_TUNING_ADJUST_CENTS = -111.45


def _validate_rank_folder(package_root: Path, folder: str, num_pipes: int, first_midi_note: int):
    """Check a rank's sample folder on disk: every path segment exists with
    the exact case given (case-insensitive filesystems like macOS would
    silently accept a wrong-case path that breaks on Windows/Linux), and the
    `.wav` files form a contiguous MIDI note range of exactly `num_pipes`
    notes starting at `first_midi_note`."""
    current = package_root
    for part in folder.split("/"):
        entries = {p.name for p in current.iterdir()} if current.is_dir() else set()
        if part not in entries:
            raise ValueError(f"'{part}' (exact case) not found under {current}; available: {sorted(entries)}")
        current = current / part

    strict_note_file = re.compile(r"^\d{3}-[A-Ga-g]#?\.wav$")
    notes = sorted(
        int(p.name[:3]) for p in current.glob("*.wav") if strict_note_file.match(p.name)
    )
    expected = list(range(first_midi_note, first_midi_note + num_pipes))
    if notes != expected:
        raise ValueError(
            f"{current}: expected contiguous notes {expected[0]}-{expected[-1]} "
            f"({num_pipes} files), found {notes}"
        )


def build_brustwerk_division(zoblitz_root: Path, division_code: int = DIVISION_CODE):
    division = Division(
        division_code=division_code,
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
        stop_code = 2000 + (division_code - 1) * 100 + i
        main_folder = f"{folder}/lang/haupt"
        short_release_folder = f"{folder}/kurz/haupt"

        _validate_rank_folder(zoblitz_root, main_folder, NUM_PIPES, FIRST_MIDI_NOTE)
        _validate_rank_folder(zoblitz_root, short_release_folder, NUM_PIPES, FIRST_MIDI_NOTE)

        ranks.append(
            Rank(
                rank_id=rank_id,
                name=name,
                num_pipes=NUM_PIPES,
                first_midi_note=FIRST_MIDI_NOTE,
                package_id=PACKAGE_ID,
                main_folder=main_folder,
                short_release_folder=short_release_folder,
                short_release_max_ms=200,
                pitch_harmonic_num=pitch_harmonic_num,
                windchest_division_code=division_code,
                tuning_adjust_semitones_036=CHORTON_TUNING_ADJUST_CENTS,
                tuning_adjust_semitones_096=CHORTON_TUNING_ADJUST_CENTS,
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

    return division, ranks, stops, stopranks, REQUIRED_PACKAGES


def build_brustwerk_pilot(zoblitz_root: Path) -> str:
    division, ranks, stops, stopranks, required_packages = build_brustwerk_division(
        zoblitz_root, division_code=DIVISION_CODE
    )
    return render_custom_organ(
        organ_id=ORGAN_ID,
        name="Brustwerk Zoblitz Pilot",
        divisions=[division],
        stops=stops,
        ranks=ranks,
        stopranks=stopranks,
        required_packages=required_packages,
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
