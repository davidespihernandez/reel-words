from functools import reduce
from pathlib import Path
from unittest import TestCase

from game.scorer import Scorer


class TestScorer(TestCase):
    def setUp(self) -> None:
        self.scorer = Scorer()
        self.all_scores = {
            "a": 1,
            "b": 3,
            "c": 3,
            "d": 2,
            "e": 1,
            "f": 4,
            "g": 2,
            "h": 4,
            "i": 1,
            "j": 8,
            "k": 5,
            "l": 1,
            "m": 3,
            "n": 1,
            "o": 1,
            "p": 3,
            "q": 1,
            "r": 1,
            "s": 1,
            "t": 1,
            "u": 1,
            "v": 4,
            "w": 4,
            "x": 8,
            "y": 4,
            "z": 10,
        }
        path = Path(__file__).parent / "resources" / "scores.txt"
        self.scorer.load_from_file(path)

    def test_all_scores_are_loaded(self):
        self.assertEqual(self.scorer.scores, self.all_scores)

    def test_calculate_word_score(self):
        all_scores = [v for k, v in self.all_scores.items()]
        all_letters = [k for k, v in self.all_scores.items()]
        all_scores_sum = reduce((lambda a, b: a + b), all_scores)
        all_letters_word = "".join(all_letters)
        self.assertEqual(
            self.scorer.calculate_word_score(all_letters_word), all_scores_sum
        )
