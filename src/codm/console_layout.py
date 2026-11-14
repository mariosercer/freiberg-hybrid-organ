"""Computes pixel positions for the FreibergHybrid custom console page.

Everything here is pure layout arithmetic - no Hauptwerk-specific
semantics beyond the knob/keyboard sizes copied from the chosen style
(ControlStyle "Drwkb07WoodSm" is 65x65px; see model.py/full_organ.py).
"""

KNOB_SIZE = 65
KNOB_STEP = 70  # knob size + 5px gap
MAX_PER_ROW = 12
MARGIN_LEFT = 20
MARGIN_TOP = 20
# Hauptwerk rejects a custom console narrower than 1016 px (message code
# 5625); its own GUI examples (ExampleCustomOrgan2/4/5/6) use 1016x640.
MIN_CONSOLE_WIDTH = 1016
MIN_CONSOLE_HEIGHT = 640

# Divisions, in the order their knob rows stack top-to-bottom (my call,
# documented in the plan: Pedal, Oberwerk, Hauptwerk, Brustwerk).
KNOB_ROW_DIVISION_ORDER = [1, 3, 2, 4]

# Keyboards, in the order they stack top-to-bottom beneath the knobs (my
# call: Oberwerk, Hauptwerk, Brustwerk, Pedal - pedal always last/bottom
# since it is played with the feet).
KEYBOARD_STACK_ORDER = [3, 2, 4, 1]

MANUAL_KEYBOARD_HEIGHT = 32  # Man07IvorySm clickable area height
PEDAL_KEYBOARD_HEIGHT = 70  # Ped06OldSm clickable area height
KEYBOARD_ROW_GAP = 20

NATURAL_SEMITONES = {0, 2, 4, 5, 7, 9, 11}  # C D E F G A B, relative to C


def natural_key_count(first_midi_note: int, num_keys: int) -> int:
    """How many of num_keys keys (starting at first_midi_note) are natural
    (white) keys, used only to estimate a keyboard's on-screen width."""
    return sum(
        1 for note in range(first_midi_note, first_midi_note + num_keys)
        if (note % 12) in NATURAL_SEMITONES
    )


def _division_code_of_stop_code(stop_code: int) -> int:
    # Confirmed scheme (full_organ.py, hauptwerk_division.py, etc.):
    # StopCode = 2000 + (division_code - 1) * 100 + index.
    return (stop_code - 2000) // 100 + 1


def layout_controls(stops, couplers, tremulants) -> dict:
    """One knob-sized slot per stop/coupler/tremulant: one row block per
    division (stops), then a couplers row, then a tremulants row."""
    positions = {}
    y = MARGIN_TOP

    stops_by_division = {d: [] for d in KNOB_ROW_DIVISION_ORDER}
    for s in stops:
        stops_by_division[_division_code_of_stop_code(s.stop_code)].append(s)

    def place_row(items, key_prefix, code_attr):
        nonlocal y
        x = MARGIN_LEFT
        in_row = 0
        for item in sorted(items, key=lambda i: getattr(i, code_attr)):
            positions[f"{key_prefix}:{getattr(item, code_attr)}"] = (x, y)
            x += KNOB_STEP
            in_row += 1
            if in_row >= MAX_PER_ROW:
                in_row = 0
                x = MARGIN_LEFT
                y += KNOB_STEP
        if in_row > 0:
            y += KNOB_STEP

    for div in KNOB_ROW_DIVISION_ORDER:
        place_row(stops_by_division[div], "stop", "stop_code")

    place_row(couplers, "coupler", "coupler_code")
    place_row(tremulants, "tremulant", "tremulant_code")

    return positions


def layout_keyboard_anchors(controls_bottom_y: int) -> dict:
    """One (x, y) anchor per division code, stacked below the controls."""
    anchors = {}
    y = controls_bottom_y + KEYBOARD_ROW_GAP
    for div in KEYBOARD_STACK_ORDER:
        anchors[div] = (MARGIN_LEFT, y)
        height = PEDAL_KEYBOARD_HEIGHT if div == 1 else MANUAL_KEYBOARD_HEIGHT
        y += height + KEYBOARD_ROW_GAP
    return anchors


def controls_bottom_y(control_positions: dict) -> int:
    if not control_positions:
        return MARGIN_TOP
    return max(y for _, y in control_positions.values()) + KNOB_STEP


def console_size(control_positions: dict, keyboard_anchors: dict, divisions) -> tuple:
    max_x = max((x + KNOB_SIZE for x, _ in control_positions.values()), default=0)
    max_y = max((y + KNOB_SIZE for _, y in control_positions.values()), default=0)

    divisions_by_code = {d.division_code: d for d in divisions}
    for div, (x, y) in keyboard_anchors.items():
        d = divisions_by_code[div]
        width = natural_key_count(d.first_key_midi_note, d.number_of_keys) * 24  # widest (pedal) spacing, safe overestimate
        height = PEDAL_KEYBOARD_HEIGHT if div == 1 else MANUAL_KEYBOARD_HEIGHT
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)

    return (max(max_x + MARGIN_LEFT, MIN_CONSOLE_WIDTH),
            max(max_y + MARGIN_TOP, MIN_CONSOLE_HEIGHT))
