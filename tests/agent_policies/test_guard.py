"""Task 43 — bypass HARNESS_ALLOW_DESTRUCTIVE + fail closed/open."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.agent_policies.guard import (
    BYPASS_ENV,
    GuardResult,
    evaluate_command,
)


def test_bypass_allows_deny_hard_with_audit_log(
    contract_yaml_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv(BYPASS_ENV, "1")
    result = evaluate_command(
        "rm -rf /tmp/x",
        contract_path=contract_yaml_path,
    )
    assert result.action == "allow"
    assert result.bypassed is True
    assert result.family_id == "shell"
    assert result.pattern_id == "rm-rf"
    err = capsys.readouterr().err
    assert "bypass" in err.lower()
    assert "shell" in err
    assert "rm-rf" in err
    # sem secret/PII no log
    assert "password" not in err.lower()
    assert "token" not in err.lower()


def test_fail_closed_on_deny_path_when_contract_broken(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(BYPASS_ENV, raising=False)
    broken = tmp_path / "broken.yaml"
    broken.write_text("version: 1\nfamilies:\n", encoding="utf-8")
    result = evaluate_command(
        "rm -rf /tmp/x",
        contract_path=broken,
        assumed_severity="deny",
    )
    assert result.action == "deny"
    assert result.fail_mode == "closed"
    assert result.error


def test_fail_open_on_ask_path_when_contract_broken(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv(BYPASS_ENV, raising=False)
    broken = tmp_path / "broken.yaml"
    broken.write_text("version: 1\nfamilies:\n", encoding="utf-8")
    result = evaluate_command(
        "git push --force",
        contract_path=broken,
        assumed_severity="ask",
    )
    assert result.action == "allow"
    assert result.fail_mode == "open"
    assert "warn" in capsys.readouterr().err.lower() or result.warning


def test_without_bypass_deny_hard_stays_deny(
    contract_yaml_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(BYPASS_ENV, raising=False)
    result = evaluate_command(
        "docker volume rm myvol",
        contract_path=contract_yaml_path,
    )
    assert isinstance(result, GuardResult)
    assert result.action == "deny"
    assert result.bypassed is False
