# WorldEvals — design

> **WorldEvals** is the "Inspect Evals for robotics": a curated **collection /
> index** of physical-AI benchmarks built on
> [RoboInspect](https://github.com/robocurve/roboinspect). Because each benchmark is
> its *own repo* (e.g. [KitchenBench](https://github.com/robocurve/kitchenbench)),
> WorldEvals is a lightweight **catalog + CLI**, not a monorepo — it tells you
> what benchmarks exist, what tasks each provides, and how to install them.

## Why an index (not a monorepo)

Inspect Evals is one big repo. We deliberately chose per-benchmark repos (each
benchmark owns its release cadence, deps, hardware notes, and leaderboard).
WorldEvals therefore plays the role Inspect Evals' `listing.yaml` + generated
README play, but pointing at *external* repos:

- a machine-readable **catalog** of benchmarks (name, description, repo, install
  spec, the RoboInspect task keys it registers, tags, bimanual, contributors,
  status);
- a **CLI** to browse it and to show which RoboInspect tasks are installed locally;
- a **landing-page README** with the benchmark table and a contribution guide.

It complements RoboInspect's runtime discovery: RoboInspect (`roboinspect list`) shows
what's *installed*; WorldEvals shows what *exists* and how to get it.

## Architecture

```
worldevals/
  pyproject.toml            # depends on roboinspect; console script `worldevals`
  src/worldevals/
    __init__.py             # public API (catalog, get, Benchmark)
    py.typed
    catalog.py              # Benchmark dataclass + CATALOG (the registry of repos)
    cli.py                  # worldevals list | info | tasks
  tests/                    # 100% coverage
  README.md                 # collection landing page (benchmark table + how to add)
```

### Data model

```python
@dataclass(frozen=True)
class Benchmark:
    name: str                 # "kitchenbench"
    title: str
    description: str
    repo: str                 # https://github.com/robocurve/kitchenbench
    install: str              # pip install spec (git URL until on PyPI)
    task_keys: tuple[str, ...]  # roboinspect task entry-point names it registers
    tags: tuple[str, ...]     # ("bimanual", "kitchen", "manipulation")
    bimanual: bool
    contributors: tuple[str, ...]
    status: str = "alpha"
```

`CATALOG: tuple[Benchmark, ...]` is the single source of truth. Accessors:
`catalog()`, `get(name)`, `by_tag(tag)`. KitchenBench is the first entry, listing
all 10 of its task keys.

### CLI

- `worldevals list [--tag T]` — table of benchmarks (name, title, #tasks, tags,
  status).
- `worldevals info <name>` — full detail incl. repo, install command, task keys.
- `worldevals tasks` — the RoboInspect tasks **currently installed** (via
  `roboinspect.registry.registered("task")`), annotated with which catalog
  benchmark they belong to — bridging "what exists" and "what's installed".

### How to add a benchmark (contribution guide, in README)

A benchmark is any repo that (1) depends on `roboinspect`, (2) defines `Task`s, and
(3) registers them via `[project.entry-points."roboinspect.tasks"]`. To list it in
WorldEvals, add a `Benchmark(...)` entry to `catalog.py` (PR). A test validates
every entry (non-empty fields, unique names, well-formed repo URL, ≥1 task key).

## Quality bar (same as RoboInspect / KitchenBench)

`ruff` + `ruff format` + `mypy --strict` + `pytest` at **100% coverage**;
pre-commit hooks; GitHub Actions; MIT; `py.typed`. Catalog-integrity test.

## Milestones (commit/push each)

- **M0** skeleton, packaging, CI, pre-commit, README stub.
- **M1** `Benchmark` + `catalog` (KitchenBench entry) + integrity tests.
- **M2** CLI (`list`/`info`/`tasks`) + tests → 100% coverage.
- **M3** README landing page (benchmark table + contribution guide); branch
  protection; push.
