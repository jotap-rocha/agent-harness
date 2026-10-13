# Render dual-map Dev

**Status:** done  
**Blocked by:** tasks/fluxo-events-dev-loop-live/67-contrato-dev-loop-map.md, tasks/fluxo-events-dev-loop-live/68-helper-slug-from-prompt.md

## What to build

`render` escolhe `dev_loop_map` quando slug começa com `dev-loop-`; caso contrário
mantém `sdd_map`. HTML lista fases 0–6 + highlight ativo.

## Acceptance criteria

- [x] Slug `dev-loop-*` renderiza fases Dev Loop — tested by: `tests/fluxo_events/test_render_dual_map.py::test_render_dev_loop_map`
- [x] Slug SDD continua com mapa 0–4 — tested by: `tests/fluxo_events/test_render_dual_map.py::test_render_sdd_unchanged`
- [x] Highlight ativo a partir do último evento — tested by: `tests/fluxo_events/test_render_dual_map.py::test_dev_loop_highlight`

## Notes

AC2, AC5.
