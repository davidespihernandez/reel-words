from pathlib import Path
from unittest import TestCase, mock

from game import ReelGame
from game.reel import Reel
from game.scorer import Scorer
from game.trie import Trie


class TestGame(TestCase):
    @mock.patch("game.ReelGame.load_data_from_files")
    def test_current_word(self, mock_load):
        game = ReelGame()
        game.reels = [
            Reel(letters="abc", initial_index=0),
            Reel(letters="bcd", initial_index=0),
            Reel(letters="cde", initial_index=0),
        ]
        # the current word is the first letter of each reel -> abc
        self.assertEqual(game.current_word(), "abc")

    @mock.patch("game.ReelGame.load_data_from_files")
    def test_selected_word(self, mock_load):
        game = ReelGame()
        game.reels = [
            Reel(letters="abc", initial_index=1),
            Reel(letters="bcd", initial_index=1),
            Reel(letters="cde", initial_index=1),
        ]
        # the current word is the second letter of each reel -> bcd
        # selected_word moves forward each selected reel
        self.assertEqual(game.selected_word([0]), "b")
        self.assertEqual(game.selected_word([1]), "c")
        self.assertEqual(game.selected_word([2]), "d")
        self.assertEqual(game.selected_word([0, 1]), "cd")
        self.assertEqual(game.selected_word([0, 1, 2]), "abe")

    @mock.patch("game.ReelGame.load_data_from_files")
    def test_word_score(self, mock_load):
        game = ReelGame()

        path = Path(__file__).parent / "resources" / "scores.txt"
        game.scorer.load_from_file(path)
        word = "abc"
        game.trie.add_word(word)
        self.assertEqual(game.word_score(word), 7)  # 1 + 3 + 3
        self.assertEqual(game.word_score("other"), 0)

    def test_actual_load(self):
        game = ReelGame()
        self.assertTrue(len(game.reels) > 0)
        self.assertTrue(game.trie.number_of_words > 0)
        self.assertTrue(len(game.scorer.scores) > 0)
