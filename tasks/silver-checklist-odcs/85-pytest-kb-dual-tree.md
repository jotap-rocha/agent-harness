# Pytest smoke KB e dual-tree

**Status:** done  
**Blocked by:** tasks/silver-checklist-odcs/82-kb-pattern-silver-checklist.md, tasks/silver-checklist-odcs/83-crosslinks-pipeline-de.md, tasks/silver-checklist-odcs/84-agents-jit-de.md

## What to build

Consolidar o pacote de testes `tests/data_engineering/test_silver_checklist_kb.py` que
valida presença do KB, seções obrigatórias, contagem de regras orders, dual snippets,
cross-links, refs de agents e espelho `.claude`↔`.cursor` nos paths tocados pelo ship.

## Acceptance criteria

- [x] Módulo pytest existe e roda no `/validar` — tested by: `tests/data_engineering/test_silver_checklist_kb.py` (suite completa verde)
- [x] Cobertura mínima: KB + index + de-conformidade + 2 agents — tested by: mesma suite (≥8 test functions)
- [x] Nenhum teste depende de network ou API live — no test — invariante DE FS-only; revisão no code review

## Notes

22 test functions (incl. parametrized mirror). Evidence-gate task 85 verde.
