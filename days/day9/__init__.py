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

    def intersects_line(self, line: Line) -> bool:
        """
        >>> Ray(Vec2(2, 3), Vec2(1, 0)).intersects_line(Line(Vec2(4, 3), Vec2(6, 3))) # Horizontal ray and horizontal line, with ray starting before line
        True
        >>> Ray(Vec2(5, 3), Vec2(1, 0)).intersects_line(Line(Vec2(4, 3), Vec2(6, 3))) # Horizontal ray and horizontal line, with ray starting inside line
        True
        >>> Ray(Vec2(7, 3), Vec2(1, 0)).intersects_line(Line(Vec2(4, 3), Vec2(6, 3))) # Horizontal ray and horizontal line, with ray starting after line
        False
        """
        if self.horizontal() and line.horizontal():
            if self.start.y != line.p1.y:
                return False

            if self.start.x in line.xrange():
                return True

            if self.direction.x > 0:
                return self.start.x <= line.xrange().start
            else:
                return self.start.x >= line.xrange().end

        elif self.vertical() and line.vertical():
            if self.start.x != line.p1.x:
                return False

            if self.start.y in line.yrange():
                return True

            if self.direction.y > 0:
                return self.start.y <= line.yrange().start
            else:
                return self.start.y >= line.yrange().end

        elif self.horizontal() and line.vertical():
            if self.start.y in line.yrange():
                if self.direction.x > 0:
                    return self.start.x <= line.p1.x
                else:
                    return self.start.x >= line.p1.x
            return False

        elif self.vertical() and line.horizontal():
            if self.start.x in line.xrange():
                if self.direction.y > 0:
                    return self.start.y <= line.p1.y
                else:
                    return self.start.y >= line.p1.y
            return False

        raise AssertionError("Unreachable")


@dataclass(eq=True, frozen=True, slots=True)
class Rectangle:
    p1: Vec2
    p2: Vec2

    def corners(self) -> list[Vec2]:
        return [
            Vec2(self.p1.x, self.p1.y),
            Vec2(self.p1.x, self.p2.y),
            Vec2(self.p2.x, self.p1.y),
            Vec2(self.p2.x, self.p2.y),
        ]

    def center(self) -> Vec2:
        return Vec2((self.p1.x + self.p2.x) // 2, (self.p1.y + self.p2.y) // 2)

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

    @cache
    def contains_point(self, point: Vec2) -> bool:
        rays = [
            Ray(point, Vec2(1, 0)),
            Ray(point, Vec2(-1, 0)),
            Ray(point, Vec2(0, 1)),
            Ray(point, Vec2(0, -1)),
        ]

        return all(
            any(ray.intersects_line(line) for line in self.lines) for ray in rays
        )

    def intersects_line(self, line: Line) -> bool:
        return any(line.intersects(other) for other in self.lines)

    def contains_rectangle(self, rectangle: Rectangle) -> bool:
        return all(
            self.contains_point(corner) for corner in rectangle.corners()
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

    rect = Rectangle(p1=Vec2(x=9, y=5), p2=Vec2(x=2, y=3))

    import matplotlib.pyplot as plt

    for line in shape.lines:
        x1, y1 = line.p1.x, line.p1.y
        x2, y2 = line.p2.x, line.p2.y
        plt.plot([x1, x2], [y1, y2], color="red")

    plt.axis("equal")  # keep scale consistent so lines aren't distorted
    plt.show()
