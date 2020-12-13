from pathlib import Path

from game.scorer import Scorer
from game.trie import Trie


class ReelGame:
    scorer: Scorer
    trie: Trie

    def __init__(self):
        self.scorer = Scorer()
        parent = Path(__file__).parent
        path = parent / "resources" / "scores.txt"
        self.scorer.load_from_file(path)
        path = parent / "resources" / "american-english-large.txt"
        self.trie.load_from_file(path)
