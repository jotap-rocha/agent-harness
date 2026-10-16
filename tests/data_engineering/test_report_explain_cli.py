"""Testes externos da CLI report/explain — Task 13."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_BLOCKERS, EXIT_OK, EXIT_USAGE
from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
PSEUDO_SECRET = "sk-test-report-must-not-leak"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _project_with_secret(root: Path) -> Path:
    _write(
        root / "pipeline.py",
        credential_assignment("api_key", PSEUDO_SECRET),
    )
    return root


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "config.canonical_data_check", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_report_json_emits_sanitized_findings(tmp_path: Path) -> None:
    project = _project_with_secret(tmp_path / "json-report")

    proc = _run_cli(
        "report",
        str(project),
        "--contract",
        str(CONTRACT_PATH),
        "--format",
        "json",
    )

    assert proc.returncode == EXIT_BLOCKERS
    payload = json.loads(proc.stdout)
    assert payload["profile"] == "spark-yarn-airflow"
    assert payload["findings"]
    assert {"rule_id", "severity", "status", "path"} == set(payload["findings"][0])
    assert all(item["rule_id"].startswith("DE-") for item in payload["findings"])
    assert all("message" not in item for item in payload["findings"])
    assert PSEUDO_SECRET not in proc.stdout


def test_report_markdown_emits_readable_structure_without_secret(tmp_path: Path) -> None:
    project = _project_with_secret(tmp_path / "markdown-report")

    proc = _run_cli(
        "report",
        str(project),
        "--contract",
        str(CONTRACT_PATH),
        "--format",
        "markdown",
    )

    assert proc.returncode == EXIT_BLOCKERS
    assert "# Relatório de conformidade DE" in proc.stdout
    assert "| Rule ID | Severidade | Status | Path |" in proc.stdout
    assert "DE-A001" in proc.stdout
    assert PSEUDO_SECRET not in proc.stdout


def test_explain_returns_actionable_rule_content_from_yaml() -> None:
    proc = _run_cli(
        "explain",
        "DE-B002",
        "--contract",
        str(CONTRACT_PATH),
    )

    assert proc.returncode == EXIT_OK
    assert "DE-B002 — Transformações não podem usar SELECT star" in proc.stdout
    assert "Aplicabilidade: spark-yarn-airflow" in proc.stdout
    assert "Descrição: Seleção implícita" in proc.stdout
    assert "Remediação: Liste explicitamente" in proc.stdout


def test_explain_unknown_rule_fails_clearly() -> None:
    proc = _run_cli(
        "explain",
        "DE-Z999",
        "--contract",
        str(CONTRACT_PATH),
    )

    assert proc.returncode == EXIT_USAGE
    assert proc.stdout == ""
    assert "Regra inexistente: DE-Z999" in proc.stderr
