"""Read a benchmark's task entry points from its pinned pyproject.toml.

Fetch only pyproject.toml at a pinned commit and read the
`[project.entry-points."inspect_robots.tasks"]` table.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from collections.abc import Callable

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - stdlib tomllib backport for 3.10
    import tomli as tomllib

_ENTRY_POINT_GROUP = "inspect_robots.tasks"


class ExtractError(Exception):
    """A benchmark's task keys could not be extracted."""


class NoTaskEntryPointsError(ExtractError):
    """The pinned pyproject.toml declares no inspect_robots.tasks entry points."""


def parse_task_keys(pyproject_bytes: bytes) -> tuple[str, ...]:
    """Return sorted task entry-point names from pyproject.toml bytes.

    Raises ``NoTaskEntryPointsError`` if the entry-point table is missing or
    empty, and ``ExtractError`` if the TOML cannot be parsed.
    """
    try:
        data = tomllib.loads(pyproject_bytes.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise ExtractError(f"malformed pyproject.toml: {exc}") from exc
    table = data.get("project", {}).get("entry-points", {}).get(_ENTRY_POINT_GROUP, {})
    if not table:
        raise NoTaskEntryPointsError(
            f'no [project.entry-points."{_ENTRY_POINT_GROUP}"] table found'
        )
    return tuple(sorted(table))


_RAW_URL = "https://raw.githubusercontent.com/{owner}/{repo}/{sha}/pyproject.toml"


def parse_owner_repo(repository_url: str) -> tuple[str, str]:
    """Split ``https://github.com/<owner>/<repo>`` into ``(owner, repo)``."""
    prefix = "https://github.com/"
    if not repository_url.startswith(prefix):
        raise ExtractError(f"not a github.com URL: {repository_url}")
    parts = repository_url[len(prefix) :].strip("/").split("/")
    if len(parts) != 2 or not all(parts):
        raise ExtractError(f"cannot parse owner/repo from: {repository_url}")
    return parts[0], parts[1]


def _fetch_pyproject(owner: str, repo: str, sha: str) -> bytes:  # pragma: no cover
    url = _RAW_URL.format(owner=owner, repo=repo, sha=sha)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data: bytes = resp.read()
            return data
    except urllib.error.URLError as exc:
        raise ExtractError(f"failed to fetch {url}: {exc}") from exc


_FETCH: Callable[[str, str, str], bytes] = _fetch_pyproject


def fetch_task_keys(repository_url: str, sha: str) -> tuple[str, ...]:
    """Fetch the pinned pyproject.toml and return its sorted task entry-point names."""
    owner, repo = parse_owner_repo(repository_url)
    return parse_task_keys(_FETCH(owner, repo, sha))
