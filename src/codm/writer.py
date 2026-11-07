from xml.sax.saxutils import escape

from src.codm.model import Division, Rank, Stop, StopRank


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


def _general_fields(organ_id, name):
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
        ("CustomDisplay_ConsoleWidthPixels", 0),
        ("CustomDisplay_ConsoleHeightPixels", 0),
        ("CustomDisplay_AlternateLayout1_ConsoleWidthPixels", 0),
        ("CustomDisplay_AlternateLayout1_ConsoleHeightPixels", 0),
        ("CustomDisplay_EnableStdPages_Controls", "Y"),
        ("CustomDisplay_EnableStdPages_Keyboards", "Y"),
        ("CustomDisplay_EnableStdPages_Wind", "Y"),
        ("CustomDisplay_EnableStdPages_Enclosures", "Y"),
        ("CustomDisplay_DefaultDisplayPageID", None),
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


def _division_display_block(layout_num):
    p = f"CustomDisplay{layout_num}"
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
        (f"{p}_Keyboard_DisplayPageID", None),
        (f"{p}_Keyboard_KeyboardStyleID", None),
        (f"{p}_Keyboard_PosPixels_X", 0),
        (f"{p}_Keyboard_PosPixels_Y", 0),
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
    fields.extend(_division_display_block(1))
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
        ("Samples_RelSampleFileFolderIfRelSamplesStoredInSeparateFiles", None),
        ("Samples_ShortNoteReleaseSampleFileFolderIfAny", r.short_release_folder),
        ("Samples_MaxNoteTimeMsForShortNoteReleaseSamplesIfAny", 200 if r.short_release_folder else 0),
        ("Samples_MediumNoteReleaseSampleFileFolderIfAny", None),
        ("Samples_MaxNoteTimeMsForMediumNoteReleaseSamplesIfAny", 0),
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
        ("Pitch_PipeMIDINoteNum036_TuningAdjustPercentSemitones", 0),
        ("Pitch_PipeMIDINoteNum096_TuningAdjustPercentSemitones", 0),
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
        ("Trem_TremulantCode", None),
        ("Trem_SampleInstallationPackageID", None),
        ("Trem_WaveformSampleFileFolder", None),
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
        ("CustomDisplay1_DisplayPageID", None),
        ("CustomDisplay1_Text", None),
        ("CustomDisplay1_ControlStyleID", None),
        ("CustomDisplay1_PosPixels_X", 0),
        ("CustomDisplay1_PosPixels_Y", 0),
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


def render_custom_organ(organ_id, name, divisions, stops, ranks, stopranks, required_packages):
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<Hauptwerk FileFormat="CustomOrgan" FileFormatVersion="5.00">',
        _object_list("_general", "_general", [_general_fields(organ_id, name)]),
        _empty_object_list("coupler"),
        _empty_object_list("customdisplaycontrolstyle"),
        _empty_object_list("customdisplaykeyboardstyle"),
        _empty_object_list("customdisplaylabel"),
        _empty_object_list("customdisplaypage"),
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
        _empty_object_list("tremulant"),
        "</Hauptwerk>",
    ]
    return "\n".join(parts) + "\n"
