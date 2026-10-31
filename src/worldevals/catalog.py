"""The WorldEvals catalog — the registry of physical-AI benchmark repos.

Each benchmark is its own repository (built on Inspect Robots) that registers its tasks
via entry points. WorldEvals indexes them so you can discover what exists and how
to install it. To add a benchmark, append a
[`Benchmark`][worldevals.catalog.Benchmark] entry here (PR).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


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
    status: Literal["alpha", "beta", "stable"] = "alpha"


CATALOG: tuple[Benchmark, ...] = (
    Benchmark(
        name="stationerybench",
        title="StationeryBench",
        description=(
            "5 bimanual desk-stationery tasks, one fixed setup each: uncap a marker, "
            "open a box, take out an eraser, and close the lid, pull the middle pad from "
            "a sticky-note stack, pour paper clips into a lifted bowl, and hand a ruler "
            "between arms cup to cup."
        ),
        repo="https://github.com/robocurve/stationerybench",
        install='pip install "stationerybench @ git+https://github.com/robocurve/stationerybench"',
        task_keys=(
            "stationerybench/uncap_marker",
            "stationerybench/eraser_from_box",
            "stationerybench/middle_sticky_pad",
            "stationerybench/pour_paperclips",
            "stationerybench/ruler_handover",
        ),
        tags=("stationery", "bimanual", "manipulation"),
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
