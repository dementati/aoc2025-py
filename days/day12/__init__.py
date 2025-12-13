from __future__ import annotations
from dataclasses import dataclass
from functools import cache
import math
from pathlib import Path

from icecream import ic
import numpy as np
from numpy.typing import NDArray

from demapples.vec import Vec2


@dataclass(eq=True, frozen=True, order=True)
class Tile:
    data: bytes

    def __post_init__(self):
        assert self.as_array() is not None

    def as_array(self) -> NDArray[np.int8]:
        return np.frombuffer(self.data, dtype=np.int8).reshape(3, 3)

    def rot90(self) -> Tile:
        """
        >>> tile = Tile.from_str("0:\\n#..\\n...\\n...")
        >>> tile.rot90().as_array()
        array([[0, 0, 0],
               [0, 0, 0],
               [1, 0, 0]], dtype=int8)
        """
        arr = self.as_array()
        rotated = np.rot90(arr)
        return Tile(rotated.tobytes())

    def fliplr(self) -> Tile:
        """
        >>> tile = Tile.from_str("0:\\n#..\\n...\\n...")
        >>> tile.fliplr().as_array()
        array([[0, 0, 1],
               [0, 0, 0],
               [0, 0, 0]], dtype=int8)
        """
        arr = self.as_array()
        flipped = np.fliplr(arr)
        return Tile(flipped.tobytes())

    @cache
    def orientations(self) -> list[Tile]:
        """
        >>> tile = Tile.from_str("0:\\n#..\\n...\\n...")
        >>> len(tile.orientations())
        4
        >>> tile = Tile.from_str("0:\\n##.\\n...\\n...")
        >>> len(tile.orientations())
        8
        """
        result = set()
        current = self
        for _ in range(4):
            result.add(current)
            result.add(current.fliplr())
            current = current.rot90()

        return sorted(result)

    @cache
    def mask(self, offset: Vec2, W: int) -> int:
        array = self.as_array()

        result = 0
        for y in range(3):
            for x in range(3):
                if array[y, x]:
                    result = on(
                        result,
                        W,
                        Vec2(x, y) + offset,
                    )

        return result

    def size(self) -> int:
        arr = self.as_array()
        return np.sum(arr).item()

    @cache
    def compute_masks(self, dim: Vec2) -> set[int]:
        result = set()
        for orientation in self.orientations():
            for y in range(dim.y - 2):
                for x in range(dim.x - 2):
                    offset = Vec2(x, y)
                    result.add(orientation.mask(offset, dim.x))

        return result

    def __len__(self) -> int:
        return len(self.orientations())

    @classmethod
    def from_str(cls, tile_str: str) -> Tile:
        """
        >>> Tile.from_str("Tile 0:\\n#..\\n...\\n...").as_array()
        array([[1, 0, 0],
               [0, 0, 0],
               [0, 0, 0]], dtype=int8)
        """
        lines = tile_str.splitlines()[1:]
        data = np.array(
            [[1 if c == "#" else 0 for c in line] for line in lines], dtype=np.int8
        )

        return cls(data.tobytes())


@dataclass
class Spec:
    dim: Vec2
    counts: list[int]

    @classmethod
    def from_str(cls, problem_str: str) -> Spec:
        """
        >>> Spec.from_str("4x4: 0 0 0 0 2 0")
        Spec(dim=Vec2(x=4, y=4), counts=[0, 0, 0, 0, 2, 0])
        """
        dim_str, counts_str = problem_str.split(":")
        x_str, y_str = dim_str.split("x")
        dim = Vec2(int(x_str), int(y_str))
        counts = [int(c) for c in counts_str.strip().split()]
        return cls(dim, counts)


def idx(pos: Vec2, W: int) -> int:
    return pos.y * W + pos.x


def coord(idx: int, W: int) -> Vec2:
    y, x = divmod(idx, W)
    return Vec2(x, y)


def on(board: int, W: int, pos: Vec2) -> int:
    mask = 1 << idx(pos, W)
    return board | mask


def board_to_str(board: int, dim: Vec2) -> str:
    rows = []
    for y in range(dim.y):
        row = []
        for x in range(dim.x):
            pos = Vec2(x, y)
            mask = 1 << idx(pos, dim.x)
            row.append("#" if (board & mask) != 0 else ".")
        rows.append("".join(row))
    return "\n".join(rows)


def parse_input(input_str: str) -> tuple[list[Tile], list[Spec]]:
    """
    >>> tiles, specs = parse_input(Path("days/day12/examples/1.txt").read_text())
    >>> len(tiles)
    6
    >>> len(specs)
    3
    """
    *tiles, specs = input_str.split("\n\n")
    tiles = [Tile.from_str(tile) for tile in tiles]
    specs = [Spec.from_str(spec) for spec in specs.splitlines()]
    return tiles, specs


def write_solutions(solutions: dict[int, bool]) -> None:
    with open("days/day12/solutions.txt", "w") as f:
        for key in sorted(solutions.keys()):
            f.write(f"{key}: {solutions[key]}\n")


def load_solutions() -> dict[int, bool]:
    result = {}

    if not Path("days/day12/solutions.txt").exists():
        return result

    with open("days/day12/solutions.txt", "r") as f:
        for line in f:
            key_str, value_str = line.strip().split(":")
            key = int(key_str)
            value = value_str.strip() == "True"
            result[key] = value
    return result


TICK_LIMIT = 1000


def feasible(
    tiles: list[Tile], spec: Spec, spec_index: int, solutions: dict[int, bool]
) -> bool:
    if spec_index in solutions:
        return solutions[spec_index]

    order = sorted(
        range(len(tiles)),
        key=lambda i: (len(tiles[i].compute_masks(spec.dim)), -tiles[i].size()),
    )
    tiles = [tiles[i] for i in order]
    counts = [spec.counts[i] for i in order]
    total_tile_area = sum(tiles[i].size() * counts[i] for i in range(len(tiles)))
    board_area = spec.dim.x * spec.dim.y

    if total_tile_area > board_area:
        solutions[spec_index] = False
        return False

    def select_tile_idx(
        board: int, remaining: tuple[int, ...]
    ) -> tuple[int, list[int]] | None:
        types_available = [i for i, c in enumerate(remaining) if c > 0]

        min_option_count = None
        selected_idx = None
        selected_options = []
        for tile_idx in types_available:
            tile = tiles[tile_idx]
            options = [
                mask for mask in tile.compute_masks(spec.dim) if (board & mask) == 0
            ]

            if remaining[tile_idx] > len(options):
                return None

            if remaining[tile_idx] == len(options):
                return tile_idx, options

            if min_option_count is None or len(options) < min_option_count:
                min_option_count = len(options)
                selected_idx = tile_idx
                selected_options = options

        assert selected_idx is not None
        return selected_idx, selected_options

    @cache
    def dfs(board: int, remaining: tuple[int, ...]) -> bool:
        if sum(remaining) == 0:
            solutions[spec_index] = True
            return True

        selection = select_tile_idx(board, remaining)

        if selection is None:
            return False

        tile_idx, options = selection

        remaining = tuple(
            c - (1 if i == tile_idx else 0) for i, c in enumerate(remaining)
        )

        if any(dfs(board | mask, remaining) for mask in options):
            return True

        return False

    dfs.cache_clear()
    result = dfs(0, tuple(counts))
    return result


def count_feasible(input_str: str) -> str:
    """
    >>> count_feasible(Path("days/day12/examples/1.txt").read_text())
    '2'
    """
    tiles, specs = parse_input(input_str)

    solutions = load_solutions()

    result = 0
    for i, spec in enumerate(specs):
        if i in solutions:
            result += solutions[i]
            continue

        result += feasible(tiles, spec, i, solutions)

    write_solutions(solutions)

    return str(result)


def star1(input_str: str) -> str:
    def feasible(line: str) -> bool:
        dim_str, counts_str = line.split(":")
        return sum(int(c) * 9 for c in counts_str.strip().split()) <= math.prod(
            map(int, dim_str.split("x"))
        )

    return str(sum(feasible(spec) for spec in input_str.split("\n\n")[-1].splitlines()))
