from __future__ import annotations

from demapples.range import Range


def parse_input(input_str: str) -> tuple[list[Range], list[int]]:
    ranges_str, numbers_str = input_str.strip().split("\n\n")
    ranges = [Range.from_str(line) for line in ranges_str.splitlines()]
    numbers = [int(num) for num in numbers_str.splitlines()]
    return ranges, numbers


def read_example() -> tuple[list[Range], list[int]]:
    with open("days/day5/examples/1.txt") as file:
        input_str = file.read()
    return parse_input(input_str)


def read_input() -> tuple[list[Range], list[int]]:
    with open("days/day5/input.txt") as file:
        input_str = file.read()
    return parse_input(input_str)


def fresh(ranges: list[Range], numbers: list[int]) -> int:
    """
    >>> fresh(*read_example())
    3
    >>> fresh(*read_input())
    598
    """
    merged = merge_all(ranges)

    sorted_numbers = sorted(numbers)
    i = 0
    count = 0
    for n in sorted_numbers:
        while i < len(merged) and merged[i].end < n:
            i += 1
        if i == len(merged):
            break
        if n in merged[i]:
            count += 1

    return count


def merge_all(ranges: list[Range]) -> list[Range]:
    """
    >>> count_ranges(merge_all(read_example()[0]))
    14
    >>> count_ranges(merge_all(read_input()[0]))
    360341832208407
    """
    sorted_ranges = sorted(ranges, key=lambda r: (r.start, r.end))
    merged = [sorted_ranges[0]]
    for r in sorted_ranges[1:]:
        last_merged = merged[-1]
        if last_merged.overlaps(r):
            merged[-1] = last_merged.merge(r)
        else:
            merged.append(r)

    return merged


def count_ranges(ranges: list[Range]) -> int:
    return sum(len(r) for r in ranges)


def star1(input_str: str) -> str:
    ranges, numbers = parse_input(input_str)
    return str(fresh(ranges, numbers))


def star2(input_str: str) -> str:
    ranges, _ = parse_input(input_str)
    return str(count_ranges(merge_all(ranges)))
