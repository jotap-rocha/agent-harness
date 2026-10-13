"""Task 78 — build_causal_svg + dois SVGs no live.html."""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.emit import emit_event
from config.fluxo_events.render import (
    build_causal_svg,
    render_live,
)

CAUSAL_TYPES = frozenset({"phase_enter", "agent_enter", "task_enter"})
EXCLUDED = frozenset(
    {"phase_exit", "agent_exit", "task_exit", "ship_truncate"}
)


def _sample_events() -> list[dict]:
    root = "aaaaaaaa-bbbb-4ccc-8ddd-111111111111"
    child = "bbbbbbbb-cccc-4ddd-8eee-222222222222"
    task = "cccccccc-dddd-4eee-8fff-333333333333"
    return [
        {
            "event_type": "phase_enter",
            "phase": 3,
            "agent": "harness-build",
            "slug": "causal",
            "event_id": root,
            "run_id": "rrrrrrrr-rrrr-4rrr-8rrr-rrrrrrrrrrrr",
        },
        {
            "event_type": "agent_enter",
            "phase": 3,
            "agent": "harness-build",
            "slug": "causal",
            "event_id": child,
            "run_id": "rrrrrrrr-rrrr-4rrr-8rrr-rrrrrrrrrrrr",
            "parent_event_id": root,
        },
        {
            "event_type": "task_enter",
            "phase": 3,
            "agent": "harness-build",
            "task_id": "78",
            "slug": "causal",
            "event_id": task,
            "run_id": "rrrrrrrr-rrrr-4rrr-8rrr-rrrrrrrrrrrr",
            "parent_event_id": child,
        },
        {
            "event_type": "agent_exit",
            "phase": 3,
            "agent": "harness-build",
            "slug": "causal",
            "event_id": "dddddddd-eeee-4fff-8aaa-444444444444",
            "run_id": "rrrrrrrr-rrrr-4rrr-8rrr-rrrrrrrrrrrr",
            "parent_event_id": child,
        },
        {
            "event_type": "ship_truncate",
            "phase": 4,
            "agent": "harness-ship",
            "slug": "causal",
            "event_id": "eeeeeeee-ffff-4aaa-8bbb-555555555555",
            "run_id": "rrrrrrrr-rrrr-4rrr-8rrr-rrrrrrrrrrrr",
        },
    ]


def test_two_svgs_in_html(tmp_path: Path, contract_yaml_path: Path) -> None:
    proj = tmp_path / "projetos"
    emit_event(
        slug="two-svg",
        event_type="phase_enter",
        agent="harness-build",
        phase=3,
        contract_path=contract_yaml_path,
        projetos_root=proj,
        auto_render=True,
    )
    result = render_live(
        slug="two-svg",
        contract_path=contract_yaml_path,
        projetos_root=proj,
    )
    assert result.ok and result.html_path
    html = result.html_path.read_text(encoding="utf-8")
    assert 'data-testid="fluxograma"' in html
    assert 'data-testid="fluxograma-execucao"' in html
    assert "fluxograma-previsto" in html
    assert html.count("<svg") >= 2


def test_causal_node_types() -> None:
    svg = build_causal_svg(_sample_events())
    for et in EXCLUDED:
        assert f'data-event-type="{et}"' not in svg
    for et in ("phase_enter", "agent_enter", "task_enter"):
        assert f'data-event-type="{et}"' in svg
    assert 'data-event-type="ship_truncate"' not in svg


def test_phase_enter_is_root() -> None:
    svg = build_causal_svg(_sample_events())
    assert 'data-testid="fluxograma-causal"' in svg
    assert 'data-causal-role="root"' in svg
    assert 'data-event-type="phase_enter"' in svg


def test_truncated_id_labels() -> None:
    events = _sample_events()
    full = events[0]["event_id"]
    assert isinstance(full, str) and len(full) > 8
    svg = build_causal_svg(events)
    short = full[:8]
    assert short in svg
    assert "…" in svg or "..." in svg
    # Label visual truncado: o UUID completo pode existir em data-*, mas o texto usa short+…
    assert f">{short}…" in svg or f"{short}..." in svg


def test_empty_causal_svg() -> None:
    svg = build_causal_svg([])
    assert 'data-testid="fluxograma-causal"' in svg
