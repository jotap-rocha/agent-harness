# Docs validar dogfood

**Status:** done  
**Blocked by:** tasks/fluxo-events-dev-loop-live/70-wiring-ux-crafter-executor.md, tasks/fluxo-events-dev-loop-live/71-truncate-exit-complete.md, tasks/fluxo-events-dev-loop-live/72-backfill-commits-58-65.md, tasks/fluxo-events-dev-loop-live/73-guardrail-naming-ptbr.md

## What to build

SHOULD: cheatsheet + addendum ADR-005 (ou ADR-006) com Dev Loop + naming + §1.3.
`/validar` / pytest `tests/fluxo_events/` verde. Dogfood opcional: emit num slug
`dev-loop-*`. Ortogonalidade evidence-gate documentada.

## Acceptance criteria

- [x] Cheatsheet menciona Dev Loop + naming PT-BR + §1.3 — tested by: `tests/fluxo_events/test_docs_dev_loop.py::test_cheatsheet_dev_loop` (ou waiver docs + grep)
- [x] ADR addendum presente — tested by: no test — docs review + waiver humano
- [x] Suite `tests/fluxo_events/` + ruff/mypy verdes — tested by: `/validar` / pytest path
- [x] Docs não unificam com evidence-gate (AC15) — tested by: `tests/fluxo_events/test_docs_dev_loop.py::test_orthogonal_mention`

## Notes

AC14, AC15, AC17. Fecha o pacote.

Revisor auto: aprovado com ressalvas — dogfood emit ok em `dev-loop-dogfood`; mirror
`.cursor/projetos/dev-loop-*` fail-soft (Errno 30 em sandbox). Suite `tests/fluxo_events/`
55 passed; ruff/mypy verdes. `commit: pending`. CLI `evidence_gate check --entregas` resolve
`evidencias_ref` relativo a `metrics/` (quirk pré-existente); check verde com
`ref_base=repo root` via API.

Revisor auto: Revisor: aprovado com ressalvas — dogfood emit ok; mirror cursor dogfood fail-soft (Errno 30). Suite 55 passed. commit pending.
