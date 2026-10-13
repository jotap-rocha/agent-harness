# Task 98 — pytest + ship

**Status:** done  
**Blocked by:** tasks/pipeline-runtime-gates/95-gates-brainstorm-4a.md, tasks/pipeline-runtime-gates/96-gates-define-2a.md, tasks/pipeline-runtime-gates/97-rules-index-crossrefs.md

## Objetivo

Pacote `test_pipeline_runtime_gates.py` verde; `/validar` full; evidence-gate 94–98;
revisor-codigo; ship (`05-retro`, `metrics/entregas.jsonl`, sync-context).

## Critérios de aceite

- [x] `pytest tests/data_engineering/test_pipeline_runtime_gates.py` verde — tested by: 18 passed
- [x] `/validar` (ruff + pytest full 512 passed) verde — tested by: gate local
- [x] evidence-gate check tasks 94–98 — tested by: `python -m config.evidence_gate check`
- [x] revisor-codigo aprovado (0 bloqueantes) — tested by: veredito aprovado com ressalvas
- [x] delivery record em `metrics/entregas.jsonl` — tested by: linhas issue 94–98

## Notes

- mypy raiz falha em `examples/` (duplicate module pré-existente); `mypy config tests` verde.
- Excluir `visao-grafica-fluxo-agentes/fluxo/` do commit deste fluxo (ressalva revisor).
