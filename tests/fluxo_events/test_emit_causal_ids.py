"""Task 75 — emit gera event_id / run_id / parent_event_id (schema aditivo)."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

from config.fluxo_events.emit import ALLOWED_KEYS, emit_event
from config.fluxo_events.paths import fluxo_dir_for_slug
from config.fluxo_events.render import build_html, derive_active_state
from config.fluxo_events.contract import SddPhase

UUID_V4 = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.I,
)


def test_allowed_keys_include_causal() -> None:
    assert "event_id" in ALLOWED_KEYS
    assert "run_id" in ALLOWED_KEYS
    assert "parent_event_id" in ALLOWED_KEYS


def test_generates_event_id(tmp_path: Path, contract_yaml_path: Path) -> None:
    result = emit_event(
        slug="causal-demo",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    assert result.ok and result.line
    payload = json.loads(result.line)
    assert UUID_V4.match(payload["event_id"])
    uuid.UUID(payload["event_id"], version=4)


def test_run_id_auto_and_override(tmp_path: Path, contract_yaml_path: Path) -> None:
    r1 = emit_event(
        slug="causal-demo",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    assert r1.ok and r1.line
    p1 = json.loads(r1.line)
    assert UUID_V4.match(p1["run_id"])

    fixed = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
    r2 = emit_event(
        slug="causal-demo",
        event_type="task_enter",
        agent="harness-build",
        phase=3,
        task_id="75",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
        run_id=fixed,
    )
    assert r2.ok and r2.line
    p2 = json.loads(r2.line)
    assert p2["run_id"] == fixed


def test_legacy_events_without_ids(tmp_path: Path, contract_yaml_path: Path) -> None:
    """Eventos antigos sem IDs ainda carregam e renderizam (órfãos ok)."""
    legacy = {
        "event_type": "agent_enter",
        "ts": "2026-01-01T00:00:00+00:00",
        "phase": 3,
        "agent": "harness-build",
        "slug": "legacy-slug",
    }
    assert "event_id" not in legacy
    phases = (
        SddPhase(phase=3, slug="IMPLEMENTAR", agents=("harness-build",)),
    )
    html = build_html(
        slug="legacy-slug",
        phase_map=phases,
        events=[legacy],
        active=derive_active_state([legacy]),
    )
    assert "fluxograma" in html
    assert "harness-build" in html


def test_fixtures_metadata_only(tmp_path: Path, contract_yaml_path: Path) -> None:
    forbidden = ("prompt", "password", "secret", "cpf", "token", "api_key")
    result = emit_event(
        slug="causal-demo",
        event_type="agent_exit",
        agent="grill-me",
        phase=1,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
        source="cli",
    )
    assert result.ok and result.line
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
    events = fluxo_dir_for_slug(tmp_path / "projetos", "causal-demo") / "events.jsonl"
    assert events.is_file()
