import re
import unittest
from pathlib import Path

from src.codm.full_organ import (
    CONSOLE_CONTROL_STYLE,
    CONSOLE_DISPLAY_PAGE,
    CONSOLE_KEYBOARD_STYLE_MANUAL,
    CONSOLE_KEYBOARD_STYLE_PEDAL,
)
from src.codm.local_paths import custom_organ_definitions_dir
from src.codm.writer import render_custom_organ

HAUPTWERK_EXAMPLES_DIR = custom_organ_definitions_dir()
EXAMPLE2 = HAUPTWERK_EXAMPLES_DIR / "ExampleCustomOrgan2.CustomOrgan_Hauptwerk_xml"
EXAMPLE4 = HAUPTWERK_EXAMPLES_DIR / "ExampleCustomOrgan4-StAnnes-WithBasicGUIConsole.CustomOrgan_Hauptwerk_xml"


def _object_fields(xml_text, tag, id_tag, id_value):
    """Every <FieldName>value</FieldName> pair inside the <tag>...</tag>
    block whose id_tag equals id_value, as a dict. Used to diff our
    generated objects against Hauptwerk's own example files field-by-field,
    instead of trusting that a few hand-picked substrings match."""
    for block in re.findall(rf"<{tag}>(.*?)</{tag}>", xml_text, re.DOTALL):
        if re.search(rf"<{id_tag}>{id_value}</{id_tag}>", block):
            return dict(re.findall(r"<(\w+)>(.*?)</\1>", block, re.DOTALL))
    raise AssertionError(f"no <{tag}> with <{id_tag}>{id_value}</{id_tag}> found")


@unittest.skipUnless(EXAMPLE2.is_file() and EXAMPLE4.is_file(), "Hauptwerk example organs not installed locally")
class TestConsoleStyles(unittest.TestCase):
    def test_control_style_matches_example2_verbatim(self):
        # Every field of the ControlStyle this project actually ships
        # (CONSOLE_CONTROL_STYLE, imported from full_organ.py - not a
        # hand-retyped copy that could silently drift from it) must match
        # Hauptwerk's own ExampleCustomOrgan2 ControlStyleID=10
        # ("Drwkb07WoodSm/WhtTxt") field-for-field, except the ID itself
        # (renumbered 10 -> 1 per the plan).
        source = _object_fields(
            EXAMPLE2.read_text(encoding="utf-8", errors="replace"),
            "customdisplaycontrolstyle", "ControlStyleID", 10,
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   control_styles=[CONSOLE_CONTROL_STYLE])
        shipped = _object_fields(xml, "customdisplaycontrolstyle", "ControlStyleID",
                                  CONSOLE_CONTROL_STYLE.control_style_id)

        source.pop("ControlStyleID")
        shipped.pop("ControlStyleID")
        self.assertEqual(shipped, source)

    def test_keyboard_style_manual_matches_example2_verbatim(self):
        # CONSOLE_KEYBOARD_STYLE_MANUAL vs ExampleCustomOrgan2 KeyboardStyleID=4
        # ("Man07IvorySm").
        source = _object_fields(
            EXAMPLE2.read_text(encoding="utf-8", errors="replace"),
            "customdisplaykeyboardstyle", "KeyboardStyleID", 4,
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   keyboard_styles=[CONSOLE_KEYBOARD_STYLE_MANUAL])
        shipped = _object_fields(xml, "customdisplaykeyboardstyle", "KeyboardStyleID",
                                  CONSOLE_KEYBOARD_STYLE_MANUAL.keyboard_style_id)

        source.pop("KeyboardStyleID")
        shipped.pop("KeyboardStyleID")
        self.assertEqual(shipped, source)

    def test_keyboard_style_pedal_matches_example2_verbatim(self):
        # CONSOLE_KEYBOARD_STYLE_PEDAL vs ExampleCustomOrgan2 KeyboardStyleID=7
        # ("Ped06OldSm"). This is the style whose clickable_*_right_x fields
        # were previously left at the dataclass default (0 instead of the
        # real 12) - a full field diff against the source is exactly what
        # would have caught that.
        source = _object_fields(
            EXAMPLE2.read_text(encoding="utf-8", errors="replace"),
            "customdisplaykeyboardstyle", "KeyboardStyleID", 7,
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   keyboard_styles=[CONSOLE_KEYBOARD_STYLE_PEDAL])
        shipped = _object_fields(xml, "customdisplaykeyboardstyle", "KeyboardStyleID",
                                  CONSOLE_KEYBOARD_STYLE_PEDAL.keyboard_style_id)

        source.pop("KeyboardStyleID")
        shipped.pop("KeyboardStyleID")
        self.assertEqual(shipped, source)

    def test_display_page_matches_example4_verbatim(self):
        # CONSOLE_DISPLAY_PAGE vs ExampleCustomOrgan4's single custom page.
        source = _object_fields(
            EXAMPLE4.read_text(encoding="utf-8", errors="replace"),
            "customdisplaypage", "DisplayPageID", 1,
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   display_pages=[CONSOLE_DISPLAY_PAGE])
        shipped = _object_fields(xml, "customdisplaypage", "DisplayPageID",
                                  CONSOLE_DISPLAY_PAGE.display_page_id)

        # Example4's own page already uses DisplayPageID=1 and Name="Console",
        # same as this project's choice - the whole object matches verbatim,
        # no ID renumbering needed here.
        self.assertEqual(shipped, source)


if __name__ == "__main__":
    unittest.main()
