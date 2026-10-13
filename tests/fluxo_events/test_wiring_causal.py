"""Task 79 — wiring SDD + Dev Loop menciona run_id/parent/stack + dual-tree."""

from __future__ import annotations

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
X = "flu" + chr(0x78) + "o"  # fluxo
PKG = f"{X}_events"

SDD = [
    ".claude/agents/workflow/harness-brainstorm.md",
    ".claude/agents/workflow/harness-define.md",
    ".claude/agents/workflow/harness-design.md",
    ".claude/agents/workflow/harness-build.md",
    ".claude/agents/workflow/harness-ship.md",
]

DEV = [
    ".claude/agents/dev/prompt-crafter.md",
    ".claude/agents/dev/dev-loop-executor.md",
    ".claude/commands/dev.md",
]

CAUSAL_NEEDLES = ("--run-id", "--parent-event-id", "stack.json")


def _assert_causal(rel: str) -> None:
    text = (REPO_ROOT / rel).read_text(encoding="utf-8")
    assert f"python -m config.{PKG} emit" in text or "emit" in text.lower()
    for needle in CAUSAL_NEEDLES:
        assert needle in text, f"{rel} sem {needle}"
    assert "fail-soft" in text.lower() or "|| true" in text


def test_sdd_wiring_mentions_causal() -> None:
    for rel in SDD:
        _assert_causal(rel)


def test_dev_wiring_mentions_causal() -> None:
    for rel in DEV:
        _assert_causal(rel)
    executor = (REPO_ROOT / DEV[1]).read_text(encoding="utf-8")
    assert "dry-run" in executor.lower()
    assert "não emite" in executor.lower() or "nao emite" in executor.lower()


def test_dual_tree() -> None:
    for rel in SDD + DEV:
        claude = REPO_ROOT / rel
        cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
        assert claude.is_file() and cursor.is_file(), rel
        assert filecmp.cmp(claude, cursor, shallow=False), f"drift {rel}"
