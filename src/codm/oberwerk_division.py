from pathlib import Path

from src.codm.brustwerk_pilot import _validate_rank_folder
from src.codm.goerlitz_paths import goerlitz_package_root
from src.codm.model import Division, Rank, Stop, StopRank

DIVISION_CODE = 3
FIRST_MIDI_NOTE = 36
NUM_PIPES = 58  # same Görlitz manual compass as Hauptwerk: C-a''' (MIDI 36-93)

GOERLITZ_PACKAGES = {
    1812: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.10"),
    1813: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.0"),
}
WASSELONNE_PACKAGE_ID = 802
WASSELONNE_PACKAGE = ("Jeux d'orgues 3 - Silbermann (1745)", 40, "Jeuxdorgues", "1.00")

REQUIRED_PACKAGES = [
    (1, "Hauptwerk Standard Components", 1, "Milan Digital Audio", "4"),
] + [
    (pkg_id, *meta) for pkg_id, meta in GOERLITZ_PACKAGES.items()
] + [
    (WASSELONNE_PACKAGE_ID, *WASSELONNE_PACKAGE),
]

# Pitch_RankBaseOutputPitch64ftHarmonicNum measured from each rank's 060-C.wav
# smpl chunk, as the frequency ratio to Görlitz OW's own Principal 8'
# (reference harmonic 8) - see hauptwerk_division.py for why this is not
# simply 64/nominal_footage. Mixtur 3f (Scharff-Mixtur) measured 24 (its
# lowest component at note 60), same mixture-break caveat as elsewhere.
# Flaschlöt 1' (Super-Sedecima) measured 64 (=64/1, a true 1' - consistent
# with its name, unlike the mutation stops). Quintaden 16' measured 4
# (=64/16, a true 16' - "Quintade" describes the tone colour/construction,
# not a mutation pitch). Echo 5f and Vox humana 8' (Wasselonne) both
# measured cleanly at harmonic 8 (true 8' pitch), confirmed against their
# own nominal footage.
#
# (name, package_id, rank_folder, num_pipes, first_midi_note,
#  pitch_harmonic_num, short_dir, short_ms, medium_dir, medium_ms, rel_dir)
OBERWERK_STOPS = [
    ("Quintaden 16'", 1813, "pipes/OW/01-AB_quintd16", 58, 36, 4, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Principal 8'", 1812, "pipes/OW/01-AB_Principal8", 58, 36, 8, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Gedackt 8'", 1812, "pipes/OW/01-AB_Gedackt8", 58, 36, 8, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Quintaden 8'", 1812, "pipes/OW/01-AB_Quintadena8", 58, 36, 8, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Octava 4'", 1812, "pipes/OW/01-AB_octava4", 58, 36, 16, "rel00200", 200, "rel00460", 460, "rel99999"),
    # Spitzflöte 4' is cross-borrowed from Görlitz's HW division, not OW.
    ("Spitzflöte 4'", 1812, "pipes/HW/01-AB_spitzflt4", 58, 36, 16, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Super-Oktava 2'", 1812, "pipes/OW/01-AB_sedecima2", 58, 36, 32, "rel00200", 200, "rel00460", 460, "rel99999"),
    # Flaschlöt 1' and Mixtur 3f are cross-borrowed from Görlitz's BW division.
    ("Flaschlöt 1'", 1813, "pipes/BW/01-AB_supersed1", 58, 36, 64, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Mixtur 3f", 1813, "pipes/BW/01-AB_scharfmix3", 58, 36, 24, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Cimbeln 2f", 1812, "pipes/OW/01-AB_scharfcimbel", 58, 36, 32, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Krumbhorn 8'", 1812, "pipes/OW/01-AB_krumhorn8", 58, 36, 8, "rel00200", 200, "rel00460", 460, "rel99999"),
]

# Wasselonne's short/medium/long folders carry no numeric ms threshold in
# their names (unlike Görlitz's relNNNNN convention) - no vendor-documented
# value exists, so these are reasonable defaults, not measurements.
WASSELONNE_SHORT_MS = 200
WASSELONNE_MEDIUM_MS = 500

# (name, rank_folder, num_pipes, first_midi_note, pitch_harmonic_num)
WASSELONNE_STOPS = [
    ("Echo 5f", "EchoCornet", 25, 60, 8),
    ("Vox humana 8'", "GoVoixHumaine8", 49, 36, 8),
]


def build_oberwerk_division(goerlitz_extract_root: Path, wasselonne_root: Path, rank_id_base: int = 1):
    division = Division(
        division_code=DIVISION_CODE,
        name="OBERWERK",
        short_name="Oberwerk",
        number_of_keys=NUM_PIPES,
        first_key_midi_note=FIRST_MIDI_NOTE,
    )

    ranks = []
    stops = []
    stopranks = []

    for i, (name, pkg_id, folder, num_pipes, first_midi_note, harmonic,
            short_dir, short_ms, medium_dir, medium_ms, rel_dir) in enumerate(OBERWERK_STOPS, start=1):
        rank_id = rank_id_base + i - 1
        stop_code = 2000 + (DIVISION_CODE - 1) * 100 + i

        pkg_root = goerlitz_package_root(goerlitz_extract_root, pkg_id)
        short_release_folder = f"{folder}/{short_dir}"
        medium_release_folder = f"{folder}/{medium_dir}"
        rel_release_folder = f"{folder}/{rel_dir}"

        _validate_rank_folder(pkg_root, folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, short_release_folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, medium_release_folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, rel_release_folder, num_pipes, first_midi_note)

        ranks.append(
            Rank(
                rank_id=rank_id, name=name, num_pipes=num_pipes, first_midi_note=first_midi_note,
                package_id=pkg_id, main_folder=folder,
                short_release_folder=short_release_folder, short_release_max_ms=short_ms,
                medium_release_folder=medium_release_folder, medium_release_max_ms=medium_ms,
                rel_release_folder=rel_release_folder,
                pitch_harmonic_num=harmonic, windchest_division_code=DIVISION_CODE,
            )
        )
        stops.append(Stop(stop_code=stop_code, name=name, display_name=name.upper()))
        stopranks.append(
            StopRank(stop_code=stop_code, rank_id=rank_id,
                     first_mapped_key=first_midi_note, num_mapped_keys=num_pipes)
        )

    next_rank_id = rank_id_base + len(OBERWERK_STOPS)
    next_stop_index = len(OBERWERK_STOPS) + 1
    for name, folder, num_pipes, first_midi_note, harmonic in WASSELONNE_STOPS:
        rank_id = next_rank_id
        stop_code = 2000 + (DIVISION_CODE - 1) * 100 + next_stop_index
        next_rank_id += 1
        next_stop_index += 1

        main_folder = f"{folder}/long"
        short_release_folder = f"{folder}/short"
        medium_release_folder = f"{folder}/medium"

        _validate_rank_folder(wasselonne_root, main_folder, num_pipes, first_midi_note)
        _validate_rank_folder(wasselonne_root, short_release_folder, num_pipes, first_midi_note)
        _validate_rank_folder(wasselonne_root, medium_release_folder, num_pipes, first_midi_note)

        ranks.append(
            Rank(
                rank_id=rank_id, name=name, num_pipes=num_pipes, first_midi_note=first_midi_note,
                package_id=WASSELONNE_PACKAGE_ID, main_folder=main_folder,
                short_release_folder=short_release_folder, short_release_max_ms=WASSELONNE_SHORT_MS,
                medium_release_folder=medium_release_folder, medium_release_max_ms=WASSELONNE_MEDIUM_MS,
                pitch_harmonic_num=harmonic, windchest_division_code=DIVISION_CODE,
            )
        )
        stops.append(Stop(stop_code=stop_code, name=name, display_name=name.upper()))
        stopranks.append(
            StopRank(stop_code=stop_code, rank_id=rank_id,
                     first_mapped_key=first_midi_note, num_mapped_keys=num_pipes)
        )

    return division, ranks, stops, stopranks, REQUIRED_PACKAGES
