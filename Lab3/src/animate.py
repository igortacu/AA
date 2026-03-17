"""
Step-by-step BFS and DFS animations saved as GIF files.
Also exports PNG snapshots for embedding in the LaTeX report.
"""

from __future__ import annotations

import os
from collections import deque

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# ── Demo graph (12 nodes, 4 clear levels) ────────────────────────────────────
DEMO_EDGES = [
    (0, 1), (0, 2), (0, 3),
    (1, 4), (1, 5),
    (2, 5), (2, 6),
    (3, 7),
    (4, 8),
    (5, 9),
    (6, 9), (6, 10),
    (7, 10), (7, 11),
]
DEMO_NODES = list(range(12))

# Manual hierarchical positions for a clean look
POS = {
    0:  ( 0.0,  3.0),
    1:  (-3.0,  2.0),  2: ( 0.0,  2.0),  3: ( 3.0,  2.0),
    4:  (-4.0,  1.0),  5: (-1.0,  1.0),  6: ( 2.0,  1.0),  7: ( 4.0,  1.0),
    8:  (-4.5,  0.0),  9: (-0.5,  0.0), 10: ( 2.5,  0.0), 11: ( 4.5,  0.0),
}

# Colour palette
C_UNVISITED = "#D0D7E3"   # light grey-blue
C_FRONTIER  = "#FFB347"   # orange  – in queue / stack
C_CURRENT   = "#E74C3C"   # red     – currently being processed
C_VISITED   = "#2ECC71"   # green   – fully done
C_EDGE      = "#95A5A6"   # grey    – normal edge
C_TREE_EDGE = "#2980B9"   # blue    – traversal tree edge


def _build_demo_graph() -> dict:
    graph: dict = {i: [] for i in DEMO_NODES}
    for u, v in DEMO_EDGES:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# ── Step generators ──────────────────────────────────────────────────────────

def _bfs_steps(graph: dict, start: int) -> list:
    """Return list of state dicts, one per BFS step (including initial state)."""
    states = []

    # Initial state: start node is in the queue, nothing visited yet
    states.append({
        "current":    None,
        "frontier":   {start},
        "visited":    set(),
        "tree_edges": [],
    })

    visited    = {start}
    queue      = deque([start])
    done       = set()
    tree_edges: list = []

    while queue:
        node = queue.popleft()
        done.add(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
                tree_edges.append((node, nbr))
        states.append({
            "current":    node,
            "frontier":   set(queue),
            "visited":    set(done),
            "tree_edges": list(tree_edges),
        })

    return states


def _dfs_steps(graph: dict, start: int) -> list:
    """Return list of state dicts, one per DFS step (including initial state)."""
    states = []

    # Initial state
    states.append({
        "current":    None,
        "frontier":   {start},
        "visited":    set(),
        "tree_edges": [],
    })

    visited    = set()
    stack      = [(None, start)]  # (parent, node)
    in_stack   = {start}
    done       = set()
    tree_edges: list = []

    while stack:
        parent, node = stack.pop()
        if node in done:
            in_stack.discard(node)
            continue
        done.add(node)
        in_stack.discard(node)
        if parent is not None:
            tree_edges.append((parent, node))
        for nbr in sorted(graph.get(node, []), reverse=True):
            if nbr not in done:
                stack.append((node, nbr))
                in_stack.add(nbr)
        states.append({
            "current":    node,
            "frontier":   set(in_stack) - done,
            "visited":    set(done),
            "tree_edges": list(tree_edges),
        })

    return states


# ── Frame renderer ───────────────────────────────────────────────────────────

def _render_frame(ax, state: dict, algo_name: str, step: int, total: int) -> None:
    ax.clear()
    ax.set_axis_off()
    ax.set_facecolor("#FAFAFA")

    label = "Initial state" if state["current"] is None else f"Step {step} / {total - 1}"
    ax.set_title(f"{algo_name}  —  {label}", fontsize=14, fontweight="bold", pad=10)

    current    = state["current"]
    frontier   = state["frontier"]
    visited    = state["visited"]
    tree_set   = {frozenset(e) for e in state["tree_edges"]}

    # ── Edges ────────────────────────────────────────────────────────────────
    for u, v in DEMO_EDGES:
        is_tree = frozenset((u, v)) in tree_set
        xs = [POS[u][0], POS[v][0]]
        ys = [POS[u][1], POS[v][1]]
        ax.plot(xs, ys,
                color=C_TREE_EDGE if is_tree else C_EDGE,
                linewidth=2.5 if is_tree else 1.0,
                zorder=1, solid_capstyle="round")

    # ── Nodes ────────────────────────────────────────────────────────────────
    for node in DEMO_NODES:
        x, y = POS[node]
        if node == current:
            color, size = C_CURRENT, 480
        elif node in frontier:
            color, size = C_FRONTIER, 380
        elif node in visited:
            color, size = C_VISITED,  380
        else:
            color, size = C_UNVISITED, 380
        ax.scatter(x, y, s=size, c=color, zorder=3,
                   edgecolors="white", linewidths=1.8)
        ax.text(x, y, str(node), ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=4)

    # ── Legend ───────────────────────────────────────────────────────────────
    handles = [
        mpatches.Patch(color=C_CURRENT,   label="Currently processing"),
        mpatches.Patch(color=C_FRONTIER,  label="Queue / Stack (frontier)"),
        mpatches.Patch(color=C_VISITED,   label="Visited (done)"),
        mpatches.Patch(color=C_UNVISITED, label="Not yet visited"),
    ]
    ax.legend(handles=handles, loc="lower left", fontsize=8,
              framealpha=0.9, edgecolor="#AAAAAA")

    xs_all = [p[0] for p in POS.values()]
    ys_all = [p[1] for p in POS.values()]
    ax.set_xlim(min(xs_all) - 1.0, max(xs_all) + 1.0)
    ax.set_ylim(min(ys_all) - 0.9, max(ys_all) + 0.6)


# ── GIF + snapshot writers ───────────────────────────────────────────────────

def _make_gif(steps: list, algo_name: str, filename: str) -> None:
    total = len(steps)
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor("white")

    def update(i: int) -> None:
        _render_frame(ax, steps[i], algo_name, i, total)

    anim = FuncAnimation(fig, update, frames=total, interval=1000, repeat=True)
    path = os.path.join(CHART_DIR, filename)
    anim.save(path, writer=PillowWriter(fps=1), dpi=100)
    plt.close(fig)
    print(f"  Saved {filename}  ({total} frames)")


def _save_snapshots(steps: list, algo_name: str, prefix: str,
                    indices: list) -> None:
    total  = len(steps)
    indices = [i for i in indices if i < total]
    for i in indices:
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.patch.set_facecolor("white")
        _render_frame(ax, steps[i], algo_name, i, total)
        path = os.path.join(CHART_DIR, f"{prefix}_step{i:02d}.png")
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved {prefix}_step{i:02d}.png")


def generate_all() -> None:
    graph = _build_demo_graph()

    # ── BFS ──────────────────────────────────────────────────────────────────
    print("  Generating BFS animation…")
    bfs_steps = _bfs_steps(graph, 0)
    _make_gif(bfs_steps, "Breadth-First Search (BFS)", "bfs_demo.gif")
    # pick 5 representative snapshots: initial, early, mid, late, final
    n = len(bfs_steps)
    _save_snapshots(bfs_steps, "BFS", "bfs",
                    [0, n // 4, n // 2, 3 * n // 4, n - 1])

    # ── DFS ──────────────────────────────────────────────────────────────────
    print("  Generating DFS animation…")
    dfs_steps = _dfs_steps(graph, 0)
    _make_gif(dfs_steps, "Depth-First Search (DFS)", "dfs_demo.gif")
    n = len(dfs_steps)
    _save_snapshots(dfs_steps, "DFS", "dfs",
                    [0, n // 4, n // 2, 3 * n // 4, n - 1])
