"""Reconcile catalog pins against upstream releases.

For each benchmark (or a single named one), resolve the latest semver tag via
``git ls-remote --tags``, extract task keys at that SHA, and decide whether to
bump. When bumping, rewrite the register/ YAML files and emit step outputs for
the GitHub Actions workflow to open a PR or an issue on failure.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

import yaml

from worldevals._extract import ExtractError, fetch_task_keys
from worldevals._reconcile import decide_bump, format_pr_body, select_latest_tag
from worldevals.catalog import _REGISTER_DIR, _load_catalog


def _write_github_output(pairs: dict[str, str]) -> None:
    """Append key=value pairs to $GITHUB_OUTPUT; print if unset."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as fh:
            for key, value in pairs.items():
                if "\n" in value:
                    # Multi-line: use heredoc form
                    fh.write(f"{key}<<EOF\n{value}\nEOF\n")
                else:
                    fh.write(f"{key}={value}\n")
    else:
        for key, value in pairs.items():
            print(f"{key}={value}")


def _resolve_latest_tag(repository_url: str) -> tuple[str, str] | None:
    """Run git ls-remote --tags and pick the highest semver tag."""
    result = subprocess.run(
        ["git", "ls-remote", "--tags", repository_url],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return None
    lines = result.stdout.strip().splitlines()
    return select_latest_tag(lines)


def main(argv: list[str] | None = None) -> int:
    """Entry point: reconcile catalog pins against upstream releases."""
    parser = argparse.ArgumentParser(description="Reconcile catalog pins")
    parser.add_argument(
        "--benchmark",
        type=str,
        default=None,
        help="Process only the named benchmark (default: all)",
    )
    args = parser.parse_args(argv)

    benchmarks = _load_catalog()
    if args.benchmark:
        benchmarks = tuple(b for b in benchmarks if b.name == args.benchmark)
        if not benchmarks:
            print(f"error: no benchmark named {args.benchmark!r}", file=sys.stderr)
            return 1

    for benchmark in benchmarks:
        name = benchmark.name
        print(f"[{name}] checking...")

        tag_result = _resolve_latest_tag(benchmark.source.repository_url)
        if tag_result is None:
            print(f"[{name}] no semver tags found; skipping")
            continue

        latest_tag, latest_sha = tag_result

        try:
            latest_keys = fetch_task_keys(benchmark.source.repository_url, latest_sha)
        except ExtractError as exc:
            print(f"[{name}] extract error: {exc}", file=sys.stderr)
            _write_github_output(
                {
                    "failed": "true",
                    "name": name,
                    "reason": str(exc),
                }
            )
            continue

        bump = decide_bump(
            name=name,
            current_sha=benchmark.source.repository_commit,
            current_tag=benchmark.source.tag,
            current_keys=benchmark.task_keys,
            latest_sha=latest_sha,
            latest_tag=latest_tag,
            latest_keys=latest_keys,
        )

        if bump is None:
            print(f"[{name}] up to date")
            continue

        # Rewrite register/<name>/benchmark.yaml (source section only)
        benchmark_yaml_path = _REGISTER_DIR / name / "benchmark.yaml"
        meta = yaml.safe_load(benchmark_yaml_path.read_text())
        meta["source"]["repository_commit"] = bump.new_sha
        meta["source"]["tag"] = bump.new_tag
        benchmark_yaml_path.write_text(yaml.safe_dump(meta, sort_keys=False))

        # Rewrite register/<name>/task_keys.yaml
        task_keys_path = _REGISTER_DIR / name / "task_keys.yaml"
        task_keys_path.write_text(
            yaml.safe_dump({"task_keys": list(bump.new_keys)}, sort_keys=False)
        )

        title = f"bump({name}): {bump.old_tag} to {bump.new_tag}"
        body = format_pr_body(bump)
        print(f"[{name}] {title}")

        _write_github_output(
            {
                "bumped": "true",
                "name": name,
                "title": title,
                "body": body,
            }
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
