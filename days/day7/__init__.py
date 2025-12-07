from functools import cache
from pathlib import Path


def parse_input(input_str: str) -> list[list[int]]:
    """
    >>> parse_input(Path("days/day7/examples/1.txt").read_text())
    [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0]]
    """
    result = [[1 if c in "S^" else 0 for c in line] for line in input_str.splitlines()]
    return [line for line in result if any(line)]


def parse_input_bits(input_str: str) -> tuple[str, ...]:
    lines = [
        "".join("1" if c in "S^" else "0" for c in line)
        for line in input_str.splitlines()
    ]
    return tuple(line for line in lines if "1" in line)


def split(a: list[int], b: list[int]) -> tuple[list[int], int]:
    """
    >>> split([0], [0])
    ([0], 0)
    >>> split([1], [0])
    ([1], 0)
    >>> split([0], [1])
    ([0], 0)
    >>> split([0,1,0], [0,1,0])
    ([1, 0, 1], 1)
    >>> split([0,1,0,1,0], [0,1,0,1,0])
    ([1, 0, 1, 0, 1], 2)
    >>> split([0,1,0,0,1,0], [0,1,0,0,1,0])
    ([1, 0, 1, 1, 0, 1], 2)
    """
    result = [0] * len(a)

    split_count = 0
    for i in range(len(a)):
        if a[i] and b[i]:
            split_count += 1

        if not a[i]:
            continue

        if not b[i]:
            result[i] = 1
            continue

        result[i - 1] |= 1
        result[i + 1] |= 1

    return result, split_count


def total_splits(inp: list[list[int]]) -> int:
    """
    >>> total_splits(parse_input(Path("days/day7/examples/1.txt").read_text()))
    21
    """
    total_count = 0
    curr = inp[0]
    for nxt in inp[1:]:
        curr, split_count = split(curr, nxt)
        total_count += split_count
    return total_count


@cache
def quantum_split(xs: tuple[str]) -> int:
    """
    >>> quantum_split(("010",))
    1
    >>> quantum_split(("010", "000"))
    1
    >>> quantum_split(("010", "010"))
    2
    >>> quantum_split(("00100", "00100", "01010"))
    4
    >>> quantum_split(parse_input_bits(Path("days/day7/examples/1.txt").read_text()))
    40
    """

    if len(xs) == 1:
        return 1

    x, y, *ys_list = xs
    ys = tuple(ys_list)

    for i, (char_a, char_b) in enumerate(zip(x, y)):
        if char_a == "1" and char_b == "1":
            split_a = "".join(
                "1" if j == i - 1 else "0" if j == i else c for j, c in enumerate(x)
            )
            split_b = "".join(
                "1" if j == i + 1 else "0" if j == i else c for j, c in enumerate(x)
            )
            return quantum_split((split_a,) + ys) + quantum_split((split_b,) + ys)

    return quantum_split((x,) + ys)


def star1(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(total_splits(inp))


def star2(input_str: str) -> str:
    inp = parse_input_bits(input_str)
    return str(quantum_split(inp))
