# WorldEvals — agent guide

WorldEvals is the **"Inspect Evals for robotics"**: a curated **catalog + CLI**
indexing physical-AI benchmarks built on
[Inspect Robots](https://github.com/robocurve/inspect-robots). Unlike Inspect Evals' monorepo,
each benchmark here is **its own repo** (e.g.
[KitchenBench](https://github.com/robocurve/kitchenbench)); WorldEvals is the
lightweight index that ties them together.

## The one big idea

- `inspect-robots list` → what Inspect Robots tasks are **installed**.
- `worldevals list` → what benchmarks **exist** and how to install them.

WorldEvals does **not** depend on or import the benchmark repos (they're separate
packages). It only keeps a static `catalog.py` of `Benchmark` entries; the
`worldevals tasks` command bridges the two by annotating *installed* Inspect Robots
tasks with the catalogued benchmark they belong to.

## Layout

```
src/worldevals/
  catalog.py   # Benchmark dataclass + CATALOG (the registry of benchmark repos) +
               # accessors: catalog(), get(name), by_tag(tag), benchmark_for_task(key)
  cli.py       # `worldevals list [--tag] | info <name> | tasks`
  __init__.py  # public API (catalog, get, by_tag, benchmark_for_task, Benchmark)
tests/         # 100% coverage; catalog-integrity + CLI tests
plans/0001-worldevals-design.md   # design doc
README.md      # collection landing page (benchmark table + contribution guide)
```

The package is small and self-documenting, so there's no separate `src/` guide.

## Working here (important gotchas)

- **Dependency on Inspect Robots is a git tag** (`[tool.uv.sources] inspect-robots = { git =
  ..., tag = "v0.3.0" }`); it's used only by the `tasks` command (to read the
  Inspect Robots registry). `tool.uv.sources` is **uv-only**: plain pip ignores it,
  and `inspect-robots` isn't on PyPI, so every pip-facing install instruction is
  **two-step** — `pip install "inspect-robots @
  git+https://github.com/robocurve/inspect-robots@v0.3.0"` first, then the
  package. Keep README, `catalog.py` install strings, `scripts/gen_catalog.py`,
  and `docs/contributing.md` in that form.
- **Conda is active in this shell** — `uv pip install -e .` lands in conda base,
  not `.venv`. Activate first: `source .venv/bin/activate && export
  VIRTUAL_ENV="$PWD/.venv"` (or use `uv run`).
- Dev loop: `uv venv && uv pip install -e ".[dev]"`, `uv run pre-commit install`,
  `uv run pytest --cov`.
- **Gates (all required, blocking PR checks):** `ruff check .`,
  `ruff format --check .`, `mypy` (strict), `pytest --cov` at **100% coverage**.

## Adding a benchmark to the catalog

Append a `Benchmark(...)` entry to `src/worldevals/catalog.py` with its name,
title, description, repo URL, install command, the Inspect Robots task keys it
registers, tags, and contributors. `tests/test_catalog_cli.py` validates every
entry (unique name, well-formed `https://github.com/...` repo URL, ≥1 task key) —
so a malformed entry fails CI. Keep `task_keys` in sync with the benchmark repo's
actual registered task names.
