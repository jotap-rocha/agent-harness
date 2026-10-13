"""Task 48 — presença de docs/ADR/ponte SI + dogfood sem path de máquina."""

from __future__ import annotations

import json
from pathlib import Path

from config.agent_policies.generate import generate_artifacts

REPO = Path(__file__).resolve().parents[2]


def test_cheatsheet_exists() -> None:
    path = REPO / "docs" / "cheatsheets" / "agent-policies-cheatsheet.md"
    text = path.read_text(encoding="utf-8")
    assert "§1.3" in text or "1.3" in text
    assert "DE-A002" in text
    assert "HARNESS_ALLOW_DESTRUCTIVE" in text


def test_adr_003_and_index() -> None:
    adr = REPO / "docs" / "adr" / "003-kernel-agent-policies-dual-runtime.md"
    index = REPO / "docs" / "adr" / "README.md"
    assert adr.is_file()
    assert "003" in index.read_text(encoding="utf-8")
    assert "DE-A002" in adr.read_text(encoding="utf-8")


def test_seguranca_ponte_mirrored() -> None:
    md = (REPO / ".claude" / "rules" / "seguranca.md").read_text(encoding="utf-8")
    mdc = (REPO / ".cursor" / "rules" / "seguranca.mdc").read_text(encoding="utf-8")
    for text in (md, mdc):
        assert "agent-policies" in text.lower() or "Agent-policies" in text
        assert "HARNESS_ALLOW_DESTRUCTIVE" in text
        assert "§1.3" in text or "1.3" in text
        assert "DE-A002" in text


def test_claude_agents_context_mention_kernel() -> None:
    for rel in ("CLAUDE.md", "AGENTS.md", "CONTEXT.md"):
        text = (REPO / rel).read_text(encoding="utf-8")
        assert "agent-policies" in text.lower() or "Agent-policies" in text


def test_dogfood_settings_aligned_no_machine_path() -> None:
    settings = json.loads(
        (REPO / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    deny = settings["permissions"]["deny"]
    assert deny
    generated = generate_artifacts(contract_path=REPO / "agent-policies.yaml")
    assert set(deny) == set(generated.claude_deny)
    blob = json.dumps(settings)
    assert "/home/" not in blob
    assert "PreToolUse" in settings.get("hooks", {})

    hooks = json.loads((REPO / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
    assert "beforeShellExecution" in hooks["hooks"]
    assert "/home/" not in json.dumps(hooks)
