"""Task 74 — docs Dev Loop + ortogonalidade evidence-gate."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHEATSHEET = REPO_ROOT / "docs" / "fluxo-events-cheatsheet.md"
ADR005 = REPO_ROOT / "docs" / "adr" / "005-kernel-fluxo-events.md"
ADR006 = REPO_ROOT / "docs" / "adr" / "006-fluxo-events-dev-loop.md"


def test_cheatsheet_dev_loop() -> None:
    text = CHEATSHEET.read_text(encoding="utf-8")
    assert "Dev Loop" in text or "dev-loop-" in text
    assert "dev_loop_map" in text or "0–6" in text or "0-6" in text
    assert "§1.3" in text or "1.3" in text
    # naming PT-BR: menciona fluxo e rejeita forma com j
    assert "fluxo" in text
    spanish = "flu" + "j" + "o"
    assert spanish in text  # documenta a forma proibida


def test_orthogonal_mention() -> None:
    text = CHEATSHEET.read_text(encoding="utf-8")
    assert "evidence-gate" in text.lower()
    assert "ortogonal" in text.lower() or "não unifica" in text.lower()
    assert "agent-policies" in text.lower()


def test_adr_addendum_present() -> None:
    has005 = ADR005.is_file() and (
        "dev_loop_map" in ADR005.read_text(encoding="utf-8")
        or "Dev Loop" in ADR005.read_text(encoding="utf-8")
        or "Addendum" in ADR005.read_text(encoding="utf-8")
    )
    has006 = ADR006.is_file()
    assert has005 or has006, "falta addendum ADR-005 ou ADR-006"
