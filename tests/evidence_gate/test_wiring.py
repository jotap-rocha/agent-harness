"""Task 53 — wiring build/ship + evidencias_ref + helper close."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from config.evidence_gate.close import (
    append_entrega_with_ref,
    close_task_evidence_gate,
    collect_then_check,
    evidencias_ref_for,
    require_evidencias_ref_field,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_metrics_readme_documents_evidencias_ref() -> None:
    text = (REPO_ROOT / "metrics" / "README.md").read_text(encoding="utf-8")
    assert "evidencias_ref" in text


def test_append_entrega_requires_evidencias_ref(tmp_path: Path) -> None:
    path = tmp_path / "entregas.jsonl"
    with pytest.raises(ValueError, match="evidencias_ref"):
        append_entrega_with_ref(
            path,
            {
                "issue": 53,
                "titulo": "x",
                "data": "2026-08-13",
                "criterios_aceite": {"total": 1, "atendidos": 1},
                "gate": {"resultado": "verde", "tentativas_ate_verde": 1},
                "revisor": {"veredito": "aprovado", "bloqueantes": 0, "ressalvas": 0},
                "intervencoes_humanas": 0,
                "commit": "abc",
            },
        )


def test_collect_check_ref_integration(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    outcome, check = collect_then_check(
        root=root,
        task_id="53",
        criterion_id="wire",
        command=f"{sys.executable} -c \"print('wire')\"",
        test_paths=("tests/evidence_gate/test_wiring.py",),
        contract_path=contract_yaml_path,
    )
    assert outcome.collect_ok
    assert check.ok, check.errors
    ref = evidencias_ref_for(root, "53", relative_to=tmp_path)
    assert ref.endswith("tasks/53.yaml")
    entregas = tmp_path / "entregas.jsonl"
    append_entrega_with_ref(
        entregas,
        {
            "issue": 53,
            "titulo": "wiring",
            "data": "2026-08-13",
            "criterios_aceite": {"total": 1, "atendidos": 1},
            "gate": {"resultado": "verde", "tentativas_ate_verde": 1},
            "revisor": {"veredito": "aprovado", "bloqueantes": 0, "ressalvas": 0},
            "intervencoes_humanas": 0,
            "commit": "abc",
            "evidencias_ref": ref,
        },
    )
    gate = close_task_evidence_gate(
        root=root,
        task_id="53",
        entregas_path=entregas,
        issue=53,
        contract_path=contract_yaml_path,
        ref_base=tmp_path,
    )
    assert gate.ok, gate.errors


def test_harness_build_documents_evidence_gate_block() -> None:
    for rel in (
        ".claude/agents/workflow/harness-build.md",
        ".cursor/agents/workflow/harness-build.md",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "evidence-gate" in text or "evidencias" in text.lower()
        assert "collect" in text and "check" in text


def test_harness_ship_documents_revalidate() -> None:
    for rel in (
        ".claude/agents/workflow/harness-ship.md",
        ".cursor/agents/workflow/harness-ship.md",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "evidence-gate" in text or "evidencias" in text.lower()
        assert "revalid" in text.lower() or "check" in text


def test_require_evidencias_ref_field_ok() -> None:
    require_evidencias_ref_field({"evidencias_ref": "evidencias/tasks/1.yaml"})
