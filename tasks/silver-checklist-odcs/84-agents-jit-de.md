# Agents JIT data-quality e contracts

**Status:** done  
**Blocked by:** tasks/silver-checklist-odcs/82-kb-pattern-silver-checklist.md

## What to build

Adicionar referência JIT ao pattern `silver-checklist-odcs.md` nos agents DE
`data-quality-analyst` e `data-contracts-engineer` (seção Referências), espelhando
`.cursor/agents/data-engineering/`. Uma linha por agent apontando quando usar o checklist
(Silver expectations / contrato ODCS → regras).

## Acceptance criteria

- [x] `data-quality-analyst.md` referencia o KB pattern — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_data_quality_analyst_jit_link`
- [x] `data-contracts-engineer.md` referencia o KB pattern — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_data_contracts_engineer_jit_link`
- [x] Espelho `.cursor/agents/data-engineering/` para os dois agents — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_agents_dual_tree`

## Notes

Evidence-gate task 84 verde.
