from unittest import TestCase

from game.scorer import Scorer


class TestScorer(TestCase):
    def setUp(self) -> None:
        self.scorer = Scorer()

    def test_all_scores_are_loaded(self):
        self.assertEqual(len(self.scorer.scores), 26)

    def test_a_score(self):
        self.assertEqual(self.scorer.scores.get("a"), 1)

    def test_z_score(self):
        self.assertEqual(self.scorer.scores.get("z"), 10)

    def test_m_score(self):
        self.assertEqual(self.scorer.scores.get("m"), 3)
