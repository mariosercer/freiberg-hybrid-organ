from pathlib import Path

from src.codm.brustwerk_pilot import CHORTON_TUNING_ADJUST_CENTS
from src.codm.brustwerk_pilot import PACKAGE_ID as ZOBLITZ_PACKAGE_ID
from src.codm.brustwerk_pilot import build_brustwerk_division
from src.codm.console_layout import console_size, controls_bottom_y, layout_controls, layout_keyboard_anchors
from src.codm.goerlitz_paths import default_goerlitz_extract_root
from src.codm.hauptwerk_division import build_hauptwerk_division
from src.codm.local_paths import custom_organ_definitions_dir, waltershausen_root, wasselonne_root, zoblitz_root
from src.codm.model import ControlStyle, Coupler, DisplayPage, KeyboardStyle, Tremulant
from src.codm.oberwerk_division import build_oberwerk_division
from src.codm.pedal_division import build_pedal_division
from src.codm.writer import render_custom_organ

ORGAN_ID = 800200

GOERLITZ_EXTRACT_ROOT = default_goerlitz_extract_root()
WALTERSHAUSEN_ROOT = waltershausen_root()
WASSELONNE_ROOT = wasselonne_root()
ZOBLITZ_ROOT = zoblitz_root()

DIVISION_CODE_BRUSTWERK = 4

# Generic graphical console (user's explicit request: "generički izgled iz
# Hauptwerkove biblioteke", single page) - every field below copied
# verbatim from Hauptwerk's own ExampleCustomOrgan2/4.CustomOrgan_Hauptwerk_xml
# (installed locally), confirmed by direct read, not invented.
CONSOLE_DISPLAY_PAGE_ID = 1
CONSOLE_CONTROL_STYLE_ID = 1
CONSOLE_KEYBOARD_STYLE_ID_MANUAL = 1
CONSOLE_KEYBOARD_STYLE_ID_PEDAL = 2

CONSOLE_DISPLAY_PAGE = DisplayPage(
    display_page_id=CONSOLE_DISPLAY_PAGE_ID,
    name="Console",
    background_filename="HauptwerkStandardImages/SeamlessBackgrounds-WoodPanelling-DarkCherry.png",
)

# ExampleCustomOrgan2 ControlStyleID=10 ("Drwkb07WoodSm/WhtTxt").
CONSOLE_CONTROL_STYLE = ControlStyle(
    control_style_id=CONSOLE_CONTROL_STYLE_ID,
    name="Drwkb07WoodSm/WhtTxt",
    clickable_right_x=65,
    clickable_bottom_y=65,
    mask_filename="HauptwerkStandardImages/Stop07-Drawknob-Wood-Small-Mask.bmp",
    stage00_filename="HauptwerkStandardImages/Stop07-Drawknob-Wood-Small-Off.bmp",
    stage01_filename="HauptwerkStandardImages/Stop07-Drawknob-Wood-Small-On.bmp",
    font_height_pixels=8,
    text_right_x=61,
    text_bottom_y=61,
)

# ExampleCustomOrgan2 KeyboardStyleID=4 ("Man07IvorySm", KeyImageSet007).
CONSOLE_KEYBOARD_STYLE_MANUAL = KeyboardStyle(
    keyboard_style_id=CONSOLE_KEYBOARD_STYLE_ID_MANUAL,
    name="Man07IvorySm",
    cf_keydown="HauptwerkStandardImages/KeyImageSet007-Down-CF.bmp",
    cf_keyup="HauptwerkStandardImages/KeyImageSet007-Up-CF.bmp",
    cf_mask="HauptwerkStandardImages/KeyImageSet007-Mask-CF.bmp",
    d_keydown="HauptwerkStandardImages/KeyImageSet007-Down-D.bmp",
    d_keyup="HauptwerkStandardImages/KeyImageSet007-Up-D.bmp",
    d_mask="HauptwerkStandardImages/KeyImageSet007-Mask-D.bmp",
    eb_keydown="HauptwerkStandardImages/KeyImageSet007-Down-EB.bmp",
    eb_keyup="HauptwerkStandardImages/KeyImageSet007-Up-EB.bmp",
    eb_mask="HauptwerkStandardImages/KeyImageSet007-Mask-EB.bmp",
    g_keydown="HauptwerkStandardImages/KeyImageSet007-Down-G.bmp",
    g_keyup="HauptwerkStandardImages/KeyImageSet007-Up-G.bmp",
    g_mask="HauptwerkStandardImages/KeyImageSet007-Mask-G.bmp",
    a_keydown="HauptwerkStandardImages/KeyImageSet007-Down-A.bmp",
    a_keyup="HauptwerkStandardImages/KeyImageSet007-Up-A.bmp",
    a_mask="HauptwerkStandardImages/KeyImageSet007-Mask-A.bmp",
    sharp_keydown="HauptwerkStandardImages/KeyImageSet007-Down-Sharp.bmp",
    sharp_keyup="HauptwerkStandardImages/KeyImageSet007-Up-Sharp.bmp",
    sharp_mask="",
    wholenatural_keydown="HauptwerkStandardImages/KeyImageSet007-Down-WholeNatural.bmp",
    wholenatural_keyup="HauptwerkStandardImages/KeyImageSet007-Up-WholeNatural.bmp",
    wholenatural_mask="",
    firstkeyda_keydown="HauptwerkStandardImages/KeyImageSet007-Down-FirstKeyDA.bmp",
    firstkeyda_keyup="HauptwerkStandardImages/KeyImageSet007-Up-FirstKeyDA.bmp",
    firstkeyda_mask="HauptwerkStandardImages/KeyImageSet007-Mask-FirstKeyDA.bmp",
    firstkeyg_keydown="HauptwerkStandardImages/KeyImageSet007-Down-FirstKeyG.bmp",
    firstkeyg_keyup="HauptwerkStandardImages/KeyImageSet007-Up-FirstKeyG.bmp",
    firstkeyg_mask="HauptwerkStandardImages/KeyImageSet007-Mask-FirstKeyG.bmp",
    lastkeydg_keydown="HauptwerkStandardImages/KeyImageSet007-Down-LastKeyDG.bmp",
    lastkeydg_keyup="HauptwerkStandardImages/KeyImageSet007-Up-LastKeyDG.bmp",
    lastkeydg_mask="HauptwerkStandardImages/KeyImageSet007-Mask-LastKeyDG.bmp",
    lastkeya_keydown="HauptwerkStandardImages/KeyImageSet007-Down-LastKeyA.bmp",
    lastkeya_keyup="HauptwerkStandardImages/KeyImageSet007-Up-LastKeyA.bmp",
    lastkeya_mask="HauptwerkStandardImages/KeyImageSet007-Mask-LastKeyA.bmp",
    horiz_natural=12, horiz_cf_sharp=8, horiz_da_sharp=10, horiz_g_sharp=9,
    horiz_dg_from_cfsharp=4, horiz_eb_from_dasharp=2, horiz_a_from_gsharp=3,
    clickable_natural_top_y=17, clickable_natural_right_x=12, clickable_natural_bottom_y=32,
    clickable_sharp_right_x=6, clickable_sharp_bottom_y=17,
)

# ExampleCustomOrgan2 KeyboardStyleID=7 ("Ped06OldSm", KeyImageSet006).
CONSOLE_KEYBOARD_STYLE_PEDAL = KeyboardStyle(
    keyboard_style_id=CONSOLE_KEYBOARD_STYLE_ID_PEDAL,
    name="Ped06OldSm",
    cf_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    cf_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    d_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    d_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    eb_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightDown.bmp",
    eb_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightUp.bmp",
    g_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    g_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    a_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    a_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    sharp_keydown="HauptwerkStandardImages/KeyImageSet006-SharpDown.bmp",
    sharp_keyup="HauptwerkStandardImages/KeyImageSet006-SharpUp.bmp",
    wholenatural_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightDown.bmp",
    wholenatural_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightUp.bmp",
    firstkeyda_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    firstkeyda_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    firstkeyg_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightDown.bmp",
    firstkeyg_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithSharpToTheRightUp.bmp",
    lastkeydg_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightDown.bmp",
    lastkeydg_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightUp.bmp",
    lastkeya_keydown="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightDown.bmp",
    lastkeya_keyup="HauptwerkStandardImages/KeyImageSet006-NaturalWithNoSharpToTheRightUp.bmp",
    horiz_natural=24, horiz_cf_sharp=12, horiz_da_sharp=12, horiz_g_sharp=12,
    horiz_dg_from_cfsharp=12, horiz_eb_from_dasharp=12, horiz_a_from_gsharp=12,
    clickable_natural_right_x=12, clickable_natural_bottom_y=70,
    clickable_sharp_right_x=12, clickable_sharp_bottom_y=70,
)

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
TREMULANT_OBERWERK = Tremulant(tremulant_code=1720, name="Tremulant: Oberwerk", display_name="TREM-OW")
TREMULANT_BRUSTWERK = Tremulant(tremulant_code=1730, name="Tremulant: Brustwerk", display_name="TREM-BW")
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

    control_positions, keyboard_anchors = _wire_console_graphics(divisions, stops, COUPLERS, TREMULANTS)
    console_width, console_height = console_size(control_positions, keyboard_anchors, divisions)

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
        control_styles=[CONSOLE_CONTROL_STYLE],
        keyboard_styles=[CONSOLE_KEYBOARD_STYLE_MANUAL, CONSOLE_KEYBOARD_STYLE_PEDAL],
        display_pages=[CONSOLE_DISPLAY_PAGE],
        console_width=console_width,
        console_height=console_height,
        default_display_page_id=CONSOLE_DISPLAY_PAGE_ID,
    )


def _wire_console_graphics(divisions, stops, couplers, tremulants):
    control_positions = layout_controls(stops, couplers, tremulants)
    anchors = layout_keyboard_anchors(controls_bottom_y(control_positions))

    for s in stops:
        s.display_page_id = CONSOLE_DISPLAY_PAGE_ID
        s.control_style_id = CONSOLE_CONTROL_STYLE_ID
        s.pos_x, s.pos_y = control_positions[f"stop:{s.stop_code}"]

    for c in couplers:
        c.display_page_id = CONSOLE_DISPLAY_PAGE_ID
        c.control_style_id = CONSOLE_CONTROL_STYLE_ID
        c.pos_x, c.pos_y = control_positions[f"coupler:{c.coupler_code}"]

    for t in tremulants:
        t.display_page_id = CONSOLE_DISPLAY_PAGE_ID
        t.control_style_id = CONSOLE_CONTROL_STYLE_ID
        t.pos_x, t.pos_y = control_positions[f"tremulant:{t.tremulant_code}"]

    for d in divisions:
        d.keyboard_display_page_id = CONSOLE_DISPLAY_PAGE_ID
        d.keyboard_style_id = (
            CONSOLE_KEYBOARD_STYLE_ID_PEDAL if d.division_code == 1 else CONSOLE_KEYBOARD_STYLE_ID_MANUAL
        )
        d.keyboard_pos_x, d.keyboard_pos_y = anchors[d.division_code]

    return control_positions, anchors


def main():
    xml = build_full_organ()
    out_path = custom_organ_definitions_dir() / "FreibergHybrid.CustomOrgan_Hauptwerk_xml"
    out_path.write_text(xml, encoding="utf-8")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
