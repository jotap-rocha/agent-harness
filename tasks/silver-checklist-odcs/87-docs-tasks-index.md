# Docs tasks index e STATUS

**Status:** done  
**Blocked by:** tasks/silver-checklist-odcs/86-validar-kernel-intacto.md

## What to build

Fechar a fase de tasks no SDD: `04-tasks-index.md`, `tasks/README.md`, `STATUS.md` fase 5.

## Acceptance criteria

- [x] `04-tasks-index.md` lista tasks 82–87 com blocked-by — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_tasks_index_file_exists`
- [x] `tasks/README.md` inclui seção `silver-checklist-odcs` — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_readme_lists_silver_checklist_slug`
- [x] `STATUS.md` fase tasks atualizada — tested by: revisão manual + espelho `.cursor/projetos/`

## Notes

Evidence-gate task 87 verde. Próximo: harness-ship + commit com acordo.
