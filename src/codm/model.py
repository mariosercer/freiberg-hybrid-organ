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


@dataclass
class Tremulant:
    tremulant_code: int
    name: str
    display_name: str


@dataclass
class Division:
    division_code: int
    name: str
    short_name: str
    number_of_keys: int
    first_key_midi_note: int
