from typing import Dict
from pathlib import Path


class Scorer:
    scores: Dict[str, int] = {}

    def load_from_file(self, path: Path):
        """
        Loads the scores from a text file.
        :param path: Path to a text file.
        :return: None
        """
        with path.open() as file:
            file_contents = file.read().splitlines()
        lines = [line.split() for line in file_contents]
        self.scores = {line[0]: int(line[1]) for line in lines}

    def calculate_word_score(self, word: str) -> int:
        """
        Calculates the total score for a word.
        :param word: Word to score.
        :return: Score
        """
        score: int = 0
        for letter in word:
            score += self.scores.get(letter)
        return score
