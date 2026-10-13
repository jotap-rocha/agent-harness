"""Task 52 — audit.jsonl append-only (G4)."""

from __future__ import annotations

import sys
from pathlib import Path

from config.evidence_gate.audit import read_audit_events
from config.evidence_gate.check import check_task
from config.evidence_gate.collect import collect_criterion
from config.evidence_gate.manifest import load_task_manifest


def test_collect_appends_audit_line(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    collect_criterion(
        root=root,
        task_id="52",
        criterion_id="a1",
        command=f"\"{sys.executable}\" -c \"print('one')\"",
        test_paths=("tests/evidence_gate/test_audit.py",),
        contract_path=contract_yaml_path,
    )
    events = read_audit_events(root)
    assert len(events) == 1
    assert events[0].task_id == "52"
    assert events[0].criterion_id == "a1"
    assert events[0].exit_code == 0
    assert events[0].log_path.endswith("a1.log")
    assert events[0].timestamp


def test_two_collects_two_audit_lines_manifest_lww(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    collect_criterion(
        root=root,
        task_id="52",
        criterion_id="lww",
        command=f"\"{sys.executable}\" -c \"print('v1')\"",
        test_paths=("tests/evidence_gate/test_audit.py",),
        contract_path=contract_yaml_path,
    )
    collect_criterion(
        root=root,
        task_id="52",
        criterion_id="lww",
        command=f"\"{sys.executable}\" -c \"print('v2')\"",
        test_paths=("tests/evidence_gate/test_audit.py",),
        contract_path=contract_yaml_path,
    )
    events = read_audit_events(root)
    assert len(events) == 2
    log = (root / "logs" / "52" / "lww.log").read_text(encoding="utf-8")
    assert "v2" in log
    assert "v1" not in log
    manifest = load_task_manifest(root, "52")
    assert manifest.criterion("lww").exit_code == 0


def test_check_does_not_rewrite_audit(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    root = tmp_path / "evidencias"
    collect_criterion(
        root=root,
        task_id="52",
        criterion_id="stable",
        command=f"\"{sys.executable}\" -c \"print('x')\"",
        test_paths=("tests/evidence_gate/test_audit.py",),
        contract_path=contract_yaml_path,
    )
    audit = root / "audit.jsonl"
    before = audit.read_text(encoding="utf-8")
    result = check_task(
        root=root,
        task_id="52",
        contract_path=contract_yaml_path,
    )
    assert result.ok, result.errors
    after = audit.read_text(encoding="utf-8")
    assert after == before


def test_audit_schema_fields_documented(
    contract_yaml_path: Path,
    repo_root: Path,
) -> None:
    """Formato JSONL estável: campos no SCHEMA/contrato."""
    schema = (
        repo_root
        / "config"
        / "evidence_gate"
        / "templates"
        / "evidencias"
        / "SCHEMA.md"
    )
    assert schema.is_file(), "SCHEMA.md do seed deve documentar audit.jsonl"
    text = schema.read_text(encoding="utf-8")
    for field in (
        "timestamp",
        "task_id",
        "criterion_id",
        "exit_code",
        "log_path",
        "audit.jsonl",
    ):
        assert field in text
    contract_text = contract_yaml_path.read_text(encoding="utf-8")
    assert "audit.jsonl" in contract_text
