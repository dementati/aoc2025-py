def parse_input(input_string: str) -> list[tuple[bool, int]]:
    """Parses the input string into a list of tuples.

    >>> parse_input("L2\\nR3\\nL4")
    [(True, 2), (False, 3), (True, 4)]
    """

    return [
        (line[0] == "L", int(line[1:])) for line in input_string.strip().split("\n")
    ]


def parse_input_file(file_path: str) -> list[tuple[bool, int]]:
    """Reads the input file and parses its content."""

    with open(file_path, "r") as file:
        input_string = file.read()
    return parse_input(input_string)


def star1(input_str: str) -> str:
    instructions = parse_input(input_str)
    result = solve_star1(instructions)
    return str(result)


def star2(input_str: str) -> str:
    instructions = parse_input(input_str)
    return str(solve_star2(instructions))


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
    """

    dial = 50
    zero_count = 0
    for turn_left, dist in instructions:
        for _ in range(dist):
            dial = (dial + (-1 if turn_left else 1)) % 100
            if dial == 0:
                zero_count += 1

    return zero_count
