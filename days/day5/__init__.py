from __future__ import annotations
from dataclasses import dataclass


@dataclass(eq=True, frozen=True, slots=True)
class Range:
    start: int
    end: int

    def __len__(self) -> int:
        """
        >>> len(Range(3, 7))
        5
        >>> len(Range(1, 1))
        1
        >>> len(Range(1, 4))
        4
        >>> len(Range(6, 8))
        3
        """
        return self.end - self.start + 1

    def contains(self, number: int) -> bool:
        return self.start <= number <= self.end

    def overlaps(self, other: Range) -> bool:
        return not (self.end < other.start or other.end < self.start)

    def merge(self, other: Range) -> Range:
        return Range(start=min(self.start, other.start), end=max(self.end, other.end))

    @classmethod
    def from_str(cls, range_str: str) -> Range:
        start_str, end_str = range_str.split("-")
        return cls(start=int(start_str), end=int(end_str))


def parse_input(input_str: str) -> tuple[list[Range], list[int]]:
    ranges_str, numbers_str = input_str.strip().split("\n\n")
    ranges = [Range.from_str(line) for line in ranges_str.splitlines()]
    numbers = [int(num) for num in numbers_str.splitlines()]
    return ranges, numbers


def read_example() -> tuple[list[Range], list[int]]:
    with open("days/day5/examples/1.txt") as file:
        input_str = file.read()
    return parse_input(input_str)


def fresh(ranges: list[Range], numbers: list[int]) -> int:
    """
    >>> fresh(*read_example())
    3
    """
    return sum(1 for number in numbers if any(r.contains(number) for r in ranges))


def merge_all_and_count(ranges: list[Range]) -> int:
    """
    >>> merge_all_and_count([Range(1, 3), Range(2, 4), Range(6, 8)])
    7
    >>> merge_all_and_count(read_example()[0])
    14
    """
    sorted_ranges = sorted(ranges, key=lambda r: (r.start, r.end))
    merged = [sorted_ranges[0]]
    for r in sorted_ranges[1:]:
        last_merged = merged[-1]
        if last_merged.overlaps(r):
            merged[-1] = last_merged.merge(r)
        else:
            merged.append(r)

    return sum(len(r) for r in merged)


def star1(input_str: str) -> str:
    ranges, numbers = parse_input(input_str)
    return str(fresh(ranges, numbers))


def star2(input_str: str) -> str:
    ranges, _ = parse_input(input_str)
    return str(merge_all_and_count(ranges))
