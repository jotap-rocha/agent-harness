"""Task 77 — CLI emit --run-id / --parent-event-id."""

from __future__ import annotations

import json
from pathlib import Path

from config.fluxo_events.cli import main
from config.fluxo_events.paths import fluxo_dir_for_slug


def test_emit_cli_run_and_parent(
    tmp_path: Path, contract_yaml_path: Path, capsys: object
) -> None:
    proj = tmp_path / "projetos"
    run_id = "bbbbbbbb-cccc-4ddd-8eee-ffffffffffff"
    parent = "cccccccc-dddd-4eee-8fff-000000000000"
    code = main(
        [
            "emit",
            "--slug",
            "cli-causal",
            "--event-type",
            "agent_enter",
            "--agent",
            "harness-build",
            "--phase",
            "3",
            "--run-id",
            run_id,
            "--parent-event-id",
            parent,
            "--projetos-root",
            str(proj),
            "--contract",
            str(contract_yaml_path),
            "--no-render",
        ]
    )
    assert code == 0
    events = fluxo_dir_for_slug(proj, "cli-causal") / "events.jsonl"
    assert events.is_file()
    payload = json.loads(events.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert payload["run_id"] == run_id
    assert payload["parent_event_id"] == parent
    assert "event_id" in payload
