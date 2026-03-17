"""Graph generators for empirical analysis."""

import math
import random


def _ensure_connected(graph: dict, n: int, rng: random.Random) -> None:
    """Connect all isolated nodes to the component containing node 0."""
    reachable = {0}
    changed = True
    while changed:
        changed = False
        for node, nbrs in graph.items():
            if node in reachable:
                for nbr in nbrs:
                    if nbr not in reachable:
                        reachable.add(nbr)
                        changed = True
    for node in range(n):
        if node not in reachable:
            target = rng.choice(list(reachable))
            graph[node].append(target)
            graph[target].append(node)
            reachable.add(node)


def sparse_graph(n: int, seed: int = 42) -> dict:
    """Undirected random sparse graph — average degree ≈ 2."""
    rng = random.Random(seed)
    p   = min(2.0 / max(n - 1, 1), 1.0)
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                graph[i].append(j)
                graph[j].append(i)
    _ensure_connected(graph, n, rng)
    return graph


def dense_graph(n: int, seed: int = 42, p: float = 0.3) -> dict:
    """Undirected random dense graph — edge probability = p."""
    rng = random.Random(seed)
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                graph[i].append(j)
                graph[j].append(i)
    _ensure_connected(graph, n, rng)
    return graph


def binary_tree(n: int) -> dict:
    """Complete binary tree with n nodes (0-indexed, node i → children 2i+1, 2i+2)."""
    graph = {i: [] for i in range(n)}
    for i in range(n):
        l, r = 2 * i + 1, 2 * i + 2
        if l < n:
            graph[i].append(l)
            graph[l].append(i)
        if r < n:
            graph[i].append(r)
            graph[r].append(i)
    return graph


def grid_graph(n: int) -> tuple:
    """
    Square grid graph closest to n nodes.
    Returns (graph, actual_n) where actual_n = floor(sqrt(n))^2.
    """
    side   = int(math.isqrt(n))
    actual = side * side
    graph  = {i: [] for i in range(actual)}
    for r in range(side):
        for c in range(side):
            node = r * side + c
            if c + 1 < side:
                nbr = r * side + c + 1
                graph[node].append(nbr)
                graph[nbr].append(node)
            if r + 1 < side:
                nbr = (r + 1) * side + c
                graph[node].append(nbr)
                graph[nbr].append(node)
    return graph, actual


def chain_graph(n: int) -> dict:
    """Linear chain: 0 — 1 — 2 — … — (n-1)."""
    graph = {i: [] for i in range(n)}
    for i in range(n - 1):
        graph[i].append(i + 1)
        graph[i + 1].append(i)
    return graph
