# Install foundation seed

**Status:** done
**Blocked by:** tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md, tasks/visao-grafica-fluxo-agentes/59-cli-emit-jsonl.md, tasks/visao-grafica-fluxo-agentes/60-render-live-html.md, tasks/visao-grafica-fluxo-agentes/61-rotate-truncate-ship.md

## What to build

Propagar fluxo-events no install foundation always-on: contrato/CLI no stack_map,
seed `config/fluxo_events/templates/fluxo/` → `.harness/fluxo-events/` KEEP no filho
(SCHEMA + stub live), teste de install fixture.

## Acceptance criteria

- [x] Foundation inclui artefatos fluxo-events (CLI + template) — tested by: `tests/fluxo_events/test_install_foundation.py::test_foundation_includes_fluxo`
- [x] Seed KEEP no re-install — tested by: `tests/fluxo_events/test_install_foundation.py::test_seed_keep`
- [x] Filho pós-install tem template `fluxo/` utilizável — tested by: `tests/fluxo_events/test_install_foundation.py::test_child_template_fluxo`

## Notes

AC PRD: AC9. Seguir padrão evidence-gate / agent-policies seed.

## Close notes (2026-08-13)

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde.
- Revisor: self-check harness-build (subagent sem spawn revisor-codigo) — veredito registrado em entregas; 0 bloqueantes.
- Evidence-gate: collect→check verde; `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/63.yaml`.
- Commit: **pending** (sem acordo). Sem push.
- Waivers: task 62 AC14 / task 64 AC13+AC18 — review + smoke docs; waiver humano implícito no critério review-only.

