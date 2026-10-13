# Aviso UX painel live

**Status:** done  
**Blocked by:** none

## What to build

No SDD, o agente deve **avisar o usuário** (1× no enter da fase) como acessar o
painel gráfico live — não só emitir eventos em silêncio. Escopo curto: wiring em
`harness-brainstorm` (fase 0) e `harness-build` (fase 3), mais reforço em
`/fluxo-live`. Dev Loop fora (MVP).

## Acceptance criteria

- [x] `harness-brainstorm` instrui avisar o usuário com path `live.html` + http.server opcional + `/fluxo-live` — tested by: `tests/fluxo_events/test_ux_aviso_live.py::test_brainstorm_avisar_usuario`
- [x] `harness-build` instrui o mesmo aviso no enter do build — tested by: `tests/fluxo_events/test_ux_aviso_live.py::test_build_avisar_usuario`
- [x] `/fluxo-live` menciona abertura no browser / file path — tested by: `tests/fluxo_events/test_ux_aviso_live.py::test_fluxo_live_command_docs`
- [x] Espelho `.claude`↔`.cursor` dos agents/command tocados — tested by: `tests/fluxo_events/test_ux_aviso_live.py::test_dual_tree_ux`

## Notes

Slug: `visao-grafica-fluxo-agentes`. Branch: `chore/tasks-por-slug`.  
Gate: pytest 4 passed (`test_ux_aviso_live`). Sem evidence-gate formal nesta fatia curta
(chore na mesma branch de layout). Commit acordado pelo usuário.
