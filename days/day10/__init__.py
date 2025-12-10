from pathlib import Path
from typing import cast
from demapples.path import find_path
from icecream import ic
import numpy as np
from scipy.optimize import linprog


Indicator = tuple[bool, ...]
Button = tuple[int, ...]
Req = tuple[int, ...]


def parse_input(input_str: str) -> list[tuple[Indicator, tuple[Button, ...], Req]]:
    def parse_line(line: str) -> tuple[Indicator, tuple[Button, ...], Req]:
        target, *buttons, reqs = line.split()
        target = tuple(c == "#" for c in target[1:-1])
        buttons_list = [
            tuple(int(wiring) for wiring in button[1:-1].split(","))
            for button in buttons
        ]
        reqs = tuple(int(r) for r in reqs[1:-1].split(","))
        return target, tuple(buttons_list), reqs

    return [parse_line(line) for line in input_str.splitlines()]


def get_indicator_neighbours(
    ind: Indicator, buttons: tuple[Button, ...]
) -> tuple[Indicator, ...]:
    """
    >>> get_indicator_neighbours((False, True, False), ((0,2), (1,)))
    ((True, True, True), (False, False, False))
    """
    result = []
    for button in buttons:
        new_ind = tuple(not x if i in button else x for i, x in enumerate(ind))
        result.append(new_ind)

    return tuple(result)


def indicator_fewest(indicator: Indicator, buttons: tuple[Button, ...]) -> int:
    """
    >>> indicator, buttons, _ = parse_input("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")[0]
    >>> indicator_fewest(indicator, buttons)
    2
    """

    start = indicator
    end = tuple(False for _ in indicator)
    dist = lambda a, b: 1

    def heuristic(ind: Indicator) -> int:
        return 0

    result = find_path(
        start, end, dist, lambda ind: get_indicator_neighbours(ind, buttons), heuristic
    )

    if not result:
        raise AssertionError("no solution")

    steps, _ = result
    return cast(int, steps)


def indicator_fewest_total(
    inputs: list[tuple[Indicator, tuple[Button, ...], Req]],
) -> int:
    """
    >>> indicator_fewest_total(parse_input(Path("days/day10/examples/1.txt").read_text()))
    7
    """

    total = 0
    for indicator, buttons, _ in inputs:
        total += indicator_fewest(indicator, buttons)

    return total


def reqs_fewest(reqs: Req, buttons: tuple[Button, ...]) -> int | None:
    """
    >>> _, buttons, reqs = parse_input("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}")[0]
    >>> reqs_fewest(reqs, buttons)
    10
    """

    n = len(reqs)
    m = len(buttons)

    c = np.ones(m, dtype=float)

    A_eq = np.zeros((n, m), dtype=float)
    for j, button in enumerate(buttons):
        for i in button:
            A_eq[i, j] = 1.0

    res = linprog(
        c,
        A_eq=A_eq,
        b_eq=np.array(reqs, dtype=float),
        bounds=[(0, None)] * m,
        integrality=np.ones(m, dtype=int),
        method="highs",
    )

    presses = [int(round(x)) for x in res.x]
    total_presses = sum(presses)
    return total_presses


def total_reqs_fewest(inputs: list[tuple[Indicator, tuple[Button, ...], Req]]) -> int:
    """
    >>> total_reqs_fewest(parse_input(Path("days/day10/examples/1.txt").read_text()))
    33
    """

    total = 0
    for _, buttons, reqs in inputs:
        result = reqs_fewest(reqs, tuple(buttons))
        assert result is not None
        total += result

    return total


def star1(input_str: str) -> str:
    inputs = parse_input(input_str)
    return str(indicator_fewest_total(inputs))


def star2(input_str: str) -> str:
    inputs = parse_input(input_str)
    return str(total_reqs_fewest(inputs))
