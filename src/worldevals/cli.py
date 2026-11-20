"""The ``worldevals`` CLI: browse the benchmark catalog and see what's installed."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict

from worldevals.catalog import benchmark_for_task, by_tag, catalog, get


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the catalog browsing commands."""
    parser = argparse.ArgumentParser(
        prog="worldevals",
        description="WorldEvals — the Inspect Evals for robotics (a benchmark catalog).",
    )
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="list catalogued benchmarks")
    p_list.add_argument("--tag", help="only benchmarks carrying this tag")
    p_list.add_argument(
        "--search",
        metavar="TEXT",
        help="case-insensitive substring of a name, title, description, tag or task key",
    )
    p_list.add_argument(
        "--json", action="store_true", help="print matching benchmark records as JSON"
    )

    p_info = sub.add_parser("info", help="show details for one benchmark")
    p_info.add_argument("name")

    sub.add_parser("tasks", help="Inspect Robots tasks installed locally, by benchmark")
    return parser


def _cmd_list(tag: str | None, search: str | None, as_json: bool) -> int:
    benchmarks = by_tag(tag) if tag else list(catalog())
    if search:
        query = search.casefold()
        benchmarks = [
            b
            for b in benchmarks
            if any(
                query in value.casefold()
                for value in (b.name, b.title, b.description, *b.tags, *b.task_keys)
            )
        ]
    if as_json:
        print(json.dumps([asdict(b) for b in benchmarks], indent=2))
        return 0
    if not benchmarks:
        tag_filter = f" tagged {tag!r}" if tag else ""
        search_filter = f" matching {search!r}" if search else ""
        print(f"(no benchmarks{tag_filter}{search_filter})")
        return 0
    for b in benchmarks:
        print(f"{b.name}  [{b.status}]  {b.title}")
        print(f"  {len(b.task_keys)} tasks · tags: {', '.join(b.tags)}")
    return 0


def _cmd_info(name: str) -> int:
    try:
        b = get(name)
    except KeyError as exc:
        print(str(exc))
        return 1
    print(f"{b.title} ({b.name})  [{b.status}]")
    print(f"  {b.description}")
    print(f"  repo:    {b.repo}")
    print(f"  install: {b.install}")
    print(f"  bimanual: {b.bimanual}   tags: {', '.join(b.tags)}")
    print("  tasks:")
    for key in b.task_keys:
        print(f"    - {key}")
    return 0


def _cmd_tasks() -> int:
    from inspect_robots.registry import registered

    tasks = sorted(registered("task"))
    if not tasks:
        print("(no Inspect Robots tasks installed)")
        return 0
    for key in tasks:
        b = benchmark_for_task(key)
        print(f"{key}  ←  {b.name if b is not None else '—'}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the catalog CLI and return its process exit status."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "list":
        return _cmd_list(args.tag, args.search, args.json)
    if args.command == "info":
        return _cmd_info(args.name)
    if args.command == "tasks":
        return _cmd_tasks()
    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
