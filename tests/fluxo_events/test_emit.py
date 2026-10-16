"""Task 59 — CLI emit JSONL (test-first)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from config.fluxo_events.emit import EmitResult, emit_event
from config.fluxo_events.paths import fluxo_dir_for_slug


def test_emit_appends_jsonl(tmp_path: Path, contract_yaml_path: Path) -> None:
    result = emit_event(
        slug="demo-slug",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    assert result.ok
    assert result.soft is False
    events = fluxo_dir_for_slug(tmp_path / "projetos", "demo-slug") / "events.jsonl"
    assert events.is_file()
    lines = events.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["event_type"] == "agent_enter"
    assert payload["agent"] == "harness-build"
    assert payload["phase"] == 3
    assert payload["slug"] == "demo-slug"
    assert "ts" in payload


def test_rejects_non_metadata(tmp_path: Path, contract_yaml_path: Path) -> None:
    result = emit_event(
        slug="demo-slug",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
        extra={"prompt": "segredo do usuário", "cpf": "12345678901"},
    )
    assert result.ok is False or "prompt" not in (result.line or "")
    events = fluxo_dir_for_slug(tmp_path / "projetos", "demo-slug") / "events.jsonl"
    if events.is_file() and events.read_text(encoding="utf-8").strip():
        line = events.read_text(encoding="utf-8").strip().splitlines()[-1]
        assert "prompt" not in line
        assert "cpf" not in line
        assert "segredo" not in line


def test_emit_fail_soft(tmp_path: Path, contract_yaml_path: Path) -> None:
    """FS error → warning soft; caller não bloqueado (ok soft, sem raise)."""
    with patch(
        "config.fluxo_events.rotate.append_with_rotate",
        side_effect=OSError("disk full"),
    ):
        result = emit_event(
            slug="demo-slug",
            event_type="phase_enter",
            agent="harness-brainstorm",
            phase=0,
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            auto_render=False,
        )
    assert isinstance(result, EmitResult)
    assert result.soft is True
    assert result.ok is False
    assert result.warning


def test_append_best_effort(tmp_path: Path, contract_yaml_path: Path) -> None:
    """Dois emits sequenciais sem mutex (G2-a)."""
    kwargs = {
        "slug": "demo-slug",
        "event_type": "task_enter",
        "agent": "harness-build",
        "phase": 3,
        "task_id": "59",
        "contract_path": contract_yaml_path,
        "projetos_root": tmp_path / "projetos",
        "auto_render": False,
    }
    r1 = emit_event(**kwargs)  # type: ignore[arg-type]
    r2 = emit_event(
        slug="demo-slug",
        event_type="task_exit",
        agent="harness-build",
        phase=3,
        task_id="59",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    assert r1.ok and r2.ok
    assert r1.event_id and r1.run_id
    events = fluxo_dir_for_slug(tmp_path / "projetos", "demo-slug") / "events.jsonl"
    lines = events.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2


def test_fixtures_metadata_only(tmp_path: Path, contract_yaml_path: Path) -> None:
    """AC10: fixtures sem prompt/PII/secret."""
    forbidden = ("prompt", "password", "secret", "cpf", "token", "api_key")
    result = emit_event(
        slug="demo-slug",
        event_type="agent_exit",
        agent="grill-me",
        phase=1,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
        source="cli",
    )
    assert result.ok
    assert result.line
    lowered = result.line.lower()
    for word in forbidden:
        assert word not in lowered
    payload = json.loads(result.line)
    allowed = {
        "event_type",
        "ts",
        "phase",
        "agent",
        "task_id",
        "slug",
        "source",
        "event_id",
        "run_id",
        "parent_event_id",
    }
    assert set(payload.keys()) <= allowed
