"""Task 60 — render live.html mapa SDD."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import fluxo_dir_for_slug, live_html_path
from config.fluxo_events.render import RenderResult, render_live


def test_render_full_map_empty_log(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    result = render_live(
        slug="empty-slug",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    assert result.ok
    html_path = live_html_path(tmp_path / "projetos", "empty-slug")
    assert html_path.is_file()
    content = html_path.read_text(encoding="utf-8")
    for phase in range(5):
        assert f'data-phase="{phase}"' in content
    for agent in (
        "harness-brainstorm",
        "grill-me",
        "harness-define",
        "harness-design",
        "to-prd",
        "harness-architect",
        "to-tasks",
        "harness-build",
        "revisor-codigo",
        "harness-ship",
        "/scorecard",
    ):
        assert agent in content
    assert 'data-testid="timeline"' in content


def test_render_highlights_active(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    emit_event(
        slug="active-slug",
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=True,
    )
    html_path = live_html_path(tmp_path / "projetos", "active-slug")
    content = html_path.read_text(encoding="utf-8")
    assert 'data-phase="3"' in content
    assert 'data-agent="harness-build"' in content
    assert "exec-node active" in content or "resumo-item active" in content


def test_render_fail_soft(tmp_path: Path, contract_yaml_path: Path) -> None:
    import config.fluxo_events.render as render_mod

    with patch.object(
        render_mod,
        "_write_html",
        side_effect=OSError("readonly"),
    ):
        result = render_live(
            slug="soft-slug",
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
        )
    assert isinstance(result, RenderResult)
    assert result.ok is False
    assert result.soft is True
    assert result.warning


def test_fixture_matches_mockup_structure(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    """AC17: HTML cobre fases + ativo + timeline."""
    emit_event(
        slug="mockup-slug",
        event_type="phase_enter",
        agent="harness-design",
        phase=2,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    emit_event(
        slug="mockup-slug",
        event_type="agent_enter",
        agent="harness-design",
        phase=2,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=True,
    )
    content = live_html_path(tmp_path / "projetos", "mockup-slug").read_text(
        encoding="utf-8"
    )
    assert "Mapa previsto" in content or "Mapa SDD 0–4" in content or "Mapa SDD 0-4" in content
    assert "Atividade" in content or "Timeline" in content
    assert "harness-design" in content
    assert "exec-node active" in content or "resumo-item active" in content
    # log dir exists
    assert (fluxo_dir_for_slug(tmp_path / "projetos", "mockup-slug") / "events.jsonl").is_file()
