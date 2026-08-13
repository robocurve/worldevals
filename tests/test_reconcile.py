"""Pin-bump decisions, PR-body rendering, and tag selection (pure logic)."""

from __future__ import annotations

from worldevals._reconcile import Bump, decide_bump, format_pr_body, select_latest_tag

_PINNED = {
    "name": "kitchenbench",
    "current_sha": "0123456789abcdef",
    "current_tag": "v0.5.0",
    "current_keys": ("kitchenbench/pour_pasta", "kitchenbench/stack"),
}


def test_decide_bump_when_sha_is_unchanged() -> None:
    assert (
        decide_bump(
            **_PINNED,
            latest_sha="0123456789abcdef",
            latest_tag="v0.5.0",
            latest_keys=("kitchenbench/pour_pasta", "kitchenbench/stack"),
        )
        is None
    )


def test_decide_bump_when_sha_moved() -> None:
    bump = decide_bump(
        **_PINNED,
        latest_sha="fedcba9876543210",
        latest_tag="v0.6.0",
        latest_keys=("kitchenbench/pour_pasta", "kitchenbench/fold_cloth"),
    )
    assert bump == Bump(
        name="kitchenbench",
        old_sha="0123456789abcdef",
        new_sha="fedcba9876543210",
        old_tag="v0.5.0",
        new_tag="v0.6.0",
        old_keys=("kitchenbench/pour_pasta", "kitchenbench/stack"),
        new_keys=("kitchenbench/pour_pasta", "kitchenbench/fold_cloth"),
    )


def test_format_pr_body_shows_the_task_key_delta() -> None:
    body = format_pr_body(
        Bump(
            name="kitchenbench",
            old_sha="0123456789abcdef",
            new_sha="fedcba9876543210",
            old_tag="v0.5.0",
            new_tag="v0.6.0",
            old_keys=("kitchenbench/pour_pasta", "kitchenbench/stack"),
            new_keys=("kitchenbench/pour_pasta", "kitchenbench/fold_cloth"),
        )
    )
    assert body.startswith("Bump **kitchenbench** v0.5.0 to v0.6.0.")
    assert "- SHA: `01234567` to `fedcba98`" in body  # abbreviated, not full
    assert "    + kitchenbench/fold_cloth" in body
    assert "    - kitchenbench/stack" in body
    assert "no task-key changes" not in body


def test_format_pr_body_when_only_the_sha_moved() -> None:
    body = format_pr_body(
        Bump(
            name="kitchenbench",
            old_sha="0123456789abcdef",
            new_sha="fedcba9876543210",
            old_tag="v0.5.0",
            new_tag="v0.5.1",
            old_keys=("kitchenbench/pour_pasta",),
            new_keys=("kitchenbench/pour_pasta",),
        )
    )
    assert body.endswith("    (no task-key changes)")


def test_select_latest_tag_orders_numerically() -> None:
    refs = [
        "aaaaaaa\trefs/tags/v0.9.0",
        "bbbbbbb\trefs/tags/v0.10.0",  # 10 > 9, despite sorting lower as text
        "ccccccc\trefs/tags/v1.0.0",
    ]
    assert select_latest_tag(refs) == ("v1.0.0", "ccccccc")


def test_select_latest_tag_skips_noise_and_non_semver() -> None:
    refs = [
        "",
        "   ",
        "no-tab-separator",
        "aaaaaaa\trefs/heads/main",
        "bbbbbbb\trefs/tags/nightly",
        "ccccccc\trefs/tags/v1.2",  # not three-part semver
        "ddddddd\trefs/tags/v0.5.0",
    ]
    assert select_latest_tag(refs) == ("v0.5.0", "ddddddd")


def test_select_latest_tag_prefers_the_dereferenced_commit() -> None:
    # An annotated tag resolves to the tag object; `^{}` is the commit it points
    # at, which is what the pin needs.
    refs = [
        "7a9c0e1\trefs/tags/v1.0.0",
        "c0ffee1\trefs/tags/v1.0.0^{}",
    ]
    assert select_latest_tag(refs) == ("v1.0.0", "c0ffee1")


def test_select_latest_tag_when_deref_precedes_the_tag_object() -> None:
    refs = [
        "c0ffee1\trefs/tags/v1.0.0^{}",
        "7a9c0e1\trefs/tags/v1.0.0",
    ]
    assert select_latest_tag(refs) == ("v1.0.0", "c0ffee1")


def test_select_latest_tag_with_deref_only() -> None:
    assert select_latest_tag(["c0ffee1\trefs/tags/v2.0.0^{}"]) == ("v2.0.0", "c0ffee1")


def test_select_latest_tag_without_any_semver_tags() -> None:
    assert select_latest_tag(["aaaaaaa\trefs/heads/main"]) is None
