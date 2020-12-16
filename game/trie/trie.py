import itertools
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import unidecode as unidecode


class Node:
    letter: str
    children: Dict[str, "Node"]
    is_leaf: bool = False

    def __init__(self, letter: str):
        self.children = {}
        self.letter = letter

    def add_child(self, letter: str) -> "Node":
        new_node = Node(letter=letter)
        self.children[letter] = new_node
        return new_node


class Trie:
    root: Node
    number_of_words: int

    def __init__(self):
        self.root = Node(letter="^")
        self.number_of_words = 0  # for testing purposes

    def _normalize_word(self, word):
        normalized = unidecode.unidecode(word)
        return normalized.replace("'", "").lower()

    def add_word(self, word: str) -> None:
        """
        Adds a word to the tree. The word is normalized to remove accents and other not ascii chars.
        Increases the internal number of words if the word is new (not existing in the tree).
        :param word: word to add
        :return: None
        """
        if not word:
            return
        node: Node = self.root
        for letter in self._normalize_word(word):
            existing = node.children.get(letter)
            if existing:
                node = existing
            else:
                node = node.add_child(letter)
        node.is_leaf = True
        if not existing:
            self.number_of_words += 1

    def search_word(self, word: str) -> bool:
        """
        Searches for a word in the tree.
        :param word: word to search
        :return: True if the word exists, false otherwise.
        """
        if not word:
            return False
        node: Node = self.root
        for letter in self._normalize_word(word):
            node = node.children.get(letter)
            if not node:
                return False
        return node.is_leaf

    def delete_word(self, word: str) -> bool:
        """
        Deletes a word from the Tree. Deletes nodes if necessary.
        :param word: word to delete
        :return: None
        """
        if not word:
            return False
        node: Node = self.root
        parent_node: Optional[Node]
        nodes_to_delete: List[Tuple[Node, Node]] = []
        for letter in self._normalize_word(word):
            parent_node = node
            node = node.children.get(letter)
            if not node:
                return False
            nodes_to_delete.append(
                (
                    node,
                    parent_node,
                )
            )
        nodes_to_delete = list(reversed(nodes_to_delete))
        for i, node_tuple in enumerate(nodes_to_delete):
            node: Node = node_tuple[0]
            parent_node: Node = node_tuple[1]
            if i == 0:
                node.is_leaf = False
            if len(node.children) == 0 and not node.is_leaf:
                del parent_node.children[node.letter]

        self.number_of_words -= 1
        return True

    def load_from_file(self, path: Path):
        """
        Loads words into the tree from a file.
        :param path: Path to a text file.
        :return: None
        """
        with path.open() as file:
            file_contents = file.read().splitlines()
        for word in file_contents:
            self.add_word(word)

    def get_all_possible_words(self, letters: str) -> List[str]:
        """
        Given some letters to combine, returns all the possible words that can be created
        using these letters.
        :param letters: Letters to combine (reels letters)
        :return: A list of all possible words.
        """
        words: List[str] = []
        if not letters or not letters.strip():
            return words
        # first single letter
        for letter in letters:
            if self.search_word(letter):
                words.append(letter)
        # now permutations from 2 -> len(word) groups
        for group_length in range(2, len(letters) + 1):
            for permutation in itertools.permutations(letters, group_length):
                permutation_str = "".join(permutation)
                if self.search_word(permutation_str):
                    words.append(permutation_str)
        return words
