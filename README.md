<div align="center">

# 🌍 WorldEvals

**The [Inspect Evals](https://inspect.aisi.org.uk/evals/) for robotics.**

A curated catalog of physical-AI / VLA benchmarks built on
[Inspect Robots](https://github.com/robocurve/inspect-robots).

[![CI](https://github.com/robocurve/worldevals/actions/workflows/ci.yml/badge.svg)](https://github.com/robocurve/worldevals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/robocurve/worldevals/actions/workflows/ci.yml)
[![Built on Inspect Robots](https://img.shields.io/badge/built%20on-Inspect%20Robots-indigo)](https://github.com/robocurve/inspect-robots)

**[📖 Browse the catalog → robocurve.github.io/worldevals](https://robocurve.github.io/worldevals/)**

</div>

[Inspect Robots](https://github.com/robocurve/inspect-robots) is the *framework* (the "Inspect
AI for robotics"). **WorldEvals is the collection** — but unlike Inspect Evals'
monorepo, each benchmark here lives in **its own repository** so it owns its
release cadence, dependencies, hardware notes, and leaderboard. WorldEvals is the
lightweight index that ties them together: what benchmarks exist, what tasks each
provides, and how to install them.

- `inspect-robots list` tells you what's **installed**.
- `worldevals list` tells you what **exists** and how to get it.

## Benchmarks

| Benchmark | Tasks | Tags | Status |
|---|--:|---|---|
| [KitchenBench](https://github.com/robocurve/kitchenbench) — 10 bimanual kitchen-manipulation tasks | 10 | kitchen, bimanual, manipulation | alpha |

## Install & use

```bash
pip install "worldevals @ git+https://github.com/robocurve/worldevals"

worldevals list                 # all benchmarks
worldevals list --tag bimanual  # filter by tag
worldevals info kitchenbench    # repo, install command, task keys
worldevals tasks                # Inspect Robots tasks installed locally, by benchmark
```

Then install a benchmark and run it through Inspect Robots:

```bash
pip install "kitchenbench @ git+https://github.com/robocurve/kitchenbench"
inspect-robots run --task kitchenbench/pour_pasta --policy kitchen_scripted --embodiment kitchen
```

## Backends (run on real robots)

Benchmarks are embodiment-agnostic; **backend adapters** supply a concrete
`Policy` + `Embodiment` so a benchmark runs on real hardware or a simulator.
These are their own repos too (not catalog entries):

| Adapter | Policy · Embodiment | Stack |
|---|---|---|
| [inspect-robots-yam](https://github.com/robocurve/inspect-robots-yam) | `molmoact2` · `yam_arms` | [MolmoAct2](https://github.com/allenai/molmoact2) on [I2RT YAM](https://i2rt.com/products/yam-6-dof-arm) bimanual arms |

```bash
inspect-robots run --task kitchenbench/pour_pasta --policy molmoact2 --embodiment yam_arms
```

## Add your benchmark

A benchmark is any repo that:

1. depends on `inspect-robots`,
2. defines one or more Inspect Robots `Task`s, and
3. registers them via `[project.entry-points."inspect_robots.tasks"]` (and, if it ships
   a sim/embodiment or policy, `inspect_robots.embodiments` / `inspect_robots.policies`).

To list it here, add a `Benchmark(...)` entry to
[`src/worldevals/catalog.py`](src/worldevals/catalog.py) and open a PR. A test
validates every entry (unique name, well-formed repo URL, ≥1 task key). See
[KitchenBench](https://github.com/robocurve/kitchenbench) as the reference
implementation.

## Development

```bash
uv venv && uv pip install -e ".[dev]"     # inspect_robots resolved from the v0.2.0 tag
uv run pre-commit install
uv run pytest --cov                        # 100% coverage required
uv run ruff check . && uv run mypy
```

## Citation

If you use WorldEvals in your research, please cite it:

```bibtex
@software{worldevals,
  author  = {Robocurve},
  title   = {WorldEvals: A curated catalog of physical-AI benchmarks},
  year    = {2026},
  url     = {https://github.com/robocurve/worldevals},
  version = {0.3.0},
  license = {MIT}
}
```

## License

[MIT](LICENSE)
