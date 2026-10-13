"""Grafo visual (fluxograma SVG) — nós, setas, caminho executado e dual-map.

Test-first: o render deve produzir um fluxograma SVG com nós de fase, nós de
agente e arestas com seta entre fases consecutivas, destacando o caminho já
executado e o nó ativo. Mantém compat com o painel de fases + timeline.
"""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import live_html_path
from config.fluxo_events.render import build_flow_svg, render_live
from config.fluxo_events.contract import SddPhase


def _read(tmp_path: Path, slug: str) -> str:
    return live_html_path(tmp_path / "projetos", slug).read_text(encoding="utf-8")


def test_svg_present_with_nodes_and_edges(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    render_live(
        slug="grafo-sdd",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    content = _read(tmp_path, "grafo-sdd")
    assert "<svg" in content
    assert 'data-testid="fluxograma"' in content
    # nó de cada fase 0–4
    for phase in range(5):
        assert f'data-node-phase="{phase}"' in content
    # arestas entre fases consecutivas (4 arestas p/ 5 fases)
    assert content.count('class="edge') >= 4
    # seta (marker) definida
    assert "marker" in content and "arrow" in content.lower()
    # nós de agente
    assert 'data-node-agent="harness-brainstorm"' in content
    assert 'data-node-agent="harness-ship"' in content


def test_svg_highlights_executed_path(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    for phase, agent in ((0, "harness-brainstorm"), (1, "grill-me"), (2, "harness-design")):
        emit_event(
            slug="grafo-path",
            event_type="agent_enter",
            agent=agent,
            phase=phase,
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            auto_render=(phase == 2),
        )
    content = _read(tmp_path, "grafo-path")
    # fase ativa (2) marcada como ativa no grafo
    assert 'data-node-phase="2"' in content
    assert "node phase active" in content or 'class="node phase active"' in content
    # caminho executado (fases 0..2) marcado como done
    assert content.count("done") >= 2
    # agente ativo no grafo
    assert 'data-node-agent="harness-design"' in content
    assert "node-agent active" in content


def test_svg_dev_loop_has_seven_phases(
    tmp_path: Path,
    contract_yaml_path: Path,
) -> None:
    render_live(
        slug="dev-loop-grafo",
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
    )
    content = _read(tmp_path, "dev-loop-grafo")
    for phase in range(7):
        assert f'data-node-phase="{phase}"' in content
    assert 'data-node-phase="6"' in content
    assert 'data-node-agent="dev-loop-executor"' in content
    # SDD não deve vazar no grafo Dev
    assert 'data-node-agent="harness-brainstorm"' not in content


def test_build_flow_svg_pure_function() -> None:
    phases = (
        SddPhase(phase=0, slug="IDEIA", agents=("harness-brainstorm",)),
        SddPhase(phase=1, slug="REQUISITOS", agents=("grill-me", "harness-define")),
    )
    from config.fluxo_events.render import ActiveState

    svg = build_flow_svg(
        phases=phases,
        active=ActiveState(phase=1, agent="grill-me"),
        is_dev=False,
    )
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert 'data-node-phase="0"' in svg
    assert 'data-node-phase="1"' in svg
    assert 'data-node-agent="grill-me"' in svg
    # aresta única entre 2 fases
    assert svg.count("<line") >= 1 or svg.count("<path") >= 1
    # escape seguro (sem tag crua injetada)
    assert "<script" not in svg
