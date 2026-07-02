"""WorldEvals — the Inspect Evals for robotics.

A curated catalog of physical-AI benchmarks built on
`Inspect Robots <https://github.com/robocurve/inspect-robots>`_. Each benchmark is its own
repo (e.g. `KitchenBench <https://github.com/robocurve/kitchenbench>`_); this
package indexes them and bridges "what exists" with "what's installed".
"""

from __future__ import annotations

from worldevals.catalog import (
    CATALOG,
    Benchmark,
    benchmark_for_task,
    by_tag,
    catalog,
    get,
)

__version__ = "0.3.0"

__all__ = [
    "CATALOG",
    "Benchmark",
    "__version__",
    "benchmark_for_task",
    "by_tag",
    "catalog",
    "get",
]
