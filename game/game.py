import logging
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

    def load_data_from_files(self):
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

    def selected_word(self, reel_numbers: List[int]) -> str:
        """
        Calculates the word selected by the player, based on the selected reels (in order of selection).
        Moves forward the selected reels to the next value.
        :param reel_numbers: list of reel indexes
        :return: a string with the word
        Example:
            a b c d e f <- current value in reels
            [5, 4, 0] <- reel_numbers
            "fea" -> returned word
        """
        word = []
        for reel_number in reel_numbers:
            if reel_number < 0 or reel_number >= len(self.reels):
                raise ValueError("Wrong reel number")
            reel = self.reels[reel_number]
            word.append(reel.current_letter())
            next(reel)
        return "".join(word)

    def current_word(self):
        """
        :return: The current word from all the reels current letter, in reel order
        """
        return "".join([reel.current_letter() for reel in self.reels])

    def word_score(self, word: str):
        score: int = 0
        if self.trie.search_word(word):
            score = self.scorer.calculate_word_score(word)
        self.total_words += 1
        self.total_score += score
        return score

    def reset(self) -> None:
        self.total_words = 0
        self.total_score = 0
