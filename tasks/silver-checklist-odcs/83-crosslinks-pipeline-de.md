# Cross-links pipeline e de-conformidade

**Status:** done  
**Blocked by:** tasks/silver-checklist-odcs/82-kb-pattern-silver-checklist.md

## What to build

Conectar o novo pattern ao restante do catálogo DE: seção Integração Silver em
`data-contracts.md`, linha na tabela Padrões de `pipeline/index.md`, ponte em
`de-conformidade/references/` (DE-B003 → checklist Silver), e entrada no índice
`kb/_index.yaml` do domínio pipeline quando patterns forem listados. Espelhar edits
em `.cursor/`.

## Acceptance criteria

- [x] `data-contracts.md` linka o pattern Silver checklist — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_data_contracts_links_pattern`
- [x] `pipeline/index.md` lista o pattern na tabela Padrões — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_pipeline_index_lists_pattern`
- [x] de-conformidade referencia o checklist (DE-B003 ponte) — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_de_conformidade_references_checklist`
- [x] `_index.yaml` pipeline inclui o pattern se o índice catalogar patterns — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_kb_index_lists_pattern_or_skip_documented`

## Notes

Evidence-gate task 83 verde. Tabela Pacotes em rule-ids-remediation corrigida pós-revisor.
