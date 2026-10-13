# Wiring UX crafter/executor

**Status:** done  
**Blocked by:** tasks/fluxo-events-dev-loop-live/68-helper-slug-from-prompt.md, tasks/fluxo-events-dev-loop-live/69-render-dual-map-dev.md

## What to build

Instruir emit + aviso UX (path `live.html` / http.server / `/fluxo-live`) em
`prompt-crafter`, `dev-loop-executor`, `/dev` e `DEV-LOOP.md`. Dry-run **não** emite.
Espelho dual-tree.

## Acceptance criteria

- [x] Crafter e executor mencionam emit + aviso UX + `dev-loop-` — tested by: `tests/fluxo_events/test_wiring_dev_loop.py::test_agents_mention_emit_ux`
- [x] `/dev` e `DEV-LOOP.md` apontam painel live — tested by: `tests/fluxo_events/test_wiring_dev_loop.py::test_docs_mention_live`
- [x] Documentado: dry-run sem emit — tested by: `tests/fluxo_events/test_wiring_dev_loop.py::test_dry_run_no_emit_documented`
- [x] Espelho `.claude`↔`.cursor` dos artefatos tocados — tested by: `tests/fluxo_events/test_wiring_dev_loop.py::test_dual_tree`

## Notes

AC6, AC7, AC13. Fail soft.

Revisor auto: Revisor: aprovado com ressalvas — mirror `.cursor/projetos/dev-loop-*` pode falhar soft em FS read-only; wiring dual-tree agents/commands OK.
