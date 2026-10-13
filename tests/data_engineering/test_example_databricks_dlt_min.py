"""Testes do example greenfield databricks-dlt-min (Task 22).

Cobertura alinhada aos ACs: layout DLT/DAB + quarentena, validate A+D exit 0,
auto-detect de ``databricks-dlt-legacy`` sem depender de override de marker,
D002 skip (sem SDP), D001/D003/D004/D005 aplicáveis, ausência no ``stack_map``,
e stubs sem PII/secrets versionados.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_OK, validate_project
from config.canonical_data_check.de_marker import (
    DATABRICKS_DLT_PROFILE,
    read_profile_override,
    resolve_effective_profile,
)
from config.data_engineering import DataEngineeringContract
from tests.data_engineering._secret_fixtures import forbidden_credential_needles

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_ROOT = REPO_ROOT / "examples" / "databricks-dlt-min"
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)

REQUIRED_PATHS = (
    "README.md",
    "OWNER",
    "databricks.yml",
    "config/pipeline.yaml",
    "config/schema-rescue-policy.yaml",
    "config/quarantine-policy.yaml",
    "pipelines/orders_dlt.py",
    "tests/test_smoke_databricks_dlt.py",
    "uc/grants.yaml",
    "uc/lineage.md",
)

FORBIDDEN_PII_TOKENS = (
    "cpf:",
    "passaporte",
    "@example.com",
) + forbidden_credential_needles()


def _contract_profiles() -> frozenset[str]:
    contract = DataEngineeringContract.load(CONTRACT_PATH)
    return frozenset(item.id for item in contract.profiles)


def test_example_directory_has_minimum_dlt_layout() -> None:
    assert EXAMPLE_ROOT.is_dir(), f"Example ausente: {EXAMPLE_ROOT}"
    for relative in REQUIRED_PATHS:
        path = EXAMPLE_ROOT / relative
        assert path.exists(), f"Layout DLT/DAB mínimo incompleto: {relative}"


def test_example_effective_profile_autodetects_without_marker_override() -> None:
    """AC implícito: perfil vem do auto-detect, não de project_profile override."""
    override = read_profile_override(
        EXAMPLE_ROOT,
        valid_profiles=_contract_profiles(),
    )
    assert override is None, (
        "Marker com profile override mascararia o teste de auto-detect; "
        f"encontrado override={override!r}"
    )
    effective = resolve_effective_profile(
        EXAMPLE_ROOT,
        valid_profiles=_contract_profiles(),
    )
    assert effective == DATABRICKS_DLT_PROFILE


def test_example_validate_passes_packages_a_and_d() -> None:
    result = validate_project(EXAMPLE_ROOT, contract_path=CONTRACT_PATH)
    assert result.profile == DATABRICKS_DLT_PROFILE
    assert result.exit_code == EXIT_OK
    failed = {
        finding.rule_id
        for finding in result.findings
        if finding.status == "fail" and finding.rule_id.startswith(("DE-A", "DE-D"))
    }
    assert not failed, f"Blockers A/D inesperados: {sorted(failed)}"
    # Pass silencioso (sem finding); D002 skip por ausência de sinal SDP.
    # D001/D003/D004/D005 devem estar aplicáveis (não skip) e sem fail.
    skipped = {f.rule_id for f in result.findings if f.status == "skip"}
    applicable_dlt_d = frozenset({"DE-D001", "DE-D003", "DE-D004", "DE-D005"})
    assert "DE-D002" in skipped
    assert not (applicable_dlt_d & skipped), (
        f"Regras DLT aplicáveis não devem skip: {sorted(applicable_dlt_d & skipped)}"
    )
    assert not (applicable_dlt_d & failed)


def test_example_cli_subprocess_passes_with_findings_payload() -> None:
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
    assert proc.returncode == EXIT_OK, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["exit_code"] == EXIT_OK
    assert payload["profile"] == DATABRICKS_DLT_PROFILE
    assert "findings" in payload
    assert isinstance(payload["findings"], list)


def test_example_stubs_have_no_pii_or_hardcoded_secrets() -> None:
    text_files = [
        path
        for path in EXAMPLE_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".yaml", ".yml", ".md", ".csv", ""}
    ]
    assert text_files, "Example sem arquivos de texto para revisar"
    for path in text_files:
        lowered = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_PII_TOKENS:
            assert token.lower() not in lowered, (
                f"Token proibido {token!r} em {path.relative_to(EXAMPLE_ROOT)}"
            )


def test_example_not_listed_in_install_stack_map() -> None:
    forbidden_markers = (
        "examples/databricks-dlt-min",
        "databricks-dlt-min",
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
