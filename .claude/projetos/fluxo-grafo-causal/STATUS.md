# Fluxo — Grafo Causal Real
Slug: fluxo-grafo-causal
Iniciado em: 2026-08-18

## SI Assessment: Nível a

## Tipo: e — Evolução do harness canônico

## Fase atual: CONCLUÍDO — Projeto arquivado

## Checklist
- [x] 0. Ideia + SI assessment (2026-08-18)
- [x] 0b. Codebase-explorer (pulado — b)
- [x] 1. Grill + define → `01-grill.md` (2026-08-18)
- [x] 1b. Judge define (b) pulado
- [x] 2. PRD gerado → `02-prd.md` (2026-08-18)
- [x] 2b. Judge PRD (b) pulado
- [x] 3. Harness montado → `03-harness.md` (2026-08-18)
- [x] 4. Tasks criadas → `04-tasks-index.md` + `tasks/…/75`–`81` (2026-08-18)
- [x] 5. Implementação concluída (2026-08-18)
- [x] 6. Ship / retrospectiva (2026-08-18)

## Resultado final

Schema aditivo `event_id`/`run_id`/`parent_event_id`, stack fail-soft (`stack.json`
gitignore), CLI `--run-id`/`--parent-event-id`, `live.html` com SVG canônico + causal,
wiring SDD/Dev, docs/ADR. Evidence-gate 75–81 verde; suite `tests/fluxo_events/` 79 passed.

## Git
- Branch: `feat/fluxo-grafo-causal`
- Soft-block: fetch Azure 403
- Commit tip: `5912c73` (entregas `57085aa`)
## Tasks
75–81 **done** (evidence-gate revalidado no ship)
