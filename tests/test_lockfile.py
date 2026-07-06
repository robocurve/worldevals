"""Lockfile hygiene.

CI installs with ``uv sync --locked``, so the committed ``uv.lock`` is the real
gate on what runs in CI and docs builds.
"""

from __future__ import annotations

from pathlib import Path

_LOCKFILE = Path(__file__).resolve().parent.parent / "uv.lock"


def test_lockfile_has_no_properdocs() -> None:
    # mkdocs-gen-files 0.6.1 depends on "properdocs", an mkdocs fork that
    # injects promo content into every built page. pyproject caps
    # mkdocs-gen-files at <0.6.1; this guards the lock against re-resolution.
    assert "properdocs" not in _LOCKFILE.read_text(encoding="utf-8")
