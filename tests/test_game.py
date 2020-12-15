from pathlib import Path
from unittest import TestCase, mock

from game import ReelGame
from game.reel import Reel


class TestGame(TestCase):
    def setUp(self):
        self.game = ReelGame()
        self.game.reels = [
            Reel(letters="abc", initial_index=0),
            Reel(letters="bcd", initial_index=0),
            Reel(letters="cde", initial_index=0),
        ]
        path = Path(__file__).parent / "resources" / "scores.txt"
        self.game.scorer.load_from_file(path)

    def current_reels_letters(self):
        # the current word is the first letter of each reel -> abc
        self.assertEqual(self.game.current_reels_letters(), "abc")

    def test_game_process_word(self):
        word = "abc"
        self.game.trie.add_word(word)
        self.assertEqual(self.game.process_word(word), 7)  # 1 + 3 + 3
        self.assertEqual(self.game.current_reels_letters(), "bcd")
        self.assertEqual(self.game.last_existing_word, word)
        self.assertEqual(self.game.number_of_existing_words, 1)
        self.assertEqual(self.game.total_score, 7)
        self.assertEqual(self.game.total_words, 1)
        # search a new word with the new reels
        word = "dc"
        self.game.trie.add_word(word)
        self.assertEqual(self.game.process_word(word), 5)  # 3 + 2
        self.assertEqual(self.game.current_reels_letters(), "bde")
        self.assertEqual(self.game.last_existing_word, word)
        self.assertEqual(self.game.number_of_existing_words, 2)
        self.assertEqual(self.game.total_score, 7 + 5)
        self.assertEqual(self.game.total_words, 2)
        # now a not existing word
        word = "be"
        self.assertEqual(self.game.process_word(word), 0)  # not existing
        self.assertEqual(self.game.current_reels_letters(), "bde")  # no changes
        self.assertEqual(self.game.last_existing_word, "dc")
        self.assertEqual(self.game.last_not_existing_word, word)
        self.assertEqual(self.game.number_of_existing_words, 2)
        self.assertEqual(self.game.number_of_not_existing_words, 1)
        self.assertEqual(self.game.total_score, 7 + 5)  # same score
        self.assertEqual(self.game.total_words, 3)
        # now an invalid word (not buildable with the reels letters)
        word = "ba"
        self.assertEqual(self.game.process_word(word), -1)  # invalid
        self.assertEqual(self.game.current_reels_letters(), "bde")  # no changes
        self.assertEqual(self.game.last_existing_word, "dc")
        self.assertEqual(self.game.last_not_existing_word, "be")
        self.assertEqual(self.game.number_of_existing_words, 2)
        self.assertEqual(self.game.number_of_not_existing_words, 1)
        self.assertEqual(self.game.number_of_invalid_words, 1)
        self.assertEqual(self.game.total_score, 7 + 5)  # same score
        self.assertEqual(self.game.total_words, 4)

    def test_process_invalid_word(self):
        self.assertEqual(self.game.current_reels_letters(), "abc")
        self.assertEqual(self.game.process_word("bba"), -1)
        self.assertEqual(self.game.process_word("aab"), -1)
        self.assertEqual(self.game.process_word("fa"), -1)
        self.assertEqual(self.game.process_word("f"), -1)
        self.assertEqual(self.game.process_word(""), -1)

    def test_process_valid_not_existing_word(self):
        self.assertEqual(self.game.current_reels_letters(), "abc")
        self.assertEqual(self.game.process_word("a"), 0)
        self.assertEqual(self.game.process_word("b"), 0)
        self.assertEqual(self.game.process_word("c"), 0)
        self.assertEqual(self.game.process_word("ab"), 0)
        self.assertEqual(self.game.process_word("bc"), 0)
        self.assertEqual(self.game.process_word("ac"), 0)
        self.assertEqual(self.game.process_word("ba"), 0)
        self.assertEqual(self.game.process_word("cb"), 0)
        self.assertEqual(self.game.process_word("ca"), 0)
        self.assertEqual(self.game.process_word("abc"), 0)
        self.assertEqual(self.game.process_word("bca"), 0)
        self.assertEqual(self.game.process_word("cab"), 0)
        # reels are the same
        self.assertEqual(self.game.current_reels_letters(), "abc")

    def test_actual_load(self):
        game = ReelGame()
        game.load_data_from_files()
        self.assertTrue(len(game.reels) > 0)
        self.assertTrue(game.trie.number_of_words > 0)
        self.assertTrue(len(game.scorer.scores) > 0)
