# Wiring SDD Dev causal

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/75-emit-causal-ids.md, tasks/fluxo-grafo-causal/76-stack-parent-gitignore.md, tasks/fluxo-grafo-causal/77-cli-run-parent-flags.md

## What to build

Instruir emits SDD e Dev Loop a usar `--run-id` / `--parent-event-id` (ou stack) quando
souberem o parent. Espelho `.claude` ↔ `.cursor` dos agents/commands tocados.

## Acceptance criteria

- [x] Agents/commands SDD mencionam IDs/parent/stack — tested by: `tests/fluxo_events/test_wiring_causal.py::test_sdd_wiring_mentions_causal`
- [x] Agents/commands Dev mencionam IDs/parent/stack — tested by: `tests/fluxo_events/test_wiring_causal.py::test_dev_wiring_mentions_causal`
- [x] Espelho dual-tree dos artefatos tocados — tested by: `tests/fluxo_events/test_wiring_causal.py::test_dual_tree`

## Notes

AC16. Fail-soft; dry-run Dev continua sem emit.

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
