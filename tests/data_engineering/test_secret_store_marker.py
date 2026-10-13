"""Testes da Task 33 — marker secret_store + auto-detect vault."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.canonical_data_check import engine
from config.canonical_data_check.de_marker import (
    SECRET_STORE_AZURE,
    SECRET_STORE_MULTI,
    SECRET_STORE_OCI,
    VaultSignals,
    detect_vault_signals,
    read_secret_store_override,
    resolve_effective_secret_store,
)
from config.canonical_data_check.findings import Finding
from config.canonical_data_check.scanner import TextFile

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.parametrize(
    ("relative_path", "content", "expected"),
    [
        (
            "src/key_oci.py",
            "from oci.secrets import SecretsClient\n",
            VaultSignals(oci=True),
        ),
        (
            "src/key_azure.py",
            "from azure.keyvault.secrets import SecretClient\n",
            VaultSignals(azure=True),
        ),
        (
            "config/secrets_map.yaml",
            "db: ocid1.vaultsecret.oc1..aaaaaaaaEXAMPLE\n",
            VaultSignals(oci=True),
        ),
        (
            "config/secrets_map.yaml",
            "db: https://myvault.vault.azure.net/secrets/db\n",
            VaultSignals(azure=True),
        ),
    ],
)
def test_detect_vault_signals_oci_or_azure(
    tmp_path: Path,
    relative_path: str,
    content: str,
    expected: VaultSignals,
) -> None:
    root = tmp_path / "project"
    _write(root / relative_path, content)
    assert detect_vault_signals(root) == expected


def test_detect_vault_both_signals(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(root / "src/key_oci.py", "from oci.secrets import SecretsClient\n")
    _write(
        root / "src/key_azure.py",
        "from azure.keyvault.secrets import SecretClient\n",
    )
    assert detect_vault_signals(root) == VaultSignals(oci=True, azure=True)


def test_detect_vault_none(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(root / "pipelines/job.py", "import logging\n")
    assert detect_vault_signals(root) == VaultSignals()


def test_secret_store_marker_override_wins(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(
        root / ".harness/data-check/project_profile.yaml",
        f"profile: spark-yarn-airflow\nsecret_store: {SECRET_STORE_OCI}\n",
    )
    # Azure signal present — marker still wins
    _write(
        root / "src/key_azure.py",
        "from azure.keyvault.secrets import SecretClient\n",
    )
    assert read_secret_store_override(root) == SECRET_STORE_OCI
    assert resolve_effective_secret_store(root) == SECRET_STORE_OCI


def test_invalid_secret_store_ignored(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(
        root / ".harness/data-check/project_profile.yaml",
        "profile: spark-yarn-airflow\nsecret_store: aws\n",
    )
    _write(root / "src/key_oci.py", "from oci.secrets import SecretsClient\n")
    assert read_secret_store_override(root) is None
    assert resolve_effective_secret_store(root) == SECRET_STORE_OCI


def test_auto_detect_resolves_oci_azure_multi(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(root / "src/key_oci.py", "from oci.secrets import SecretsClient\n")
    assert resolve_effective_secret_store(root) == SECRET_STORE_OCI

    _write(
        root / "src/key_azure.py",
        "from azure.keyvault.secrets import SecretClient\n",
    )
    assert resolve_effective_secret_store(root) == SECRET_STORE_MULTI


def test_auto_detect_azure_only(tmp_path: Path) -> None:
    root = tmp_path / "project"
    _write(
        root / "config/secrets_map.yaml",
        "x: https://x.vault.azure.net/secrets/y\n",
    )
    assert resolve_effective_secret_store(root) == SECRET_STORE_AZURE


def test_engine_dispatches_package_e_when_secret_store_applies(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "project"
    _write(
        root / ".harness/data-check/project_profile.yaml",
        f"profile: spark-yarn-airflow\nsecret_store: {SECRET_STORE_OCI}\n",
    )

    calls: list[str] = []

    def stub(
        package_id: str,
    ):
        def _inner(
            project_root: Path,
            files: tuple[TextFile, ...],
        ) -> tuple[Finding, ...]:
            del project_root, files
            calls.append(package_id)
            return (
                Finding(
                    rule_id=f"DE-{package_id}-STUB",
                    severity="warning",
                    status="pass",
                    path=".",
                    message=f"package {package_id}",
                ),
            )

        return _inner

    for package_id in ("A", "B", "C", "E"):
        monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, package_id, stub(package_id))

    result = engine.validate_project(root, contract_path=CONTRACT_PATH)

    assert "E" in calls
    assert any(f.rule_id == "DE-E-STUB" for f in result.findings)


def test_engine_does_not_dispatch_e_without_vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "project"
    _write(root / "pipelines/job.py", "import logging\n")

    e_calls = 0

    def stub_e(
        project_root: Path,
        files: tuple[TextFile, ...],
    ) -> tuple[Finding, ...]:
        nonlocal e_calls
        del project_root, files
        e_calls += 1
        return ()

    def stub_other(
        project_root: Path,
        files: tuple[TextFile, ...],
    ) -> tuple[Finding, ...]:
        del project_root, files
        return ()

    for package_id in ("A", "B", "C"):
        monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, package_id, stub_other)
    monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, "E", stub_e)

    engine.validate_project(root, contract_path=CONTRACT_PATH)
    assert e_calls == 0
