from dataclasses import dataclass
from functools import cache
from itertools import product


NEIGHBOURS: set[tuple[int, int]] = {
    (x, y) for (x, y) in product(range(-1, 2), repeat=2) if not (x == 0 and y == 0)
}


@dataclass(eq=True, frozen=True, slots=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    @cache
    def neighbours(self) -> set["Vec2"]:
        return {Vec2(self.x + dx, self.y + dy) for (dx, dy) in NEIGHBOURS}


@dataclass
class Diagram:
    rolls: set[Vec2]
    to_check: set[Vec2]
    size: Vec2

    @classmethod
    def from_str(cls, input_str: str) -> "Diagram":
        rolls = set()
        lines = input_str.splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "@":
                    rolls.add(Vec2(x, y))
        size = Vec2(len(lines[0]), len(lines))
        return cls(rolls=rolls, to_check=rolls, size=size)

    @classmethod
    def from_file(cls, filepath: str) -> "Diagram":
        with open(filepath) as file:
            input_str = file.read()
        return cls.from_str(input_str)

    def neighbours(self, vec: Vec2) -> set[Vec2]:
        max_x, max_y = self.size.x, self.size.y

        return {
            nb
            for nb in vec.neighbours()
            if 0 <= nb.x < max_x and 0 <= nb.y < max_y and nb in self.rolls
        }


def read_example() -> Diagram:
    return Diagram.from_file("days/day4/examples/1.txt")


def accessible(inp: Diagram) -> set[Vec2]:
    """
    >>> accessible(read_example())
    {Vec2(x=0, y=1), Vec2(x=0, y=7), Vec2(x=6, y=2), Vec2(x=0, y=4), Vec2(x=2, y=0), Vec2(x=0, y=9), Vec2(x=8, y=0), Vec2(x=3, y=0), Vec2(x=2, y=9), Vec2(x=8, y=9), Vec2(x=5, y=0), Vec2(x=6, y=0), Vec2(x=9, y=4)}
    """

    return {roll for roll in inp.to_check if len(inp.neighbours(roll)) < 4}


def remove(inp: Diagram, to_remove: set[Vec2]) -> None:
    inp.rolls = inp.rolls - to_remove
    inp.to_check = {nb for roll in to_remove for nb in inp.neighbours(roll)} & inp.rolls


def repeat(inp: Diagram) -> int:
    """
    >>> repeat(read_example())
    43
    """
    to_remove = accessible(inp)
    total_count = len(to_remove)
    while to_remove:
        remove(inp, to_remove)
        to_remove = accessible(inp)
        total_count += len(to_remove)

    return total_count


def star1(input_str: str) -> str:
    inp = Diagram.from_str(input_str)
    return str(len(accessible(inp)))


def star2(input_str: str) -> str:
    inp = Diagram.from_str(input_str)
    return str(repeat(inp))
