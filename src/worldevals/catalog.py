"""The WorldEvals catalog, loaded from per-benchmark YAML in ``register/``.

Each benchmark is its own repository (built on Inspect Robots). Metadata lives
in ``src/worldevals/register/<name>/benchmark.yaml`` (hand-authored) with
generated task keys in a sibling ``task_keys.yaml``. ``CATALOG`` is assembled
from those files at import and is the single in-process source of truth for the
accessors below.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

_REGISTER_DIR = Path(__file__).resolve().parent / "register"


@dataclass(frozen=True)
class Source:
    """The pinned upstream source of a benchmark."""

    repository_url: str
    repository_commit: str
    tag: str


@dataclass(frozen=True)
class Benchmark:
    """One benchmark repo in the WorldEvals collection."""

    name: str
    title: str
    description: str
    source: Source
    task_keys: tuple[str, ...]
    tags: tuple[str, ...]
    bimanual: bool
    contributors: tuple[str, ...]
    status: Literal["alpha", "beta", "stable"] = "alpha"

    @property
    def repo(self) -> str:
        """The benchmark's repository URL (from its pinned source)."""
        return self.source.repository_url

    @property
    def install(self) -> str:
        """Derived install command: PyPI name if published, else the pinned git URL."""
        # Unpublished benchmarks install from their tagged git source; the two-step
        # inspect-robots prerequisite is documented separately (see README).
        return f'pip install "{self.name} @ git+{self.source.repository_url}@{self.source.tag}"'


def _load_benchmark(directory: Path) -> Benchmark:
    meta = yaml.safe_load((directory / "benchmark.yaml").read_text())
    keys = yaml.safe_load((directory / "task_keys.yaml").read_text())
    src = meta["source"]
    return Benchmark(
        name=meta["name"],
        title=meta["title"],
        description=meta["description"].strip(),
        source=Source(
            repository_url=src["repository_url"],
            repository_commit=src["repository_commit"],
            tag=src["tag"],
        ),
        task_keys=tuple(keys["task_keys"]),
        tags=tuple(meta["tags"]),
        bimanual=bool(meta["bimanual"]),
        contributors=tuple(meta["contributors"]),
        status=meta.get("status", "alpha"),
    )


def _load_catalog() -> tuple[Benchmark, ...]:
    dirs = sorted(p.parent for p in _REGISTER_DIR.glob("*/benchmark.yaml"))
    return tuple(_load_benchmark(d) for d in dirs)


CATALOG: tuple[Benchmark, ...] = _load_catalog()


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
