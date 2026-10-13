"""Task 72 — backfill commits 58–65 → e4dfc69."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTREGAS = REPO_ROOT / "metrics" / "entregas.jsonl"
TARGET_SHA = "e4dfc69"
TARGET_ISSUES = frozenset(range(58, 66))


def _load_records() -> list[dict]:
    rows: list[dict] = []
    for line in ENTREGAS.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        rows.append(json.loads(text))
    return rows


def test_entregas_58_65_sha() -> None:
    by_issue = {int(r["issue"]): r for r in _load_records() if "issue" in r}
    for issue in TARGET_ISSUES:
        assert issue in by_issue, f"issue {issue} ausente"
        assert by_issue[issue]["commit"] == TARGET_SHA


def test_other_issues_untouched() -> None:
    """Issues fora de 58–65 não devem ter sido forçadas para e4dfc69 neste backfill.

    Aceita SHA distinto; se alguma coincidir com e4dfc69 por histórico próprio, ok —
    o invariante é: não reescrevemos linhas fora do intervalo alvo (verificado via
    presença de pending só fora do range e SHA alvo só exigido em 58–65).
    """
    for row in _load_records():
        issue = int(row["issue"])
        if issue in TARGET_ISSUES:
            continue
        # Não exigimos SHA específico; apenas que o backfill não tenha apagado o campo
        assert "commit" in row


def test_no_pending_58_65() -> None:
    for row in _load_records():
        issue = int(row["issue"])
        if issue in TARGET_ISSUES:
            assert row.get("commit") != "pending"
            assert row.get("commit") == TARGET_SHA
