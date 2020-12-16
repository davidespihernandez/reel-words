import collections
import logging
from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import List

from game.reel import Reel
from game.scorer import Scorer
from game.trie import Trie


logger = logging.getLogger(__name__)


class ReelGame:
    scorer: Scorer
    trie: Trie
    reels: List[Reel]
    total_score: int = 0
    total_words: int = 0
    last_existing_word: str = ""
    last_not_existing_word: str = ""
    # words that are not formed using the reels letters
    number_of_invalid_words: int = 0
    # valid word (formed using the reels letters) and existing in the trie
    number_of_existing_words: int = 0
    # valid word (formed using the reels letters) and not existing in the trie
    number_of_not_existing_words: int = 0
    previous_reels_letters: str = ""

    def load_data_from_files(self):
        """
        Loads the scorer, trie and reels data from the resources files
        """
        # separated method to allow mock easier
        logger.info("Loading data...")
        parent = Path(__file__).parent
        path = parent / "resources" / "scores.txt"
        self.scorer.load_from_file(path)
        path = parent / "resources" / "american-english-large.txt"
        self.trie.load_from_file(path)
        path = parent / "resources" / "reels.txt"
        self.reels = Reel.get_from_file(path)
        logger.info("Data loaded!")

    def __init__(self):
        self.scorer = Scorer()
        self.trie = Trie()
        self.reels = []

    def _get_reel_numbers(self, word: str) -> List[int]:
        reels_letters = defaultdict(list)
        for i, reel in enumerate(self.reels):
            reels_letters[reel.current_letter()].append(i)
        word_indexes: List[int] = []
        for letter in word:
            if len(reels_letters[letter]) > 0:
                word_indexes.append(reels_letters[letter].pop())
            else:
                # incorrect word for the current reels
                return []
        return word_indexes

    def get_current_reels_letters(self):
        """
        :return: The current letters from all the reels current letter,
        in reel order
        """
        return "".join([reel.current_letter() for reel in self.reels])

    def _move_reels(self, reels_to_move: List[int]):
        self.previous_reels_letters = self.get_current_reels_letters()
        # move the reels for the next word
        for reel_number in reels_to_move:
            next(self.reels[reel_number])

    def add_word_to_dictionary(self, word: str):
        """
        Inserts a word in the game trie
        :param word: word to imsert
        """
        self.trie.add_word(word)

    def evaluate_word(self, word: str):
        """
        Calculates the score of a word typed by the player
        :param word: the word to score
        :return:
            -1 if the word is invalid (can't be built using the reels)
            0 if the word is valid but not existing in the dictionary
            >0 (the word score) if the word is valid and exists in the trie
        """
        # first, the word must be created using the current_reel_letters
        reels_to_move = self._get_reel_numbers(word)
        if len(reels_to_move) == 0:
            self.number_of_invalid_words += 1
            self.total_words += 1
            return -1

        score: int = 0
        if self.trie.search_word(word):
            score = self.scorer.calculate_word_score(word)
            self.last_existing_word = word
            self.number_of_existing_words += 1
            self._move_reels(reels_to_move)
        else:
            self.last_not_existing_word = word
            self.number_of_not_existing_words += 1

        self.total_words += 1
        self.total_score += score

        return score

    def reset(self) -> None:
        """
        Resets all the game internal variables and the reels (not the trie or scores)
        """
        self.total_words = 0
        self.total_score = 0
        self.number_of_existing_words = 0
        self.number_of_not_existing_words = 0
        self.number_of_invalid_words = 0
        self.last_existing_word = ""
        self.last_not_existing_word = ""
        self.previous_reels_letters = ""

        # load reels again
        parent = Path(__file__).parent
        path = parent / "resources" / "reels.txt"
        self.reels = Reel.get_from_file(path)

    def cheat(self) -> List[str]:
        """
        Returns the 3 most scored words within all the possible words
        that can be created using the current reels letters. Each word is
        followed by the score in parenthesis
        :return: List of words
        """
        all_possible_words = self.trie.get_all_possible_words(
            self.get_current_reels_letters()
        )
        better_words = OrderedDict()
        for word in all_possible_words:
            score = self.scorer.calculate_word_score(word)
            if len(better_words) > 2:
                first_word = next(iter(better_words.items()))
                if first_word[0] < score:
                    better_words.popitem(last=False)
                    better_words[score] = word
            else:
                better_words[score] = word
            better_words = OrderedDict(sorted(better_words.items()))
        return [f"{word} ({score})" for score, word in better_words.items()]
