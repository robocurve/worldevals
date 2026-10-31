# Add a benchmark

WorldEvals indexes benchmark repos; it doesn't host them. A benchmark is any
repository that:

1. **depends on [Inspect Robots](https://github.com/robocurve/inspect-robots)**,
2. **defines one or more Inspect Robots `Task`s**, and
3. **registers them via entry points**: `[project.entry-points."inspect_robots.tasks"]`
   (and, if it ships a simulator/embodiment or policy,
   `inspect_robots.embodiments` / `inspect_robots.policies`).

See [StationeryBench](https://github.com/robocurve/stationerybench) as the reference
implementation.

## List it in the catalog

Add a `Benchmark(...)` entry to
[`src/worldevals/catalog.py`](https://github.com/robocurve/worldevals/blob/main/src/worldevals/catalog.py)
and open a PR:

```python
Benchmark(
    name="stationerybench",
    title="StationeryBench",
    description="5 bimanual desk-stationery tasks, one fixed setup each: ...",
    repo="https://github.com/robocurve/stationerybench",
    install='pip install "stationerybench @ git+https://github.com/robocurve/stationerybench"',  # PyPI name once published
    task_keys=("stationerybench/uncap_marker", ...),  # the Inspect Robots task keys it registers
    tags=("stationery", "bimanual", "manipulation"),
    bimanual=True,
    contributors=("your-handle",),
    status="alpha",
)
```

The homepage card grid is generated from this catalog at build time, so adding
an entry updates the site automatically. A test validates every entry (unique
name, well-formed `https://github.com/...` repo URL, ≥1 task key), and CI requires
100% coverage. Keep `task_keys` in sync with the benchmark's actual registered
task names.

Every public module, class, and function needs a docstring, enforced by `ruff` D1;
state the contract, don't restate the name.

See the [API reference](api.md) for the `Benchmark` fields.
