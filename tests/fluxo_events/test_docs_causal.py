"""Task 80 — cheatsheet + ADR-005 addendum causal + naming regressão."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHEATSHEET = REPO_ROOT / "docs" / "fluxo-events-cheatsheet.md"
ADR005 = REPO_ROOT / "docs" / "adr" / "005-kernel-fluxo-events.md"


def test_cheatsheet_causal() -> None:
    text = CHEATSHEET.read_text(encoding="utf-8")
    assert "event_id" in text
    assert "run_id" in text
    assert "parent_event_id" in text
    assert "stack.json" in text
    assert "fluxograma-causal" in text or "build_causal_svg" in text
    assert "fluxo" in text
    spanish = "flu" + "j" + "o"
    assert spanish in text  # forma proibida documentada
    assert "officer" not in text.lower() or "sem agent" in text.lower()


def test_adr_causal_addendum() -> None:
    text = ADR005.read_text(encoding="utf-8")
    assert "event_id" in text
    assert "run_id" in text
    assert "parent_event_id" in text
    assert "stack.json" in text
    assert "build_causal_svg" in text or "fluxograma-causal" in text
    assert "Addendum" in text or "addendum" in text
