# Stack parent gitignore

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/75-emit-causal-ids.md

## What to build

Módulo `stack.py`: parent explícito prevalece; senão topo de
`projetos/{slug}/fluxo/stack.json`; omitido = órfão. Arquivo gitignored. Fail-soft em
erro de FS (warning; emit segue sem parent).

## Acceptance criteria

- [x] Parent explícito vence a stack — tested by: `tests/fluxo_events/test_stack_parent.py::test_explicit_parent_wins`
- [x] Sem explícito → usa topo de `stack.json` — tested by: `tests/fluxo_events/test_stack_parent.py::test_uses_stack_top`
- [x] Path sob `fluxo/stack.json` e entrada no `.gitignore` — tested by: `tests/fluxo_events/test_stack_parent.py::test_stack_path_and_gitignore`
- [x] FS error na stack → warning soft; emit não bloqueia — tested by: `tests/fluxo_events/test_stack_parent.py::test_stack_fail_soft`

## Notes

AC4, AC5, AC12, AC13. Sem mutex (WON'T).

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
