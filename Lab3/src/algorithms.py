"""BFS and DFS implementations with full instrumentation."""

import sys
import time
from collections import deque


def bfs(graph: dict, start) -> dict:
    """
    Breadth-First Search.

    Returns dict with:
      order         – nodes in visit order
      time_ms       – elapsed milliseconds
      max_queue     – peak BFS queue size
      nodes_visited – total nodes visited
    """
    visited = {start}
    queue   = deque([start])
    order   = []
    max_queue = 1

    t0 = time.perf_counter()
    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
                if len(queue) > max_queue:
                    max_queue = len(queue)
    elapsed_ms = (time.perf_counter() - t0) * 1_000

    return {
        "order":         order,
        "time_ms":       elapsed_ms,
        "max_queue":     max_queue,
        "nodes_visited": len(order),
    }


def dfs_iterative(graph: dict, start) -> dict:
    """
    Depth-First Search – explicit stack (avoids recursion-limit issues).

    Returns dict with:
      order         – nodes in visit order
      time_ms       – elapsed milliseconds
      max_stack     – peak DFS stack size
      nodes_visited – total nodes visited
    """
    visited   = set()
    stack     = [start]
    order     = []
    max_stack = 1

    t0 = time.perf_counter()
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # push neighbours in reverse-sorted order so lower-indexed nodes
        # are popped first — matches the recursive traversal order
        for nbr in sorted(graph.get(node, []), reverse=True):
            if nbr not in visited:
                stack.append(nbr)
                if len(stack) > max_stack:
                    max_stack = len(stack)
    elapsed_ms = (time.perf_counter() - t0) * 1_000

    return {
        "order":         order,
        "time_ms":       elapsed_ms,
        "max_stack":     max_stack,
        "nodes_visited": len(order),
    }


def dfs_recursive(graph: dict, start) -> dict:
    """
    Depth-First Search – recursive.

    Returns dict with:
      order         – nodes in visit order
      time_ms       – elapsed milliseconds
      max_depth     – maximum recursion depth reached
      nodes_visited – total nodes visited
    """
    visited   = set()
    order     = []
    max_depth = [0]

    def _dfs(node: int, depth: int) -> None:
        visited.add(node)
        order.append(node)
        if depth > max_depth[0]:
            max_depth[0] = depth
        for nbr in sorted(graph.get(node, [])):
            if nbr not in visited:
                _dfs(nbr, depth + 1)

    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old_limit, 20_000))

    t0 = time.perf_counter()
    _dfs(start, 0)
    elapsed_ms = (time.perf_counter() - t0) * 1_000

    sys.setrecursionlimit(old_limit)

    return {
        "order":         order,
        "time_ms":       elapsed_ms,
        "max_depth":     max_depth[0],
        "nodes_visited": len(order),
    }
