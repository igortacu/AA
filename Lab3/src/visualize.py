"""Generate all benchmark charts and save them to Lab3/charts/."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

PALETTE = {
    "bfs":     "#2196F3",   # blue
    "dfs":     "#F44336",   # red
    "dfs_rec": "#FF9800",   # orange
}

TYPE_LABELS = {
    "sparse": "Sparse Random Graph  (avg degree ≈ 2)",
    "dense":  "Dense Random Graph  (p = 0.30)",
    "tree":   "Complete Binary Tree",
    "chain":  "Chain Graph  (worst-case depth)",
    "grid":   "Grid Graph",
}


def _save(fig, filename: str) -> None:
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {filename}")


def plot_time_by_type(results: dict) -> None:
    """One chart per graph type: BFS vs DFS-iter vs DFS-rec execution time."""
    for gtype, data in results.items():
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(data["sizes"], data["bfs_time"],
                "-o", color=PALETTE["bfs"],     label="BFS",         linewidth=2, markersize=5)
        ax.plot(data["sizes"], data["dfs_time"],
                "-s", color=PALETTE["dfs"],     label="DFS (iter)",  linewidth=2, markersize=5)
        ax.plot(data["sizes"], data["dfs_rec_time"],
                "--^", color=PALETTE["dfs_rec"], label="DFS (rec)",   linewidth=2, markersize=5)
        ax.set_title(f"Execution Time — {TYPE_LABELS[gtype]}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Number of nodes  (n)", fontsize=11)
        ax.set_ylabel("Average time (ms)", fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        fig.tight_layout()
        _save(fig, f"time_{gtype}.png")


def plot_memory_comparison(results: dict) -> None:
    """BFS queue vs DFS stack peak sizes for each graph type."""
    for gtype, data in results.items():
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(data["sizes"], data["bfs_mem"],
                "-o", color=PALETTE["bfs"], label="BFS  (max queue)", linewidth=2, markersize=5)
        ax.plot(data["sizes"], data["dfs_mem"],
                "-s", color=PALETTE["dfs"], label="DFS  (max stack)", linewidth=2, markersize=5)
        ax.set_title(f"Peak Memory Usage — {TYPE_LABELS[gtype]}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Number of nodes  (n)", fontsize=11)
        ax.set_ylabel("Peak structure size (nodes)", fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        fig.tight_layout()
        _save(fig, f"memory_{gtype}.png")


def plot_all_types_comparison(results: dict) -> None:
    """Side-by-side BFS and DFS timing across all graph types."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    order = ["sparse", "dense", "tree", "chain", "grid"]

    for algo_key, title, ax in [
        ("bfs_time",  "BFS — All Graph Types",        axes[0]),
        ("dfs_time",  "DFS (iter) — All Graph Types", axes[1]),
    ]:
        for gtype in order:
            if gtype not in results:
                continue
            data = results[gtype]
            ax.plot(data["sizes"], data[algo_key],
                    "-o", label=TYPE_LABELS[gtype].split("  ")[0],
                    linewidth=1.8, markersize=4)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Number of nodes  (n)", fontsize=10)
        ax.set_ylabel("Average time (ms)", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.tight_layout()
    _save(fig, "all_types_comparison.png")


def plot_memory_all_types(results: dict) -> None:
    """Side-by-side BFS and DFS memory across all graph types."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    order = ["sparse", "dense", "tree", "chain", "grid"]

    for mem_key, title, ax in [
        ("bfs_mem", "BFS Max Queue — All Graph Types",  axes[0]),
        ("dfs_mem", "DFS Max Stack — All Graph Types",  axes[1]),
    ]:
        for gtype in order:
            if gtype not in results:
                continue
            data = results[gtype]
            ax.plot(data["sizes"], data[mem_key],
                    "-o", label=TYPE_LABELS[gtype].split("  ")[0],
                    linewidth=1.8, markersize=4)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Number of nodes  (n)", fontsize=10)
        ax.set_ylabel("Peak structure size (nodes)", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    fig.tight_layout()
    _save(fig, "memory_all_types.png")
