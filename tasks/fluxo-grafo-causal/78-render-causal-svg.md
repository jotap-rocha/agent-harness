# Render causal SVG

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/75-emit-causal-ids.md

## What to build

`build_causal_svg(events)` + `live.html` com **dois** SVGs (canônico existente + causal
`data-testid="fluxograma-causal"`). Nós: `phase_enter` (raiz) + `agent_enter` +
`task_enter`; sem exits/truncate no SVG causal. IDs truncados visualmente (SHOULD).
Dual-map SDD/Dev intacto.

## Acceptance criteria

- [x] HTML contém dois SVGs (canônico + causal) — tested by: `tests/fluxo_events/test_render_causal.py::test_two_svgs_in_html`
- [x] Nós causal só dos tipos permitidos — tested by: `tests/fluxo_events/test_render_causal.py::test_causal_node_types`
- [x] `phase_enter` atua como raiz quando presente — tested by: `tests/fluxo_events/test_render_causal.py::test_phase_enter_is_root`
- [x] Labels de UUID truncados no SVG — tested by: `tests/fluxo_events/test_render_causal.py::test_truncated_id_labels`
- [x] Dual-map `dev-loop-*` permanece verde — tested by: `tests/fluxo_events/test_render_dual_map.py` (regressão)

## Notes

AC7–10, AC14. Função pura testável; offline; sem JS.

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
