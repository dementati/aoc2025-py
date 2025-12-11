from __future__ import annotations
from functools import cache
from pathlib import Path


def parse_input(input_str: str) -> dict[str, tuple[str, ...]]:
    """
    >>> parse_input(Path("days/day11/examples/1.txt").read_text())
    {'aaa': ('you', 'hhh'), 'you': ('bbb', 'ccc'), 'bbb': ('ddd', 'eee'), 'ccc': ('ddd', 'eee', 'fff'), 'ddd': ('ggg',), 'eee': ('out',), 'fff': ('out',), 'ggg': ('out',), 'hhh': ('ccc', 'fff', 'iii'), 'iii': ('out',)}
    """
    result = {}
    for line in input_str.splitlines():
        key, *values = line.split()
        key = key[:-1]
        result[key] = tuple(v for v in values)
    return result


def all_paths(input_str: str) -> int:
    """
    >>> all_paths(Path("days/day11/examples/1.txt").read_text())
    5
    """

    graph = parse_input(input_str)

    def dfs(start: str, path: list[str] | None = None) -> int:
        path = path or []

        if start == "out":
            # print(path)
            return 1

        assert start in graph

        return sum(dfs(n, path + [start]) for n in graph[start])

    return dfs("you")


def all_paths_2(input_str: str) -> int:
    """
    >>> all_paths_2(Path("days/day11/examples/2.txt").read_text())
    2
    """

    graph = parse_input(input_str)

    @cache
    def dfs(start: str, found: frozenset[str]) -> int:
        if start == "out":
            return len(found) == 2

        assert start in graph, f"no start in graph: {start}"

        if start == "fft" or start == "dac":
            found = found.union({start})

        return sum(dfs(n, found) for n in graph[start])

    return dfs("svr", frozenset({}))


def star1(input_str: str) -> int:
    return all_paths(input_str)


def star2(input_str: str) -> int:
    return all_paths_2(input_str)


def render(input_str: str):
    import networkx as nx
    import matplotlib.pyplot as plt

    graph = parse_input(input_str)

    G = nx.Graph()

    # Add nodes and edges
    G.add_nodes_from(graph.keys())
    G.add_edges_from(
        [(key, neighbor) for key, neighbors in graph.items() for neighbor in neighbors]
    )

    out_nodes = [node for node in G.nodes if node == "out"]

    # Draw
    pos = nx.spring_layout(G)  # force-directed layout
    nx.draw(G, pos, with_labels=True, node_size=600)
    nx.draw_networkx_nodes(G, pos, nodelist=["you"], node_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=out_nodes, node_color="lightgreen")
    plt.show()
