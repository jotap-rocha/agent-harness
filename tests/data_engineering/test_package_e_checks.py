"""Testes da Task 33 — checks executáveis do pacote E (keyvault-cloud)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.canonical_data_check import validate_project
from config.canonical_data_check.checks import PACKAGE_CHECK_REGISTRY
from config.canonical_data_check.checks.package_e import check_package_e
from config.canonical_data_check.de_marker import (
    SECRET_STORE_AZURE,
    SECRET_STORE_MULTI,
    SECRET_STORE_OCI,
)
from config.canonical_data_check.findings import Finding
from config.canonical_data_check.scanner import TextFile, iter_text_files

from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _marker(root: Path, *, secret_store: str, profile: str = "spark-yarn-airflow") -> None:
    _write(
        root / ".harness" / "data-check" / "project_profile.yaml",
        f"profile: {profile}\nsecret_store: {secret_store}\n",
    )


def _layout_a_minimum(root: Path) -> None:
    _write(
        root / "config" / "pipeline.yaml",
        "owner: data-platform\nrun_id_field: run_id\nlogging: structured\n",
    )
    _write(
        root / "pipelines" / "transform.py",
        (
            "import logging\n"
            "run_id = context['run_id']\n"
            "logging.getLogger(__name__).info('start', extra={'run_id': run_id})\n"
        ),
    )
    _write(root / "tests" / "test_smoke.py", "def test_ok() -> None:\n    assert True\n")
    _write(root / "OWNER", "data-platform\n")


def _oci_facade(root: Path) -> None:
    _write(
        root / "src" / "key_oci.py",
        (
            "from oci.secrets import SecretsClient\n\n"
            "def get_secret(secret_id: str) -> str:\n"
            "    return SecretsClient(config={}).get_secret_bundle(secret_id).data\n"
        ),
    )


def _azure_facade(root: Path) -> None:
    _write(
        root / "src" / "key_azure.py",
        (
            "from azure.keyvault.secrets import SecretClient\n\n"
            "def get_secret(secret_name: str) -> str:\n"
            "    return SecretClient(vault_url='https://example.vault.azure.net', "
            "credential=None).get_secret(secret_name).value\n"
        ),
    )


def _oci_map(root: Path, *, with_literal: bool = False) -> None:
    if with_literal:
        body = 'db_password: "SuperSecretValue123"\n'
    else:
        body = (
            "db_password: ocid1.vaultsecret.oc1..aaaaaaaaEXAMPLEPLACEHOLDER\n"
            "api_token: <OCI_VAULT_SECRET_OCID>\n"
        )
    _write(root / "config" / "secrets_map.yaml", body)


def _azure_map(root: Path, *, with_literal: bool = False) -> None:
    if with_literal:
        body = 'db_password: "SuperSecretValue123"\n'
    else:
        body = (
            "db_password: https://example.vault.azure.net/secrets/db-password\n"
            "api_token: <AZURE_KEYVAULT_SECRET_URI>\n"
        )
    _write(root / "config" / "secrets_map.yaml", body)


def _failed_ids(findings: tuple[Finding, ...] | list[Finding]) -> set[str]:
    return {f.rule_id for f in findings if f.status == "fail"}


def _skipped_ids(findings: tuple[Finding, ...] | list[Finding]) -> set[str]:
    return {f.rule_id for f in findings if f.status == "skip"}


def test_package_e_registered_in_registry() -> None:
    assert "E" in PACKAGE_CHECK_REGISTRY
    assert PACKAGE_CHECK_REGISTRY["E"] is check_package_e


def test_check_package_e_skips_when_vault_not_applicable(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _layout_a_minimum(root)
    files = iter_text_files(root)

    findings = check_package_e(root, files)

    assert _skipped_ids(findings) == {"DE-E001", "DE-E002", "DE-E003"}
    assert _failed_ids(findings) == set()


def test_e001_fails_without_facade(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_map(root)
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E001" in _failed_ids(findings)


def test_e001_passes_with_oci_facade(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_facade(root)
    _oci_map(root)
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E001" not in _failed_ids(findings)


def test_e002_fails_when_map_missing(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_facade(root)
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E002" in _failed_ids(findings)


def test_e002_fails_when_map_has_literal_secret(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_facade(root)
    _oci_map(root, with_literal=True)
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E002" in _failed_ids(findings)
    # SI: finding message must not echo the secret value
    for finding in findings:
        if finding.rule_id == "DE-E002" and finding.status == "fail":
            assert "SuperSecretValue123" not in finding.message


def test_e002_passes_with_id_uri_placeholders(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_AZURE)
    _azure_facade(root)
    _azure_map(root)
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E002" not in _failed_ids(findings)


def test_e003_fails_when_consumer_imports_vault_sdk(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_facade(root)
    _oci_map(root)
    _write(
        root / "pipelines" / "load.py",
        "from oci.secrets import SecretsClient\n\nclient = SecretsClient(config={})\n",
    )
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E003" in _failed_ids(findings)


def test_e003_passes_when_only_facade_imports_sdk(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_OCI)
    _oci_facade(root)
    _oci_map(root)
    _write(
        root / "pipelines" / "load.py",
        "from src.key_oci import get_secret\n\nvalue = get_secret('db_password')\n",
    )
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E003" not in _failed_ids(findings)


def test_multi_union_flags_azure_consumer_when_both_stores(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _marker(root, secret_store=SECRET_STORE_MULTI)
    _oci_facade(root)
    _azure_facade(root)
    _write(
        root / "config" / "secrets_map.yaml",
        (
            "oci_db: ocid1.vaultsecret.oc1..aaaaaaaaEXAMPLE\n"
            "azure_db: https://example.vault.azure.net/secrets/db\n"
        ),
    )
    _write(
        root / "pipelines" / "azure_consumer.py",
        "from azure.keyvault.secrets import SecretClient\n",
    )
    findings = check_package_e(root, iter_text_files(root))
    assert "DE-E003" in _failed_ids(findings)


def test_validate_runs_package_e_when_secret_store_marker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "project"
    _layout_a_minimum(root)
    _marker(root, secret_store=SECRET_STORE_OCI, profile="spark-yarn-airflow")

    def stub_empty(
        project_root: Path,
        files: tuple[TextFile, ...],
    ) -> tuple[Finding, ...]:
        del project_root, files
        return ()

    from config.canonical_data_check import engine

    for package_id in ("A", "B", "C"):
        monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, package_id, stub_empty)

    result = validate_project(root, contract_path=CONTRACT_PATH)
    failed = _failed_ids(result.findings)
    assert "DE-E001" in failed or "DE-E002" in failed


def test_de_a001_still_fails_with_package_e_present(tmp_path: Path) -> None:
    """I3: literais continuam bloqueando via DE-A001 independentemente de E."""
    root = tmp_path / "project"
    _layout_a_minimum(root)
    _marker(
        root,
        secret_store=SECRET_STORE_OCI,
        profile="databricks-sdp-medallion",
    )
    _oci_facade(root)
    _oci_map(root)
    # Satisfy D enough to avoid drowning the assertion (optional layers)
    _write(
        root / "config" / "layers.yaml",
        "layers:\n  - bronze\n  - silver\n  - gold\n",
    )
    _write(
        root / "pipelines" / "orders_sdp.py",
        "from pyspark import pipelines as dp\n@dp.table\ndef bronze_orders():\n    return None\n",
    )
    _write(
        root / "policies" / "schema-rescue.md",
        "schema_rescue\non_drift: fail\nquarantine\n",
    )
    _write(
        root / "policies" / "uc.md",
        "grants: SELECT\nlineage: documented\n",
    )
    _write(
        root / "pipelines" / "leaky.py",
        credential_assignment("password", "literal-must-still-fail-a001"),
    )

    result = validate_project(root, contract_path=CONTRACT_PATH)
    failed = _failed_ids(result.findings)
    assert "DE-A001" in failed
