"""Task 51 — check manifesto + logs + evidencias_ref."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from config.evidence_gate.check import check_task
from config.evidence_gate.collect import collect_criterion
from config.evidence_gate.manifest import (
    CriterionEvidence,
    TaskManifest,
    save_task_manifest,
)


def test_check_passes_valid_manifest_and_logs(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    collect_criterion(
        root=root,
        task_id="51",
        criterion_id="ac1",
        command=f"\"{sys.executable}\" -c \"print('ok')\"",
        test_paths=("tests/evidence_gate/test_check.py",),
        contract_path=contract_yaml_path,
    )
    entregas = tmp_path / "entregas.jsonl"
    # path relativo ao cwd do teste — usamos relativo sob tmp
    rel_ref = "evidencias/tasks/51.yaml"
    # recria layout com ref relativo: check resolve contra repo ou parent
    entregas.write_text(
        json.dumps(
            {
                "issue": 51,
                "titulo": "check",
                "data": "2026-08-13",
                "criterios_aceite": {"total": 1, "atendidos": 1},
                "gate": {"resultado": "verde", "tentativas_ate_verde": 1},
                "revisor": {"veredito": "aprovado", "bloqueantes": 0, "ressalvas": 0},
                "intervencoes_humanas": 0,
                "commit": "abc1234",
                "evidencias_ref": rel_ref,
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    # symlink/copy tree so rel_ref from tmp_path works
    # check resolves evidencias_ref relative to entregas parent or explicit base
    result = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
        entregas_path=entregas,
        issue=51,
        ref_base=tmp_path,
    )
    assert result.ok, result.errors
    assert result.criteria_checked >= 1


def test_check_fails_without_test_and_without_waiver(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    root.mkdir()
    (root / "tasks").mkdir()
    (root / "logs" / "51").mkdir(parents=True)
    log = root / "logs" / "51" / "no-test.log"
    log.write_text("ok\n", encoding="utf-8")
    save_task_manifest(
        root,
        TaskManifest(
            task_id="51",
            criteria=(
                CriterionEvidence(
                    id="no-test",
                    command="true",
                    test_paths=(),
                    exit_code=0,
                    log_path="logs/51/no-test.log",
                ),
            ),
        ),
    )
    result = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
    )
    assert not result.ok
    assert any("teste" in e.lower() or "waiver" in e.lower() for e in result.errors)


def test_check_fails_missing_log_or_nonzero_exit(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    root.mkdir()
    (root / "tasks").mkdir()
    save_task_manifest(
        root,
        TaskManifest(
            task_id="51",
            criteria=(
                CriterionEvidence(
                    id="missing-log",
                    command="true",
                    test_paths=("tests/evidence_gate/test_check.py",),
                    exit_code=0,
                    log_path="logs/51/missing-log.log",
                ),
            ),
        ),
    )
    result = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
    )
    assert not result.ok
    assert any("log" in e.lower() for e in result.errors)

    (root / "logs" / "51").mkdir(parents=True)
    log = root / "logs" / "51" / "bad-exit.log"
    log.write_text("fail\n", encoding="utf-8")
    save_task_manifest(
        root,
        TaskManifest(
            task_id="51",
            criteria=(
                CriterionEvidence(
                    id="bad-exit",
                    command="false",
                    test_paths=("tests/evidence_gate/test_check.py",),
                    exit_code=1,
                    log_path="logs/51/bad-exit.log",
                ),
            ),
        ),
    )
    result2 = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
    )
    assert not result2.ok
    assert any("exit" in e.lower() for e in result2.errors)


def test_check_fails_broken_or_missing_evidencias_ref(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    collect_criterion(
        root=root,
        task_id="51",
        criterion_id="ac-ref",
        command=f"\"{sys.executable}\" -c \"print('ok')\"",
        test_paths=("tests/evidence_gate/test_check.py",),
        contract_path=contract_yaml_path,
    )
    entregas = tmp_path / "entregas.jsonl"
    entregas.write_text(
        json.dumps(
            {
                "issue": 51,
                "titulo": "check",
                "data": "2026-08-13",
                "criterios_aceite": {"total": 1, "atendidos": 1},
                "gate": {"resultado": "verde", "tentativas_ate_verde": 1},
                "revisor": {"veredito": "aprovado", "bloqueantes": 0, "ressalvas": 0},
                "intervencoes_humanas": 0,
                "commit": "abc1234",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    result = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
        entregas_path=entregas,
        issue=51,
        ref_base=tmp_path,
    )
    assert not result.ok
    assert any("evidencias_ref" in e for e in result.errors)

    entregas.write_text(
        json.dumps(
            {
                "issue": 51,
                "titulo": "check",
                "data": "2026-08-13",
                "criterios_aceite": {"total": 1, "atendidos": 1},
                "gate": {"resultado": "verde", "tentativas_ate_verde": 1},
                "revisor": {"veredito": "aprovado", "bloqueantes": 0, "ressalvas": 0},
                "intervencoes_humanas": 0,
                "commit": "abc1234",
                "evidencias_ref": "evidencias/tasks/does-not-exist.yaml",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    result2 = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
        entregas_path=entregas,
        issue=51,
        ref_base=tmp_path,
    )
    assert not result2.ok
    assert any("evidencias_ref" in e for e in result2.errors)


def test_check_accepts_human_waiver_without_tests(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    root.mkdir()
    (root / "tasks").mkdir()
    (root / "logs" / "51").mkdir(parents=True)
    log = root / "logs" / "51" / "docs.log"
    log.write_text("n/a\n", encoding="utf-8")
    save_task_manifest(
        root,
        TaskManifest(
            task_id="51",
            criteria=(
                CriterionEvidence(
                    id="docs",
                    command="true",
                    test_paths=(),
                    exit_code=0,
                    log_path="logs/51/docs.log",
                    waiver_human=True,
                    waiver_reason="critério só documental",
                ),
            ),
        ),
    )
    result = check_task(
        root=root,
        task_id="51",
        contract_path=contract_yaml_path,
    )
    assert result.ok, result.errors
