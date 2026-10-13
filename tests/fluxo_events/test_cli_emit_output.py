"""CLI emit — --print-event-id / --json (Dev Loop FLUXO_EMIT_RUNTIME)."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

from config.fluxo_events.cli import main
from config.fluxo_events.emit import parse_emit_line
from config.fluxo_events.paths import fluxo_dir_for_slug
from config.fluxo_events.render import ActiveState, build_execution_trail_svg

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)


def test_parse_emit_line_extracts_ids() -> None:
    line = '{"event_id":"aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeeeee","run_id":"11111111-2222-4333-8444-555555555555"}'
    eid, rid = parse_emit_line(line)
    assert eid == "aaaaaaaa-bbbb-4ccc-dddd-eeeeeeeeeeee"
    assert rid == "11111111-2222-4333-8444-555555555555"


def test_emit_default_stdout_legacy(
    tmp_path: Path, contract_yaml_path: Path, capsys: object
) -> None:
    proj = tmp_path / "projetos"
    code = main(
        [
            "emit",
            "--slug",
            "cli-out-default",
            "--event-type",
            "agent_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--projetos-root",
            str(proj),
            "--contract",
            str(contract_yaml_path),
            "--no-render",
        ]
    )
    assert code == 0
    out = capsys.readouterr()
    assert out.out.startswith("ok: appended ")
    assert UUID_RE.search(out.out) is None


def test_emit_print_event_id_stdout_uuid_only(
    tmp_path: Path, contract_yaml_path: Path, capsys: object
) -> None:
    proj = tmp_path / "projetos"
    code = main(
        [
            "emit",
            "--slug",
            "cli-out-event-id",
            "--event-type",
            "agent_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--print-event-id",
            "--projetos-root",
            str(proj),
            "--contract",
            str(contract_yaml_path),
            "--no-render",
        ]
    )
    assert code == 0
    out = capsys.readouterr()
    printed = out.out.strip()
    assert UUID_RE.match(printed)
    uuid.UUID(printed)
    events = fluxo_dir_for_slug(proj, "cli-out-event-id") / "events.jsonl"
    payload = json.loads(events.read_text(encoding="utf-8").strip())
    assert payload["event_id"] == printed


def test_emit_json_stdout_full_line(
    tmp_path: Path, contract_yaml_path: Path, capsys: object
) -> None:
    proj = tmp_path / "projetos"
    code = main(
        [
            "emit",
            "--slug",
            "cli-out-json",
            "--event-type",
            "agent_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--json",
            "--projetos-root",
            str(proj),
            "--contract",
            str(contract_yaml_path),
            "--no-render",
        ]
    )
    assert code == 0
    out = capsys.readouterr()
    payload = json.loads(out.out.strip())
    assert payload["event_type"] == "agent_enter"
    assert payload["agent"] == "harness-build"


def test_emit_print_event_id_and_json_mutually_exclusive(capsys: object) -> None:
    code = main(
        [
            "emit",
            "--slug",
            "x",
            "--event-type",
            "agent_enter",
            "--agent",
            "a",
            "--phase",
            "0",
            "--print-event-id",
            "--json",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "mutually exclusive" in err


def test_cli_build_enter_then_task_render_shows_exec_task(
    tmp_path: Path, contract_yaml_path: Path, capsys: object
) -> None:
    """Integração: captura event_id → task_enter com parent → SVG contém exec-task."""
    proj = tmp_path / "projetos"
    slug = "cli-runtime-chain"
    base = [
        "--projetos-root",
        str(proj),
        "--contract",
        str(contract_yaml_path),
        "--no-render",
    ]
    code = main(
        [
            "emit",
            "--slug",
            slug,
            "--event-type",
            "agent_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--print-event-id",
            *base,
        ]
    )
    assert code == 0
    build_enter_id = capsys.readouterr().out.strip()
    assert UUID_RE.match(build_enter_id)

    code = main(
        [
            "emit",
            "--slug",
            slug,
            "--event-type",
            "task_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--task-id",
            "99",
            "--parent-event-id",
            build_enter_id,
            *base,
        ]
    )
    assert code == 0

    events_file = fluxo_dir_for_slug(proj, slug) / "events.jsonl"
    events = [
        json.loads(line)
        for line in events_file.read_text(encoding="utf-8").strip().splitlines()
    ]
    svg = build_execution_trail_svg(events, ActiveState(phase=3, agent="harness-build"))
    assert "exec-task" in svg
    assert "task 99" in svg
