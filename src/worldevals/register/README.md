# Registration contract

WorldEvals catalogs physical-AI benchmarks. Each benchmark is registered as a
directory under `src/worldevals/register/<name>/` containing two files:

- `benchmark.yaml` (hand-authored): the benchmark's metadata and source pin.
- `task_keys.yaml` (CI-generated): the Inspect Robots task keys extracted from
  the pinned commit. Never edit this file by hand.


## benchmark.yaml schema

```yaml
name: kitchenbench
title: KitchenBench
description: >
  Short description of what the benchmark evaluates.
tags: [kitchen, bimanual, manipulation]
bimanual: true
contributors: [robocurve]
status: alpha
source:
  repository_url: https://github.com/robocurve/kitchenbench
  repository_commit: "814e63c7b46b383de89af0a38e0a6499a6467bee"
  tag: v0.3.0
```

**name:** must be unique across the catalog and match the directory name.

**source.repository_url:** a public `https://github.com/...` URL.

**source.repository_commit:** the full 40-character SHA of the pinned commit.

**source.tag:** the git tag corresponding to the pinned commit.


## How to add a benchmark

1. Create `src/worldevals/register/<name>/benchmark.yaml` with your benchmark's
   metadata and source pin (SHA + tag).
2. Generate the task keys by running `uv run python scripts/gen_task_keys.py`.
   This reads your pinned commit's `pyproject.toml` and writes
   `src/worldevals/register/<name>/task_keys.yaml`. Commit both files.
3. Open a pull request.

See "Keeping the pin current" below for how the pin is updated after a new
release.


## Keeping the pin current

A catalogued pin does not update itself. When a benchmark publishes a new
release, a WorldEvals maintainer bumps the pin by running the `Reconcile`
workflow (Actions tab, "Run workflow"). You do not need to add any workflow
trigger to your benchmark repo.

The workflow reads each benchmark's public release tags (via `git ls-remote`),
and for any benchmark whose latest release tag differs from the committed pin,
it regenerates `task_keys.yaml` at the new commit and opens a bump PR. Leave
the optional `benchmark` input blank to check every catalogue entry, or set it
to bump a single benchmark. A maintainer reviews and merges the PR.

To signal that your benchmark has a new release worth pinning, open an issue on
WorldEvals or ping a maintainer; there is no automatic push from your repo.


## Static pyproject.toml requirement

A catalogued benchmark MUST declare its Inspect Robots tasks statically under
`[project.entry-points."inspect_robots.tasks"]` in a root-level
`pyproject.toml`. The task-key extractor reads this table directly from the
pinned commit (without installing the package).

### Known limitations

Three layouts are not supported:

1. **Dynamic or build-generated entry points.** If entry points are produced by
   a build backend plugin or code generation step, the extractor cannot see
   them.
2. **Non-standard table keys.** Only
   `[project.entry-points."inspect_robots.tasks"]` is recognized. Older
   alternatives (such as `roboinspect.tasks`) are ignored.
3. **Non-root pyproject.toml.** Monorepo layouts where the package lives in a
   subdirectory are not supported. The extractor looks only at
   `pyproject.toml` in the repository root.

The extractor fails loudly when the expected table is missing. A
non-conforming benchmark cannot be silently catalogued as taskless; CI will
surface the error.
