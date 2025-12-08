from __future__ import annotations
from dataclasses import dataclass

from demapples.vec import Vec2


@dataclass
class Diagram:
    rolls: set[Vec2]
    to_check: set[Vec2]

    @classmethod
    def from_str(cls, input_str: str) -> Diagram:
        rolls = set()
        lines = input_str.splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "@":
                    rolls.add(Vec2(x, y))
        return cls(rolls=rolls, to_check=rolls)

    @classmethod
    def from_file(cls, filepath: str) -> Diagram:
        with open(filepath) as file:
            input_str = file.read()
        return cls.from_str(input_str)

    @classmethod
    def from_example(cls) -> Diagram:
        return cls.from_file("days/day4/examples/1.txt")

    def accessible(self) -> set[Vec2]:
        """
        >>> Diagram.from_example().accessible()
        {Vec2(x=0, y=1), Vec2(x=0, y=7), Vec2(x=6, y=2), Vec2(x=0, y=4), Vec2(x=2, y=0), Vec2(x=0, y=9), Vec2(x=8, y=0), Vec2(x=3, y=0), Vec2(x=2, y=9), Vec2(x=8, y=9), Vec2(x=5, y=0), Vec2(x=6, y=0), Vec2(x=9, y=4)}
        """

        return {
            roll for roll in self.to_check if len(roll.neighbours() & self.rolls) < 4
        }

    def remove(self, to_remove: set[Vec2]) -> None:
        self.rolls = self.rolls - to_remove
        self.to_check = {
            nb for roll in to_remove for nb in roll.neighbours()
        } & self.rolls

    def repeat(self) -> int:
        """
        >>> Diagram.from_example().repeat()
        43
        """
        to_remove = self.accessible()
        total_count = len(to_remove)
        while to_remove:
            self.remove(to_remove)
            to_remove = self.accessible()
            total_count += len(to_remove)

        return total_count


def star1(input_str: str) -> str:
    inp = Diagram.from_str(input_str)
    return str(len(inp.accessible()))


def star2(input_str: str) -> str:
    inp = Diagram.from_str(input_str)
    return str(inp.repeat())
