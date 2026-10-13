# CLI run parent flags

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/75-emit-causal-ids.md, tasks/fluxo-grafo-causal/76-stack-parent-gitignore.md

## What to build

CLI `emit` expõe `--run-id` e `--parent-event-id` e encaminha ao engine.

## Acceptance criteria

- [x] Flags `--run-id` e `--parent-event-id` aceitas e gravadas no JSONL — tested by: `tests/fluxo_events/test_cli_causal_flags.py::test_emit_cli_run_and_parent`

## Notes

AC11. Superfície CLI existente (`python -m config.fluxo_events emit`).

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
