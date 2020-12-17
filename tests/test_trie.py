from pathlib import Path
from unittest import TestCase

from game.trie import Trie


class TestTrie(TestCase):
    def setUp(self):
        self.trie = Trie()

    def test_load_from_file_and_search(self):
        path = Path(__file__).parent / "resources" / "words.txt"
        self.trie.load_from_file(path)
        words_in_file = ["word", "words", "Joe's", "a", "Übermenschen's", "éclair"]
        expected = ["word", "words", "joes", "a", "ubermenschens", "eclair"]
        self.assertEqual(self.trie.number_of_words, len(words_in_file))
        search_result = {word: self.trie.search_word(word) for word in expected}
        self.assertTrue(all([v for k, v in search_result.items()]))
        self.assertFalse(self.trie.search_word("other"))

    def test_add_word(self):
        word: str = "abc"
        self.trie.add_word(word)
        self.trie.add_word(word)
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertTrue(self.trie.search_word(word))
        self.assertFalse(self.trie.search_word("other"))
        self.assertFalse(self.trie.search_word(word[:2]))

    def test_delete_word_simple(self):
        word: str = "abc"
        self.trie.add_word(word)
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertTrue(self.trie.search_word(word))
        self.assertTrue(self.trie.delete_word(word))
        self.assertEqual(self.trie.number_of_words, 0)
        self.assertFalse(self.trie.search_word(word))

    def test_delete_not_existing_word(self):
        word: str = "abc"
        self.trie.add_word(word)
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertFalse(self.trie.delete_word("other"))
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertTrue(self.trie.search_word(word))

    def test_delete_parent_word_sharing_tree(self):
        parent_word: str = "word"
        child_word: str = "words"
        self.trie.add_word(parent_word)
        self.trie.add_word(child_word)
        self.assertEqual(self.trie.number_of_words, 2)
        self.assertTrue(self.trie.search_word(parent_word))
        self.assertTrue(self.trie.delete_word(parent_word))
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertFalse(self.trie.search_word(parent_word))
        self.assertTrue(self.trie.search_word(child_word))

    def test_delete_child_word_sharing_tree(self):
        parent_word: str = "word"
        child_word: str = "words"
        self.trie.add_word(parent_word)
        self.trie.add_word(child_word)
        self.assertEqual(self.trie.number_of_words, 2)
        self.assertTrue(self.trie.search_word(child_word))
        self.assertTrue(self.trie.delete_word(child_word))
        self.assertEqual(self.trie.number_of_words, 1)
        self.assertFalse(self.trie.search_word(child_word))
        self.assertTrue(self.trie.search_word(parent_word))

    def test_all_possible_words(self):
        self.trie.add_word("a")
        self.trie.add_word("a")
        self.trie.add_word("at")
        self.trie.add_word("sat")
        self.trie.add_word("other")
        result = sorted(self.trie.get_all_possible_words("tas"))
        expected = ["a", "at", "sat"]  # only the 3 best are returned
        self.assertEqual(expected, result)
