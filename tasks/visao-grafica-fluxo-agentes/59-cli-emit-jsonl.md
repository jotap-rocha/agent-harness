# CLI emit JSONL

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md

## What to build

Implementar `python -m config.fluxo_events emit`: valida metadados (`event_type`, agent,
phase, task id opcional, timestamps), appenda 1 linha em
`projetos/{slug}/fluxo/events.jsonl`, auto-render por default (`--no-render` opt-out),
fail-soft (nunca exit hard que bloqueie SDD). Append best-effort sem lock (G2-a).

## Acceptance criteria

- [x] `emit` appenda 1 linha JSONL válida sob `fluxo/events.jsonl` — tested by: `tests/fluxo_events/test_emit.py::test_emit_appends_jsonl`
- [x] Campos fora do schema / PII-like rejeitados ou stripados conforme contrato — tested by: `tests/fluxo_events/test_emit.py::test_rejects_non_metadata`
- [x] FS error simulado → warning soft; caller não bloqueado (exit soft) — tested by: `tests/fluxo_events/test_emit.py::test_emit_fail_soft`
- [x] Dois emits sequenciais sem mutex — tested by: `tests/fluxo_events/test_emit.py::test_append_best_effort`
- [x] Fixtures sem prompt/PII/secret — tested by: `tests/fluxo_events/test_emit.py::test_fixtures_metadata_only`

## Notes

AC PRD: AC2, AC5, AC7, AC10. `event_type`: phase_enter/exit, agent_enter/exit, task_enter/exit.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/59.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

