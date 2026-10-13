# Validar + dogfood slug

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/62-wiring-sdd-emit.md, tasks/visao-grafica-fluxo-agentes/63-install-foundation-seed.md, tasks/visao-grafica-fluxo-agentes/64-docs-adr-fluxo-live.md

## What to build

Fechar o pacote: `/validar` verde com `tests/fluxo_events/`; dogfood no próprio slug
`visao-grafica-fluxo-agentes` (emit/render sob `projetos/.../fluxo/`); evidências das
tasks 58–65; sync-context leve se CLAUDE/AGENTS mudaram. Não commit sem acordo.

## Acceptance criteria

- [x] `/validar` (ruff + mypy + pytest) verde incluindo `tests/fluxo_events/` — tested by: suite `/validar` / pytest path
- [x] Dogfood: `fluxo/events.jsonl` + `live.html` no slug do projeto — tested by: `tests/fluxo_events/test_dogfood.py::test_project_fluxo_artifacts` (ou smoke CLI no path do slug)
- [x] Manifestos evidence-gate das tasks deste pacote com `collect|check` quando aplicável — tested by: `python -m config.evidence_gate check` por task
- [x] Espelho dual-tree do dogfood `fluxo/` se gerado sob `.claude/projetos/` — tested by: checklist AC11 / filecmp smoke

## Notes

AC PRD: AC11, AC12. Ship do projeto só depois: `harness-ship` + retro.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/65.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

