"""Task 66 — aviso UX ao usuário sobre painel live.html (SDD)."""

from __future__ import annotations

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

BRAINSTORM = ".claude/agents/workflow/harness-brainstorm.md"
BUILD = ".claude/agents/workflow/harness-build.md"
CMD = ".claude/commands/fluxo-live.md"

NEEDLES = (
    "Aviso ao usuário",
    "live.html",
    "http.server",
    "/fluxo-live",
)


def _assert_aviso(rel: str) -> None:
    text = (REPO_ROOT / rel).read_text(encoding="utf-8")
    for needle in NEEDLES:
        assert needle in text, f"{rel} sem {needle!r}"


def test_brainstorm_avisar_usuario() -> None:
    _assert_aviso(BRAINSTORM)


def test_build_avisar_usuario() -> None:
    _assert_aviso(BUILD)


def test_fluxo_live_command_docs() -> None:
    text = (REPO_ROOT / CMD).read_text(encoding="utf-8")
    assert "live.html" in text
    assert "browser" in text.lower() or "Abra" in text
    assert "http.server" in text


def test_dual_tree_ux() -> None:
    for rel in (BRAINSTORM, BUILD, CMD):
        claude = REPO_ROOT / rel
        cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
        assert claude.is_file() and cursor.is_file(), rel
        assert filecmp.cmp(claude, cursor, shallow=False), f"drift {rel}"
