"""Testes Task 35 — scaffold cloud-secrets + examples keyvault-*-min."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_OK, validate_project
from config.canonical_data_check.de_marker import (
    SECRET_STORE_AZURE,
    SECRET_STORE_OCI,
    read_secret_store_override,
)
from tests.data_engineering._secret_fixtures import forbidden_credential_needles

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
TEMPLATE_ROOT = REPO_ROOT / "config" / "templates" / "cloud-secrets"
OCI_EXAMPLE = REPO_ROOT / "examples" / "keyvault-oci-min"
AZURE_EXAMPLE = REPO_ROOT / "examples" / "keyvault-azure-min"
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)

TEMPLATE_REQUIRED = (
    "README.md",
    "key_oci.py",
    "key_azure.py",
    "secrets_map.oci.yaml",
    "secrets_map.azure.yaml",
    "consumer_stub.py",
)

OCI_REQUIRED = (
    "README.md",
    "OWNER",
    "config/pipeline.yaml",
    "config/layers.yaml",
    "config/secrets_map.yaml",
    "contracts/orders.v1.yaml",
    "pipelines/transform.py",
    "src/key_oci.py",
    "src/consumer_stub.py",
    "tests/test_smoke_keyvault_oci.py",
    ".harness/data-check/project_profile.yaml",
)

AZURE_REQUIRED = (
    "README.md",
    "OWNER",
    "config/pipeline.yaml",
    "config/layers.yaml",
    "config/secrets_map.yaml",
    "contracts/orders.v1.yaml",
    "pipelines/transform.py",
    "src/key_azure.py",
    "src/consumer_stub.py",
    "tests/test_smoke_keyvault_azure.py",
    ".harness/data-check/project_profile.yaml",
)

FORBIDDEN_PII_TOKENS = (
    "cpf:",
    "passaporte",
    "@example.com",
) + forbidden_credential_needles()

_REAL_SECRET_HEURISTIC = re.compile(
    r"(?i)(ocid1\.[a-z0-9]+\.oc1\.[a-z0-9]*\.[a-z0-9]{40,}"
    r"|-----BEGIN (?:RSA )?PRIVATE KEY-----"
    r"|sk-[a-zA-Z0-9]{20,})"
)


def test_scaffold_template_exists() -> None:
    assert TEMPLATE_ROOT.is_dir(), f"Scaffold ausente: {TEMPLATE_ROOT}"
    for relative in TEMPLATE_REQUIRED:
        assert (TEMPLATE_ROOT / relative).is_file(), f"Template incompleto: {relative}"


def test_examples_instantiate_scaffold_not_fork() -> None:
    """Examples reutilizam o stub do scaffold (sem lógica divergente)."""
    oci_facade = (OCI_EXAMPLE / "src" / "key_oci.py").read_text(encoding="utf-8")
    azure_facade = (AZURE_EXAMPLE / "src" / "key_azure.py").read_text(encoding="utf-8")
    tmpl_oci = (TEMPLATE_ROOT / "key_oci.py").read_text(encoding="utf-8")
    tmpl_azure = (TEMPLATE_ROOT / "key_azure.py").read_text(encoding="utf-8")
    assert oci_facade == tmpl_oci
    assert azure_facade == tmpl_azure

    oci_map = (OCI_EXAMPLE / "config" / "secrets_map.yaml").read_text(encoding="utf-8")
    azure_map = (AZURE_EXAMPLE / "config" / "secrets_map.yaml").read_text(encoding="utf-8")
    assert oci_map == (TEMPLATE_ROOT / "secrets_map.oci.yaml").read_text(encoding="utf-8")
    assert azure_map == (TEMPLATE_ROOT / "secrets_map.azure.yaml").read_text(
        encoding="utf-8"
    )


def test_oci_example_layout_and_marker() -> None:
    assert OCI_EXAMPLE.is_dir()
    for relative in OCI_REQUIRED:
        assert (OCI_EXAMPLE / relative).exists(), f"OCI layout incompleto: {relative}"
    assert read_secret_store_override(OCI_EXAMPLE) == SECRET_STORE_OCI
    readme = (OCI_EXAMPLE / "README.md").read_text(encoding="utf-8").lower()
    assert "sem live api" in readme or "sem api live" in readme


def test_azure_example_layout_and_marker() -> None:
    assert AZURE_EXAMPLE.is_dir()
    for relative in AZURE_REQUIRED:
        assert (AZURE_EXAMPLE / relative).exists(), f"Azure layout incompleto: {relative}"
    assert read_secret_store_override(AZURE_EXAMPLE) == SECRET_STORE_AZURE
    readme = (AZURE_EXAMPLE / "README.md").read_text(encoding="utf-8").lower()
    assert "sem live api" in readme or "sem api live" in readme


def test_validate_keyvault_oci_min_passes() -> None:
    result = validate_project(OCI_EXAMPLE, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_OK, [
        (f.rule_id, f.status, f.message) for f in result.findings if f.status == "fail"
    ]
    e_failed = {
        f.rule_id
        for f in result.findings
        if f.status == "fail" and f.rule_id.startswith("DE-E")
    }
    assert not e_failed


def test_validate_keyvault_azure_min_passes() -> None:
    result = validate_project(AZURE_EXAMPLE, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_OK, [
        (f.rule_id, f.status, f.message) for f in result.findings if f.status == "fail"
    ]
    e_failed = {
        f.rule_id
        for f in result.findings
        if f.status == "fail" and f.rule_id.startswith("DE-E")
    }
    assert not e_failed


def test_cli_validate_both_examples() -> None:
    for example in (OCI_EXAMPLE, AZURE_EXAMPLE):
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "config.canonical_data_check",
                "validate",
                str(example),
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
        assert proc.returncode == EXIT_OK, proc.stderr or proc.stdout
        payload = json.loads(proc.stdout)
        assert payload["exit_code"] == EXIT_OK


def test_examples_not_in_stack_map() -> None:
    markers = ("keyvault-oci-min", "keyvault-azure-min", "examples/keyvault")
    for stack_map_path in STACK_MAP_PATHS:
        text = stack_map_path.read_text(encoding="utf-8")
        data = json.loads(text)
        blob = json.dumps(data)
        for marker in markers:
            assert marker not in blob, f"{stack_map_path} não deve listar {marker!r}"
            assert marker not in text


def test_zero_real_secrets_in_new_artifacts() -> None:
    roots = (TEMPLATE_ROOT, OCI_EXAMPLE, AZURE_EXAMPLE)
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".py", ".yaml", ".yml", ".md", ".json", ""}:
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for token in FORBIDDEN_PII_TOKENS:
                assert token.lower() not in lowered, (
                    f"Token proibido {token!r} em {path}"
                )
            assert _REAL_SECRET_HEURISTIC.search(text) is None, (
                f"Heurística de secret real em {path}"
            )
