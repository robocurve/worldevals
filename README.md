<div align="center">

# 🌍 WorldEvals

**A curated catalog of physical-AI / VLA benchmarks** — each one installable,
versioned, and runnable on real robots or simulators via
[Inspect Robots](https://github.com/robocurve/inspect-robots).

If you know [Inspect Evals](https://inspect.aisi.org.uk/evals/), this is that for robotics.

[![CI](https://github.com/robocurve/worldevals/actions/workflows/ci.yml/badge.svg)](https://github.com/robocurve/worldevals/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/robocurve/worldevals/actions/workflows/ci.yml)
[![Built on Inspect Robots](https://img.shields.io/badge/built%20on-Inspect%20Robots-indigo)](https://github.com/robocurve/inspect-robots)

**[📖 Browse the catalog → worldevals.org](https://worldevals.org/)**

</div>

> **⚠️ Early alpha.** Under active development. APIs, data formats, and results may change without notice.

[Inspect Robots](https://github.com/robocurve/inspect-robots) is the *framework*;
**WorldEvals is the collection**. Each benchmark lives in **its own repository**,
owning its release cadence, dependencies, hardware notes, and leaderboard —
WorldEvals is the lightweight index that ties them together: what benchmarks
exist, what tasks each provides, and how to install them. If you come from
Inspect AI, this is the Inspect Evals of that ecosystem, minus the monorepo.

- `inspect-robots list` tells you what's **installed**.
- `worldevals list` tells you what **exists** and how to get it.

## Benchmarks

| Benchmark | Tasks | Tags | Status |
|---|--:|---|---|
| [KitchenBench](https://github.com/robocurve/kitchenbench) — 10 bimanual kitchen-manipulation tasks | 10 | kitchen, bimanual, manipulation | alpha |

## Install & use

```bash
pip install worldevals   # pulls in inspect-robots

worldevals list                 # all benchmarks
worldevals list --tag bimanual  # filter by tag
worldevals info kitchenbench    # repo, install command, task keys
worldevals tasks                # Inspect Robots tasks installed locally, by benchmark
```

Then install a benchmark and run it through Inspect Robots:

```bash
pip install kitchenbench
inspect-robots run --task kitchenbench/pour_pasta --policy kitchen_scripted --embodiment kitchen
```

## Backends (run on real robots)

Benchmarks are embodiment-agnostic; **backend adapters** supply a concrete
`Policy` + `Embodiment` so a benchmark runs on real hardware or a simulator.
These are their own repos too (not catalog entries):

| Adapter | Policy · Embodiment | Stack |
|---|---|---|
| [inspect-robots-yam](https://github.com/robocurve/inspect-robots-yam) | `molmoact2` · `yam_arms` | [MolmoAct2](https://github.com/allenai/molmoact2) on [I2RT YAM](https://i2rt.com/products/yam-6-dof-arm) bimanual arms |
| [inspect-robots-so101](https://github.com/robocurve/inspect-robots-so101) | `lerobot` · `so_arm` | [LeRobot](https://github.com/huggingface/lerobot) policies (ACT, SmolVLA, π0, …) on [SO-ARM](https://github.com/TheRobotStudio/SO-ARM100) (SO-100 / SO-101) follower arms |

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

> **Dependency changes:** after editing dependencies in `pyproject.toml`, run
> `uv lock` and commit the updated lockfile — CI installs with
> `uv sync --locked` and fails with "the lockfile needs to be updated" if you
> forget. Day-to-day conventions (PR-only `main`, the required `ci-ok` check,
> one-click releases) are documented in [`CLAUDE.md`](CLAUDE.md).

```bash
uv venv && uv pip install -e ".[dev]"     # inspect_robots resolved from the v0.3.0 tag
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
