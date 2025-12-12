from __future__ import annotations
import math


def star1(input_str: str) -> str:
    def feasible(line: str) -> bool:
        dim_str, counts_str = line.split(":")
        return sum(int(c) * 9 for c in counts_str.strip().split()) <= math.prod(
            map(int, dim_str.split("x"))
        )

    return str(sum(feasible(spec) for spec in input_str.split("\n\n")[-1].splitlines()))
