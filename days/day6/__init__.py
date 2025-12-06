from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(eq=True, frozen=True, slots=True)
class Problem:
    values: tuple[str, ...]
    operator: str

    def solve(self) -> int:
        if self.operator == "+":
            return sum(int(v) for v in self.values)
        elif self.operator == "*":
            return math.prod(int(v) for v in self.values)
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def c_values(self) -> tuple[int, ...]:
        """
        >>> Problem(values=('64 ', '23 ', '314'), operator="+").c_values()
        (4, 431, 623)
        >>> Problem(values=(' 51', '387', '215'), operator="*").c_values()
        (175, 581, 32)
        """
        result = []
        for i in range(len(self.values[0]) - 1, -1, -1):
            digits = []
            for s in self.values:
                if i < len(s):
                    digits.append(s[i])
            result.append(int("".join(str(d) for d in digits)))

        return tuple(result)

    def solve_c_values(self) -> int:
        c_vals = self.c_values()
        if self.operator == "+":
            return sum(c_vals)
        elif self.operator == "*":
            return math.prod(c_vals)
        else:
            raise ValueError(f"Unknown operator: {self.operator}")


def parse_input(input_str: str) -> list[Problem]:
    """
    >>> parse_input(read_example_str())
    [Problem(values=('123', ' 45', '  6'), operator='*'), Problem(values=('328', '64 ', '98 '), operator='+'), Problem(values=(' 51', '387', '215'), operator='*'), Problem(values=('64 ', '23 ', '314'), operator='+')]
    """

    *rows, operators = input_str.splitlines()

    operators = operators.replace(" ", "")

    max_width = []
    for line in rows:
        parts = line.split()
        for i, part in enumerate(parts):
            if len(part) > (max_width[i] if i < len(max_width) else 0):
                if i >= len(max_width):
                    max_width.append(len(part))
                else:
                    max_width[i] = len(part)

    grid = []
    for line in rows:
        row = []
        mw_i = 0
        line_i = 0
        while line_i <= len(line):
            curr = line[line_i : line_i + max_width[mw_i]]
            row.append(curr)
            line_i += max_width[mw_i] + 1  # +1 for space
            mw_i += 1

        grid.append(row)

    problems = []
    for col in range(len(grid[0])):
        values = tuple(grid[row][col] for row in range(len(grid)))
        problem = Problem(values=values, operator=operators[col])
        problems.append(problem)

    return problems


def read_example_str() -> str:
    with open("days/day6/examples/1.txt") as file:
        input_str = file.read()
    return input_str


def read_example() -> list[Problem]:
    with open("days/day6/examples/1.txt") as file:
        input_str = file.read()
    return parse_input(input_str)


def grand_total(problems: list[Problem]) -> int:
    """
    >>> grand_total(read_example())
    4277556
    """
    return sum(problem.solve() for problem in problems)


def grand_total_c_values(problems: list[Problem]) -> int:
    """
    >>> grand_total_c_values(read_example())
    3263827
    """
    return sum(problem.solve_c_values() for problem in problems)


def star1(input_str: str) -> str:
    problems = parse_input(input_str)
    return str(grand_total(problems))


def star2(input_str: str) -> str:
    problems = parse_input(input_str)
    return str(grand_total_c_values(problems))
