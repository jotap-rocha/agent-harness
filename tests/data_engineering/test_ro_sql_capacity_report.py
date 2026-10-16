"""Testes do job RO para o relatório brownfield sql-capacity — Task 14."""

from __future__ import annotations

import json
import stat
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_BLOCKERS, EXIT_OK, EXIT_USAGE
from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
DEFAULT_SQL_CAPACITY_PATH = Path(
    "/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd"
)
PSEUDO_SECRET = "sk-test-ro-report-must-not-leak"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_read_only(root: Path) -> None:
    for path in root.rglob("*"):
        path.chmod(0o555 if path.is_dir() else 0o444)
    root.chmod(0o555)


def _restore_write_permission(root: Path) -> None:
    root.chmod(0o755)
    for path in root.rglob("*"):
        path.chmod(0o755 if path.is_dir() else 0o644)


def _snapshot(root: Path) -> dict[str, tuple[int, bytes]]:
    return {
        str(path.relative_to(root)): (
            stat.S_IMODE(path.stat().st_mode),
            b"" if path.is_dir() else path.read_bytes(),
        )
        for path in sorted(root.rglob("*"))
    }


def _run_job(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "config.canonical_data_check.ro_report", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_job_defaults_to_sql_capacity_path() -> None:
    from config.canonical_data_check.ro_report import build_parser

    args = build_parser().parse_args([])

    assert args.target == DEFAULT_SQL_CAPACITY_PATH


def test_job_writes_sanitized_json_only_outside_read_only_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "sql-capacity"
    _write(target / "pipeline.py", credential_assignment("api_key", PSEUDO_SECRET))
    before = _snapshot(target)
    _make_read_only(target)
    read_only_before = _snapshot(target)
    output = tmp_path / "canonical-reports" / "sql-capacity.json"

    try:
        proc = _run_job(
            "--target",
            str(target),
            "--output",
            str(output),
            "--contract",
            str(CONTRACT_PATH),
            "--format",
            "json",
        )

        assert proc.returncode == EXIT_BLOCKERS
        assert output.is_file()
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert payload["findings"]
        assert all(
            {"rule_id", "severity", "status", "path"} == set(finding)
            for finding in payload["findings"]
        )
        assert PSEUDO_SECRET not in output.read_text(encoding="utf-8")
        assert _snapshot(target) == read_only_before
        assert not (target / ".harness" / "data-check" / "baseline.json").exists()
    finally:
        _restore_write_permission(target)

    assert _snapshot(target) == before


def test_job_writes_markdown_artifact_outside_target(tmp_path: Path) -> None:
    target = tmp_path / "sql-capacity"
    _write(target / "pipeline.py", "print('pipeline')\n")
    output = tmp_path / "canonical-reports" / "sql-capacity.md"

    proc = _run_job(
        "--target",
        str(target),
        "--output",
        str(output),
        "--contract",
        str(CONTRACT_PATH),
        "--format",
        "markdown",
    )

    assert proc.returncode == EXIT_BLOCKERS
    assert output.read_text(encoding="utf-8").startswith(
        "# Relatório de conformidade DE\n"
    )
    assert not (target / ".harness" / "data-check" / "baseline.json").exists()


def test_missing_target_is_documented_soft_fail_without_artifact(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing-sql-capacity"
    output = tmp_path / "canonical-reports" / "sql-capacity.json"

    proc = _run_job(
        "--target",
        str(missing),
        "--output",
        str(output),
        "--contract",
        str(CONTRACT_PATH),
    )

    assert proc.returncode == EXIT_OK
    assert proc.stdout == ""
    assert "SOFT-FAIL" in proc.stderr
    assert str(missing) in proc.stderr
    assert not output.exists()


def test_job_rejects_output_inside_target_without_writing(tmp_path: Path) -> None:
    target = tmp_path / "sql-capacity"
    target.mkdir()
    before = _snapshot(target)
    output = target / "reports" / "sql-capacity.json"

    proc = _run_job(
        "--target",
        str(target),
        "--output",
        str(output),
        "--contract",
        str(CONTRACT_PATH),
    )

    assert proc.returncode == EXIT_USAGE
    assert "fora do projeto-alvo" in proc.stderr
    assert _snapshot(target) == before
    assert not output.exists()
