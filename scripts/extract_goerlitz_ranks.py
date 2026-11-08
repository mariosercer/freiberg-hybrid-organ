"""Selectively extract only the Görlitz rank folders this project needs.

The Görlitz "Sonnenorgel" sample set ships as 4 ZIP parts (~11-21 GB each,
~76 GB total) on the external drive. Extracting them in full is both slow
and unnecessary: hauptwerk_division.py / oberwerk_division.py /
pedal_division.py only ever reference ~33 specific rank folders. This
script extracts exactly those, nothing else, into GOERLITZ_EXTRACT_ROOT.

Usage:
    python3 scripts/extract_goerlitz_ranks.py [destination_dir]

If destination_dir is omitted, uses the GOERLITZ_EXTRACT_ROOT environment
variable, falling back to the default scratch path the division modules
and tests also default to (see src/codm/goerlitz_paths.py).

Re-running is safe: zipfile.extract() overwrites existing files in place.
"""
import sys
import zipfile
from pathlib import Path

# Allow running as `python3 scripts/extract_goerlitz_ranks.py` from the repo
# root without needing PYTHONPATH=. set first.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ZIP_DIR = Path("/Volumes/Samsung T7/Orgulje/Sonus paradisi Goerlitz Sonnenorgel")

# (zip part, package_id, division, rank_folder_name) - casing verified
# directly against each ZIP's own listing; Görlitz is NOT consistent about
# capitalising rank folder names (e.g. "01-AB_octava4" vs "01-AB_Octava4"
# elsewhere), so these must not be "tidied up".
HAUPTWERK_RANKS = [
    (1, "001811", "HW", "01-AB_grossoct8"),
    (2, "001812", "HW", "01-AB_violdigam8"),
    (3, "001813", "HW", "01-AB_rohrflot8"),
    (1, "001811", "HW", "01-AB_octav4"),
    (2, "001812", "HW", "01-AB_quinta3"),
    (2, "001812", "HW", "01-AB_superoct2"),
    (2, "001812", "BW", "01-AB_tercia"),
    (2, "001812", "HW", "01-AB_mix4x"),
    (2, "001812", "HW", "01-AB_cimbal"),
    (3, "001813", "HW", "01-AB_cornet"),
    (1, "001811", "HW", "01-AB_trompet8"),
    (3, "001813", "HW", "01-AB_clarin4"),
]

OBERWERK_RANKS = [
    (3, "001813", "OW", "01-AB_quintd16"),
    (2, "001812", "OW", "01-AB_Principal8"),
    (2, "001812", "OW", "01-AB_Gedackt8"),
    (2, "001812", "OW", "01-AB_Quintadena8"),
    (2, "001812", "OW", "01-AB_octava4"),
    (2, "001812", "HW", "01-AB_spitzflt4"),
    (2, "001812", "OW", "01-AB_sedecima2"),
    (3, "001813", "BW", "01-AB_supersed1"),
    (3, "001813", "BW", "01-AB_scharfmix3"),
    (2, "001812", "OW", "01-AB_scharfcimbel"),
    (2, "001812", "OW", "01-AB_krumhorn8"),
]

PEDAL_RANKS = [
    (3, "001813", "Pedal", "01-AB_principalbas32"),
    (4, "001814", "Pedal", "01-AB_Contrabass16"),
    (2, "001812", "Pedal", "01-AB_principalbas16"),
    (1, "001811", "Pedal", "01-AB_Subbass16"),
    (2, "001812", "Pedal", "01-AB_octavbas8"),
    (2, "001812", "Pedal", "01-AB_Superoctbas4"),
    (3, "001813", "Pedal", "01-AB_mix6"),
    (3, "001813", "Pedal", "01-AB_posaun16"),
    (2, "001812", "Pedal", "01-AB_TrompBass8"),
    (3, "001813", "Pedal", "01-AB_ClarinBass4"),
]

ALL_RANKS = HAUPTWERK_RANKS + OBERWERK_RANKS + PEDAL_RANKS


def extract(dest: Path):
    parts = sorted(set(p for p, *_ in ALL_RANKS))
    for part in parts:
        zip_path = ZIP_DIR / f"Sonus paradisi Goerlitz Sonnenorgel Hauptwerk (Part {part}).zip"
        wanted_prefixes = [f"{pkg}/pipes/{div}/{folder}/" for p, pkg, div, folder in ALL_RANKS if p == part]
        print(f"=== Part {part}: {len(wanted_prefixes)} rank prefixes ===")
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            to_extract = [n for n in names if "__MACOSX" not in n and any(pfx in n for pfx in wanted_prefixes)]
            print(f"  extracting {len(to_extract)} entries...")
            for n in to_extract:
                z.extract(n, dest)
        print(f"  done part {part}")
    print(f"DONE -> {dest}")


if __name__ == "__main__":
    from src.codm.goerlitz_paths import default_goerlitz_extract_root

    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else default_goerlitz_extract_root()
    extract(dest)
