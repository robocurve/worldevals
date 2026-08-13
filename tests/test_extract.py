"""Task-key extraction from a benchmark's pinned pyproject.toml."""

from __future__ import annotations

import pytest

from worldevals import _extract
from worldevals._extract import (
    ExtractError,
    NoTaskEntryPointsError,
    fetch_task_keys,
    parse_owner_repo,
    parse_task_keys,
)

# Entry-point names carry the `<benchmark>/` prefix, so they're quoted keys.
_PYPROJECT = b"""\
[project]
name = "kitchenbench"

[project.entry-points."inspect_robots.tasks"]
"kitchenbench/pour_pasta" = "kitchenbench.tasks:pour_pasta"
"kitchenbench/fold_cloth" = "kitchenbench.tasks:fold_cloth"
"""


def test_parse_task_keys_returns_sorted_names() -> None:
    assert parse_task_keys(_PYPROJECT) == (
        "kitchenbench/fold_cloth",
        "kitchenbench/pour_pasta",
    )


@pytest.mark.parametrize(
    "pyproject",
    [
        b'[project]\nname = "kitchenbench"\n',  # no entry-points table at all
        b'[project.entry-points."inspect_robots.tasks"]\n',  # table present but empty
    ],
    ids=["missing-table", "empty-table"],
)
def test_parse_task_keys_without_entry_points(pyproject: bytes) -> None:
    with pytest.raises(NoTaskEntryPointsError, match=r"inspect_robots\.tasks"):
        parse_task_keys(pyproject)
    assert issubclass(NoTaskEntryPointsError, ExtractError)


def test_parse_task_keys_malformed_toml() -> None:
    with pytest.raises(ExtractError, match=r"malformed pyproject\.toml"):
        parse_task_keys(b"[project\nname =\n")


def test_parse_task_keys_undecodable_bytes() -> None:
    with pytest.raises(ExtractError, match=r"malformed pyproject\.toml"):
        parse_task_keys(b"\xff\xfe not utf-8")


def test_parse_owner_repo() -> None:
    assert parse_owner_repo("https://github.com/robocurve/kitchenbench") == (
        "robocurve",
        "kitchenbench",
    )


def test_parse_owner_repo_rejects_non_github() -> None:
    with pytest.raises(ExtractError, match=r"not a github\.com URL"):
        parse_owner_repo("https://gitlab.com/robocurve/kitchenbench")


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/robocurve",  # owner only
        "https://github.com/robocurve/kitchenbench/tree/main",  # too many segments
    ],
    ids=["owner-only", "extra-segments"],
)
def test_parse_owner_repo_rejects_malformed_path(url: str) -> None:
    with pytest.raises(ExtractError, match="cannot parse owner/repo"):
        parse_owner_repo(url)


def test_fetch_task_keys_fetches_at_the_pinned_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    # The network fetch itself is out of scope here; what matters is that the
    # repo URL is split correctly and the pinned SHA is passed through.
    calls: list[tuple[str, str, str]] = []

    def fake_fetch(owner: str, repo: str, sha: str) -> bytes:
        calls.append((owner, repo, sha))
        return _PYPROJECT

    monkeypatch.setattr(_extract, "_FETCH", fake_fetch)
    keys = fetch_task_keys("https://github.com/robocurve/kitchenbench", "e781f931")
    assert keys == ("kitchenbench/fold_cloth", "kitchenbench/pour_pasta")
    assert calls == [("robocurve", "kitchenbench", "e781f931")]
