"""Run all benchmarks and return structured result tables."""

from __future__ import annotations

import statistics

from .algorithms import bfs, dfs_iterative, dfs_recursive
from .graph_gen import (
    sparse_graph, dense_graph, binary_tree, grid_graph, chain_graph
)

RUNS = 7  # repetitions per data point


def _avg_time(fn, graph, start) -> float:
    """Return mean execution time in ms over RUNS runs."""
    return statistics.mean(fn(graph, start)["time_ms"] for _ in range(RUNS))


def run_all() -> dict:
    """
    Benchmark BFS, DFS-iterative, and DFS-recursive on five graph types.

    Returns a dict keyed by graph type, each containing:
      sizes        – list of node counts
      bfs_time     – mean BFS time (ms)
      dfs_time     – mean DFS-iterative time (ms)
      dfs_rec_time – mean DFS-recursive time (ms)
      bfs_mem      – peak BFS queue size
      dfs_mem      – peak DFS stack size
    """
    sparse_sizes = [10, 50, 100, 250, 500, 1_000, 2_000, 5_000]
    dense_sizes  = [10, 50, 100, 250, 500, 1_000]
    tree_sizes   = [10, 50, 100, 250, 500, 1_000, 2_000, 5_000]
    chain_sizes  = [10, 50, 100, 250, 500, 1_000, 2_000, 5_000]
    grid_sizes   = [9, 25, 64, 100, 225, 400, 625, 900, 1_600, 2_500]

    results = {}

    configs = [
        ("sparse", sparse_sizes, lambda n: sparse_graph(n),  False),
        ("dense",  dense_sizes,  lambda n: dense_graph(n),   False),
        ("tree",   tree_sizes,   lambda n: binary_tree(n),   False),
        ("chain",  chain_sizes,  lambda n: chain_graph(n),   True),
    ]

    for name, sizes, gen, is_chain in configs:
        print(f"  Benchmarking {name} graphs…")
        r = {
            "sizes":        [],
            "bfs_time":     [], "dfs_time":     [], "dfs_rec_time": [],
            "bfs_mem":      [], "dfs_mem":      [],
        }
        for n in sizes:
            g = gen(n)
            r["sizes"].append(n)
            r["bfs_time"].append(_avg_time(bfs, g, 0))
            r["dfs_time"].append(_avg_time(dfs_iterative, g, 0))
            # skip recursive DFS for deep chains — would exceed recursion limit
            if is_chain and n > 500:
                r["dfs_rec_time"].append(_avg_time(dfs_iterative, g, 0))
            else:
                r["dfs_rec_time"].append(_avg_time(dfs_recursive, g, 0))
            r["bfs_mem"].append(bfs(g, 0)["max_queue"])
            r["dfs_mem"].append(dfs_iterative(g, 0)["max_stack"])
        results[name] = r

    # ── Grid graphs (return actual node count from grid_graph) ───────────────
    print("  Benchmarking grid graphs…")
    r = {
        "sizes":        [],
        "bfs_time":     [], "dfs_time":     [], "dfs_rec_time": [],
        "bfs_mem":      [], "dfs_mem":      [],
    }
    for n in grid_sizes:
        g, actual = grid_graph(n)
        r["sizes"].append(actual)
        r["bfs_time"].append(_avg_time(bfs, g, 0))
        r["dfs_time"].append(_avg_time(dfs_iterative, g, 0))
        r["dfs_rec_time"].append(_avg_time(dfs_recursive, g, 0))
        r["bfs_mem"].append(bfs(g, 0)["max_queue"])
        r["dfs_mem"].append(dfs_iterative(g, 0)["max_stack"])
    results["grid"] = r

    return results
