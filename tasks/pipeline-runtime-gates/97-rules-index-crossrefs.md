# Task 97 — Rules + index cross-refs

**Status:** done  
**Blocked by:** tasks/pipeline-runtime-gates/94-kb-ai-dev-kit-gate.md

## Objetivo

Atualizar `rules/pipeline.md`, `medallion-sdd-gates.md`, `databricks/index.md` e `_index.yaml`
com cross-links dos gates 4a/4a-bis/2a.

## Critérios de aceite

- [x] `rules/pipeline.md` referencia 4a, 4a-bis, 2a e ai-dev-kit-gate — tested by: `test_pipeline_rule_references_gates`
- [x] `medallion-sdd-gates.md` exige 4a/4a-bis antes — tested by: `test_medallion_gates_prerequisite_runtime`
- [x] Espelho `.cursor/rules/pipeline.mdc` e KB — tested by: `test_mirror_paths_exist`
