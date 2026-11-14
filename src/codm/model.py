from dataclasses import dataclass


@dataclass
class Rank:
    rank_id: int
    name: str
    num_pipes: int
    first_midi_note: int
    package_id: int
    main_folder: str
    short_release_folder: str | None
    pitch_harmonic_num: float
    windchest_division_code: int
    tuning_adjust_cents_036: float = 0.0
    tuning_adjust_cents_096: float = 0.0
    short_release_max_ms: int = 0
    medium_release_folder: str | None = None
    medium_release_max_ms: int = 0
    rel_release_folder: str | None = None
    trem_code: int | None = None
    trem_package_id: int | None = None
    trem_waveform_folder: str | None = None


@dataclass
class Stop:
    stop_code: int
    name: str
    display_name: str
    display_page_id: int | None = None
    control_style_id: int | None = None
    pos_x: int = 0
    pos_y: int = 0


@dataclass
class StopRank:
    stop_code: int
    rank_id: int
    first_mapped_key: int
    num_mapped_keys: int


@dataclass
class Coupler:
    coupler_code: int
    name: str
    display_name: str
    display_page_id: int | None = None
    control_style_id: int | None = None
    pos_x: int = 0
    pos_y: int = 0


@dataclass
class Tremulant:
    tremulant_code: int
    name: str
    display_name: str
    display_page_id: int | None = None
    control_style_id: int | None = None
    pos_x: int = 0
    pos_y: int = 0


@dataclass
class Division:
    division_code: int
    name: str
    short_name: str
    number_of_keys: int
    first_key_midi_note: int
    keyboard_display_page_id: int | None = None
    keyboard_style_id: int | None = None
    keyboard_pos_x: int = 0
    keyboard_pos_y: int = 0

    # Hauptwerk's Custom Organ loader rejects a division ShortName longer
    # than 5 characters (its own examples use Pedal/Great/Swell/Noise).
    MAX_SHORT_NAME_LEN = 5

    def __post_init__(self):
        if not self.short_name or len(self.short_name) > self.MAX_SHORT_NAME_LEN:
            raise ValueError(
                f"Division {self.name!r}: short_name {self.short_name!r} must be "
                f"1-{self.MAX_SHORT_NAME_LEN} characters (Hauptwerk limit)"
            )


@dataclass
class ControlStyle:
    """One Hauptwerk-standard-library drawknob style, reused for every
    stop/coupler/tremulant - fields copied verbatim from Hauptwerk's own
    ExampleCustomOrgan2.CustomOrgan_Hauptwerk_xml, ControlStyleID=10
    ("Drwkb07WoodSm/WhtTxt")."""
    control_style_id: int
    name: str
    image_package_id: int = 1
    clickable_right_x: int = 65
    clickable_bottom_y: int = 65
    mask_filename: str = ""
    num_stages: int = 2
    stage00_filename: str = ""
    stage01_filename: str = ""
    font_face: str = "Verdana"
    font_height_pixels: int = 8
    font_weight_code: int = 2
    text_red: int = 255
    text_green: int = 255
    text_blue: int = 255
    text_left_x: int = 2
    text_top_y: int = 1
    text_right_x: int = 61
    text_bottom_y: int = 61


@dataclass
class KeyboardStyle:
    """One Hauptwerk-standard-library keyboard key-shape style. Hauptwerk
    lays out every individual key from a single per-division anchor
    position plus these style-defined spacings - no per-key position is
    ever specified by the organ definition itself. Fields copied verbatim
    from ExampleCustomOrgan2's KeyboardStyleID=4 ("Man07IvorySm") and
    KeyboardStyleID=7 ("Ped06OldSm")."""
    keyboard_style_id: int
    name: str
    image_package_id: int = 1
    cf_keydown: str = ""
    cf_keyup: str = ""
    cf_mask: str = ""
    d_keydown: str = ""
    d_keyup: str = ""
    d_mask: str = ""
    eb_keydown: str = ""
    eb_keyup: str = ""
    eb_mask: str = ""
    g_keydown: str = ""
    g_keyup: str = ""
    g_mask: str = ""
    a_keydown: str = ""
    a_keyup: str = ""
    a_mask: str = ""
    sharp_keydown: str = ""
    sharp_keyup: str = ""
    sharp_mask: str = ""
    wholenatural_keydown: str = ""
    wholenatural_keyup: str = ""
    wholenatural_mask: str = ""
    firstkeyda_keydown: str = ""
    firstkeyda_keyup: str = ""
    firstkeyda_mask: str = ""
    firstkeyg_keydown: str = ""
    firstkeyg_keyup: str = ""
    firstkeyg_mask: str = ""
    lastkeydg_keydown: str = ""
    lastkeydg_keyup: str = ""
    lastkeydg_mask: str = ""
    lastkeya_keydown: str = ""
    lastkeya_keyup: str = ""
    lastkeya_mask: str = ""
    horiz_natural: int = 0
    horiz_cf_sharp: int = 0
    horiz_da_sharp: int = 0
    horiz_g_sharp: int = 0
    horiz_dg_from_cfsharp: int = 0
    horiz_eb_from_dasharp: int = 0
    horiz_a_from_gsharp: int = 0
    clickable_natural_left_x: int = 0
    clickable_natural_top_y: int = 0
    clickable_natural_right_x: int = 0
    clickable_natural_bottom_y: int = 0
    clickable_sharp_left_x: int = 0
    clickable_sharp_top_y: int = 0
    clickable_sharp_right_x: int = 0
    clickable_sharp_bottom_y: int = 0


@dataclass
class DisplayPage:
    """One custom console display page. Fields copied verbatim from
    ExampleCustomOrgan4-StAnnes-WithBasicGUIConsole's single page."""
    display_page_id: int
    name: str
    background_package_id: int = 1
    background_filename: str = ""
