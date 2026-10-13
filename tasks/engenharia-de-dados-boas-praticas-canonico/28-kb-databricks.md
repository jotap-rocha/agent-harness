# KB Databricks (DE-D001–005)

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/27-kbs-de-ponte-ids.md

## What to build

Criar domínio novo `kb/databricks/` com `index.md`, `quick-reference.md`, concepts e
patterns alinhados às regras **DE-D001–005** (DAB, SDP medallion, DLT quarentena,
schema rescue, UC FS). Registrar em `_index.yaml`. Espelhar em `.cursor/kb/`.

## Acceptance criteria

- [x] Árvore `kb/databricks/` com index + quick-ref + concepts + patterns — tested by: file asserts (AC4)
- [x] Conteúdo referencia DE-D001…DE-D005 sem live API — tested by: grep IDs + ausência de credenciais (AC4, AC11)
- [x] `_index.yaml` lista o domínio `databricks` com entry_points — tested by: parse YAML/assert
- [x] Espelho `.claude` ↔ `.cursor` — tested by: assert espelho (AC10)

## Notes

- Pattern dos outros KBs DE; limites de linhas em `_index.yaml` (`limits`).
- Agents sugeridos no index: `lakehouse-architect`, `data-platform-engineer`, `data-quality-analyst`, `schema-designer` (+ `spark-engineer` no `_index.yaml`).
- **Granularidade concepts:** 1:1 com DE-D00n (5 concepts) — fechado na implementação.
- Patterns: `greenfield-sdp-min`, `dlt-quarantine`, `dab-identity`.
- Freeze Loop 2 inventário atualizado para incluir domínio `databricks` (gate verde; freeze DoD final = task 32).
- **Evidência:** `tests/data_engineering/test_loop3_kb_databricks_and_skill.py` (`test_ac4_*`).
- **Revisor:** aprovado com ressalvas (typo description corrigido; nome legado freeze deferido à 32).
- Sem commit.
