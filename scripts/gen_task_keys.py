"""Regenerate register/<name>/task_keys.yaml from each benchmark's pinned source.

Reads benchmark.yaml, fetches the pinned commit's pyproject.toml, and writes the
extracted inspect_robots.tasks entry-point names.
"""

from __future__ import annotations

import yaml

from worldevals._extract import fetch_task_keys
from worldevals.catalog import _REGISTER_DIR


def main() -> int:
    for benchmark_yaml in sorted(_REGISTER_DIR.glob("*/benchmark.yaml")):
        meta = yaml.safe_load(benchmark_yaml.read_text())
        src = meta["source"]
        keys = fetch_task_keys(src["repository_url"], src["repository_commit"])
        out = benchmark_yaml.parent / "task_keys.yaml"
        out.write_text(yaml.safe_dump({"task_keys": list(keys)}, sort_keys=False))
        print(f"{meta['name']}: {len(keys)} task keys")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
