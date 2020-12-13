import random
from pathlib import Path
from typing import Optional, List


class Reel:
    initial_index: int
    letters: str

    def __init__(self, letters: str, initial_index: Optional[int] = None):
        if not letters or len(letters) <= 1:
            raise ValueError("A reel needs at least 2 letters")
        if initial_index is not None and (
            initial_index >= len(letters) or initial_index < 0
        ):
            raise ValueError("Wrong initial index")
        self.letters = letters
        self.initial_index = (
            initial_index
            if initial_index is not None
            else random.randint(0, len(letters) - 1)
        )

    def __next__(self):
        return_value = self.current_letter()
        self.initial_index += 1
        if self.initial_index >= len(self.letters):
            self.initial_index = 0
        return return_value

    def current_letter(self) -> str:
        return self.letters[self.initial_index]

    def __iter__(self):
        return self

    def __eq__(self, other: "Reel"):
        return self.letters == other.letters

    @staticmethod
    def get_from_file(path: Path) -> List["Reel"]:
        with path.open() as file:
            file_contents = file.read().splitlines()
        return [Reel(letters=line.replace(" ", "")) for line in file_contents]
