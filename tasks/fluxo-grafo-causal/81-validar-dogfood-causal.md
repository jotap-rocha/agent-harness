# Validar dogfood causal

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/76-stack-parent-gitignore.md, tasks/fluxo-grafo-causal/77-cli-run-parent-flags.md, tasks/fluxo-grafo-causal/78-render-causal-svg.md, tasks/fluxo-grafo-causal/79-wiring-sdd-dev-causal.md, tasks/fluxo-grafo-causal/80-docs-adr-cheatsheet.md

## What to build

`/validar` verde (ruff+mypy+pytest `tests/fluxo_events/`). Caps/truncate/sem mutex
preservados. Dogfood: emit com parent no slug `flujo-grafo-causal` e conferir dois SVGs.
Orthografia e ausência de agent officer.

## Acceptance criteria

- [x] Caps 2 MiB / truncate N=100 / sem mutex intactos — tested by: `tests/fluxo_events/test_dev_loop_map.py::test_limits_unchanged` (ou contrato) + review
- [x] Suite `tests/fluxo_events/` + ruff/mypy verdes — tested by: `/validar` / pytest path
- [x] Naming PT-BR + sem officer — tested by: `tests/fluxo_events/test_naming_ptbr.py` + review AC19
- [x] Dogfood: live.html do slug com dois fluxogramas — tested by: no test — demo + waiver humano opcional

## Notes

AC15, AC19, AC20. Fecha o pacote.

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
