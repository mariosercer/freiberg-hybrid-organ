from pathlib import Path

from src.codm.brustwerk_pilot import CHORTON_TUNING_ADJUST_CENTS
from src.codm.brustwerk_pilot import PACKAGE_ID as ZOBLITZ_PACKAGE_ID
from src.codm.brustwerk_pilot import build_brustwerk_division
from src.codm.goerlitz_paths import default_goerlitz_extract_root
from src.codm.hauptwerk_division import build_hauptwerk_division
from src.codm.model import Coupler, Tremulant
from src.codm.oberwerk_division import build_oberwerk_division
from src.codm.pedal_division import build_pedal_division
from src.codm.writer import render_custom_organ

ORGAN_ID = 800200

GOERLITZ_EXTRACT_ROOT = default_goerlitz_extract_root()
WALTERSHAUSEN_ROOT = Path("/Volumes/Samsung T7/Orgulje/Trost Waltershausen/OrganInstallationPackages")
WASSELONNE_ROOT = Path("/Volumes/Samsung T7/Orgulje/Silbermann Wasselonne/OrganInstallationPackages/000802")
ZOBLITZ_ROOT = Path("/Volumes/Samsung T7/Orgulje/Stadtkirche Zoeblitz/OrganInstallationPackages/000458")

DIVISION_CODE_BRUSTWERK = 4

# Confirmed empirically against Hauptwerk's own ExampleCustomOrgan2, which
# uses the exact same division-code layout as this project (1=PEDAL,
# 2=GREAT/Hauptwerk, 3=SWELL/Oberwerk, 4=CHOIR/Brustwerk) - these are the
# real "standard" coupler codes for those division pairs, not a guess:
# "Gt to Ped"=1006, "Sw to Ped"=1011, "Ch to Ped"=1016, "Sw to Gt"=1111,
# "Ch to Gt"=1116, "Ch to Sw"=1216.
COUPLERS = [
    Coupler(coupler_code=1006, name="Coupler: Hauptwerk to Pedal", display_name="HW-P"),
    Coupler(coupler_code=1011, name="Coupler: Oberwerk to Pedal", display_name="OW-P"),
    Coupler(coupler_code=1016, name="Coupler: Brustwerk to Pedal", display_name="BW-P"),
    Coupler(coupler_code=1111, name="Coupler: Oberwerk to Hauptwerk", display_name="OW-HW"),
    Coupler(coupler_code=1116, name="Coupler: Brustwerk to Hauptwerk", display_name="BW-HW"),
    Coupler(coupler_code=1216, name="Coupler: Brustwerk to Oberwerk", display_name="BW-OW"),
]

# Tremulant codes follow the same confirmed 1700+10*(division_code-1)
# pattern as Example2's Swell(1720)/Choir(1730) tremulants - Hauptwerk gets
# none: Görlitz's own real Hauptwerk division has no tremulant waveform
# samples at all (confirmed on disk), matching normal Baroque practice
# where the main principal chorus is not tremulated.
TREMULANT_OBERWERK = Tremulant(tremulant_code=1720, name="Tremulant: Oberwerk", display_name="TREMULANT")
TREMULANT_BRUSTWERK = Tremulant(tremulant_code=1730, name="Tremulant: Brustwerk", display_name="TREMULANT")
TREMULANTS = [TREMULANT_OBERWERK, TREMULANT_BRUSTWERK]

# Oberwerk ranks with confirmed native tremulant-waveform folders on disk
# (every Görlitz OW/BW-sourced rank except Spitzflöte 4', which is
# cross-borrowed from HW - and HW has no tremulant data at all).
OBERWERK_TREM_RANKS = {
    "Quintaden 16'", "Principal 8'", "Gedackt 8'", "Quintaden 8'", "Octava 4'",
    "Super-Oktava 2'", "Flaschlöt 1'", "Mixtur 3f", "Cimbeln 2f", "Krumbhorn 8'",
}

# Brustwerk (Zöblitz) tremulant waveform folders - confirmed present under
# tremulantTemplates/<bare-name>/haupt (a different root than the rank's own
# samples/<bare-name>/lang|kurz/haupt folder, with no numeric "01_"-style
# prefix). All 9 Brustwerk ranks have a matching template folder.
BRUSTWERK_TREM_FOLDERS = {
    "Gedackt 8'": "tremulantTemplates/ow/gedackt8/haupt",
    "Principal 4'": "tremulantTemplates/ma/octava4/haupt",
    "Rohrflöte 4'": "tremulantTemplates/ow/rohrfloethe4/haupt",
    "Nasat 3'": "tremulantTemplates/ow/nasat3/haupt",
    "Octava 2'": "tremulantTemplates/ow/octava2/haupt",
    "Tertia 1 3/5'": "tremulantTemplates/ow/tertia135/haupt",
    "Quinta 1 1/2'": "tremulantTemplates/ow/quinta112/haupt",
    "Sifflöt 1'": "tremulantTemplates/ow/sufflet1/haupt",
    "Mixtur 3f": "tremulantTemplates/ow/cimbel2f/haupt",
}


def _wire_oberwerk_tremulant(ranks):
    for r in ranks:
        if r.name in OBERWERK_TREM_RANKS:
            r.trem_code = TREMULANT_OBERWERK.tremulant_code
            r.trem_package_id = r.package_id
            r.trem_waveform_folder = f"{r.main_folder}/trem"


def _wire_brustwerk_tremulant(ranks):
    for r in ranks:
        folder = BRUSTWERK_TREM_FOLDERS.get(r.name)
        if folder:
            r.trem_code = TREMULANT_BRUSTWERK.tremulant_code
            r.trem_package_id = ZOBLITZ_PACKAGE_ID
            r.trem_waveform_folder = folder


def _dedupe_packages(packages):
    seen = {}
    for p in packages:
        seen[p[0]] = p
    return list(seen.values())


def build_full_organ() -> str:
    # RankID must be globally unique across all 4 divisions when merged
    # (CODM identifies Rank objects by this code alone - confirmed in
    # Hauptwerk's own CODM format guide, p.8: "No two objects of a given
    # type can have the same code"). Each division module numbers its own
    # ranks starting at 1 by default (for standalone use/tests); give each
    # a distinct 100-wide base here, following the same per-division-code
    # spacing as StopCode, well clear of any division's rank count (max 13).
    ped_division, ped_ranks, ped_stops, ped_stopranks, ped_packages = build_pedal_division(
        GOERLITZ_EXTRACT_ROOT, rank_id_base=1
    )
    hw_division, hw_ranks, hw_stops, hw_stopranks, hw_packages = build_hauptwerk_division(
        GOERLITZ_EXTRACT_ROOT, WALTERSHAUSEN_ROOT, rank_id_base=101
    )
    ow_division, ow_ranks, ow_stops, ow_stopranks, ow_packages = build_oberwerk_division(
        GOERLITZ_EXTRACT_ROOT, WASSELONNE_ROOT, rank_id_base=201
    )
    bw_division, bw_ranks, bw_stops, bw_stopranks, bw_packages = build_brustwerk_division(
        ZOBLITZ_ROOT, division_code=DIVISION_CODE_BRUSTWERK, rank_id_base=301,
        tuning_adjust_cents=CHORTON_TUNING_ADJUST_CENTS,
    )

    _wire_oberwerk_tremulant(ow_ranks)
    _wire_brustwerk_tremulant(bw_ranks)

    divisions = [ped_division, hw_division, ow_division, bw_division]
    ranks = ped_ranks + hw_ranks + ow_ranks + bw_ranks
    stops = ped_stops + hw_stops + ow_stops + bw_stops
    stopranks = ped_stopranks + hw_stopranks + ow_stopranks + bw_stopranks
    required_packages = _dedupe_packages(ped_packages + hw_packages + ow_packages + bw_packages)

    return render_custom_organ(
        organ_id=ORGAN_ID,
        name="Freiberg Hybrid",
        divisions=divisions,
        stops=stops,
        ranks=ranks,
        stopranks=stopranks,
        required_packages=required_packages,
        couplers=COUPLERS,
        tremulants=TREMULANTS,
    )


def main():
    xml = build_full_organ()
    out_path = Path(
        "/Users/pilepale/Hauptwerk/HauptwerkUserData/CustomOrganDefinitions/"
        "FreibergHybrid.CustomOrgan_Hauptwerk_xml"
    )
    out_path.write_text(xml, encoding="utf-8")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
