# Task 94 — KB ai-dev-kit-gate

**Status:** done  
**Blocked by:** none

## Objetivo

Criar KB `kb/databricks/patterns/ai-dev-kit-gate.md` como fonte única do gate AI-DEV-KIT
(pré-requisito SDD Databricks) + espelho `.cursor/`.

## Critérios de aceite

- [x] KB existe com perguntas, regras b/c stop e mensagem padrão — tested by: `test_ai_dev_kit_kb_exists`
- [x] Dual-tree `.claude/` ↔ `.cursor/` — tested by: `test_ai_dev_kit_kb_dual_tree`
- [x] Index databricks + `_index.yaml` listam pattern — tested by: `test_databricks_index_lists_ai_dev_kit`
