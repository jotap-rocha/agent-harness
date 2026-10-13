"""Task 46 — adapters Claude/Cursor via fixtures stdin JSON."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from config.agent_policies.hooks import claude_pretooluse, cursor_before_shell

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return FIXTURES


def _run_module(module: str, payload: dict, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        [sys.executable, "-m", module],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
        env=merged,
        cwd=str(Path(__file__).resolve().parents[2]),
    )


def test_claude_deny_hard_blocks(fixtures_dir: Path) -> None:
    payload = json.loads((fixtures_dir / "claude_deny_rm.json").read_text(encoding="utf-8"))
    code, body = claude_pretooluse.handle_payload(payload)
    assert code == 2
    assert body["permission"] == "deny"
    assert body["family"] == "shell"


def test_cursor_deny_hard_permission(fixtures_dir: Path) -> None:
    payload = json.loads((fixtures_dir / "cursor_deny_rm.json").read_text(encoding="utf-8"))
    body = cursor_before_shell.handle_payload(payload)
    assert body["permission"] == "deny"
    assert body["family"] == "shell"


def test_ask_not_silent_allow_both_adapters(fixtures_dir: Path) -> None:
    claude_payload = json.loads(
        (fixtures_dir / "claude_ask_git.json").read_text(encoding="utf-8")
    )
    cursor_payload = json.loads(
        (fixtures_dir / "cursor_ask_git.json").read_text(encoding="utf-8")
    )
    c_code, c_body = claude_pretooluse.handle_payload(claude_payload)
    k_body = cursor_before_shell.handle_payload(cursor_payload)
    assert c_code == 0
    assert c_body["permission"] == "ask"
    assert k_body["permission"] == "ask"


def test_bypass_env_both_adapters(
    fixtures_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HARNESS_ALLOW_DESTRUCTIVE", "1")
    payload = json.loads((fixtures_dir / "claude_deny_rm.json").read_text(encoding="utf-8"))
    code, body = claude_pretooluse.handle_payload(payload)
    assert code == 0
    assert body["permission"] == "allow"
    assert body["bypassed"] is True

    cursor_payload = json.loads(
        (fixtures_dir / "cursor_deny_rm.json").read_text(encoding="utf-8")
    )
    k_body = cursor_before_shell.handle_payload(cursor_payload)
    assert k_body["permission"] == "allow"
    assert k_body["bypassed"] is True


def test_profile_extra_family_reaches_guard(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    repo_root: Path,
) -> None:
    """Extras opt-in via project_profile devem afetar o guard (task 47 wiring)."""
    monkeypatch.delenv("HARNESS_ALLOW_DESTRUCTIVE", raising=False)
    policies = tmp_path / ".harness" / "policies"
    policies.mkdir(parents=True)
    (policies / "project_profile.yaml").write_text(
        "families:\n  - cloud-cli-extra\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    # contrato ainda no canônico
    from config.agent_policies.guard import evaluate_command

    result = evaluate_command(
        "aws s3 rb s3://bucket --force",
        contract_path=repo_root / "agent-policies.yaml",
    )
    assert result.action == "deny"
    assert result.family_id == "cloud-cli-extra"


def test_subprocess_adapters_agree_on_deny(fixtures_dir: Path) -> None:
    payload = json.loads((fixtures_dir / "claude_deny_rm.json").read_text(encoding="utf-8"))
    # Cursor usa shape diferente; mapear comando
    cursor_payload = {"command": payload["tool_input"]["command"]}
    claude = _run_module("config.agent_policies.hooks.claude_pretooluse", payload)
    cursor = _run_module("config.agent_policies.hooks.cursor_before_shell", cursor_payload)
    assert claude.returncode == 2
    c_body = json.loads(claude.stdout.strip().splitlines()[-1])
    k_body = json.loads(cursor.stdout.strip().splitlines()[-1])
    assert c_body["permission"] == k_body["permission"] == "deny"
