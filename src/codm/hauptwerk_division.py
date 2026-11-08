from pathlib import Path

from src.codm.brustwerk_pilot import _validate_rank_folder
from src.codm.model import Division, Rank, Stop, StopRank

DIVISION_CODE = 2
FIRST_MIDI_NOTE = 36
NUM_PIPES = 58  # Görlitz's native manual compass: C-a''' (MIDI 36-93)

GOERLITZ_PACKAGES = {
    1811: ("Goerlitz, Sonnenorgel, Surround - Core", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.10"),
    1812: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.10"),
    1813: ("Goerlitz, Sonnenorgel, Surround - Pipes", 5, "Jiri Zurek - Sonus Paradisi - Hauptwerk.cz", "1.0"),
}
WALTERSHAUSEN_PACKAGE_ID = 255
WALTERSHAUSEN_PACKAGE = ("OrganART 1730 Trost Package-000255-PatchV3.2", 3, "OrganArt Media", "3.300000")

REQUIRED_PACKAGES = [
    (1, "Hauptwerk Standard Components", 1, "Milan Digital Audio", "4"),
] + [
    (pkg_id, *meta) for pkg_id, meta in GOERLITZ_PACKAGES.items()
] + [
    (WALTERSHAUSEN_PACKAGE_ID, *WALTERSHAUSEN_PACKAGE),
]

# Pitch_RankBaseOutputPitch64ftHarmonicNum values measured directly from the
# `smpl` chunk of each rank's 060-C.wav, as the frequency ratio to Principal
# 8' (Gross-Octava 8', reference harmonic 8) - NOT 64/nominal_footage, since
# mutation stops are named after traditional nominal footage that does not
# match their true acoustic pitch (confirmed pattern: same situation as the
# Brustwerk pilot's Nasat 3'/Quinta 1 1/2'). Measured ratios were clean,
# near-exact integers (within recording pitch wander of <1%):
#   Principal 8'=8, Viol di Gamba 8'=8, Rohrflöte 8'=8, Octava 4'=16,
#   Quinta 3'=24 (acoustically 2-2/3', same pattern as Zöblitz's Nasat 3'),
#   Super-Octava 2'=32, Tertia 1 3/5'=40, Trompet 8'=8, Clarin 4'=16.
# Mixtur 4f and Cimbeln 3f are pre-mixed multi-rank stops (single recording
# per note, same convention as Zöblitz's Cimbel II) - their measured
# harmonic (24 and 32 respectively) reflects whichever component is lowest
# at note 60 specifically; mixtures change composition by octave "breaks"
# across the keyboard, which the single-harmonic CODM model cannot capture
# per-note - this is an inherent simplification already accepted for the
# Brustwerk pilot's own mixture, not a new limitation introduced here.
# Cornet 5f measured 8 (its lowest component sounds at 8' pitch, consistent
# with Cornets commonly starting around an 8' foundation).
# Bordun 16' (Waltershausen) could NOT be measured - its sample files are
# genuinely encrypted (no RIFF/WAVE signature at all, confirmed on 2
# different Waltershausen ranks), unlike every other source in this
# project. Used the nominal harmonic for a non-mutation 16' flue (64/16=4)
# since there is no reason to suspect a plain Bordun is acoustically
# anything other than a true 16' - unlike a quint/tierce mutation, this
# nominal value is not expected to be wrong, but it is UNVERIFIED.
#
# (name, package_id, rank_folder (relative to package root, no trailing
#  slash), num_pipes, first_midi_note, pitch_harmonic_num,
#  short_release_dirname or None, short_ms, medium_release_dirname or None,
#  medium_ms, rel_release_dirname or None)
HAUPTWERK_STOPS = [
    ("Principal 8'", 1811, "pipes/HW/01-AB_grossoct8", 58, 36, 8, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Viol di Gamba 8'", 1812, "pipes/HW/01-AB_violdigam8", 58, 36, 8, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Rohrflöte 8'", 1813, "pipes/HW/01-AB_rohrflot8", 58, 36, 8, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Octava 4'", 1811, "pipes/HW/01-AB_octav4", 58, 36, 16, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Quinta 3'", 1812, "pipes/HW/01-AB_quinta3", 58, 36, 24, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Super-Octava 2'", 1812, "pipes/HW/01-AB_superoct2", 58, 36, 32, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Tertia 1 3/5'", 1812, "pipes/BW/01-AB_tercia", 58, 36, 40, "rel00200", 200, "rel00460", 460, "rel99999"),
    ("Mixtur 4f", 1812, "pipes/HW/01-AB_mix4x", 58, 36, 24, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Cimbeln 3f", 1812, "pipes/HW/01-AB_cimbal", 58, 36, 32, "rel00200", 200, "rel00450", 450, "rel99999"),
    ("Cornet 5f", 1813, "pipes/HW/01-AB_cornet", 41, 53, 8, "rel00220", 220, "rel00460", 460, "rel99999"),
    ("Trompet 8'", 1811, "pipes/HW/01-AB_trompet8", 58, 36, 8, "rel00220", 220, "rel00460", 460, "rel99999"),
    ("Clarin 4'", 1813, "pipes/HW/01-AB_clarin4", 58, 36, 16, "rel00220", 220, "rel00460", 460, "rel99999"),
]

GOERLITZ_PART_FOR_PACKAGE = {1811: 1, 1812: 2, 1813: 3}


def _goerlitz_package_root(goerlitz_extract_root: Path, package_id: int) -> Path:
    part = GOERLITZ_PART_FOR_PACKAGE[package_id]
    base = goerlitz_extract_root / f"Sonus paradisi Goerlitz Sonnenorgel Hauptwerk (Part {part})"
    nested = base / "HauptwerkSampleSetsAndComponents" / "OrganInstallationPackages" / f"{package_id:06d}"
    flat = base / f"{package_id:06d}"
    return nested if nested.is_dir() else flat


def build_hauptwerk_division(goerlitz_extract_root: Path, waltershausen_root: Path):
    division = Division(
        division_code=DIVISION_CODE,
        name="HAUPTWERK",
        short_name="Hauptwerk",
        number_of_keys=NUM_PIPES,
        first_key_midi_note=FIRST_MIDI_NOTE,
    )

    ranks = []
    stops = []
    stopranks = []

    for i, (name, pkg_id, folder, num_pipes, first_midi_note, harmonic,
            short_dir, short_ms, medium_dir, medium_ms, rel_dir) in enumerate(HAUPTWERK_STOPS, start=1):
        rank_id = i
        stop_code = 2000 + (DIVISION_CODE - 1) * 100 + i

        pkg_root = _goerlitz_package_root(goerlitz_extract_root, pkg_id)
        short_release_folder = f"{folder}/{short_dir}"
        medium_release_folder = f"{folder}/{medium_dir}"
        rel_release_folder = f"{folder}/{rel_dir}"

        _validate_rank_folder(pkg_root, folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, short_release_folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, medium_release_folder, num_pipes, first_midi_note)
        _validate_rank_folder(pkg_root, rel_release_folder, num_pipes, first_midi_note)

        ranks.append(
            Rank(
                rank_id=rank_id,
                name=name,
                num_pipes=num_pipes,
                first_midi_note=first_midi_note,
                package_id=pkg_id,
                main_folder=folder,
                short_release_folder=short_release_folder,
                short_release_max_ms=short_ms,
                medium_release_folder=medium_release_folder,
                medium_release_max_ms=medium_ms,
                rel_release_folder=rel_release_folder,
                pitch_harmonic_num=harmonic,
                windchest_division_code=DIVISION_CODE,
            )
        )
        stops.append(Stop(stop_code=stop_code, name=name, display_name=name.upper()))
        stopranks.append(
            StopRank(stop_code=stop_code, rank_id=rank_id,
                     first_mapped_key=first_midi_note, num_mapped_keys=num_pipes)
        )

    # Bordun 16' (Waltershausen) - 13th stop. Main package only (255); its
    # release takes live in a separate package (256), which CODM cannot
    # reference for the same rank (one Samples_InstallationPackageID per
    # Rank) - see ledger ruling. Harmonic number unverified (encrypted
    # samples), using the nominal non-mutation 16' value.
    bordun_folder = "HW-PortunUntersatz16"
    bordun_num_pipes = 54
    bordun_first_note = 36
    bordun_rank_id = len(HAUPTWERK_STOPS) + 1
    bordun_stop_code = 2000 + (DIVISION_CODE - 1) * 100 + bordun_rank_id

    _validate_rank_folder(waltershausen_root / f"{WALTERSHAUSEN_PACKAGE_ID:06d}", bordun_folder,
                           bordun_num_pipes, bordun_first_note)

    ranks.append(
        Rank(
            rank_id=bordun_rank_id,
            name="Bordun 16'",
            num_pipes=bordun_num_pipes,
            first_midi_note=bordun_first_note,
            package_id=WALTERSHAUSEN_PACKAGE_ID,
            main_folder=bordun_folder,
            short_release_folder=None,
            pitch_harmonic_num=4,
            windchest_division_code=DIVISION_CODE,
        )
    )
    stops.append(Stop(stop_code=bordun_stop_code, name="Bordun 16'", display_name="BORDUN 16"))
    stopranks.append(
        StopRank(stop_code=bordun_stop_code, rank_id=bordun_rank_id,
                 first_mapped_key=bordun_first_note, num_mapped_keys=bordun_num_pipes)
    )

    return division, ranks, stops, stopranks, REQUIRED_PACKAGES
