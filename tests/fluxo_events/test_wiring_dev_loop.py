"""Task 70 — wiring UX Dev Loop (crafter/executor/dev/DEV-LOOP) + dual-tree."""

from __future__ import annotations

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
X = "flu" + chr(0x78) + "o"  # fluxo (PT-BR)
PKG = f"{X}_events"

AGENTS = (
    ".claude/agents/dev/prompt-crafter.md",
    ".claude/agents/dev/dev-loop-executor.md",
)
DOCS = (
    ".claude/commands/dev.md",
    "DEV-LOOP.md",
)
MIRROR = (
    ".claude/agents/dev/prompt-crafter.md",
    ".claude/agents/dev/dev-loop-executor.md",
    ".claude/commands/dev.md",
)


def test_agents_mention_emit_ux() -> None:
    needle = f"python -m config.{PKG} emit"
    for rel in AGENTS:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert needle in text, f"{rel} sem emit"
        assert "dev-loop-" in text
        assert "live.html" in text
        assert "http.server" in text
        assert "/fluxo-live" in text
        assert "fail-soft" in text.lower() or "|| true" in text


def test_docs_mention_live() -> None:
    for rel in DOCS:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "live.html" in text, f"{rel} sem live.html"
        assert "dev-loop-" in text
        assert "/fluxo-live" in text


def test_dry_run_no_emit_documented() -> None:
    executor = (REPO_ROOT / AGENTS[1]).read_text(encoding="utf-8")
    assert "dry-run" in executor.lower()
    assert "não emite" in executor.lower() or "nao emite" in executor.lower()
    assert "não emite" in (REPO_ROOT / "DEV-LOOP.md").read_text(encoding="utf-8").lower()


def test_dual_tree() -> None:
    for rel in MIRROR:
        claude = REPO_ROOT / rel
        cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
        assert claude.is_file() and cursor.is_file(), rel
        assert filecmp.cmp(claude, cursor, shallow=False), f"drift {rel}"
