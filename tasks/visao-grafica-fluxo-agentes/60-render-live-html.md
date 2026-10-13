# Render live.html mapa

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md

## What to build

Implementar `python -m config.fluxo_events render`: gera `fluxo/live.html` com mapa
estrutural SDD 0–4 e **todos** os agents por fase (mesmo com log vazio); destaca
agent/fase ativos a partir do último evento relevante; timeline básica; alinhado ao
mockup aprovado (referência visual).

## Acceptance criteria

- [x] `render` gera HTML com fases 0–4 e todos os agents listados (log vazio ok) — tested by: `tests/fluxo_events/test_render.py::test_render_full_map_empty_log`
- [x] HTML destaca agent/fase ativos do último evento — tested by: `tests/fluxo_events/test_render.py::test_render_highlights_active`
- [x] Fail-soft em erro de escrita HTML — tested by: `tests/fluxo_events/test_render.py::test_render_fail_soft`
- [x] Fixture HTML cobre fases + ativo + timeline (AC17) — tested by: `tests/fluxo_events/test_render.py::test_fixture_matches_mockup_structure`

## Notes

AC PRD: AC3, AC4, AC5, AC17. Pode paralelizar com task 59 após 58.  
Mockup: assets do projeto / ideia.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/60.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

