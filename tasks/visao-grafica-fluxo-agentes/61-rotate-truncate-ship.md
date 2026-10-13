# Rotate + truncate ship

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/59-cli-emit-jsonl.md, tasks/visao-grafica-fluxo-agentes/60-render-live-html.md

## What to build

Cap 2 MiB no append: overflow → rotate mantém **tail** + warning soft (não fail hard).
CLI `truncate --keep N` (default N=100): reduz `events.jsonl` e re-render. Preparar
gancho para wiring do ship (task 62).

## Acceptance criteria

- [x] Overflow 2 MiB → rotate keep tail + warning soft — tested by: `tests/fluxo_events/test_rotate.py::test_rotate_keeps_tail`
- [x] `truncate --keep 100` deixa ≤ 100 linhas e re-render — tested by: `tests/fluxo_events/test_truncate.py::test_truncate_keep_100`
- [x] `ship_truncate` (ou equivalente) registrável como evento metadado — tested by: `tests/fluxo_events/test_truncate.py::test_ship_truncate_event`
- [x] Truncate fail-soft se FS falhar — tested by: `tests/fluxo_events/test_truncate.py::test_truncate_fail_soft`

## Notes

AC PRD: AC6, AC8. Naming: `python -m config.fluxo_events truncate`.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/61.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

