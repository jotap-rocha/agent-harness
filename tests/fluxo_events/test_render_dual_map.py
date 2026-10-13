"""Task 69 — render dual-map (SDD vs Dev Loop)."""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import live_html_path
from config.fluxo_events.render import render_live


def test_render_dev_loop_map(tmp_path: Path, contract_yaml_path: Path) -> None:
    result = render_live(
        slug="dev-loop-cache",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    assert result.ok
    content = live_html_path(tmp_path / "projetos", "dev-loop-cache").read_text(
        encoding="utf-8"
    )
    for phase in range(7):
        assert f'data-phase="{phase}"' in content
    for label in (
        "LOAD",
        "VALIDATE",
        "INIT_PICK",
        "EXECUTE_VERIFY",
        "UPDATE_CHECK",
        "LOOP_LOG",
        "SYNC",
    ):
        assert label in content
    assert "prompt-crafter" in content
    assert "dev-loop-executor" in content
    assert "Dev Loop" in content or "dev-loop" in content.lower()
    assert "harness-brainstorm" not in content


def test_render_sdd_unchanged(tmp_path: Path, contract_yaml_path: Path) -> None:
    result = render_live(
        slug="meu-projeto",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    assert result.ok
    content = live_html_path(tmp_path / "projetos", "meu-projeto").read_text(
        encoding="utf-8"
    )
    for phase in range(5):
        assert f'data-phase="{phase}"' in content
    assert 'data-phase="5"' not in content
    assert "IDEIA" in content
    assert "harness-brainstorm" in content
    assert "INIT_PICK" not in content
    assert "EXECUTE_VERIFY" not in content
    assert "prompt-crafter" not in content


def test_dev_loop_highlight(tmp_path: Path, contract_yaml_path: Path) -> None:
    emit_event(
        slug="dev-loop-foo",
        event_type="agent_enter",
        agent="dev-loop-executor",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=True,
    )
    content = live_html_path(tmp_path / "projetos", "dev-loop-foo").read_text(
        encoding="utf-8"
    )
    assert 'data-phase="3"' in content
    assert 'data-agent="dev-loop-executor"' in content
    assert "EXECUTE_VERIFY" in content or "Execução real" in content
