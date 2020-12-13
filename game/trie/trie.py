from typing import Dict, List, Optional, Tuple


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

    def add_word(self, word: str) -> None:
        if not word:
            return
        node: Node = self.root
        for letter in word:
            existing = node.children.get(letter)
            if existing:
                node = existing
            else:
                node = node.add_child(letter)
        node.is_leaf = True
        self.number_of_words += 1

    def search_word(self, word: str) -> bool:
        if not word:
            return False
        node: Node = self.root
        for letter in word:
            node = node.children.get(letter)
            if not node:
                return False
        return node.is_leaf

    def delete_word(self, word: str):
        if not word:
            return
        node: Node = self.root
        parent_node: Optional[Node]
        nodes_to_delete: List[Tuple[Node, Node]] = []
        for letter in word:
            parent_node = node
            node = node.children.get(letter)
            if not node:
                return
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
            if len(node.children) == 0:
                del parent_node.children[node.letter]
