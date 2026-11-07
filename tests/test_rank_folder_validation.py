import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.codm.brustwerk_pilot import _validate_rank_folder


def _make_notes(dir_path: Path, first, last):
    dir_path.mkdir(parents=True, exist_ok=True)
    names = [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
    ]
    for note in range(first, last + 1):
        (dir_path / f"{note:03d}-{names[note % 12]}.wav").write_bytes(b"")


class TestRankFolderValidation(unittest.TestCase):
    def test_accepts_a_complete_contiguous_folder(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_notes(root / "ow/01_gedackt8/lang/haupt", 36, 91)
            # should not raise
            _validate_rank_folder(root, "ow/01_gedackt8/lang/haupt", num_pipes=56, first_midi_note=36)

    def test_rejects_gap_in_note_range(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "ow/01_gedackt8/lang/haupt"
            _make_notes(folder, 36, 91)
            (folder / "060-C.wav").unlink()  # introduce a gap
            with self.assertRaises(ValueError):
                _validate_rank_folder(root, "ow/01_gedackt8/lang/haupt", num_pipes=56, first_midi_note=36)

    def test_rejects_case_mismatched_folder_name(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            # real folder is capitalised "Lang", but the rank references lowercase "lang"
            _make_notes(root / "ow/01_gedackt8/Lang/haupt", 36, 91)
            with self.assertRaises(ValueError):
                _validate_rank_folder(root, "ow/01_gedackt8/lang/haupt", num_pipes=56, first_midi_note=36)


if __name__ == "__main__":
    unittest.main()
