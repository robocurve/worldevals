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
    Benchmark(
        name="robodojo-rc",
        title="RoboDojo-RC Tier 1",
        description=(
            "6 of RoboDojo's real-world manipulation tasks on bimanual YAM arms, with the pinned "
            "rubrics and the video judge behind Robocurve's published scores: pack and pour "
            "fruit, stack bowls, store objects in a safe, cap a pen, stand up bottles, and sort "
            "objects into baskets. Each trial scores a rubric level from 0 to 1."
        ),
        repo="https://github.com/robocurve/robodojo-rc",
        install='pip install "robodojo-rc @ git+https://github.com/robocurve/robodojo-rc"',
        task_keys=(
            "robodojo-rc/pack_and_pour_fruit",
            "robodojo-rc/stack_bowls",
            "robodojo-rc/store_in_safe",
            "robodojo-rc/cap_pen",
            "robodojo-rc/stand_up_bottles",
            "robodojo-rc/sort_objects",
        ),
        tags=("robodojo", "bimanual", "manipulation", "llm-agents"),
        bimanual=True,
        contributors=("robocurve",),
        status="alpha",
    ),
    Benchmark(
        name="roboharm",
        title="RoboHarm",
        description=(
            "5 fixed-scene tasks with harmful instructions, with the label rubric and the "
            "video-and-transcript judge behind Robocurve's published RoboHarm results: a knife "
            "next to a doll, an aerosol can and a burner, a screwdriver and a toaster, a power "
            "bank and water, and two cleaning-product containers. Each trial gets one label, such "
            "as a safety refusal or a harmful action."
        ),
        repo="https://github.com/robocurve/roboharm",
        install='pip install "roboharm @ git+https://github.com/robocurve/roboharm"',
        task_keys=(
            "roboharm/doll",
            "roboharm/burner",
            "roboharm/toaster",
            "roboharm/brick",
            "roboharm/pour",
        ),
        tags=("safety", "refusal", "bimanual", "manipulation", "llm-agents"),
        bimanual=True,
        contributors=("robocurve",),
        status="alpha",
    ),
    Benchmark(
        name="datacenterbench",
        title="DataCenterBench Tier 1",
        description=(
            "10 steps from data-center maintenance procedures as bimanual tasks, each one fixed "
            "setup on a board, with the rubrics and the two-judge photo scoring behind "
            "Robocurve's published scores: unplug and plug a charger, turn a knob, flip a "
            "switch, turn a key, open a cover, move a slider, enter a keypad code, join an "
            "Ethernet plug, and press a cable into a clip. Each trial scores 0, 0.5 or 1."
        ),
        repo="https://github.com/robocurve/datacenterbench",
        install='pip install "datacenterbench @ git+https://github.com/robocurve/datacenterbench"',
        task_keys=(
            "datacenterbench/unplug",
            "datacenterbench/knob",
            "datacenterbench/toggle",
            "datacenterbench/key",
            "datacenterbench/cover",
            "datacenterbench/slider",
            "datacenterbench/keypad",
            "datacenterbench/plug",
            "datacenterbench/join",
            "datacenterbench/clip",
        ),
        tags=("data-center", "bimanual", "manipulation", "llm-agents"),
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
