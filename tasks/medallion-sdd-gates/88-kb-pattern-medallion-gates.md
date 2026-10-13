# Task 88 — KB pattern medallion-sdd-gates

**Status:** done
**Blocked by:** none

## Objetivo

Criar KB central de gates SDD/Dev Loop para pipelines Medallion.

## Critérios de aceite

- [x] `.claude/kb/pipeline/patterns/medallion-sdd-gates.md` existe com gates T/B/S/G — tested by: `tests/data_engineering/test_medallion_sdd_gates.py::test_kb_pattern_file_exists`
- [x] Espelho `.cursor/kb/pipeline/patterns/` idêntico — tested by: `test_kb_pattern_dual_tree`
- [x] Seções: transversal, Bronze, Silver, Gold+NL, contrato dual, Dev Loop PROMPT — tested by: `test_kb_pattern_required_sections`
