"""Decide whether a benchmark's pin should be bumped, and render the PR body.

Pure logic used by the dispatch-triggered reconcile workflow. Resolving the
latest tag and its SHA happens in the workflow (network); this module only
decides and formats, so it is fully unit-testable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_SEMVER_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


@dataclass
class Bump:
    """A proposed pin bump for one benchmark."""

    name: str
    old_sha: str
    new_sha: str
    old_tag: str
    new_tag: str
    old_keys: tuple[str, ...]
    new_keys: tuple[str, ...]


def decide_bump(
    name: str,
    current_sha: str,
    current_tag: str,
    current_keys: tuple[str, ...],
    latest_sha: str,
    latest_tag: str,
    latest_keys: tuple[str, ...],
) -> Bump | None:
    """Return a ``Bump`` if the latest SHA differs from the pinned one, else ``None``."""
    if current_sha == latest_sha:
        return None
    return Bump(name, current_sha, latest_sha, current_tag, latest_tag, current_keys, latest_keys)


def format_pr_body(bump: Bump) -> str:
    """Render the bump as a reviewable PR body with the task-key delta."""
    added = sorted(set(bump.new_keys) - set(bump.old_keys))
    removed = sorted(set(bump.old_keys) - set(bump.new_keys))
    lines = [
        f"Bump **{bump.name}** {bump.old_tag} to {bump.new_tag}.",
        "",
        f"- SHA: `{bump.old_sha[:8]}` to `{bump.new_sha[:8]}`",
        "",
        "Task-key changes:",
        *[f"    + {k}" for k in added],
        *[f"    - {k}" for k in removed],
    ]
    if not added and not removed:
        lines.append("    (no task-key changes)")
    return "\n".join(lines)


def select_latest_tag(refs: list[str]) -> tuple[str, str] | None:
    """Pick the highest semver tag from `git ls-remote --tags` output lines."""
    # Collect: tag -> (version_tuple, plain_sha, deref_sha | None)
    tags: dict[str, tuple[tuple[int, int, int], str, str | None]] = {}

    for line in refs:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        sha, ref = parts
        if not ref.startswith("refs/tags/"):
            continue

        is_deref = ref.endswith("^{}")
        tag_name = ref[len("refs/tags/") :]
        if is_deref:
            tag_name = tag_name[:-3]

        match = _SEMVER_RE.match(tag_name)
        if not match:
            continue

        version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))

        if tag_name in tags:
            existing_version, existing_plain, existing_deref = tags[tag_name]
            if is_deref:
                tags[tag_name] = (existing_version, existing_plain, sha)
            else:
                tags[tag_name] = (version, sha, existing_deref)
        else:
            if is_deref:
                tags[tag_name] = (version, "", sha)
            else:
                tags[tag_name] = (version, sha, None)

    if not tags:
        return None

    best_tag = max(tags, key=lambda t: tags[t][0])
    _, plain_sha, deref_sha = tags[best_tag]
    final_sha = deref_sha if deref_sha is not None else plain_sha
    return (best_tag, final_sha)
