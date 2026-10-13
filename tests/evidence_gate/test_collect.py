"""Task 50 — collect executa comando, grava log, LWW, cap 2 MiB."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from config.evidence_gate.collect import collect_criterion
from config.evidence_gate.manifest import load_task_manifest


@pytest.fixture
def evidencias_root(tmp_path: Path) -> Path:
    root = tmp_path / "evidencias"
    root.mkdir()
    (root / "tasks").mkdir()
    (root / "logs").mkdir()
    return root


def test_collect_ok_writes_log_and_exit_zero(
    evidencias_root: Path,
    contract_yaml_path: Path,
) -> None:
    outcome = collect_criterion(
        root=evidencias_root,
        task_id="50",
        criterion_id="ac-ok",
        command=f"{sys.executable} -c \"print('hello-evidence')\"",
        test_paths=("tests/evidence_gate/test_collect.py",),
        contract_path=contract_yaml_path,
    )
    assert outcome.collect_ok is True
    assert outcome.exit_code == 0
    assert outcome.log_path.is_file()
    log_text = outcome.log_path.read_text(encoding="utf-8")
    assert "hello-evidence" in log_text

    manifest = load_task_manifest(evidencias_root, "50")
    assert manifest.task_id == "50"
    crit = manifest.criterion("ac-ok")
    assert crit.exit_code == 0
    assert crit.command
    assert crit.log_path.endswith("ac-ok.log")


def test_collect_failed_command_records_nonzero(
    evidencias_root: Path,
    contract_yaml_path: Path,
) -> None:
    outcome = collect_criterion(
        root=evidencias_root,
        task_id="50",
        criterion_id="ac-fail",
        command=f"{sys.executable} -c \"raise SystemExit(7)\"",
        test_paths=("tests/evidence_gate/test_collect.py",),
        contract_path=contract_yaml_path,
    )
    assert outcome.collect_ok is False
    assert outcome.exit_code == 7
    assert outcome.log_path.is_file()
    manifest = load_task_manifest(evidencias_root, "50")
    assert manifest.criterion("ac-fail").exit_code == 7


def test_collect_over_cap_fails_without_valid_truncated_proof(
    evidencias_root: Path,
    contract_yaml_path: Path,
    tmp_path: Path,
) -> None:
    """G3: log > 2 MiB → collect falha; não deixa prova truncada válida."""
    script = tmp_path / "gen.py"
    script.write_text(
        "import sys\n"
        "chunk = b'x' * (1024 * 256)\n"
        "for _ in range(10):\n"  # 2.5 MiB
        "    sys.stdout.buffer.write(chunk)\n"
        "    sys.stdout.buffer.flush()\n",
        encoding="utf-8",
    )
    outcome = collect_criterion(
        root=evidencias_root,
        task_id="50",
        criterion_id="ac-cap",
        command=f"{sys.executable} {script}",
        test_paths=("tests/evidence_gate/test_collect.py",),
        contract_path=contract_yaml_path,
    )
    assert outcome.collect_ok is False
    assert outcome.invalid_cap is True
    assert not outcome.log_path.is_file(), "log truncado não pode permanecer como prova"
    manifest_path = evidencias_root / "tasks" / "50.yaml"
    assert manifest_path.is_file()
    from config.evidence_gate.manifest import load_task_manifest as load

    crit = load(evidencias_root, "50").criterion("ac-cap")
    assert crit.invalid_cap is True
    assert crit.exit_code != 0


def test_cli_collect_with_command_flag_works(
    tmp_path: Path,
    repo_root: Path,
    contract_yaml_path: Path,
) -> None:
    """Regressão: dest do subparser não pode colidir com --command."""
    root = tmp_path / "evidencias"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.evidence_gate",
            "collect",
            "--path",
            str(contract_yaml_path),
            "--root",
            str(root),
            "--task",
            "50",
            "--criterion",
            "cli-cmd",
            "--command",
            f"{sys.executable} -c \"print('cli-ok')\"",
            "--test-path",
            "tests/evidence_gate/test_collect.py",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cli-ok" in (root / "logs" / "50" / "cli-cmd.log").read_text(
        encoding="utf-8"
    )


def test_collect_lww_overwrites_current_proof(
    evidencias_root: Path,
    contract_yaml_path: Path,
) -> None:
    first = collect_criterion(
        root=evidencias_root,
        task_id="50",
        criterion_id="ac-lww",
        command=f"{sys.executable} -c \"print('first')\"",
        test_paths=("tests/evidence_gate/test_collect.py",),
        contract_path=contract_yaml_path,
    )
    assert first.collect_ok
    second = collect_criterion(
        root=evidencias_root,
        task_id="50",
        criterion_id="ac-lww",
        command=f"{sys.executable} -c \"print('second')\"",
        test_paths=("tests/evidence_gate/test_collect.py",),
        contract_path=contract_yaml_path,
    )
    assert second.collect_ok
    log_text = second.log_path.read_text(encoding="utf-8")
    assert "second" in log_text
    assert "first" not in log_text
    manifest = load_task_manifest(evidencias_root, "50")
    assert manifest.criterion("ac-lww").exit_code == 0
