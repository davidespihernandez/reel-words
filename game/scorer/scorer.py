from typing import Dict
from pathlib import Path


class Scorer:
    scores: Dict[str, int] = {}

    def __init__(self):
        parent = Path(__file__).parent.parent
        fname = parent / "resources" / "scores.txt"
        with fname.open() as file:
            file_contents = file.readlines()
        lines = [line.split() for line in file_contents]
        self.scores = {line[0]: int(line[1]) for line in lines}

    def get_score(self, word: str) -> int:
        score: int = 0
        for letter in word:
            score += self.scores.get(letter)
        return score
