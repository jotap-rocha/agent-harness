"""Task 44 — catálogo core families + severity samples."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.agent_policies import CORE_FAMILY_IDS, AgentPoliciesContract
from config.agent_policies.matcher import match_command

CORE_SEVEN = (
    "shell",
    "docker",
    "git",
    "sql-cli",
    "databricks-cli",
    "terraform",
    "k8s",
)


def test_seven_core_families_present(contract_yaml_path: Path) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    assert tuple(contract.core_families) == CORE_SEVEN
    assert CORE_FAMILY_IDS == frozenset(CORE_SEVEN)
    for fid in CORE_SEVEN:
        family = contract.family(fid)
        assert family.core is True
        assert family.enabled_by_default is True


@pytest.mark.parametrize(
    "command,family,pattern",
    [
        ("rm -rf /data", "shell", "rm-rf"),
        ("docker compose down -v", "docker", "compose-down-v"),
        ("dropdb prod", "sql-cli", "dropdb"),
        ("terraform destroy -auto-approve", "terraform", "destroy"),
        ("kubectl delete pods --all", "k8s", "delete-all"),
    ],
)
def test_deny_hard_irreversible_samples(
    contract_yaml_path: Path,
    command: str,
    family: str,
    pattern: str,
) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command(command, contract)
    assert decision.action == "deny"
    assert decision.family_id == family
    assert decision.pattern_id == pattern


@pytest.mark.parametrize(
    "command,family,pattern",
    [
        ("git reset --hard HEAD~1", "git", "reset-hard"),
        ("git push -f origin main", "git", "push-force"),
        ("databricks workspace delete /Users/x", "databricks-cli", "workspace-delete"),
        ("databricks clusters delete --cluster-id abc", "databricks-cli", "clusters-delete"),
    ],
)
def test_ask_recoverable_with_pain_samples(
    contract_yaml_path: Path,
    command: str,
    family: str,
    pattern: str,
) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command(command, contract)
    assert decision.action == "ask"
    assert decision.family_id == family
    assert decision.pattern_id == pattern


def test_check_passes_full_core_catalog(
    contract_yaml_path: Path,
    repo_root: Path,
) -> None:
    import subprocess
    import sys

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
    assert "ok:" in proc.stdout
