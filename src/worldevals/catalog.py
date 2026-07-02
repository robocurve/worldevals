"""The WorldEvals catalog — the registry of physical-AI benchmark repos.

Each benchmark is its own repository (built on Inspect Robots) that registers its tasks
via entry points. WorldEvals indexes them so you can discover what exists and how
to install it. To add a benchmark, append a
[`Benchmark`][worldevals.catalog.Benchmark] entry here (PR).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Benchmark:
    """One benchmark repo in the WorldEvals collection."""

    name: str
    title: str
    description: str
    repo: str
    install: str
    task_keys: tuple[str, ...]
    tags: tuple[str, ...]
    bimanual: bool
    contributors: tuple[str, ...]
    status: str = "alpha"


_KITCHENBENCH_TASKS = (
    "kitchenbench/place_cutlery",
    "kitchenbench/stack",
    "kitchenbench/place_in_rack",
    "kitchenbench/pour_pasta",
    "kitchenbench/open_container",
    "kitchenbench/fold_cloth",
    "kitchenbench/seal_container",
    "kitchenbench/handoff",
    "kitchenbench/sort_cutlery",
    "kitchenbench/scoop_pasta",
)

CATALOG: tuple[Benchmark, ...] = (
    Benchmark(
        name="kitchenbench",
        title="KitchenBench",
        description=(
            "10 bimanual kitchen-manipulation tasks: pick-place, stacking, slotted "
            "insertion, granular pour & tool-scoop, lid open/seal, cloth folding, a "
            "two-arm handover, and a multi-instance cutlery sort."
        ),
        repo="https://github.com/robocurve/kitchenbench",
        install="pip install 'kitchenbench @ git+https://github.com/robocurve/kitchenbench'",
        task_keys=_KITCHENBENCH_TASKS,
        tags=("kitchen", "bimanual", "manipulation"),
        bimanual=True,
        contributors=("robocurve",),
        status="alpha",
    ),
)


def catalog() -> tuple[Benchmark, ...]:
    """All benchmarks in the collection."""
    return CATALOG


def get(name: str) -> Benchmark:
    """Look up a benchmark by name; raise `KeyError` if unknown."""
    for benchmark in CATALOG:
        if benchmark.name == name:
            return benchmark
    raise KeyError(f"no benchmark named {name!r}; known: {sorted(b.name for b in CATALOG)}")


def by_tag(tag: str) -> list[Benchmark]:
    """All benchmarks carrying ``tag``."""
    return [b for b in CATALOG if tag in b.tags]


def benchmark_for_task(task_key: str) -> Benchmark | None:
    """The benchmark that registers ``task_key``, or ``None`` if not in the catalog."""
    for benchmark in CATALOG:
        if task_key in benchmark.task_keys:
            return benchmark
    return None
