from pathlib import Path

from src.codm.brustwerk_pilot import _validate_rank_folder
from src.codm.goerlitz_paths import goerlitz_package_root
from src.codm.model import Division, Rank, Stop, StopRank

DIVISION_CODE = 1
FIRST_MIDI_NOTE = 36
NUM_PIPES = 32  # Görlitz pedal compass: C-f' extended to g' (MIDI 36-67)

GOERLITZ_PACKAGES = {
    1811: ("Goerlitz, Sonnenorgel, Surround - Core", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.10"),
    1812: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.10"),
    1813: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.0"),
    1814: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.1"),
}

REQUIRED_PACKAGES = [
    (1, "Hauptwerk Standard Components", 1, "Milan Digital Audio", "4"),
] + [(pkg_id, *meta) for pkg_id, meta in GOERLITZ_PACKAGES.items()]

# Pitch_RankBaseOutputPitch64ftHarmonicNum measured from each rank's
# 036-c.wav smpl chunk, as the frequency ratio to Görlitz Pedal's own
# Principalbass 16' (reference harmonic 4). All measured as clean,
# near-exact integers matching their nominal footage (no mutation
# surprises in the Pedal division, unlike the manuals) except Pedalmixtur
# 6f, which - like every other pre-mixed mixture rank in this project -
# reflects whichever component is lowest at the measured note, not a
# simple per-note-constant pitch class.
#
# (stop name, rank name, package_id, rank_folder, short_dir, short_ms,
#  medium_dir, medium_ms, rel_dir, pitch_harmonic_num)
PEDAL_SIMPLE_STOPS = [
    ("Principalbaß 16'", "Principalbaß 16'", 1812, "pipes/Pedal/01-AB_principalbas16",
     "rel00220", 220, "rel00440", 440, "rel99999", 4),
    ("Subbaß 16'", "Subbaß 16'", 1811, "pipes/Pedal/01-AB_Subbass16",
     "rel00200", 200, "rel00440", 440, "rel99999", 4),
    ("Octavbaß 8'", "Octavbaß 8'", 1812, "pipes/Pedal/01-AB_octavbas8",
     "rel00220", 220, "rel00440", 440, "rel99999", 8),
    ("Octavbaß 4'", "Octavbaß 4'", 1812, "pipes/Pedal/01-AB_Superoctbas4",
     "rel00220", 220, "rel00440", 440, "rel99999", 16),
    ("Pedalmixtur 6f", "Pedalmixtur 6f", 1813, "pipes/Pedal/01-AB_mix6",
     "rel00220", 220, "rel00440", 440, "rel99999", 24),
    ("Posaunenbaß 16'", "Posaunenbaß 16'", 1813, "pipes/Pedal/01-AB_posaun16",
     "rel00220", 220, "rel00440", 440, "rel99999", 4),
    ("Trompetenbaß 8'", "Trompetenbaß 8'", 1812, "pipes/Pedal/01-AB_TrompBass8",
     "rel00200", 200, "rel00440", 440, "rel99999", 8),
    ("Clarinbaß 4'", "Clarinbaß 4'", 1813, "pipes/Pedal/01-AB_ClarinBass4",
     "rel00200", 200, "rel00440", 440, "rel99999", 16),
]

# Untersatz 32'+16' is ONE stop with TWO ranks (per spec: "Gross
# Principal-Bass 32' + Contra-Bass 16', spojeno u jedan registar").
UNTERSATZ_RANKS = [
    ("Gross Principal-Bass 32'", 1813, "pipes/Pedal/01-AB_principalbas32",
     "rel00220", 220, "rel00540", 540, "rel99999", 2),
    ("Contra-Bass 16'", 1814, "pipes/Pedal/01-AB_Contrabass16",
     "rel00200", 200, "rel00440", 440, "rel99999", 4),
]

def _make_rank(goerlitz_extract_root, rank_id, name, pkg_id, folder,
               short_dir, short_ms, medium_dir, medium_ms, rel_dir, harmonic):
    pkg_root = goerlitz_package_root(goerlitz_extract_root, pkg_id)
    short_release_folder = f"{folder}/{short_dir}"
    medium_release_folder = f"{folder}/{medium_dir}"
    rel_release_folder = f"{folder}/{rel_dir}"

    _validate_rank_folder(pkg_root, folder, NUM_PIPES, FIRST_MIDI_NOTE)
    _validate_rank_folder(pkg_root, short_release_folder, NUM_PIPES, FIRST_MIDI_NOTE)
    _validate_rank_folder(pkg_root, medium_release_folder, NUM_PIPES, FIRST_MIDI_NOTE)
    _validate_rank_folder(pkg_root, rel_release_folder, NUM_PIPES, FIRST_MIDI_NOTE)

    return Rank(
        rank_id=rank_id, name=name, num_pipes=NUM_PIPES, first_midi_note=FIRST_MIDI_NOTE,
        package_id=pkg_id, main_folder=folder,
        short_release_folder=short_release_folder, short_release_max_ms=short_ms,
        medium_release_folder=medium_release_folder, medium_release_max_ms=medium_ms,
        rel_release_folder=rel_release_folder,
        pitch_harmonic_num=harmonic, windchest_division_code=DIVISION_CODE,
    )


def build_pedal_division(goerlitz_extract_root: Path, rank_id_base: int = 1):
    division = Division(
        division_code=DIVISION_CODE,
        name="PEDAL",
        short_name="Pedal",
        number_of_keys=NUM_PIPES,
        first_key_midi_note=FIRST_MIDI_NOTE,
    )

    ranks = []
    stops = []
    stopranks = []
    rank_id = rank_id_base
    stop_index = 1

    # Untersatz 32'+16': one Stop, two Ranks/StopRanks.
    untersatz_stop_code = 2000 + (DIVISION_CODE - 1) * 100 + stop_index
    stop_index += 1
    stops.append(Stop(stop_code=untersatz_stop_code, name="Untersatz 32'+16'", display_name="UNTERSATZ 32+16"))
    for name, pkg_id, folder, short_dir, short_ms, medium_dir, medium_ms, rel_dir, harmonic in UNTERSATZ_RANKS:
        ranks.append(_make_rank(goerlitz_extract_root, rank_id, name, pkg_id, folder,
                                 short_dir, short_ms, medium_dir, medium_ms, rel_dir, harmonic))
        stopranks.append(
            StopRank(stop_code=untersatz_stop_code, rank_id=rank_id,
                     first_mapped_key=FIRST_MIDI_NOTE, num_mapped_keys=NUM_PIPES)
        )
        rank_id += 1

    for stop_name, rank_name, pkg_id, folder, short_dir, short_ms, medium_dir, medium_ms, rel_dir, harmonic \
            in PEDAL_SIMPLE_STOPS:
        stop_code = 2000 + (DIVISION_CODE - 1) * 100 + stop_index
        stop_index += 1
        ranks.append(_make_rank(goerlitz_extract_root, rank_id, rank_name, pkg_id, folder,
                                 short_dir, short_ms, medium_dir, medium_ms, rel_dir, harmonic))
        stops.append(Stop(stop_code=stop_code, name=stop_name, display_name=stop_name.upper()))
        stopranks.append(
            StopRank(stop_code=stop_code, rank_id=rank_id,
                     first_mapped_key=FIRST_MIDI_NOTE, num_mapped_keys=NUM_PIPES)
        )
        rank_id += 1

    return division, ranks, stops, stopranks, REQUIRED_PACKAGES
