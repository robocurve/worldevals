"""Catalog integrity, accessors, and the CLI."""

from __future__ import annotations

import re

import pytest

import worldevals
from worldevals.catalog import benchmark_for_task, by_tag, catalog, get
from worldevals.cli import main

_REPO_RE = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+$")


def test_catalog_nonempty_and_kitchenbench_present() -> None:
    names = {b.name for b in catalog()}
    assert "kitchenbench" in names


def test_catalog_integrity() -> None:
    names = [b.name for b in catalog()]
    assert len(names) == len(set(names))  # unique names
    for b in catalog():
        assert b.name and b.title and b.description and b.contributors
        assert _REPO_RE.match(b.repo), b.repo
        assert b.install
        assert len(b.task_keys) >= 1
        assert len(set(b.task_keys)) == len(b.task_keys)  # unique task keys


def test_get_and_missing() -> None:
    assert get("kitchenbench").title == "KitchenBench"
    with pytest.raises(KeyError, match="no benchmark named"):
        get("does-not-exist")


def test_by_tag() -> None:
    assert any(b.name == "kitchenbench" for b in by_tag("bimanual"))
    assert by_tag("no-such-tag") == []


def test_benchmark_for_task() -> None:
    assert benchmark_for_task("kitchenbench/pour_pasta").name == "kitchenbench"
    assert benchmark_for_task("inspect_robots/not-catalogued") is None


def test_public_api() -> None:
    assert set(worldevals.__all__) == {
        "CATALOG",
        "Benchmark",
        "__version__",
        "benchmark_for_task",
        "by_tag",
        "catalog",
        "get",
    }
    for name in worldevals.__all__:
        assert hasattr(worldevals, name)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def test_cli_list(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    assert "kitchenbench" in capsys.readouterr().out


def test_cli_list_by_tag(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--tag", "bimanual"]) == 0
    assert "kitchenbench" in capsys.readouterr().out


def test_cli_list_empty_tag(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--tag", "nope"]) == 0
    assert "no benchmarks tagged" in capsys.readouterr().out


def test_cli_info(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["info", "kitchenbench"]) == 0
    out = capsys.readouterr().out
    assert "kitchenbench/pour_pasta" in out and "install:" in out


def test_cli_info_missing(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["info", "nope"]) == 1
    assert "no benchmark named" in capsys.readouterr().out


def test_cli_tasks(capsys: pytest.CaptureFixture[str]) -> None:
    # inspect_robots is installed (a dependency); at least its builtin task shows up,
    # annotated with "—" since it isn't catalogued here.
    assert main(["tasks"]) == 0
    out = capsys.readouterr().out
    assert "cubepick-reach" in out and "—" in out


def test_cli_tasks_when_none_installed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("inspect_robots.registry.registered", lambda kind: {})
    assert main(["tasks"]) == 0
    assert "no Inspect Robots tasks installed" in capsys.readouterr().out


def test_cli_no_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "WorldEvals" in capsys.readouterr().out
