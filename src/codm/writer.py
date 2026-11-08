from xml.sax.saxutils import escape

from src.codm.model import (
    ControlStyle,
    Coupler,
    Division,
    DisplayPage,
    KeyboardStyle,
    Rank,
    Stop,
    StopRank,
    Tremulant,
)


def _field(name, value):
    if value is None:
        text = ""
    elif isinstance(value, str):
        text = escape(value, {'"': "&quot;"})
    else:
        text = str(value)
    return f"\t\t<{name}>{text}</{name}>"


def _object(tag, fields):
    lines = [f"\t<{tag}>"]
    lines.extend(_field(name, value) for name, value in fields)
    lines.append(f"\t</{tag}>")
    return "\n".join(lines)


def _object_list(object_type, tag, objects_fields):
    lines = [f'<ObjectList ObjectType="{object_type}">']
    lines.extend(_object(tag, fields) for fields in objects_fields)
    lines.append("</ObjectList>")
    return "\n".join(lines)


def _empty_object_list(object_type):
    return f'<ObjectList ObjectType="{object_type}">\n</ObjectList>'


def _general_fields(organ_id, name, console_width=0, console_height=0, default_display_page_id=None):
    short_name = name[:32]
    filename = "".join(c for c in name if c.isalnum())
    return [
        ("UniqueOrganID", organ_id),
        ("Name", name),
        ("ShortName", short_name),
        ("OrganDefinitionFilenameExcludingExtension", filename),
        ("CurrentHauptwerkVersion", 5),
        ("SampleRateCode", 2),
        ("VisualAppearanceCode", 1),
        ("CustomOrganInfo_InstallationPackageID", None),
        ("CustomOrganInfo_InfoFilename", None),
        ("CustomOrganInfo_MIDIDemoFilename", None),
        ("CustomDisplay_ConsoleWidthPixels", console_width),
        ("CustomDisplay_ConsoleHeightPixels", console_height),
        ("CustomDisplay_AlternateLayout1_ConsoleWidthPixels", 0),
        ("CustomDisplay_AlternateLayout1_ConsoleHeightPixels", 0),
        ("CustomDisplay_EnableStdPages_Controls", "Y"),
        ("CustomDisplay_EnableStdPages_Keyboards", "Y"),
        ("CustomDisplay_EnableStdPages_Wind", "Y"),
        ("CustomDisplay_EnableStdPages_Enclosures", "Y"),
        ("CustomDisplay_DefaultDisplayPageID", default_display_page_id),
        ("CustomDisplay1_Generals_DisplayPageID", None),
        ("CustomDisplay1_Generals_NumberDisplayed", 0),
        ("CustomDisplay1_Generals_ControlStyleID", None),
        ("CustomDisplay1_Generals_FirstDisplayedPistonPos_X", 0),
        ("CustomDisplay1_Generals_FirstDisplayedPistonPos_Y", 0),
        ("CustomDisplay1_Generals_LastDisplayedPistonPos_X", 0),
        ("CustomDisplay1_Generals_LastDisplayedPistonPos_Y", 0),
        ("CustomDisplay1_Generals_AltLayout1_ControlStyleID", None),
        ("CustomDisplay1_Generals_AltLayout1_FirstDisplayedPistonPos_X", 0),
        ("CustomDisplay1_Generals_AltLayout1_FirstDisplayedPistonPos_Y", 0),
        ("CustomDisplay1_Generals_AltLayout1_LastDisplayedPistonPos_X", 0),
        ("CustomDisplay1_Generals_AltLayout1_LastDisplayedPistonPos_Y", 0),
        ("CustomDisplay1_GeneralCancel_DisplayPageID", None),
        ("CustomDisplay1_GeneralCancel_Text", None),
        ("CustomDisplay1_GeneralCancel_ControlStyleID", None),
        ("CustomDisplay1_GeneralCancel_PosPixels_X", 0),
        ("CustomDisplay1_GeneralCancel_PosPixels_Y", 0),
        ("CustomDisplay1_GeneralCancel_AltLayout1_ControlStyleID", None),
        ("CustomDisplay1_GeneralCancel_AltLayout1_PosPixels_X", 0),
        ("CustomDisplay1_GeneralCancel_AltLayout1_PosPixels_Y", 0),
        ("CustomDisplay1_SetterSwitch_DisplayPageID", None),
        ("CustomDisplay1_SetterSwitch_Text", None),
        ("CustomDisplay1_SetterSwitch_ControlStyleID", None),
        ("CustomDisplay1_SetterSwitch_PosPixels_X", 0),
        ("CustomDisplay1_SetterSwitch_PosPixels_Y", 0),
        ("CustomDisplay1_SetterSwitch_AltLayout1_ControlStyleID", None),
        ("CustomDisplay1_SetterSwitch_AltLayout1_PosPixels_X", 0),
        ("CustomDisplay1_SetterSwitch_AltLayout1_PosPixels_Y", 0),
        ("CustomDisplay2_Generals_DisplayPageID", None),
        ("CustomDisplay2_Generals_NumberDisplayed", 0),
        ("CustomDisplay2_Generals_ControlStyleID", None),
        ("CustomDisplay2_Generals_FirstDisplayedPistonPos_X", 0),
        ("CustomDisplay2_Generals_FirstDisplayedPistonPos_Y", 0),
        ("CustomDisplay2_Generals_LastDisplayedPistonPos_X", 0),
        ("CustomDisplay2_Generals_LastDisplayedPistonPos_Y", 0),
        ("CustomDisplay2_Generals_AltLayout1_ControlStyleID", None),
        ("CustomDisplay2_Generals_AltLayout1_FirstDisplayedPistonPos_X", 0),
        ("CustomDisplay2_Generals_AltLayout1_FirstDisplayedPistonPos_Y", 0),
        ("CustomDisplay2_Generals_AltLayout1_LastDisplayedPistonPos_X", 0),
        ("CustomDisplay2_Generals_AltLayout1_LastDisplayedPistonPos_Y", 0),
        ("CustomDisplay2_GeneralCancel_DisplayPageID", None),
        ("CustomDisplay2_GeneralCancel_Text", None),
        ("CustomDisplay2_GeneralCancel_ControlStyleID", None),
        ("CustomDisplay2_GeneralCancel_PosPixels_X", 0),
        ("CustomDisplay2_GeneralCancel_PosPixels_Y", 0),
        ("CustomDisplay2_GeneralCancel_AltLayout1_ControlStyleID", None),
        ("CustomDisplay2_GeneralCancel_AltLayout1_PosPixels_X", 0),
        ("CustomDisplay2_GeneralCancel_AltLayout1_PosPixels_Y", 0),
        ("CustomDisplay2_SetterSwitch_DisplayPageID", None),
        ("CustomDisplay2_SetterSwitch_Text", None),
        ("CustomDisplay2_SetterSwitch_ControlStyleID", None),
        ("CustomDisplay2_SetterSwitch_PosPixels_X", 0),
        ("CustomDisplay2_SetterSwitch_PosPixels_Y", 0),
        ("CustomDisplay2_SetterSwitch_AltLayout1_ControlStyleID", None),
        ("CustomDisplay2_SetterSwitch_AltLayout1_PosPixels_X", 0),
        ("CustomDisplay2_SetterSwitch_AltLayout1_PosPixels_Y", 0),
    ]


def _required_package_fields(pkg):
    pkg_id, name, supplier_id, supplier_name, min_version = pkg
    short_name = "".join(c for c in name if c.isalnum())
    return [
        ("InstallationPackageID", pkg_id),
        ("Name", name),
        ("ShortName", short_name),
        ("PackageSupplierID", supplier_id),
        ("SupplierName", supplier_name),
        ("MinimumPackageVersion", min_version),
    ]


def _division_display_block(layout_num, d=None):
    p = f"CustomDisplay{layout_num}"
    keyboard_display_page_id = d.keyboard_display_page_id if d and layout_num == 1 else None
    keyboard_style_id = d.keyboard_style_id if d and layout_num == 1 else None
    keyboard_pos_x = d.keyboard_pos_x if d and layout_num == 1 else 0
    keyboard_pos_y = d.keyboard_pos_y if d and layout_num == 1 else 0
    return [
        (f"{p}_Divisionals_DisplayPageID", None),
        (f"{p}_Divisionals_NumberDisplayed", 0),
        (f"{p}_Divisionals_ControlStyleID", None),
        (f"{p}_Divisionals_FirstDisplayedPistonPos_X", 0),
        (f"{p}_Divisionals_FirstDisplayedPistonPos_Y", 0),
        (f"{p}_Divisionals_LastDisplayedPistonPos_X", 0),
        (f"{p}_Divisionals_LastDisplayedPistonPos_Y", 0),
        (f"{p}_Divisionals_AltLayout1_ControlStyleID", None),
        (f"{p}_Divisionals_AltLayout1_FirstDisplayedPistonPos_X", 0),
        (f"{p}_Divisionals_AltLayout1_FirstDisplayedPistonPos_Y", 0),
        (f"{p}_Divisionals_AltLayout1_LastDisplayedPistonPos_X", 0),
        (f"{p}_Divisionals_AltLayout1_LastDisplayedPistonPos_Y", 0),
        (f"{p}_DivisionalCancel_DisplayPageID", None),
        (f"{p}_DivisionalCancel_Text", None),
        (f"{p}_DivisionalCancel_ControlStyleID", None),
        (f"{p}_DivisionalCancel_PosPixels_X", 0),
        (f"{p}_DivisionalCancel_PosPixels_Y", 0),
        (f"{p}_DivisionalCancel_AltLayout1_ControlStyleID", None),
        (f"{p}_DivisionalCancel_AltLayout1_PosPixels_X", 0),
        (f"{p}_DivisionalCancel_AltLayout1_PosPixels_Y", 0),
        (f"{p}_Keyboard_DisplayPageID", keyboard_display_page_id),
        (f"{p}_Keyboard_KeyboardStyleID", keyboard_style_id),
        (f"{p}_Keyboard_PosPixels_X", keyboard_pos_x),
        (f"{p}_Keyboard_PosPixels_Y", keyboard_pos_y),
        (f"{p}_Keyboard_AltLayout1_KeyboardStyleID", None),
        (f"{p}_Keyboard_AltLayout1_PosPixels_X", 0),
        (f"{p}_Keyboard_AltLayout1_PosPixels_Y", 0),
    ]


def _division_fields(d: Division):
    fields = [
        ("DivisionCode", d.division_code),
        ("Name", d.name),
        ("ShortName", d.short_name),
        ("NumberOfKeys", d.number_of_keys),
        ("MIDINoteNumOfFirstKey", d.first_key_midi_note),
        ("NumberOfKeyActionNodesIfDifferentFromNumberOfKeys", 0),
        ("MIDINoteNumOfFirstKeyActionNodeIfDifferentFromFirstKey", 0),
        ("AccessibleForMIDIInputAndOutput", "Y"),
        ("WindModel_EnableWindModel", "N"),
        ("WindModel_TotalResrvrAndWndchstVolMetresCubed", 2),
        ("WindModel_AreaOfReservoirTableMetresSquared", 1.8),
        ("WindModel_ResrvrBellowsPositiveDampingCoeff", 25),
        ("WindModel_WindchestPressureDropPctAtMaxLoad", 2),
        ("PercussiveEngagingKeyActionNoise_RankID", None),
        ("PercussiveEngagingKeyActionNoise_ChooseMIDINoteNumRandomly", "N"),
        ("PercussiveDisengagingKeyActionNoise_RankID", None),
        ("PercussiveDisengagingKeyActionNoise_ChooseMIDINoteNumRandomly", "N"),
        ("SustainingKeyActionNoise_RankID", None),
        ("SustainingKeyActionNoise_ChooseMIDINoteNumberRandomly", "N"),
    ]
    fields.extend(_division_display_block(1, d))
    fields.extend(_division_display_block(2))
    return fields


def _rank_fields(r: Rank):
    return [
        ("RankID", r.rank_id),
        ("Name", r.name),
        ("NumberOfPipes", r.num_pipes),
        ("MIDINoteNumberOfFirstPipe", r.first_midi_note),
        ("IsPercussive", "N"),
        ("Samples_InstallationPackageID", r.package_id),
        ("Samples_MainSampleFileFolder", r.main_folder),
        ("Samples_RelSampleFileFolderIfRelSamplesStoredInSeparateFiles", r.rel_release_folder),
        ("Samples_ShortNoteReleaseSampleFileFolderIfAny", r.short_release_folder),
        ("Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny", r.short_release_max_ms),
        ("Samples_MediumNoteReleaseSampleFileFolderIfAny", r.medium_release_folder),
        ("Samples_MaxNoteTimeMsForMediumNoteReleaseSamplesIfAny", r.medium_release_max_ms),
        ("Samples_MIDINoteNumIncrementFromPipesToSamples", 0),
        ("Samples_RankBasePitch64ftHarmNumIfAssumedTunedToConcertPitch", 0),
        ("Position_LayoutOfPipesOnWindchestCode", 1),
        ("Position_RankDistanceFromListenerMetres", 1),
        ("WindSupply_DivisionCodeOfWindchest", r.windchest_division_code),
        ("WindSupply_MaxFlowRandomisationPct", 0),
        ("Amp_PipeMIDINoteNum036_LevelAdjustDecibels", 0),
        ("Amp_PipeMIDINoteNum096_LevelAdjustDecibels", 0),
        ("Amp_PipeMIDINoteNum036_WindModelModDepthAdjustDecibels", 0),
        ("Amp_PipeMIDINoteNum096_WindModelModDepthAdjustDecibels", 0),
        ("Amp_PipeMIDINoteNum036_TremulantModDepthAdjustDecibels", 0),
        ("Amp_PipeMIDINoteNum096_TremulantModDepthAdjustDecibels", 0),
        ("Pitch_RankBaseOutputPitch64ftHarmonicNum", r.pitch_harmonic_num),
        ("Pitch_MaxRandomTuningErrorHz", 0.25),
        ("Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones", r.tuning_adjust_cents_036),
        ("Pitch_PipeMIDINoteNum096_TuningAdjustPercentSemitones", r.tuning_adjust_cents_096),
        ("Pitch_PipeMIDINoteNum036_WindModelModDepthAdjustPercent", 0),
        ("Pitch_PipeMIDINoteNum096_WindModelModDepthAdjustPercent", 0),
        ("Pitch_PipeMIDINoteNum036_TremulantModDepthAdjustPercent", 0),
        ("Pitch_PipeMIDINoteNum096_TremulantModDepthAdjustPercent", 0),
        ("HarmonicShaping_PipeMIDINoteNum036_3rdAndUpperHarmLvlAdjDb", 0),
        ("HarmonicShaping_PipeMIDINoteNum096_3rdAndUpperHarmLvlAdjDb", 0),
        ("HarmonicShaping_PipeMIDINoteNum036_WindModelModDepthAdjDb", 0),
        ("HarmonicShaping_PipeMIDINoteNum096_WindModelModDepthAdjDb", 0),
        ("HarmonicShaping_PipeMIDINoteNum036_TremulantModDepthAdjDb", 0),
        ("HarmonicShaping_PipeMIDINoteNum096_TremulantModDepthAdjDb", 0),
        ("Encl_EnclosureCode", None),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum036_OverallAttnDb", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum036_MaxFreqHz", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum036_MinFreqHz", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum036_ExtraAttnAtMinDb", 0),
        ("Encl_FiltParamWhenOpenForPipeMIDINoteNum036_MaxFreqHz", 0),
        ("Encl_FiltParamWhenOpenForPipeMIDINoteNum036_MinFreqHz", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum096_OverallAttnDb", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum096_MaxFreqHz", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum096_MinFreqHz", 0),
        ("Encl_FiltParamWhenClsdForPipeMIDINoteNum096_ExtraAttnAtMinDb", 0),
        ("Encl_FiltParamWhenOpenForPipeMIDINoteNum096_MaxFreqHz", 0),
        ("Encl_FiltParamWhenOpenForPipeMIDINoteNum096_MinFreqHz", 0),
        ("Encl_MIDINoteNumOfFirstEnclosedPipeIfWholeRankNotEnclosed", 0),
        ("Encl_MIDINoteNumOfLastEnclosedPipeIfWholeRankNotEnclosed", 0),
        ("Trem_TremulantCode", r.trem_code),
        ("Trem_SampleInstallationPackageID", r.trem_package_id),
        ("Trem_WaveformSampleFileFolder", r.trem_waveform_folder),
        ("Trem_MIDINoteNumIncrementFromPipesToTremSamples", 0),
        ("Trem_MaxDepthRandomisationPct", 0),
        ("Trem_MIDINoteNumOfFirstTremmedPipeIfWholeRankNotTremmed", 0),
        ("Trem_MIDINoteNumOfLastTremmedPipeIfWholeRankNotTremmed", 0),
        ("ReverbTailTruncation_ModeCode", 1),
        ("ReverbTailTruncation_DecayLengthAsMsForMiddleCOn8FtStop", 0),
    ]


def _stop_fields(s: Stop):
    return [
        ("StopCode", s.stop_code),
        ("Name", s.name),
        ("CustomDisplay1_DisplayPageID", s.display_page_id),
        ("CustomDisplay1_Text", s.display_name if s.display_page_id else None),
        ("CustomDisplay1_ControlStyleID", s.control_style_id),
        ("CustomDisplay1_PosPixels_X", s.pos_x),
        ("CustomDisplay1_PosPixels_Y", s.pos_y),
        ("CustomDisplay1_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay1_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay1_AlternateLayout1_PosPixels_Y", 0),
        ("CustomDisplay2_DisplayPageID", None),
        ("CustomDisplay2_Text", None),
        ("CustomDisplay2_ControlStyleID", None),
        ("CustomDisplay2_PosPixels_X", 0),
        ("CustomDisplay2_PosPixels_Y", 0),
        ("CustomDisplay2_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay2_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay2_AlternateLayout1_PosPixels_Y", 0),
        ("DisplayName", s.display_name),
        ("DefaultToEngaged", "N"),
        ("SwitchIsLatching", "Y"),
        ("StoreInDivisionalCombinations", "Y"),
        ("StoreInGeneralCombinations", "Y"),
        ("AccessibleForMIDIInputAndOutput", "Y"),
        ("PercussiveEngagingSoundEffect_RankID", None),
        ("PercussiveEngagingSoundEffect_MIDINoteNumber", 0),
        ("PercussiveDisengagingSoundEffect_RankID", None),
        ("PercussiveDisengagingSoundEffect_MIDINoteNumber", 0),
        ("SustainingSoundEffect_RankID", None),
        ("SustainingSoundEffect_MIDINoteNumber", 0),
        ("StopCodeFromWhichToCopyState", None),
        ("OverrideSourceDivisionToSpecifiedDivisionCode", None),
    ]


def _stoprank_fields(sr: StopRank):
    return [
        ("Name", None),
        ("StopCode", sr.stop_code),
        ("RankTypeCode", 1),
        ("RankID", sr.rank_id),
        ("ExternalRankID", None),
        ("MIDINoteNumIncrementFromDivisionToRank", 0),
        ("MIDINoteNumOfFirstMappedDivisionKey", sr.first_mapped_key),
        ("NumberOfMappedDivisionKeys", sr.num_mapped_keys),
        ("ActionTypeCode", 1),
        ("ActionEffectCode", 1),
        ("PipeMIDINoteNum036_PizzOrReitPeriodMs", 0),
        ("PipeMIDINoteNum096_PizzOrReitPeriodMs", 0),
        ("StopCodeToSwitchToAlternateRank", None),
        ("RetriggerNotesWhenSwitchingBetweenNormalAndAlternateRanks", "N"),
        ("AlternateRankID", None),
        ("AlternateExternalRankID", None),
    ]


def _coupler_fields(c: Coupler):
    return [
        ("CouplerCode", c.coupler_code),
        ("Name", c.name),
        ("CustomDisplay1_DisplayPageID", c.display_page_id),
        ("CustomDisplay1_Text", c.display_name if c.display_page_id else None),
        ("CustomDisplay1_ControlStyleID", c.control_style_id),
        ("CustomDisplay1_PosPixels_X", c.pos_x),
        ("CustomDisplay1_PosPixels_Y", c.pos_y),
        ("CustomDisplay1_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay1_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay1_AlternateLayout1_PosPixels_Y", 0),
        ("CustomDisplay2_DisplayPageID", None),
        ("CustomDisplay2_Text", None),
        ("CustomDisplay2_ControlStyleID", None),
        ("CustomDisplay2_PosPixels_X", 0),
        ("CustomDisplay2_PosPixels_Y", 0),
        ("CustomDisplay2_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay2_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay2_AlternateLayout1_PosPixels_Y", 0),
        ("DisplayName", c.display_name),
        ("DefaultToEngaged", "N"),
        ("SwitchIsLatching", "Y"),
        ("StoreInDivisionalCombinations", "Y"),
        ("StoreInGeneralCombinations", "Y"),
        ("AccessibleForMIDIInputAndOutput", "Y"),
        ("PercussiveEngagingSoundEffect_RankID", None),
        ("PercussiveEngagingSoundEffect_MIDINoteNumber", 0),
        ("PercussiveDisengagingSoundEffect_RankID", None),
        ("PercussiveDisengagingSoundEffect_MIDINoteNumber", 0),
        ("SustainingSoundEffect_RankID", None),
        ("SustainingSoundEffect_MIDINoteNumber", 0),
        ("OverrideSourceDivisionToSpecifiedDivisionCode", None),
        ("OverrideDestDivisionToSpecifiedDivisionCode", None),
        ("CoupleDestinationKeyboardRatherThanKeyAction", "N"),
        ("CouplerCodeFromWhichToCopyState", None),
        ("CustomCoupler_MIDINoteNumIncrementFromSourceToDest", 0),
        ("CustomCoupler_KeyActionTypeCode", None),
        ("CustomCoupler_KeyActionEffectCode", None),
        ("CustomCoupler_PipeMIDINoteNum036_PizzOrReitPeriodMs", 0),
        ("CustomCoupler_PipeMIDINoteNum096_PizzOrReitPeriodMs", 0),
    ]


def _tremulant_fields(t: Tremulant):
    return [
        ("TremulantCode", t.tremulant_code),
        ("Name", t.name),
        ("CustomDisplay1_DisplayPageID", t.display_page_id),
        ("CustomDisplay1_Text", t.display_name if t.display_page_id else None),
        ("CustomDisplay1_ControlStyleID", t.control_style_id),
        ("CustomDisplay1_PosPixels_X", t.pos_x),
        ("CustomDisplay1_PosPixels_Y", t.pos_y),
        ("CustomDisplay1_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay1_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay1_AlternateLayout1_PosPixels_Y", 0),
        ("CustomDisplay2_DisplayPageID", None),
        ("CustomDisplay2_Text", None),
        ("CustomDisplay2_ControlStyleID", None),
        ("CustomDisplay2_PosPixels_X", 0),
        ("CustomDisplay2_PosPixels_Y", 0),
        ("CustomDisplay2_AlternateLayout1_ControlStyleID", None),
        ("CustomDisplay2_AlternateLayout1_PosPixels_X", 0),
        ("CustomDisplay2_AlternateLayout1_PosPixels_Y", 0),
        ("DisplayName", t.display_name),
        ("DefaultToEngaged", "N"),
        ("SwitchIsLatching", "Y"),
        ("StoreInDivisionalCombinations", "Y"),
        ("StoreInGeneralCombinations", "Y"),
        ("AccessibleForMIDIInputAndOutput", "Y"),
        ("PercussiveEngagingSoundEffect_RankID", None),
        ("PercussiveEngagingSoundEffect_MIDINoteNumber", 0),
        ("PercussiveDisengagingSoundEffect_RankID", None),
        ("PercussiveDisengagingSoundEffect_MIDINoteNumber", 0),
        ("SustainingSoundEffect_RankID", None),
        ("SustainingSoundEffect_MIDINoteNumber", 0),
        ("TremulantCodeFromWhichToCopyState", None),
        ("FrequencyHz", 5.2),
        ("MaxFrequencyRandomisationPct", 15),
        ("MaxDepthRandomisationPct", 15),
    ]


def _control_style_fields(cs: ControlStyle):
    return [
        ("ControlStyleID", cs.control_style_id),
        ("Name", cs.name),
        ("ImageFileInstallationPackageID", cs.image_package_id),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfControl_LeftX", 0),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfControl_TopY", 0),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfControl_RightX", cs.clickable_right_x),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfControl_Bottom", cs.clickable_bottom_y),
        ("Image_TransparencyMaskFilename", cs.mask_filename),
        ("Image_NumberOfStages", cs.num_stages),
        ("Image_Stage00_ImageFilename", cs.stage00_filename),
        ("Image_Stage01_ImageFilename", cs.stage01_filename),
        ("Image_Stage02_ImageFilename", None),
        ("Image_Stage03_ImageFilename", None),
        ("Image_Stage04_ImageFilename", None),
        ("Image_Stage05_ImageFilename", None),
        ("Image_Stage06_ImageFilename", None),
        ("Image_Stage07_ImageFilename", None),
        ("Image_Stage08_ImageFilename", None),
        ("Image_Stage09_ImageFilename", None),
        ("Image_Stage10_ImageFilename", None),
        ("Image_Stage11_ImageFilename", None),
        ("Image_Stage12_ImageFilename", None),
        ("Image_Stage13_ImageFilename", None),
        ("Image_Stage14_ImageFilename", None),
        ("Image_Stage15_ImageFilename", None),
        ("Text_HasText", "Y"),
        ("Text_Font_FaceName", cs.font_face),
        ("Text_Font_HeightPixels", cs.font_height_pixels),
        ("Text_Font_WeightCode", cs.font_weight_code),
        ("Text_Font_IsItalic", "N"),
        ("Text_Font_IsUnderlined", "N"),
        ("Text_RGBColour_Red", cs.text_red),
        ("Text_RGBColour_Green", cs.text_green),
        ("Text_RGBColour_Blue", cs.text_blue),
        ("Text_BoundingBoxPosPixelsRelToTopLeftOfImage_LeftX", cs.text_left_x),
        ("Text_BoundingBoxPosPixelsRelToTopLeftOfImage_TopY", cs.text_top_y),
        ("Text_BoundingBoxPosPixelsRelToTopLeftOfImage_RightX", cs.text_right_x),
        ("Text_BoundingBoxPosPixelsRelToTopLeftOfImage_Bottom", cs.text_bottom_y),
    ]


def _keyboard_style_fields(ks: KeyboardStyle):
    return [
        ("KeyboardStyleID", ks.keyboard_style_id),
        ("Name", ks.name),
        ("ImageFileInstallationPackageID", ks.image_package_id),
        ("KeyShapeImageFilename_CF_KeyDown", ks.cf_keydown),
        ("KeyShapeImageFilename_CF_KeyUp", ks.cf_keyup),
        ("KeyShapeImageFilename_CF_Mask", ks.cf_mask),
        ("KeyShapeImageFilename_D_KeyDown", ks.d_keydown),
        ("KeyShapeImageFilename_D_KeyUp", ks.d_keyup),
        ("KeyShapeImageFilename_D_Mask", ks.d_mask),
        ("KeyShapeImageFilename_EB_KeyDown", ks.eb_keydown),
        ("KeyShapeImageFilename_EB_KeyUp", ks.eb_keyup),
        ("KeyShapeImageFilename_EB_Mask", ks.eb_mask),
        ("KeyShapeImageFilename_G_KeyDown", ks.g_keydown),
        ("KeyShapeImageFilename_G_KeyUp", ks.g_keyup),
        ("KeyShapeImageFilename_G_Mask", ks.g_mask),
        ("KeyShapeImageFilename_A_KeyDown", ks.a_keydown),
        ("KeyShapeImageFilename_A_KeyUp", ks.a_keyup),
        ("KeyShapeImageFilename_A_Mask", ks.a_mask),
        ("KeyShapeImageFilename_Sharp_KeyDown", ks.sharp_keydown),
        ("KeyShapeImageFilename_Sharp_KeyUp", ks.sharp_keyup),
        ("KeyShapeImageFilename_Sharp_Mask", ks.sharp_mask),
        ("KeyShapeImageFilename_WholeNatural_KeyDown", ks.wholenatural_keydown),
        ("KeyShapeImageFilename_WholeNatural_KeyUp", ks.wholenatural_keyup),
        ("KeyShapeImageFilename_WholeNatural_Mask", ks.wholenatural_mask),
        ("KeyShapeImageFilename_FirstKeyDA_KeyDown", ks.firstkeyda_keydown),
        ("KeyShapeImageFilename_FirstKeyDA_KeyUp", ks.firstkeyda_keyup),
        ("KeyShapeImageFilename_FirstKeyDA_Mask", ks.firstkeyda_mask),
        ("KeyShapeImageFilename_FirstKeyG_KeyDown", ks.firstkeyg_keydown),
        ("KeyShapeImageFilename_FirstKeyG_KeyUp", ks.firstkeyg_keyup),
        ("KeyShapeImageFilename_FirstKeyG_Mask", ks.firstkeyg_mask),
        ("KeyShapeImageFilename_LastKeyDG_KeyDown", ks.lastkeydg_keydown),
        ("KeyShapeImageFilename_LastKeyDG_KeyUp", ks.lastkeydg_keyup),
        ("KeyShapeImageFilename_LastKeyDG_Mask", ks.lastkeydg_mask),
        ("KeyShapeImageFilename_LastKeyA_KeyDown", ks.lastkeya_keydown),
        ("KeyShapeImageFilename_LastKeyA_KeyUp", ks.lastkeya_keyup),
        ("KeyShapeImageFilename_LastKeyA_Mask", ks.lastkeya_mask),
        ("HorizSpacingPixels_LeftOfNaturalFromLeftOfNatural", ks.horiz_natural),
        ("HorizSpacingPixels_LeftOfCFSharpFromLeftOfCF", ks.horiz_cf_sharp),
        ("HorizSpacingPixels_LeftOfDASharpFromLeftOfDA", ks.horiz_da_sharp),
        ("HorizSpacingPixels_LeftOfGSharpFromLeftOfG", ks.horiz_g_sharp),
        ("HorizSpacingPixels_LeftOfDGFromLeftOfCFSharp", ks.horiz_dg_from_cfsharp),
        ("HorizSpacingPixels_LeftOfEBFromLeftOfDASharp", ks.horiz_eb_from_dasharp),
        ("HorizSpacingPixels_LeftOfAFromLeftOfGSharp", ks.horiz_a_from_gsharp),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Natural_LeftX", ks.clickable_natural_left_x),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Natural_TopY", ks.clickable_natural_top_y),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Natural_RightX", ks.clickable_natural_right_x),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Natural_BottomY", ks.clickable_natural_bottom_y),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Sharp_LeftX", ks.clickable_sharp_left_x),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Sharp_TopY", ks.clickable_sharp_top_y),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Sharp_RightX", ks.clickable_sharp_right_x),
        ("ClickableAreaPosPixelsRelativeToTopLeftOfKey_Sharp_BottomY", ks.clickable_sharp_bottom_y),
    ]


def _display_page_fields(dp: DisplayPage):
    return [
        ("DisplayPageID", dp.display_page_id),
        ("Name", dp.name),
        ("BackgroundImageFileInstallationPackageID", dp.background_package_id),
        ("BackgroundImageFilename", dp.background_filename),
        ("AlternateLayout1_Include", "N"),
        ("AlternateLayout1_BackgroundImageFilename", None),
    ]


def render_custom_organ(organ_id, name, divisions, stops, ranks, stopranks, required_packages,
                         couplers=(), tremulants=(), control_styles=(), keyboard_styles=(),
                         display_pages=(), console_width=0, console_height=0,
                         default_display_page_id=None):
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Hauptwerk FileFormat="CustomOrgan" FileFormatVersion="5.00">',
        _object_list("_general", "_general", [
            _general_fields(organ_id, name, console_width, console_height, default_display_page_id)
        ]),
        _object_list("coupler", "coupler", [_coupler_fields(c) for c in couplers]) if couplers
        else _empty_object_list("coupler"),
        _object_list("customdisplaycontrolstyle", "customdisplaycontrolstyle",
                      [_control_style_fields(cs) for cs in control_styles]) if control_styles
        else _empty_object_list("customdisplaycontrolstyle"),
        _object_list("customdisplaykeyboardstyle", "customdisplaykeyboardstyle",
                      [_keyboard_style_fields(ks) for ks in keyboard_styles]) if keyboard_styles
        else _empty_object_list("customdisplaykeyboardstyle"),
        _empty_object_list("customdisplaylabel"),
        _object_list("customdisplaypage", "customdisplaypage",
                      [_display_page_fields(dp) for dp in display_pages]) if display_pages
        else _empty_object_list("customdisplaypage"),
        _object_list("division", "division", [_division_fields(d) for d in divisions]),
        _empty_object_list("enclosure"),
        _empty_object_list("externalrank"),
        _object_list("rank", "rank", [_rank_fields(r) for r in ranks]),
        _object_list(
            "requiredinstallationpackage",
            "requiredinstallationpackage",
            [_required_package_fields(p) for p in required_packages],
        ),
        _empty_object_list("shortcutpiston"),
        _object_list("stop", "stop", [_stop_fields(s) for s in stops]),
        _object_list("stoprank", "stoprank", [_stoprank_fields(sr) for sr in stopranks]),
        _object_list("tremulant", "tremulant", [_tremulant_fields(t) for t in tremulants]) if tremulants
        else _empty_object_list("tremulant"),
        "</Hauptwerk>",
    ]
    return "\n".join(parts) + "\n"
