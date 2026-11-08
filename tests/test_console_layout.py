import unittest

from src.codm.console_layout import (
    KNOB_SIZE,
    console_size,
    layout_controls,
    layout_keyboard_anchors,
    natural_key_count,
)
from src.codm.model import Coupler, Division, Stop, Tremulant


def _stop(stop_code, name="x"):
    return Stop(stop_code=stop_code, name=name, display_name=name.upper())


class TestConsoleLayout(unittest.TestCase):
    def test_natural_key_count_matches_known_compass(self):
        # Görlitz manual: MIDI 36-93 (58 keys) -> 34 natural keys (C..A, 58/12*7 rounded)
        self.assertEqual(natural_key_count(36, 58), 34)
        # Görlitz pedal: MIDI 36-67 (32 keys) -> 19 natural keys
        self.assertEqual(natural_key_count(36, 32), 19)

    def test_layout_controls_places_all_52_without_overlap(self):
        stops = [_stop(2000 + (div - 1) * 100 + i) for div, n in [(1, 9), (2, 13), (3, 13), (4, 9)] for i in range(1, n + 1)]
        couplers = [Coupler(coupler_code=c, name="x", display_name="X") for c in [1006, 1011, 1016, 1111, 1116, 1216]]
        tremulants = [Tremulant(tremulant_code=t, name="x", display_name="X") for t in [1720, 1730]]

        positions = layout_controls(stops, couplers, tremulants)

        self.assertEqual(len(positions), 44 + 6 + 2)
        self.assertEqual(len(set(positions.values())), len(positions), "overlapping positions")

        # no two controls may have overlapping KNOB_SIZE x KNOB_SIZE bounding boxes
        boxes = list(positions.values())
        for i, (x1, y1) in enumerate(boxes):
            for x2, y2 in boxes[i + 1:]:
                overlap_x = abs(x1 - x2) < KNOB_SIZE
                overlap_y = abs(y1 - y2) < KNOB_SIZE
                self.assertFalse(overlap_x and overlap_y, f"{(x1,y1)} overlaps {(x2,y2)}")

    def test_layout_keyboard_anchors_stacked_without_overlapping_controls(self):
        anchors = layout_keyboard_anchors(controls_bottom_y=500)
        self.assertEqual(set(anchors.keys()), {1, 2, 3, 4})
        ys = sorted(y for x, y in anchors.values())
        # strictly increasing - each keyboard below the previous, all below controls
        self.assertTrue(all(y >= 500 for y in ys))
        self.assertEqual(len(set(ys)), 4)

    def test_console_size_covers_every_element(self):
        divisions = [
            Division(division_code=1, name="PEDAL", short_name="Pedal", number_of_keys=32, first_key_midi_note=36),
            Division(division_code=2, name="HW", short_name="HW", number_of_keys=58, first_key_midi_note=36),
            Division(division_code=3, name="OW", short_name="OW", number_of_keys=58, first_key_midi_note=36),
            Division(division_code=4, name="BW", short_name="BW", number_of_keys=56, first_key_midi_note=36),
        ]
        control_positions = {"stop:2001": (900, 50), "stop:2002": (20, 20)}
        keyboard_anchors = {1: (20, 900), 2: (20, 600), 3: (20, 700), 4: (20, 800)}
        width, height = console_size(control_positions, keyboard_anchors, divisions)
        self.assertGreaterEqual(width, 900 + KNOB_SIZE)
        self.assertGreaterEqual(height, 900 + 70)  # pedal keyboard height ~70px


if __name__ == "__main__":
    unittest.main()
