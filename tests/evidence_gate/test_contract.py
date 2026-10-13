"""Task 49 — contrato tipado + loader + CLI check --contract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from config.evidence_gate import EvidenceGateContract
from config.evidence_gate.contract import EvidenceLimits


def test_contract_yaml_exists(contract_yaml_path: Path) -> None:
    assert contract_yaml_path.is_file(), (
        f"Fonte única ausente: {contract_yaml_path}. "
        "Crie evidence-gate.yaml na raiz do canônico."
    )


def test_contract_loads_typed_limits_and_schema(
    contract_yaml_path: Path,
) -> None:
    contract = EvidenceGateContract.load(contract_yaml_path)
    assert contract.version >= 1
    assert isinstance(contract.limits, EvidenceLimits)
    assert contract.limits.max_log_bytes == 2_097_152
    assert contract.limits.collect_time_factor == 2
    assert contract.limits.fail_on_exceed is True
    assert contract.limits.hard_timeout_seconds is None
    assert contract.manifest.required_fields
    assert "task_id" in contract.manifest.required_fields
    assert "criteria" in contract.manifest.required_fields
    assert contract.check.require_exit_zero is True
    assert contract.check.require_evidencias_ref is True


def test_invalid_yaml_fails_explicitly(tmp_path: Path) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("version: 1\nlimits:\n", encoding="utf-8")
    with pytest.raises(ValueError, match="limits"):
        EvidenceGateContract.load(bad)


def test_missing_required_field_fails(tmp_path: Path) -> None:
    bad = tmp_path / "missing.yaml"
    bad.write_text(
        "version: 1\n"
        "limits:\n"
        "  max_log_bytes: 2097152\n"
        "  collect_time_factor: 2\n"
        "  fail_on_exceed: true\n"
        "manifest:\n"
        "  required_fields:\n"
        "    - task_id\n"
        "    - criteria\n"
        "  criterion_required:\n"
        "    - id\n"
        "    - command\n"
        "check:\n"
        "  require_exit_zero: true\n"
        "  require_log_exists: true\n"
        "  require_test_path_or_waiver: true\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="require_evidencias_ref"):
        EvidenceGateContract.load(bad)


def test_hard_timeout_in_yaml_rejected(tmp_path: Path) -> None:
    """G1: sem hard timeout absoluto no contrato."""
    bad = tmp_path / "hard-timeout.yaml"
    bad.write_text(
        "version: 1\n"
        "limits:\n"
        "  max_log_bytes: 2097152\n"
        "  collect_time_factor: 2\n"
        "  fail_on_exceed: true\n"
        "  hard_timeout_seconds: 30\n"
        "manifest:\n"
        "  required_fields:\n"
        "    - task_id\n"
        "    - criteria\n"
        "  criterion_required:\n"
        "    - id\n"
        "    - command\n"
        "check:\n"
        "  require_exit_zero: true\n"
        "  require_log_exists: true\n"
        "  require_test_path_or_waiver: true\n"
        "  require_evidencias_ref: true\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="hard_timeout"):
        EvidenceGateContract.load(bad)


def test_package_importable_smoke() -> None:
    import config.evidence_gate as pkg

    assert hasattr(pkg, "EvidenceGateContract")
    assert pkg.__doc__


def test_cli_check_contract_fails_on_invalid(
    tmp_path: Path,
    repo_root: Path,
) -> None:
    bad = tmp_path / "invalid-evidence-gate.yaml"
    bad.write_text("version: 0\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.evidence_gate",
            "check",
            "--contract",
            "--path",
            str(bad),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr


def test_cli_check_contract_passes_on_repo(
    contract_yaml_path: Path,
    repo_root: Path,
) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.evidence_gate",
            "check",
            "--contract",
            "--path",
            str(contract_yaml_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
