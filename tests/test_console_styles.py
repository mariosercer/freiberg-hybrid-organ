import unittest

from src.codm.model import ControlStyle, DisplayPage, KeyboardStyle
from src.codm.writer import render_custom_organ


class TestConsoleStyles(unittest.TestCase):
    def test_control_style_renders_with_copied_fields_not_invented(self):
        # Every value here is copied verbatim from Hauptwerk's own
        # ExampleCustomOrgan2.CustomOrgan_Hauptwerk_xml, ControlStyleID=10
        # ("Drwkb07WoodSm/WhtTxt") - confirmed by direct read, not guessed.
        style = ControlStyle(
            control_style_id=1,
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
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   control_styles=[style])
        self.assertIn("<ControlStyleID>1</ControlStyleID>", xml)
        self.assertIn(
            "<Image_Stage00_ImageFilename>HauptwerkStandardImages/Stop07-Drawknob-Wood-Small-Off.bmp"
            "</Image_Stage00_ImageFilename>",
            xml,
        )
        self.assertIn("<ClickableAreaPosPixelsRelativeToTopLeftOfControl_RightX>65"
                      "</ClickableAreaPosPixelsRelativeToTopLeftOfControl_RightX>", xml)

    def test_keyboard_style_renders_with_copied_fields_not_invented(self):
        # Copied verbatim from ExampleCustomOrgan2, KeyboardStyleID=7
        # ("Ped06OldSm").
        style = KeyboardStyle(
            keyboard_style_id=2,
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
            clickable_natural_bottom_y=70, clickable_sharp_bottom_y=70,
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   keyboard_styles=[style])
        self.assertIn("<KeyboardStyleID>2</KeyboardStyleID>", xml)
        self.assertIn(
            "<KeyShapeImageFilename_CF_KeyDown>HauptwerkStandardImages/"
            "KeyImageSet006-NaturalWithSharpToTheRightDown.bmp</KeyShapeImageFilename_CF_KeyDown>",
            xml,
        )
        self.assertIn("<HorizSpacingPixels_LeftOfNaturalFromLeftOfNatural>24"
                      "</HorizSpacingPixels_LeftOfNaturalFromLeftOfNatural>", xml)

    def test_display_page_renders_with_copied_background(self):
        # Copied verbatim from ExampleCustomOrgan4's single custom page.
        page = DisplayPage(
            display_page_id=1,
            name="Console",
            background_filename="HauptwerkStandardImages/SeamlessBackgrounds-WoodPanelling-DarkCherry.png",
        )
        xml = render_custom_organ(organ_id=800200, name="Test", divisions=[], stops=[],
                                   ranks=[], stopranks=[], required_packages=[],
                                   display_pages=[page])
        self.assertIn("<DisplayPageID>1</DisplayPageID>", xml)
        self.assertIn(
            "<BackgroundImageFilename>HauptwerkStandardImages/"
            "SeamlessBackgrounds-WoodPanelling-DarkCherry.png</BackgroundImageFilename>",
            xml,
        )


if __name__ == "__main__":
    unittest.main()
