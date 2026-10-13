# Pontes DE-* nos KBs adjacentes

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/25-amarrar-agents-de-kernel.md

## What to build

Adicionar **ponte curta** (parágrafo/tabela de âncoras) nos **10** KBs DE-adjacentes
ligando ao kernel (`DE-A*` / pacotes B–D / IDs relevantes) **sem** duplicar o texto da
norma em `data-engineering.yaml`. Espelhar alterações.

## Acceptance criteria

- [x] Cada um dos 10 domínios DE-adjacentes tem âncora explícita a IDs/pacotes DE — tested by: inventário KB (AC3)
- [x] Ponte não cola blocos longos da norma (anti-duplicação leve) — tested by: heuristic/tamanho ou marcador “fonte: data-engineering.yaml”
- [x] Espelho `.claude/kb` ↔ `.cursor/kb` nos arquivos tocados — tested by: assert espelho (AC10)

## Notes

- Domínios: `airflow`, `spark`, `lakehouse`, `pipeline`, `data-quality`, `dbt`,
  `data-modeling`, `sql-patterns`, `streaming`, `cloud-platforms`.
- Preferir `index.md` ou `quick-reference.md` — JIT, não proliferar arquivos.
- Não criar ainda o domínio `databricks` (task 28).
- **Evidência:** seção `## Conformidade DE (ponte)` em cada `kb/<domínio>/index.md`;
  testes `test_ac3_*` (tamanho < 900 chars + marcador fonte).
- **Revisor:** aprovado com ressalvas (lote integração Loop 3; 0 bloqueantes após entregas).
- Sem commit.
