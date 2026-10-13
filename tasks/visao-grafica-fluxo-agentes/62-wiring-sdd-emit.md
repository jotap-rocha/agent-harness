# Wiring SDD emit/ship

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/59-cli-emit-jsonl.md, tasks/visao-grafica-fluxo-agentes/60-render-live-html.md, tasks/visao-grafica-fluxo-agentes/61-rotate-truncate-ship.md

## What to build

Instruir enter/exit `emit` (fail soft) nos agents/skills SDD fases 0–4 e truncate+render
no `harness-ship`. Espelho dual-tree `.claude`↔`.cursor`. Não criar agent “fluxo officer”.
STATUS/scorecard permanecem; live é complementar.

## Acceptance criteria

- [x] Agents/skills SDD 0–4 documentam emit enter/exit fail-soft — tested by: `tests/fluxo_events/test_wiring_sdd.py::test_agents_mention_emit` (ou review checklist + pytest de presença de texto)
- [x] `harness-ship` documenta truncate `--keep 100` + re-render — tested by: `tests/fluxo_events/test_wiring_sdd.py::test_ship_mentions_truncate`
- [x] Espelho `.claude`↔`.cursor` dos artefatos de wiring tocados — tested by: `tests/fluxo_events/test_wiring_sdd.py::test_dual_tree_wiring_mirror`
- [x] Docs/agents não substituem STATUS/scorecard (AC14) — tested by: review — no test — prose constraint + waiver humano se só review

## Notes

AC PRD: AC11, AC14, AC16. Targets: brainstorm, grill-me, define, design, to-prd,
architect, to-tasks, build, revisor, ship, scorecard.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/62.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

