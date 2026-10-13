# Validar gate e kernel DE intacto

**Status:** done  
**Blocked by:** tasks/silver-checklist-odcs/85-pytest-kb-dual-tree.md

## What to build

Rodar `/validar` (ruff + mypy + pytest) com suite verde após tasks 82–85. Assert mecânico
de que `data-engineering.yaml` não foi alterado neste ship.

## Acceptance criteria

- [x] `/validar` exit 0 no repositório — tested by: ruff + mypy + pytest 461 passed
- [x] `data-engineering.yaml` sem diff vs HEAD baseline do branch — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_data_engineering_yaml_unchanged`
- [x] evidence-gate check verde para tasks implementadas — tested by: `python -m config.evidence_gate check --root .claude/projetos/silver-checklist-odcs/evidencias --task 86`

## Notes

Evidence-gate task 86 verde. Branch: `feat/silver-checklist-odcs`.
