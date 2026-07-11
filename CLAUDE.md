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
  Inspect Robots registry). A PEP 508 direct reference is used in `pyproject.toml` so that
  pip installations can be performed in a single step (e.g. `pip install "worldevals @
  git+https://github.com/robocurve/worldevals"`). Keep README, `catalog.py` install strings,
  `scripts/gen_catalog.py`, and `docs/contributing.md` in sync.
- **Conda is active in this shell** — `uv pip install -e .` lands in conda base,
  not `.venv`. Activate first: `source .venv/bin/activate && export
  VIRTUAL_ENV="$PWD/.venv"` (or use `uv run`).
- Dev loop: `uv venv && uv pip install -e ".[dev]"`, `uv run pre-commit install`,
  `uv run pytest --cov`.
- **Gates (all required, blocking PR checks):** `ruff check .`,
  `ruff format --check .`, `mypy` (strict), `pytest --cov` at **100% coverage**.

## Publishing model checkpoints to HuggingFace (any agent session)

Any checkpoint published to the robocurve HF org **must** follow
[docs/model-cards.md](docs/model-cards.md): fill in
[docs/model-card-template.md](docs/model-card-template.md) top-to-bottom, then pass the
gating checklist (any unchecked REQUIRED box blocks publish). Common traps it prevents:
license inheritance from the base model (never default apache-2.0), missing action/observation
I/O contracts, and unverifiable eval claims. Reference implementations are linked in the doc.

## Adding a benchmark to the catalog

Append a `Benchmark(...)` entry to `src/worldevals/catalog.py` with its name,
title, description, repo URL, install command, the Inspect Robots task keys it
registers, tags, and contributors. `tests/test_catalog_cli.py` validates every
entry (unique name, well-formed `https://github.com/...` repo URL, ≥1 task key) —
so a malformed entry fails CI. Keep `task_keys` in sync with the benchmark repo's
actual registered task names.

## CI, merging, and releases

- **main is PR-only** — a branch ruleset (admins included) blocks direct pushes,
  force pushes, and deletion. Merging requires the `ci-ok` check green and the
  branch up to date with main.
- **`ci-ok` is the single required status check** — an aggregate job at the end
  of `ci.yml`. When adding a CI job, add it to `ci-ok`'s `needs` list, or it
  will not gate merges.
- **Red main is stop-the-line**: if CI fails on a push to main, the
  `alert-red-main` job opens an issue. Fix forward or revert before merging
  anything else; if the failure was transient, re-run the failed jobs and close
  the issue.
- **CI installs from `uv.lock`** (`uv sync --locked`). After changing
  dependencies in `pyproject.toml`, run `uv lock` and commit the lockfile —
  otherwise CI fails with "the lockfile needs to be updated".
- A weekly **canary** (`canary.yml`) does the opposite: it installs the latest
  dependency versions the pyproject ranges allow (ignoring the lockfile), runs
  the tests, and opens an issue on failure — catching ecosystem breakage that
  locked CI can't see. A green canary means `uv lock --upgrade` is safe.
- **Releases are one-click**: Actions → Release → Run workflow → pick
  patch/minor/major. The version is derived from the git tag by hatch-vcs —
  never add a static `version =` back to pyproject (`__version__` comes from importlib.metadata). The same
  run publishes to PyPI via trusted publishing; nothing is pushed to main.
- **PyPI readme is transformed at build time** — `hatch-fancy-pypi-readme`
  rewrites GitHub-only alert syntax (`> [!NOTE]` etc.) in README.md into bold
  blockquotes (`> **Note:**`) that PyPI renders; keep using alert syntax in the
  README itself. Config lives at the bottom of pyproject.toml.

## Writing style (public-facing text)

READMEs, docs pages, repo/collection descriptions, and HF model cards must
avoid AI-writing tells. This repo hosts the canonical rule: the full version
with the gating checklist lives in
[docs/model-cards.md, "Writing style"](docs/model-cards.md);
short version:

- No em dashes in prose. Use periods, colons, commas, or parentheses (`—` is
  fine as an empty table cell and inside code blocks).
- Bold only for definition-list lead-ins (`**term:**`) and at most one critical
  imperative per safety bullet. Never mid-sentence for emphasis.
- No decorative emoji (functional ✅/⚠️ marks and 🤗 for Hugging Face are fine),
  no slogans or chiasmus, no "not just X, but Y".
- Headers use colons, never em dashes or italics.

Style-only edits must never touch YAML frontmatter, code blocks, numbers,
links, or safety qualifiers.
