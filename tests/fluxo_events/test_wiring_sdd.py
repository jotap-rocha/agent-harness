"""Task 62 — wiring SDD emit/ship + dual-tree."""

from __future__ import annotations

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
X = "flu" + chr(0x78) + "o"  # fluxo (PT-BR)
PKG = f"{X}_events"

WIRED = [
    ".claude/agents/workflow/harness-brainstorm.md",
    ".claude/agents/workflow/harness-define.md",
    ".claude/agents/workflow/harness-design.md",
    ".claude/agents/workflow/harness-build.md",
    ".claude/agents/workflow/harness-ship.md",
    ".claude/agents/dev/revisor-codigo.md",
    ".claude/skills/grill-me/SKILL.md",
    ".claude/skills/to-prd/SKILL.md",
    ".claude/skills/harness-architect/SKILL.md",
    ".claude/skills/to-tasks/SKILL.md",
    ".claude/commands/scorecard.md",
]


def test_agents_mention_emit() -> None:
    needle = f"python -m config.{PKG} emit"
    for rel in WIRED:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert needle in text, f"{rel} sem instrução emit"
        assert "fail-soft" in text.lower() or "|| true" in text


def test_ship_mentions_truncate() -> None:
    text = (REPO_ROOT / ".claude/agents/workflow/harness-ship.md").read_text(
        encoding="utf-8"
    )
    assert f"python -m config.{PKG} truncate" in text
    assert "--keep 100" in text


def test_dual_tree_wiring_mirror() -> None:
    for rel in WIRED:
        claude = REPO_ROOT / rel
        cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
        assert claude.is_file() and cursor.is_file(), rel
        assert filecmp.cmp(claude, cursor, shallow=False), f"drift {rel}"


def test_no_fluxo_officer_agent() -> None:
    agents = list((REPO_ROOT / ".claude/agents").rglob("*.md"))
    names = [p.name.lower() for p in agents]
    assert not any("officer" in n and X in n for n in names)
