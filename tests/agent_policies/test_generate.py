"""Task 45 — generate dual Claude deny + Cursor hooks."""

from __future__ import annotations

import json
from pathlib import Path

from config.agent_policies.contract import AgentPoliciesContract
from config.agent_policies.generate import generate_artifacts, write_artifacts


def test_generate_claude_deny_non_empty(contract_yaml_path: Path) -> None:
    result = generate_artifacts(contract_path=contract_yaml_path)
    assert result.claude_deny
    assert any("rm -rf" in entry for entry in result.claude_deny)


def test_generate_cursor_hooks_coherent(contract_yaml_path: Path) -> None:
    result = generate_artifacts(contract_path=contract_yaml_path)
    hooks = result.cursor_hooks
    assert "hooks" in hooks
    before = hooks["hooks"]["beforeShellExecution"]  # type: ignore[index]
    assert before
    assert "shell" in result.active_family_ids


def test_severity_change_affects_both_outputs(tmp_path: Path) -> None:
    yaml_path = tmp_path / "agent-policies.yaml"
    yaml_path.write_text(
        "version: 1\n"
        "core_families:\n"
        "  - shell\n"
        "families:\n"
        "  shell:\n"
        "    description: t\n"
        "    core: true\n"
        "    enabled_by_default: true\n"
        "    patterns:\n"
        "      demo:\n"
        "        severity: deny\n"
        "        match: 'demo-destroy'\n"
        "        tool_deny: \"Bash(demo-destroy:*)\"\n"
        "        message: demo\n"
        "      always-deny:\n"
        "        severity: deny\n"
        "        match: 'always-deny-cmd'\n"
        "        tool_deny: \"Bash(always-deny:*)\"\n"
        "        message: keep\n",
        encoding="utf-8",
    )
    first = generate_artifacts(contract_path=yaml_path)
    assert "Bash(demo-destroy:*)" in first.claude_deny

    text = yaml_path.read_text(encoding="utf-8")
    # só o pattern demo muda para ask
    yaml_path.write_text(
        text.replace(
            "demo:\n        severity: deny",
            "demo:\n        severity: ask",
            1,
        ),
        encoding="utf-8",
    )
    second = generate_artifacts(contract_path=yaml_path)
    assert "Bash(demo-destroy:*)" not in second.claude_deny
    assert "Bash(always-deny:*)" in second.claude_deny
    assert second.active_family_ids == first.active_family_ids


def test_generate_child_has_no_machine_paths(
    contract_yaml_path: Path,
    tmp_path: Path,
) -> None:
    out = tmp_path / "out"
    result = generate_artifacts(contract_path=contract_yaml_path)
    write_artifacts(result, out)
    blob = (out / "hooks.json").read_text(encoding="utf-8")
    assert "/home/" not in blob
    assert "/DATALAKE/" not in blob
    assert ".cursor/hooks/agent_policies_before_shell.sh" in blob
    deny = json.loads((out / "claude_permissions_deny.json").read_text(encoding="utf-8"))
    assert isinstance(deny, list) and deny


def test_extra_family_only_with_profile(
    contract_yaml_path: Path,
    tmp_path: Path,
) -> None:
    without = generate_artifacts(contract_path=contract_yaml_path)
    assert "cloud-cli-extra" not in without.active_family_ids

    profile = tmp_path / "project_profile.yaml"
    profile.write_text(
        "families:\n  - cloud-cli-extra\n",
        encoding="utf-8",
    )
    with_extra = generate_artifacts(
        contract_path=contract_yaml_path,
        profile_path=profile,
    )
    assert "cloud-cli-extra" in with_extra.active_family_ids
    assert any("aws s3 rb" in e for e in with_extra.claude_deny)
    # sanity: profile carrega
    assert "cloud-cli-extra" in load_profile_families_helper(profile)


def load_profile_families_helper(path: Path) -> frozenset[str]:
    from config.agent_policies.generate import load_profile_families

    return load_profile_families(path)


def test_contract_still_loads(contract_yaml_path: Path) -> None:
    assert AgentPoliciesContract.load(contract_yaml_path).families
