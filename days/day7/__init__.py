from functools import cache
from pathlib import Path


def split(a: str, b: str) -> tuple[str, int]:
    """
    >>> split("0", "0")
    ('0', 0)
    >>> split("1", "0")
    ('1', 0)
    >>> split("0", "1")
    ('0', 0)
    >>> split("010", "010")
    ('101', 1)
    >>> split("01010", "01010")
    ('10101', 2)
    >>> split("010010", "010010")
    ('101101', 2)
    """
    result = {}

    def set_value(i: int, value: str) -> None:
        result[i] = value if result.get(i, "0") == "0" else "1"

    split_count = 0
    for i, (char_a, char_b) in enumerate(zip(a, b)):
        if char_a == "1" and char_b == "1":
            split_count += 1

        if char_a == "0":
            set_value(i, "0")
            continue

        if char_b == "0":
            set_value(i, "1")
            continue

        set_value(i - 1, "1")
        set_value(i, "0")
        set_value(i + 1, "1")

    return "".join(result.get(i, "0") for i in range(len(a))), split_count


def parse_input(input_str: str) -> list[str]:
    """
    >>> parse_input(Path("days/day7/examples/1.txt").read_text())
    ['000000010000000', '000000010000000', '000000101000000', '000001010100000', '000010100010000', '000101000101000', '001000100000100', '010101010100010']
    """
    result = [
        "".join("1" if c in "S^" else "0" for c in line)
        for line in input_str.splitlines()
    ]
    return [line for line in result if any(c == "1" for c in line)]


def total_splits(inp: list[str]) -> int:
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
    >>> quantum_split(tuple(parse_input(Path("days/day7/examples/1.txt").read_text())))
    40
    """

    if len(xs) == 1:
        return 1

    x, y, *ys = xs

    for i, (char_a, char_b) in enumerate(zip(x, y)):
        if char_a == "1" and char_b == "1":
            split_a = "".join(
                "1" if j == i - 1 else "0" if j == i else c for j, c in enumerate(x)
            )
            split_b = "".join(
                "1" if j == i + 1 else "0" if j == i else c for j, c in enumerate(x)
            )
            return quantum_split((split_a,) + tuple(ys)) + quantum_split(
                (split_b,) + tuple(ys)
            )

    return quantum_split((x,) + tuple(ys))


def star1(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(total_splits(inp))


def star2(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(quantum_split(tuple(inp)))
