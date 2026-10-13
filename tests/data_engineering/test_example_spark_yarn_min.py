"""Testes do example greenfield spark-yarn-airflow-min (Task 11)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_OK, validate_project
from config.canonical_data_check.checks.package_c import detect_airflow
from config.canonical_data_check.scanner import iter_text_files

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_ROOT = REPO_ROOT / "examples" / "spark-yarn-airflow-min"
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)

REQUIRED_PATHS = (
    "config",
    "pipelines",
    "tests",
    "OWNER",
    "contracts",
    "README.md",
)


def test_example_directory_has_minimum_layout() -> None:
    assert EXAMPLE_ROOT.is_dir(), f"Example ausente: {EXAMPLE_ROOT}"
    for relative in REQUIRED_PATHS:
        path = EXAMPLE_ROOT / relative
        assert path.exists(), f"Layout mínimo incompleto: {relative}"


def test_example_validate_passes_packages_a_and_b() -> None:
    result = validate_project(EXAMPLE_ROOT, contract_path=CONTRACT_PATH)
    failed = {
        finding.rule_id
        for finding in result.findings
        if finding.status == "fail" and finding.rule_id.startswith(("DE-A", "DE-B"))
    }
    assert result.exit_code == EXIT_OK
    assert not failed


def test_example_package_c_is_skip_or_pass() -> None:
    result = validate_project(EXAMPLE_ROOT, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_OK
    c_findings = [f for f in result.findings if f.rule_id.startswith("DE-C")]
    failed_c = {f.rule_id for f in c_findings if f.status == "fail"}
    assert not failed_c
    files = iter_text_files(EXAMPLE_ROOT)
    assert detect_airflow(EXAMPLE_ROOT, files), "A DAG mínima deve ativar o pacote C"
    skipped = {f.rule_id for f in c_findings if f.status == "skip"}
    assert not skipped, f"Pacote C não deveria skip com Airflow/DAG: {skipped}"


def test_example_cli_subprocess_passes() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "validate",
            str(EXAMPLE_ROOT),
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


def test_example_not_listed_in_install_stack_map() -> None:
    forbidden_markers = (
        "examples/spark-yarn-airflow-min",
        "examples",
        "spark-yarn-airflow-min",
    )
    for stack_map_path in STACK_MAP_PATHS:
        assert stack_map_path.is_file(), f"stack_map ausente: {stack_map_path}"
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        artifact_paths: list[str] = []
        for category in data["categories"]:
            for artifact in category["artifacts"]:
                artifact_paths.append(str(artifact["path"]))
        for marker in forbidden_markers:
            assert marker not in artifact_paths, (
                f"{stack_map_path} não deve copiar o example automaticamente "
                f"(encontrou path={marker!r})"
            )
            assert not any(
                marker == path or path.startswith(f"{marker}/")
                for path in artifact_paths
            )
