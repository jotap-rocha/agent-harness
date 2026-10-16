"""Testes da CLI validate — pacotes A/B blockers e C condicional (Task 10)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from config.canonical_data_check import (
    EXIT_BLOCKERS,
    EXIT_OK,
    EXIT_USAGE,
    Finding,
    ValidationResult,
    validate_project,
)
from config.canonical_data_check.cli import main as cli_main
from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _minimal_good_project(root: Path) -> Path:
    """Projeto mínimo que passa A+B e não tem Airflow (C=SKIP)."""
    _write(
        root / "config" / "pipeline.yaml",
        "owner: data-platform\nrun_id_field: run_id\nlogging: structured\n",
    )
    _write(
        root / "config" / "layers.yaml",
        "layers:\n  - landing\n  - bronze\n  - silver\n  - gold\n",
    )
    _write(
        root / "config" / "spark.conf",
        "spark.executor.memory=2g\n",
    )
    _write(
        root / "pipelines" / "transform.py",
        (
            "import logging\n"
            "run_id = context['run_id']\n"
            "logging.getLogger(__name__).info('start', extra={'run_id': run_id})\n"
            "df = spark.sql('SELECT id, amount FROM bronze.orders')\n"
        ),
    )
    _write(
        root / "contracts" / "orders.v1.yaml",
        "version: 1\nfields:\n  - name: id\n    type: string\n",
    )
    _write(root / "tests" / "test_smoke.py", "def test_ok() -> None:\n    assert True\n")
    _write(root / "OWNER", "data-platform\n")
    return root


def test_validate_api_returns_stable_exit_and_rule_ids(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "good")
    result = validate_project(project, contract_path=CONTRACT_PATH)

    assert isinstance(result, ValidationResult)
    assert result.exit_code == EXIT_OK
    assert all(isinstance(f, Finding) for f in result.findings)
    assert all(f.rule_id.startswith("DE-") for f in result.findings)
    skip_c = {f.rule_id for f in result.findings if f.status == "skip"}
    assert {"DE-C001", "DE-C002", "DE-C003"} <= skip_c


def test_cli_entrypoint_validate_path(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "good")
    code = cli_main(
        [
            "validate",
            str(project),
            "--contract",
            str(CONTRACT_PATH),
        ]
    )
    assert code == EXIT_OK


def test_cli_subprocess_module_entrypoint(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "good")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "validate",
            str(project),
            "--contract",
            str(CONTRACT_PATH),
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == EXIT_OK
    payload = json.loads(proc.stdout)
    assert payload["exit_code"] == EXIT_OK
    assert "findings" in payload


def test_package_a_blocks_universal_violations(tmp_path: Path) -> None:
    project = tmp_path / "bad-a"
    # Sem layout mínimo, com secret e destrutivo sem gate
    _write(
        project / "job.py",
        (
            credential_assignment("password", "super-secret-value")
            + "spark.sql('DROP TABLE prod.customers')\n"
        ),
    )

    result = validate_project(project, contract_path=CONTRACT_PATH)
    failed = {f.rule_id for f in result.findings if f.status == "fail"}

    assert result.exit_code == EXIT_BLOCKERS
    assert "DE-A001" in failed
    assert "DE-A002" in failed
    assert "DE-A003" in failed
    assert "DE-A004" in failed
    assert "DE-A005" in failed
    # SI: valor do secret não aparece no output
    serialized = " ".join(f.message for f in result.findings)
    assert "super-secret-value" not in serialized


def test_package_b_blocks_profile_violations(tmp_path: Path) -> None:
    project = tmp_path / "bad-b"
    _write(
        project / "config" / "pipeline.yaml",
        "owner: data-platform\nrun_id_field: run_id\nlogging: structured\n",
    )
    _write(
        project / "pipelines" / "transform.sql",
        "SELECT * FROM landing.raw_events;\n",
    )
    _write(project / "tests" / "test_smoke.py", "def test_ok() -> None:\n    assert True\n")
    _write(project / "OWNER", "data-platform\n")
    # Sem layers.yaml e sem contracts/

    result = validate_project(project, contract_path=CONTRACT_PATH)
    failed = {f.rule_id for f in result.findings if f.status == "fail"}

    assert result.exit_code == EXIT_BLOCKERS
    assert "DE-B001" in failed
    assert "DE-B002" in failed
    assert "DE-B003" in failed


def test_package_c_skips_when_airflow_absent(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "no-airflow")
    result = validate_project(project, contract_path=CONTRACT_PATH)

    c_findings = [f for f in result.findings if f.rule_id.startswith("DE-C")]
    assert c_findings
    assert all(f.status == "skip" for f in c_findings)
    assert result.exit_code == EXIT_OK


def test_package_c_runs_when_dag_present(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "with-airflow")
    _write(
        project / "dags" / "orders_dag.py",
        (
            "from airflow import DAG\n"
            "with DAG(dag_id='orders') as dag:\n"
            "    pass\n"
        ),
    )

    result = validate_project(project, contract_path=CONTRACT_PATH)
    c_findings = [f for f in result.findings if f.rule_id.startswith("DE-C")]
    assert c_findings
    assert all(f.status != "skip" for f in c_findings)
    failed = {f.rule_id for f in c_findings if f.status == "fail"}
    # DAG mínima sem tags / fases / spark.conf → deve falhar C
    assert "DE-C001" in failed
    assert result.exit_code == EXIT_BLOCKERS


def test_usage_error_for_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"
    result = validate_project(missing, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_USAGE


def test_findings_are_deterministic(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "det")
    first = validate_project(project, contract_path=CONTRACT_PATH)
    second = validate_project(project, contract_path=CONTRACT_PATH)
    assert [(f.rule_id, f.status, f.path, f.message) for f in first.findings] == [
        (f.rule_id, f.status, f.path, f.message) for f in second.findings
    ]


def test_cli_help_returns_zero() -> None:
    assert cli_main(["--help"]) == 0
    assert cli_main(["validate", "--help"]) == 0


def test_empty_owner_file_fails_a005(tmp_path: Path) -> None:
    project = _minimal_good_project(tmp_path / "empty-owner")
    (project / "OWNER").write_text("\n", encoding="utf-8")
    # remove owner: from config so only OWNER file would count
    pipeline = project / "config" / "pipeline.yaml"
    pipeline.write_text("run_id_field: run_id\nlogging: structured\n", encoding="utf-8")

    result = validate_project(project, contract_path=CONTRACT_PATH)
    failed = {f.rule_id for f in result.findings if f.status == "fail"}
    assert "DE-A005" in failed


def test_airflow_import_after_docstring_is_detected(tmp_path: Path) -> None:
    from config.canonical_data_check.checks.package_c import detect_airflow
    from config.canonical_data_check.scanner import iter_text_files

    project = _minimal_good_project(tmp_path / "airflow-docstring")
    _write(
        project / "orchestration" / "orders.py",
        (
            '"""DAG module."""\n'
            "from airflow import DAG\n"
            "with DAG(dag_id='orders', tags=['orders']) as dag:\n"
            "    pre = None\n"
            "    load = None\n"
            "    post = None\n"
            "    spark_conf = 'config/spark.conf'\n"
        ),
    )
    files = iter_text_files(project)
    assert detect_airflow(project, files)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    c_skips = [
        f for f in result.findings if f.rule_id.startswith("DE-C") and f.status == "skip"
    ]
    assert not c_skips
    assert result.exit_code == EXIT_OK


@pytest.mark.parametrize("argv", [[], ["validate"]])
def test_cli_usage_error_without_path(argv: list[str]) -> None:
    assert cli_main(argv) == EXIT_USAGE
