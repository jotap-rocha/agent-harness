"""Task 41 — contrato tipado + loader + CLI check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from config.agent_policies import AgentPoliciesContract
from config.agent_policies.contract import PolicyFamily, PolicyPattern


def test_contract_yaml_exists(contract_yaml_path: Path) -> None:
    assert contract_yaml_path.is_file(), (
        f"Fonte única ausente: {contract_yaml_path}. "
        "Crie agent-policies.yaml na raiz do canônico."
    )


def test_contract_loads_typed_families_and_patterns(
    contract_yaml_path: Path,
) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    assert contract.version >= 1
    assert contract.core_families, "core_families não pode ser vazio"
    assert contract.families, "families não pode ser vazio"
    for family in contract.families:
        assert isinstance(family, PolicyFamily)
        assert family.id
        assert family.patterns, f"família {family.id} sem patterns"
        for pattern in family.patterns:
            assert isinstance(pattern, PolicyPattern)
            assert pattern.id
            assert pattern.severity in {"deny", "ask"}
            assert pattern.match.pattern


def test_invalid_yaml_fails_explicitly(tmp_path: Path) -> None:
    bad = tmp_path / "broken.yaml"
    # mapping vazio explícito (filho indentado) — loader stdlib
    bad.write_text("version: 1\nfamilies:\n", encoding="utf-8")
    with pytest.raises(ValueError, match="families"):
        AgentPoliciesContract.load(bad)


def test_missing_required_field_fails(tmp_path: Path) -> None:
    bad = tmp_path / "missing.yaml"
    bad.write_text(
        "version: 1\n"
        "core_families:\n"
        "  - shell\n"
        "families:\n"
        "  shell:\n"
        "    description: demo\n"
        "    core: true\n"
        "    enabled_by_default: true\n"
        "    patterns:\n"
        "      rm-rf:\n"
        "        match: rm\\s+-rf\n"
        "        tool_deny: \"Bash(rm -rf:*)\"\n"
        "        message: bloqueado\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="severity"):
        AgentPoliciesContract.load(bad)


def test_package_importable_smoke() -> None:
    import config.agent_policies as pkg

    assert hasattr(pkg, "AgentPoliciesContract")
    assert pkg.__doc__


def test_cli_check_fails_on_invalid_contract(
    tmp_path: Path,
    repo_root: Path,
) -> None:
    bad = tmp_path / "invalid-policies.yaml"
    bad.write_text("version: 0\n", encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.agent_policies",
            "check",
            "--path",
            str(bad),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr


def test_cli_check_passes_on_repo_contract(
    contract_yaml_path: Path,
    repo_root: Path,
) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.agent_policies",
            "check",
            "--path",
            str(contract_yaml_path),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
