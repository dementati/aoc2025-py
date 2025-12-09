from pathlib import Path

from icecream import ic


def parse_input(input_string: str) -> list[tuple[bool, int]]:
    """Parses the input string into a list of tuples.

    >>> parse_input("L2\\nR3\\nL4")
    [(True, 2), (False, 3), (True, 4)]
    """

    return [
        (line[0] == "L", int(line[1:])) for line in input_string.strip().split("\n")
    ]


def solve_star1(instructions: list[tuple[bool, int]]) -> int:
    """Solves star 1.

    >>> solve_star1([(True, 68), (True, 30), (False, 48), (True, 5), (False, 60), (True, 55), (True, 1), (True, 99), (False, 14), (True, 82)])
    3
    """

    dial = 50
    zero_count = 0
    for turn_left, dist in instructions:
        dial = (dial + (-dist if turn_left else dist)) % 100

        if dial == 0:
            zero_count += 1

    return zero_count


def sign(num: int) -> int:
    """Returns the sign of a number.

    >>> sign(10)
    1
    >>> sign(-5)
    -1
    >>> sign(0)
    0
    """

    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def solve_star2(instructions: list[tuple[bool, int]]) -> int:
    """Solves star 2.

    >>> solve_star2([(True, 68), (True, 30), (False, 48), (True, 5), (False, 60), (True, 55), (True, 1), (True, 99), (False, 14), (True, 82)])
    6
    >>> solve_star2([(True, 50), (False, 100), (True, 50), (False, 50)])
    3
    >>> solve_star2([(True, 200)])
    2
    >>> solve_star2([(True, 50)])
    1
    >>> solve_star2([(True, 50), (False, 300), (True, 10)])
    4
    >>> solve_star2(parse_input(Path("days/day1/examples/1.txt").read_text()))
    6
    """

    dial = 50
    zero_count = 0
    right_dir = True
    for turn_left, dist in instructions:
        if turn_left != right_dir:
            dial = (100 - dial) % 100
            right_dir = not right_dir

        mod = dial + dist
        dial = mod % 100
        zero_count += mod // 100

    return zero_count


def star1(input_str: str) -> str:
    instructions = parse_input(input_str)
    result = solve_star1(instructions)
    return str(result)


def star2(input_str: str) -> str:
    instructions = parse_input(input_str)
    return str(solve_star2(instructions))
