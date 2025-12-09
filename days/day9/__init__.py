from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from pathlib import Path

from demapples.vec import Vec2
from demapples.range import Range


@dataclass(eq=True, frozen=True, slots=True)
class Line:
    p1: Vec2
    p2: Vec2
    min_y: int = 0
    max_y: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "min_y", min(self.p1.y, self.p2.y))
        object.__setattr__(self, "max_y", max(self.p1.y, self.p2.y))

    def horizontal(self) -> bool:
        return self.p1.y == self.p2.y

    def vertical(self) -> bool:
        return self.p1.x == self.p2.x

    def xrange(self) -> Range:
        if self.p1.x <= self.p2.x:
            return Range(self.p1.x, self.p2.x)
        else:
            return Range(self.p2.x, self.p1.x)

    def yrange(self) -> Range:
        if self.p1.y <= self.p2.y:
            return Range(self.p1.y, self.p2.y)
        else:
            return Range(self.p2.y, self.p1.y)

    def intersects(self, other: Line) -> bool:
        """
        >>> Line(Vec2(2, 3), Vec2(5, 3)).intersects(Line(Vec2(4, 1), Vec2(4, 4))) # Horizontal and vertical lines that intersect
        True
        >>> Line(Vec2(2, 3), Vec2(5, 3)).intersects(Line(Vec2(6, 1), Vec2(6, 4))) # Horizontal and vertical lines that do not intersect
        False
        >>> Line(Vec2(2, 3), Vec2(5, 3)).intersects(Line(Vec2(3, 3), Vec2(4, 3))) # Overlapping horizontal lines
        True
        >>> Line(Vec2(2, 3), Vec2(5, 3)).intersects(Line(Vec2(6, 3), Vec2(7, 3))) # Non-overlapping horizontal lines
        False
        """
        if self.horizontal() and other.horizontal():
            if self.p1.y != other.p1.y:
                return False
            return not (
                self.xrange().end < other.xrange().start
                or other.xrange().end < self.xrange().start
            )

        elif self.vertical() and other.vertical():
            if self.p1.x != other.p1.x:
                return False
            return not (
                self.yrange().end < other.yrange().start
                or other.yrange().end < self.yrange().start
            )

        elif self.horizontal() and other.vertical():
            return other.p1.x in self.xrange() and self.p1.y in other.yrange()

        elif self.vertical() and other.horizontal():
            return self.p1.x in other.xrange() and other.p1.y in self.yrange()

        raise AssertionError("Unreachable")


@dataclass(eq=True, frozen=True, slots=True)
class Ray:
    start: Vec2
    direction: Vec2

    def horizontal(self) -> bool:
        return self.direction.y == 0

    def vertical(self) -> bool:
        return self.direction.x == 0


@dataclass(eq=True, frozen=True, slots=True)
class Rectangle:
    p1: Vec2
    p2: Vec2

    def other_corners(self) -> tuple[Vec2, Vec2]:
        """
        >>> Rectangle(Vec2(1, 2), Vec2(4, 6)).other_corners()
        (Vec2(x=1, y=6), Vec2(x=4, y=2))
        """
        return (Vec2(self.p1.x, self.p2.y), Vec2(self.p2.x, self.p1.y))

    def area(self) -> int:
        """
        >>> Rectangle(Vec2(1, 2), Vec2(4, 6)).area()
        20
        """
        return (abs(self.p2.x - self.p1.x) + 1) * (abs(self.p2.y - self.p1.y) + 1)

    def sides_inside(self, margin: int) -> list[Line]:
        return [
            Line(
                Vec2(self.p1.x + margin, self.p1.y + margin),
                Vec2(self.p2.x - margin, self.p1.y + margin),
            ),
            Line(
                Vec2(self.p2.x - margin, self.p1.y + margin),
                Vec2(self.p2.x - margin, self.p2.y - margin),
            ),
            Line(
                Vec2(self.p2.x - margin, self.p2.y - margin),
                Vec2(self.p1.x + margin, self.p2.y - margin),
            ),
            Line(
                Vec2(self.p1.x + margin, self.p2.y - margin),
                Vec2(self.p1.x + margin, self.p1.y + margin),
            ),
        ]


class Shape:
    def __init__(self, lines: list[Line]) -> None:
        assert lines[0].p1 == lines[-1].p2, "Shape must be closed"
        self.lines = tuple(lines)
        self.points = set(line.p1 for line in lines)
        self.vertical_lines = tuple(line for line in lines if line.vertical())
        self.horizontal_lines = tuple(line for line in lines if line.horizontal())

    @cache
    def contains_point(self, point: Vec2) -> bool:
        if point in self.points:
            return True

        x, y = point.x, point.y

        # Treat points on the boundary as inside.
        for line in self.horizontal_lines:
            if y == line.p1.y:
                if x in line.xrange():
                    return True

        for line in self.vertical_lines:
            if x == line.p1.x:
                if y in line.yrange():
                    return True

        crossings = 0
        for line in self.vertical_lines:
            x0 = line.p1.x

            if x < x0 and line.min_y <= y < line.max_y:
                crossings += 1

        return (crossings % 2) == 1

    def intersects_line(self, line: Line) -> bool:
        return any(line.intersects(other) for other in self.lines)

    def contains_rectangle(self, rectangle: Rectangle) -> bool:
        return all(
            self.contains_point(corner) for corner in rectangle.other_corners()
        ) and not any(self.intersects_line(side) for side in rectangle.sides_inside(-1))

    @classmethod
    def from_points(cls, points: list[Vec2]) -> Shape:
        lines = [Line(points[i], points[i + 1]) for i in range(len(points) - 1)]
        lines.append(Line(points[-1], points[0]))
        return cls(lines)


def parse_input(input_str: str) -> list[Vec2]:
    """
    >>> parse_input("1,2\\n3,4\\n5,6")
    [Vec2(x=1, y=2), Vec2(x=3, y=4), Vec2(x=5, y=6)]
    """
    return [
        Vec2(x=int(x_str), y=int(y_str))
        for x_str, y_str in (line.split(",") for line in input_str.splitlines())
    ]


def largest(points: list[Vec2]) -> int:
    """
    >>> largest(parse_input(Path("days/day9/examples/1.txt").read_text()))
    50
    """
    return max(Rectangle(p1, p2).area() for p1, p2 in combinations(points, 2))


def largest2(points: list[Vec2]) -> int:
    """
    >>> largest2(parse_input(Path("days/day9/examples/1.txt").read_text()))
    24
    """
    shape = Shape.from_points(points)
    max_area = 0
    for pair in combinations(points, 2):
        rect = Rectangle(*pair)
        if shape.contains_rectangle(rect):
            new_area = rect.area()
            if new_area > max_area:
                max_area = new_area
    return max_area


def star1(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(largest(inp))


def star2(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(largest2(inp))


def render(input_str: str) -> None:
    points = parse_input(input_str)
    shape = Shape.from_points(points)

    import matplotlib.pyplot as plt

    for line in shape.lines:
        x1, y1 = line.p1.x, line.p1.y
        x2, y2 = line.p2.x, line.p2.y
        plt.plot([x1, x2], [y1, y2], color="red")

    plt.axis("equal")  # keep scale consistent so lines aren't distorted
    plt.show()
