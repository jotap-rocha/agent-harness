"""Task 42 — matcher compartilhado deny | ask | allow."""

from __future__ import annotations

from pathlib import Path

from config.agent_policies import AgentPoliciesContract
from config.agent_policies.matcher import match_command


def test_deny_hard_command(contract_yaml_path: Path) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command("rm -rf /tmp/data", contract)
    assert decision.action == "deny"
    assert decision.family_id == "shell"
    assert decision.pattern_id == "rm-rf"
    assert decision.message


def test_ask_command(contract_yaml_path: Path) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command("git push --force origin main", contract)
    assert decision.action == "ask"
    assert decision.family_id == "git"
    assert decision.pattern_id == "push-force"
    assert "git" in decision.message.lower() or "force" in decision.message.lower()


def test_allow_unlisted_command(contract_yaml_path: Path) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command("ls -la", contract)
    assert decision.action == "allow"
    assert decision.family_id is None
    assert decision.pattern_id is None


def test_decision_includes_auditable_ids(contract_yaml_path: Path) -> None:
    contract = AgentPoliciesContract.load(contract_yaml_path)
    decision = match_command("terraform destroy -auto-approve", contract)
    assert decision.action == "deny"
    assert decision.family_id == "terraform"
    assert decision.pattern_id == "destroy"
    assert "terraform" in f"{decision.family_id}/{decision.pattern_id}"
