"""Task 55/56 — DoD/agents/docs/parity asserts."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_dod_mentions_evidence_gate() -> None:
    for rel in (
        ".claude/rules/definicao-de-pronto.md",
        ".cursor/rules/definicao-de-pronto.mdc",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "evidence-gate" in text
        assert "evidencias_ref" in text
        assert "manifesto" in text.lower() or "evidencias/tasks" in text


def test_to_tasks_requires_test_paths() -> None:
    for rel in (
        ".claude/skills/to-tasks/SKILL.md",
        ".cursor/skills/to-tasks/SKILL.md",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "evidence-gate" in text or "evidencias" in text
        assert "test_paths" in text or "tested by" in text
        assert "waiver" in text.lower()


def test_revisor_soft_not_hard_check() -> None:
    for rel in (
        ".claude/agents/dev/revisor-codigo.md",
        ".cursor/agents/dev/revisor-codigo.md",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "soft" in text.lower()
        assert "evidence-gate" in text
        assert "não" in text.lower() or "nao" in text.lower() or "Não" in text
        assert "substitui" in text.lower() or "lugar do CLI" in text


def test_docs_and_adr_and_command_exist() -> None:
    assert (REPO_ROOT / "docs/evidence-gate-cheatsheet.md").is_file()
    assert (REPO_ROOT / "docs/adr/004-kernel-evidence-gate.md").is_file()
    idx = (REPO_ROOT / "docs/adr/README.md").read_text(encoding="utf-8")
    assert "004-kernel-evidence-gate" in idx
    for rel in (".claude/commands/evidencias.md", ".cursor/commands/evidencias.md"):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "config.evidence_gate" in text


def test_claude_agents_context_list_kernel() -> None:
    for rel in ("CLAUDE.md", "AGENTS.md", "CONTEXT.md"):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "evidence-gate" in text.lower() or "Evidence-gate" in text


def test_cheatsheet_cross_links_validar_and_policies() -> None:
    text = (REPO_ROOT / "docs/evidence-gate-cheatsheet.md").read_text(encoding="utf-8")
    assert "/validar" in text
    assert "agent-policies" in text or "Bash deny" in text
    assert "§1.3" in text or "1.3" in text


def test_mirror_parity_touched_agents() -> None:
    pairs = [
        (
            ".claude/agents/workflow/harness-build.md",
            ".cursor/agents/workflow/harness-build.md",
        ),
        (
            ".claude/agents/workflow/harness-ship.md",
            ".cursor/agents/workflow/harness-ship.md",
        ),
        (
            ".claude/agents/dev/revisor-codigo.md",
            ".cursor/agents/dev/revisor-codigo.md",
        ),
        (
            ".claude/skills/to-tasks/SKILL.md",
            ".cursor/skills/to-tasks/SKILL.md",
        ),
        (
            ".claude/commands/evidencias.md",
            ".cursor/commands/evidencias.md",
        ),
    ]
    for a, b in pairs:
        assert (REPO_ROOT / a).read_text(encoding="utf-8") == (
            REPO_ROOT / b
        ).read_text(encoding="utf-8")
