"""Task 76 — stack fail-soft de parent_event_id (sem mutex)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import fluxo_dir_for_slug
from config.fluxo_events.stack import STACK_FILENAME, peek_parent, push_event, stack_path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_explicit_parent_wins(tmp_path: Path, contract_yaml_path: Path) -> None:
    proj = tmp_path / "projetos"
    push_event(proj, "stack-demo", "stack-top-aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee")
    explicit = "explicit-1111-4aaa-8bbb-cccccccccccc"
    result = emit_event(
        slug="stack-demo",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=proj,
        auto_render=False,
        parent_event_id=explicit,
    )
    assert result.ok and result.line
    payload = json.loads(result.line)
    assert payload["parent_event_id"] == explicit


def test_uses_stack_top(tmp_path: Path, contract_yaml_path: Path) -> None:
    proj = tmp_path / "projetos"
    parent_id = "parent-2222-4aaa-8bbb-dddddddddddd"
    push_event(proj, "stack-demo", parent_id)
    result = emit_event(
        slug="stack-demo",
        event_type="agent_enter",
        agent="harness-define",
        phase=1,
        contract_path=contract_yaml_path,
        projetos_root=proj,
        auto_render=False,
    )
    assert result.ok and result.line
    payload = json.loads(result.line)
    assert payload["parent_event_id"] == parent_id


def test_stack_path_and_gitignore() -> None:
    assert STACK_FILENAME == "stack.json"
    sample = stack_path(Path("/tmp/projetos"), "my-slug")
    assert sample.as_posix().endswith("my-slug/fluxo/stack.json")
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "stack.json" in gitignore
    assert "fluxo" in gitignore or "**/fluxo/stack.json" in gitignore


def test_stack_fail_soft(tmp_path: Path, contract_yaml_path: Path) -> None:
    """FS error na stack → warning soft; emit não bloqueia."""
    proj = tmp_path / "projetos"

    def boom(*_a: Any, **_k: Any) -> None:
        raise OSError("permission denied")

    with patch("config.fluxo_events.stack._read_stack", side_effect=boom):
        parent, warn = peek_parent(proj, "stack-demo")
        assert parent is None
        assert warn

    with patch(
        "config.fluxo_events.stack._read_stack",
        side_effect=OSError("disk full"),
    ):
        result = emit_event(
            slug="stack-demo",
            event_type="agent_enter",
            agent="harness-build",
            phase=3,
            contract_path=contract_yaml_path,
            projetos_root=proj,
            auto_render=False,
        )
    assert result.ok
    assert result.line
    payload = json.loads(result.line)
    # órfão ok — sem parent quando stack falha
    assert "parent_event_id" not in payload or payload.get("parent_event_id") is None
    # diretório fluxo existe (emit seguiu)
    assert fluxo_dir_for_slug(proj, "stack-demo").is_dir()
