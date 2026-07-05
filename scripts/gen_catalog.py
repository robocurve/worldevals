"""Generate the WorldEvals homepage from the catalog at build time.

Run automatically by the ``mkdocs-gen-files`` plugin during ``mkdocs build`` — it
imports :data:`worldevals.catalog.CATALOG` and renders it as a Material grid-card
listing, so the site is always in sync with ``catalog.py`` (the single source of
truth), mirroring how Inspect Evals generates its listing from per-eval metadata.
"""

from __future__ import annotations

import mkdocs_gen_files

from worldevals.catalog import CATALOG, Benchmark

# A Material icon per benchmark, chosen by its primary tag.
_TAG_ICON = {
    "kitchen": ":material-silverware-fork-knife:",
    "manipulation": ":material-robot-industrial:",
    "navigation": ":material-map-marker-path:",
    "locomotion": ":material-run:",
}
_DEFAULT_ICON = ":material-robot-outline:"


def _icon(benchmark: Benchmark) -> str:
    for tag in benchmark.tags:
        if tag in _TAG_ICON:
            return _TAG_ICON[tag]
    return _DEFAULT_ICON


def _card(benchmark: Benchmark) -> str:
    tags = " ".join(f"`{t}`" for t in benchmark.tags)
    bimanual = (
        " · :material-hand-back-left::material-hand-back-right: bimanual"
        if benchmark.bimanual
        else ""
    )
    return (
        f"-   {_icon(benchmark)}{{ .lg .middle }} "
        f"__[{benchmark.title}]({benchmark.repo})__\n\n"
        f"    ---\n\n"
        f"    {benchmark.description}\n\n"
        f"    **{len(benchmark.task_keys)} tasks**{bimanual} · {tags}\n\n"
        f"    [:octicons-mark-github-16: Repo]({benchmark.repo}) · "
        f"`{benchmark.status}`\n\n"
        f"    ```bash\n    {benchmark.install}\n    ```\n"
    )


def render_home() -> str:
    cards = "\n".join(_card(b) for b in CATALOG)
    total_tasks = sum(len(b.task_keys) for b in CATALOG)
    return f"""\
# WorldEvals

<p style="font-size: 1.25rem; font-weight: 500; margin-bottom: 0.25rem;">
The <strong>Inspect Evals</strong> for robotics.
</p>

A curated catalog of physical-AI / VLA benchmarks built on
[Inspect Robots](https://github.com/robocurve/inspect-robots). Each benchmark lives in **its
own repository** (so it owns its release cadence, dependencies, and hardware
notes); WorldEvals is the index that ties them together.

[:octicons-mark-github-16: GitHub](https://github.com/robocurve/worldevals){{ .md-button }}
[Add a benchmark](contributing.md){{ .md-button }}

!!! tip "Two views of the collection"
    `inspect-robots list` tells you what Inspect Robots tasks are **installed**.
    `worldevals list` tells you what benchmarks **exist** and how to get them.

## Benchmarks

**{len(CATALOG)} benchmark{"s" if len(CATALOG) != 1 else ""} · {total_tasks} tasks**

<div class="grid cards" markdown>

{cards}
</div>

## Browse from the command line

```bash
# Inspect Robots isn't on PyPI yet, so install it from its git tag first:
pip install "inspect-robots @ git+https://github.com/robocurve/inspect-robots@v0.3.0"
pip install "worldevals @ git+https://github.com/robocurve/worldevals"

worldevals list                 # all benchmarks
worldevals list --tag bimanual  # filter by tag
worldevals info kitchenbench    # repo, install command, task keys
worldevals tasks                # Inspect Robots tasks installed locally, by benchmark
```

For LLMs: [`llms.txt`](https://worldevals.org/llms.txt) ·
[`llms-full.txt`](https://worldevals.org/llms-full.txt).
"""


with mkdocs_gen_files.open("index.md", "w") as fh:
    fh.write(render_home())
