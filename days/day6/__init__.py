from __future__ import annotations
from dataclasses import dataclass
from itertools import groupby
import math
from pathlib import Path


@dataclass(eq=True, frozen=True, slots=True)
class Problem:
    values: tuple[str, ...]
    operator: str

    def solve(self) -> int:
        if self.operator == "+":
            return sum(int(v) for v in self.values)

        return math.prod(int(v) for v in self.values)


def parse_input(input_str: str) -> list[Problem]:
    """
    >>> parse_input(Path("days/day6/examples/1.txt").read_text())
    [Problem(values=('123', '45', '6'), operator='*'), Problem(values=('328', '64', '98'), operator='+'), Problem(values=('51', '387', '215'), operator='*'), Problem(values=('64', '23', '314'), operator='+')]
    """

    *rows, operators = input_str.splitlines()

    operators = operators.replace(" ", "")
    value_sets = list(zip(*(row.split() for row in rows)))

    return [
        Problem(values=values, operator=operators[i])
        for i, values in enumerate(value_sets)
    ]


def parse_input2(input_str: str) -> list[Problem]:
    """
    >>> parse_input2(Path("days/day6/examples/1.txt").read_text())
    [Problem(values=('1', '24', '356'), operator='*'), Problem(values=('369', '248', '8'), operator='+'), Problem(values=('32', '581', '175'), operator='*'), Problem(values=('623', '431', '4'), operator='+')]
    """
    *rows, operators = input_str.splitlines()
    operators = operators.replace(" ", "")
    value_sets = [
        list(group)
        for key, group in groupby(
            ("".join(e).strip() for e in zip(*rows)), lambda e: e == ""
        )
        if not key
    ]
    return [
        Problem(values=tuple(values), operator=operators[i])
        for i, values in enumerate(value_sets)
    ]


def grand_total(problems: list[Problem]) -> int:
    """
    >>> grand_total(parse_input(Path("days/day6/examples/1.txt").read_text()))
    4277556
    >>> grand_total(parse_input2(Path("days/day6/examples/1.txt").read_text()))
    3263827
    >>> grand_total(parse_input(Path("days/day6/input.txt").read_text()))
    7326876294741
    >>> grand_total(parse_input2(Path("days/day6/input.txt").read_text()))
    10756006415204
    """
    return sum(problem.solve() for problem in problems)


def star1(input_str: str) -> str:
    problems = parse_input(input_str)
    return str(grand_total(problems))


def star2(input_str: str) -> str:
    problems = parse_input(input_str)
    return str(grand_total(problems))
