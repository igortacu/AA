#!/usr/bin/env python3
"""
Lab 3 – Empirical Analysis of BFS and DFS
==========================================
Run this script from the Lab3/ directory to produce all benchmark charts
and GIF animations saved to Lab3/charts/.

  cd Lab3
  python main.py
"""

import os
import sys

# Allow imports from this directory
sys.path.insert(0, os.path.dirname(__file__))

from src.benchmark import run_all
from src.visualize import (
    plot_time_by_type,
    plot_memory_comparison,
    plot_all_types_comparison,
    plot_memory_all_types,
)
from src.animate import generate_all


def main() -> None:
    print("=" * 60)
    print("  Lab 3 – BFS / DFS Empirical Analysis")
    print("=" * 60)

    print("\n[1/3] Running benchmarks…")
    results = run_all()

    print("\n[2/3] Generating charts…")
    plot_time_by_type(results)
    plot_memory_comparison(results)
    plot_all_types_comparison(results)
    plot_memory_all_types(results)

    print("\n[3/3] Generating animations…")
    generate_all()

    print("\nDone!  All outputs saved to Lab3/charts/")


if __name__ == "__main__":
    main()
