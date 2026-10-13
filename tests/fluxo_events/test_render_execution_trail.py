"""Opção C — trilha de execução real + resumo + timeline humana."""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import live_html_path
from config.fluxo_events.render import (
    ActiveState,
    agent_enter_completed,
    build_execution_trail_svg,
    build_human_timeline_items,
    build_resumo_html,
    extract_agent_enter_trail,
    render_live,
)


def _silver_like_events() -> list[dict]:
    agents = (
        ("harness-brainstorm", 0, "t0"),
        ("grill-me", 1, "t1"),
        ("harness-define", 1, "t2"),
        ("harness-design", 2, "t3"),
        ("to-tasks", 3, "t4"),
        ("harness-build", 3, "t5"),
        ("revisor-codigo", 4, "t6"),
        ("harness-ship", 4, "t7"),
    )
    events: list[dict] = []
    for agent, phase, ts in agents:
        events.append(
            {
                "event_type": "agent_enter",
                "agent": agent,
                "phase": phase,
                "ts": f"2026-08-19T14:{ts}",
            }
        )
        events.append(
            {
                "event_type": "agent_exit",
                "agent": agent,
                "phase": phase,
                "ts": f"2026-08-19T15:{ts}",
            }
        )
    return events


def test_extract_trail_collapses_consecutive_same_agent() -> None:
    events = [
        {"event_type": "agent_enter", "agent": "a", "ts": "1"},
        {"event_type": "agent_enter", "agent": "a", "ts": "2"},
        {"event_type": "agent_enter", "agent": "b", "ts": "3"},
    ]
    trail = extract_agent_enter_trail(events)
    assert [e["agent"] for e in trail] == ["a", "b"]


def test_execution_svg_agent_names_only() -> None:
    events = _silver_like_events()
    svg = build_execution_trail_svg(events, ActiveState(phase=4, agent="harness-ship"))
    assert 'data-testid="fluxograma-execucao"' in svg
    assert "harness-brainstorm" in svg
    assert "harness-ship" in svg
    assert "agent_enter" not in svg
    assert "91f0872c" not in svg
    assert svg.count("exec-edge") == 7
    assert 'marker-end="url(#exec-arrow)"' in svg


def test_resumo_lists_used_agents_with_phases() -> None:
    html = build_resumo_html(_silver_like_events(), ActiveState(phase=4, agent="harness-ship"))
    assert "8 agentes utilizados" in html
    assert 'data-agent="grill-me"' in html
    assert 'data-phase="1"' in html
    assert "✓" in html


def test_human_timeline_no_raw_event_types() -> None:
    items = build_human_timeline_items(_silver_like_events())
    joined = "".join(items)
    assert "agent_enter" not in joined
    assert "agent_exit" not in joined
    assert "concluído" in joined
    assert "<strong>grill-me</strong>" in joined


def test_agent_enter_completed() -> None:
    events = [
        {"event_type": "agent_enter", "agent": "x", "ts": "2026-01-01T10:00:00"},
        {"event_type": "agent_exit", "agent": "x", "ts": "2026-01-01T10:05:00"},
    ]
    assert agent_enter_completed(events, events[0]) is True


def test_build_with_tasks_and_delegates_under_build() -> None:
    build_id = "bbbbbbbb-cccc-4ddd-8eee-build00000001"
    events = [
        {
            "event_type": "agent_enter",
            "agent": "harness-build",
            "phase": 3,
            "event_id": build_id,
            "ts": "2026-08-19T10:00:00",
        },
        {
            "event_type": "task_enter",
            "agent": "harness-build",
            "phase": 3,
            "task_id": "82",
            "parent_event_id": build_id,
            "ts": "2026-08-19T10:05:00",
        },
        {
            "event_type": "task_exit",
            "agent": "harness-build",
            "phase": 3,
            "task_id": "82",
            "parent_event_id": build_id,
            "ts": "2026-08-19T10:20:00",
        },
        {
            "event_type": "agent_enter",
            "agent": "revisor-codigo",
            "phase": 3,
            "parent_event_id": build_id,
            "ts": "2026-08-19T10:25:00",
            "event_id": "cccccccc-dddd-4eee-8fff-revisor001",
        },
        {
            "event_type": "agent_exit",
            "agent": "revisor-codigo",
            "phase": 3,
            "parent_event_id": build_id,
            "ts": "2026-08-19T10:30:00",
        },
        {
            "event_type": "agent_exit",
            "agent": "harness-build",
            "phase": 3,
            "parent_event_id": build_id,
            "ts": "2026-08-19T11:00:00",
        },
    ]
    svg = build_execution_trail_svg(events, ActiveState(phase=3, agent="harness-build"))
    assert "exec-task" in svg
    assert "task 82" in svg
    assert "exec-delegate" in svg
    assert "→ revisor-codigo" in svg
    resumo = build_resumo_html(events, ActiveState(phase=3, agent="harness-build"))
    assert "resumo-sub" in resumo
    assert "task 82" in resumo
    assert "→ revisor-codigo" in resumo
    assert "1 task" in resumo
    timeline = "".join(build_human_timeline_items(events))
    assert "↳" in timeline
    assert "task 82" in timeline


def test_live_html_option_c_layout(tmp_path: Path, contract_yaml_path: Path) -> None:
    slug = "opcao-c-layout"
    for agent, phase in (("harness-brainstorm", 0), ("grill-me", 1)):
        emit_event(
            slug=slug,
            event_type="agent_enter",
            agent=agent,
            phase=phase,
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            auto_render=False,
        )
    render_live(
        slug=slug,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    content = live_html_path(tmp_path / "projetos", slug).read_text(encoding="utf-8")
    assert "Mapa previsto" in content
    assert "Execução real" in content
    assert 'data-testid="fluxograma-execucao"' in content
    assert 'data-testid="resumo-execucao"' in content
    assert "fluxograma-previsto" in content
    assert "Grafo causal" not in content
    assert "agent_enter" not in content
    assert 'data-node-phase="0"' in content
    assert 'data-node-phase="4"' in content
