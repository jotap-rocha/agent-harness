# KB pattern Silver checklist ODCS

**Status:** done  
**Blocked by:** none

## What to build

Criar o KB pattern prescritivo que liga contrato ODCS à camada Silver: template genérico
(10 core + 5 opcionais), tabela de severidade padrão, seção Proibido no Silver,
`ingestion_mode` batch|cdc, e instância **orders** (regras SLV-ORD com mapeamento ODCS,
severidade fail|quarantine|log, snippets PySpark e DLT simétricos onde aplicável).
Espelhar o artefato em `.cursor/kb/` na mesma sessão.

## Acceptance criteria

- [x] KB pattern existe em `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_kb_pattern_file_exists`
- [x] Espelho `.cursor/` idêntico ao `.claude/` para o pattern — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_kb_pattern_dual_tree`
- [x] Seções obrigatórias presentes (Proibido Silver, severidade, template core, orders) — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_kb_pattern_required_sections`
- [x] Instância orders com ≥10 regras SLV-ORD — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_orders_instance_rule_count`
- [x] ≥3 regras orders com blocos PySpark e DLT — tested by: `tests/data_engineering/test_silver_checklist_kb.py::test_orders_dual_snippets`
- [x] Exemplos só dados sintéticos (sem PII real) — no test — revisão humana no PR + checklist AC15 PRD; waiver: `{ human: true, reason: "revisão editorial SI — sem assert automático de conteúdo semântico" }`

## Notes

Revisor: aprovado após fix tabela DE-B003 e SLV-ORD-005 (round sem cast). Evidence-gate task 82 verde.
