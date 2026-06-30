# Add a benchmark

WorldEvals indexes benchmark repos; it doesn't host them. A benchmark is any
repository that:

1. **depends on [RoboInspect](https://github.com/robocurve/roboinspect)**,
2. **defines one or more RoboInspect `Task`s**, and
3. **registers them via entry points** — `[project.entry-points."roboinspect.tasks"]`
   (and, if it ships a simulator/embodiment or policy,
   `roboinspect.embodiments` / `roboinspect.policies`).

See [KitchenBench](https://github.com/robocurve/kitchenbench) as the reference
implementation.

## List it in the catalog

Add a `Benchmark(...)` entry to
[`src/worldevals/catalog.py`](https://github.com/robocurve/worldevals/blob/main/src/worldevals/catalog.py)
and open a PR:

```python
Benchmark(
    name="kitchenbench",
    title="KitchenBench",
    description="10 bimanual kitchen-manipulation tasks: ...",
    repo="https://github.com/robocurve/kitchenbench",
    install="pip install 'kitchenbench @ git+https://github.com/robocurve/kitchenbench'",
    task_keys=("kitchenbench/place_cutlery", ...),  # the RoboInspect task keys it registers
    tags=("kitchen", "bimanual", "manipulation"),
    bimanual=True,
    contributors=("your-handle",),
    status="alpha",
)
```

The homepage card grid is **generated from this catalog at build time**, so adding
an entry updates the site automatically. A test validates every entry (unique
name, well-formed `https://github.com/...` repo URL, ≥1 task key), and CI requires
100% coverage — keep `task_keys` in sync with the benchmark's actual registered
task names.

See the [API reference](api.md) for the `Benchmark` fields.
