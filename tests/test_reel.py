from pathlib import Path
from unittest import TestCase

from game.reel.reel import Reel


class TestReel(TestCase):
    def test_get_from_file(self):
        expected = [Reel(letters="udxclae"), Reel(letters="eyvpqyn")]
        path = Path(__file__).parent / "resources" / "reels.txt"
        result = Reel.get_from_file(path)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result, expected)

    def test_constructor_no_initial_index(self):
        letters = "abcd"
        reel = Reel(letters=letters)
        self.assertEqual(reel.letters, letters)
        self.assertTrue(reel.index < len(letters))

    def test_constructor_with_index(self):
        letters = "abcd"
        initial_index = 3
        reel = Reel(letters=letters, initial_index=initial_index)
        self.assertEqual(reel.letters, letters)
        self.assertEqual(reel.index, initial_index)

    def test_constructor_wrong_index(self):
        letters = "abcd"
        with self.assertRaises(ValueError):
            Reel(letters=letters, initial_index=-1)

        with self.assertRaises(ValueError):
            Reel(letters=letters, initial_index=len(letters))

    def test_iterator(self):
        letters = "abc"
        reel = Reel(letters=letters, initial_index=1)
        result = []
        expected = ["b", "c", "a"]
        for i in range(len(letters)):
            result.append(reel.current_letter())
            next(reel)
        self.assertEqual(result, expected)
