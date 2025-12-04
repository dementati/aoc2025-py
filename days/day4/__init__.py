def read_example() -> list[str]:
    with open("days/day4/examples/1.txt") as file:
        return [line.strip() for line in file.readlines()]


def neighbours(x, y, max_x, max_y) -> list[tuple[int, int]]:
    """
    >>> neighbours(0, 0, 3, 3)
    [(1, 0), (0, 1), (1, 1)]
    >>> neighbours(1, 1, 3, 3)
    [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    >>> neighbours(2, 2, 3, 3)
    [(1, 1), (2, 1), (1, 2)]
    """

    n = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            mod_x = x + dx
            mod_y = y + dy
            if (
                mod_x >= 0
                and mod_x < max_x
                and mod_y >= 0
                and mod_y < max_y
                and (dx != 0 or dy != 0)
            ):
                n.append((mod_x, mod_y))

    return n


def accessible(inp: list[str]) -> tuple[int, list[tuple[int, int]]]:
    """
    >>> accessible(read_example())
    (13, [(2, 0), (3, 0), (5, 0), (6, 0), (8, 0), (0, 1), (6, 2), (0, 4), (9, 4), (0, 7), (0, 9), (2, 9), (8, 9)])
    """

    assert inp

    max_x = len(inp[0])
    max_y = len(inp)

    def has_roll(pos: tuple[int, int]) -> bool:
        x, y = pos
        return inp[y][x] == "@"

    count = 0
    to_remove = []
    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            if c == "@":
                nc = sum(has_roll(pos) for pos in neighbours(x, y, max_x, max_y))

                if nc < 4:
                    to_remove.append((x, y))
                    count += 1

    return count, to_remove


def remove(inp: list[str], to_remove: list[tuple[int, int]]) -> list[str]:
    to_remove_set = set(to_remove)
    result = []
    for y, line in enumerate(inp):
        new_line = ""
        for x, c in enumerate(line):
            if (x, y) in to_remove_set:
                new_line += "."
            else:
                new_line += c

        result.append(new_line)

    return result


def repeat(inp: list[str]) -> int:
    """
    >>> repeat(read_example())
    43
    """
    total_count, to_remove = accessible(inp)
    while to_remove:
        inp = remove(inp, to_remove)
        count, to_remove = accessible(inp)
        total_count += count

    return total_count


def star1(input_str: str) -> str:
    inp = input_str.splitlines()
    count, _ = accessible(inp)
    return str(count)


def star2(input_str: str) -> str:
    inp = input_str.splitlines()
    return str(repeat(inp))
