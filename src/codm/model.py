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
class Division:
    division_code: int
    name: str
    short_name: str
    number_of_keys: int
    first_key_midi_note: int
