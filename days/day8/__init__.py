from __future__ import annotations
from itertools import combinations
from math import prod
from pathlib import Path

from demapples.dsu import DisjointSetUnion
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


def shortest_pairs(nodes: list[Vec3]) -> list[tuple[int, int]]:
    """
    >>> shortest_pairs(parse_input(Path("days/day8/examples/1.txt").read_text()))[:4]
    [(0, 19), (0, 7), (2, 13), (7, 19)]
    """
    pairs: list[tuple[int, int, float]] = [
        (i, j, nodes[i].squared_distance(nodes[j]))
        for i, j in combinations(range(len(nodes)), 2)
    ]
    pairs.sort(key=lambda item: item[2])
    return [(a, b) for a, b, _ in pairs]


def connect(nodes: list[Vec3], n: int | None = None) -> tuple[int, int | None]:
    """
    >>> connect(parse_input(Path("days/day8/examples/1.txt").read_text()), 10)
    (40, None)
    >>> connect(parse_input(Path("days/day8/examples/1.txt").read_text()))
    (20, 25272)
    """

    circuits = DisjointSetUnion(len(nodes))

    p2_result = None
    for a, b in shortest_pairs(nodes)[:n]:
        circuits.union(a, b)

        if circuits.get_size(a) == len(nodes):
            p2_result = nodes[a].x * nodes[b].x
            break

    roots = set(circuits.find(i) for i in range(len(nodes)))
    p1_result = prod(sorted([circuits.get_size(r) for r in set(roots)])[-3:])

    return p1_result, p2_result


def star1(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(connect(inp, 1000)[0])


def star2(input_str: str) -> str:
    inp = parse_input(input_str)
    return str(connect(inp)[1])


def just_sort(input_str: str) -> str:
    inp = parse_input(input_str)
    pairs = shortest_pairs(inp)
    return ""
