from __future__ import annotations
from math import prod
from pathlib import Path

from demapples.vec import Vec3


def parse_input(input_str: str) -> list[Vec3]:
    """
    >>> parse_input("1,2,3\\n4,5,6\\n7,8,9")
    [Vec3(x=1, y=2, z=3), Vec3(x=4, y=5, z=6), Vec3(x=7, y=8, z=9)]
    """
    return [
        Vec3(x=int(x_str), y=int(y_str), z=int(z_str))
        for x_str, y_str, z_str in (line.split(",") for line in input_str.splitlines())
    ]


def shortest_pairs(nodes: list[Vec3]) -> list[tuple[Vec3, Vec3]]:
    """
    >>> shortest_pairs(parse_input(Path("days/day8/examples/1.txt").read_text()))[:4]
    [(Vec3(x=162, y=817, z=812), Vec3(x=425, y=690, z=689)), (Vec3(x=162, y=817, z=812), Vec3(x=431, y=825, z=988)), (Vec3(x=906, y=360, z=560), Vec3(x=805, y=96, z=715)), (Vec3(x=431, y=825, z=988), Vec3(x=425, y=690, z=689))]
    """
    pairs: list[tuple[Vec3, Vec3, float]] = []
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            if i >= j:
                continue
            distance = a.euclidean_distance(b)
            pairs.append((a, b, distance))
    pairs.sort(key=lambda item: item[2])
    return [(a, b) for a, b, _ in pairs]


def connect(nodes: list[Vec3], n: int | None = None) -> tuple[int, int | None]:
    """
    >>> connect(parse_input(Path("days/day8/examples/1.txt").read_text()), 10)
    (40, None)
    >>> connect(parse_input(Path("days/day8/examples/1.txt").read_text()))
    (20, 25272)
    """

    sorted_pairs = shortest_pairs(nodes)

    circuits: dict[Vec3, frozenset[Vec3]] = {v: frozenset({v}) for v in nodes}

    p2_result = None
    for a, b in sorted_pairs[:n]:
        if circuits[a] is circuits[b]:
            continue

        new_set = circuits[a] | circuits[b]

        if len(new_set) == len(nodes):
            p2_result = a.x * b.x

        for x in new_set:
            circuits[x] = new_set

    p1_result = prod(sorted([len(s) for s in set(circuits.values())])[-3:])

    return p1_result, p2_result


def star1(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(connect(inp, 1000)[0])


def star2(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(connect(inp)[1])
