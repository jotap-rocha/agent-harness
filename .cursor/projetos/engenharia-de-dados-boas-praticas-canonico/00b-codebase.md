# 00b — Codebase map (foco Engenharia de Dados)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-06  
Repo: `<raiz-do-clone>`  
Referência adversarial: `sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`

> Mapeamento somente leitura via `codebase-explorer`. Não altera o canônico.

---

## Executive Summary

O Agent Harness Canônico já possui uma **camada DE rica em documentação/prompts**: 10 agents, 7 commands, ~11 KBs e a rule `pipeline.md`. Não há app/serviço de dados; o produto é o framework.

O `install-harness` **não** propaga a pasta `agents/data-engineering/` nem a maioria das KBs DE — só copia `kb/pipeline` + `rules/pipeline` quando detecta keywords `airflow|spark|dbt`.

**Veredito vs sketch adversarial:** o canônico já tem a camada de agents/skills candidatas; falta o **prefixo obrigatório** do sketch — modelo normativo → validadores executáveis → CI/baseline/exceções → scaffolds. Criar mais agents agora aumenta catálogo **sem enforcement**.

---

## Inventário — Agents DE

Espelho idêntico: `.claude/agents/data-engineering/` ≡ `.cursor/agents/data-engineering/` (10).

| Agent | Papel | Fronteira |
|---|---|---|
| `data-contracts-engineer` | ODCS, SLA, schema governance | Define expectativas; não implementa |
| `data-quality-analyst` | GE, Soda, testes dbt, obs | Só leitura; não muda prod |
| `data-platform-engineer` | Snowflake/Databricks/BQ, custo | Comparativo; não desenha schema |
| `dbt-specialist` | models, testes, macros | Não dimensional; não PySpark |
| `lakehouse-architect` | Iceberg/Delta/Hudi, catálogos | Não escolhe cloud; não escreve Spark |
| `pipeline-architect` | Airflow/Dagster, DAG, SLA | Orquestra; não implementa SQL/PySpark |
| `schema-designer` | Kimball, Vault, SCD | Design; implementação → dbt |
| `spark-engineer` | PySpark/Spark SQL | Não DAG; não dbt |
| `sql-optimizer` | Query plan, dialetos | Complementa `sql-architect`; não PySpark |
| `streaming-engineer` | Kafka/Flink/Spark Streaming/CDC | Não DAG batch; não dbt |

Overlaps residuais de roteamento: contratos↔DQ↔dbt; pipeline-architect↔spark/dbt; lakehouse↔platform; sql-optimizer↔sql-architect.

---

## Inventário — Commands DE

Espelho: `.claude/commands/data-engineering/` ≡ `.cursor/` (7).

| Command | Agent |
|---|---|
| `/data-contract` | `data-contracts-engineer` |
| `/data-quality` | `data-quality-analyst` |
| `/lakehouse` | `lakehouse-architect` |
| `/migrate` | dbt / spark / pipeline-architect |
| `/pipeline` | `pipeline-architect` |
| `/schema` | `schema-designer` |
| `/sql-review` | `revisor-codigo` → `sql-optimizer` |

Ausentes: platform, streaming, spark puro, obs operacional, security-review DE, baseline/waiver.

---

## Inventário — KBs DE

Índice: `.claude/kb/_index.yaml` ≡ `.cursor/kb/_index.yaml`.

| Domínio | Observação |
|---|---|
| `airflow`, `dbt`, `spark`, `lakehouse`, `streaming`, `data-modeling`, `sql-patterns`, `cloud-platforms`, `data-quality`, `pipeline` | Cobertura ampla |
| `observabilidade` | Foco Langfuse/LLM — **não** obs de lakehouse/freshness |
| Duplicação | contratos/DQ em `pipeline/` **e** `data-quality/`; unificar fonte normativa depois |

Código de referência: `config/pipeline_config.py` + `config/environments/` (config centralizada; não é scaffold completo).

---

## Propagação `install-harness`

Categoria `pipeline_dados` em `stack_map.json`:

- **Propaga:** `kb/pipeline`, `rules/pipeline.md` (+ espelho `.cursor/`) se keywords `airflow|spark|dbt`
- **Não propaga:** 10 agents DE, 7 commands DE, KBs especializadas (airflow, dbt, spark, lakehouse, DQ, …)

Gap: canônico “tem DE”; projetos instalados recebem só um pedaço.

---

## Rules relevantes

| Rule | Papel DE |
|---|---|
| `pipeline.md` | Única rule DE path-scoped (Medallion, SOLID, contracts, quarantine, lineage…) |
| `seguranca.md` | PII/secrets/prod — sem IDs normativos DE |
| `definicao-de-pronto.md` | Gate genérico; sem lanes de pipeline review |
| `git-hygiene.md` | Secrets em commit (parcial SEC) |

Não existem: `governance/rule-schema.yaml`, rules de contrato/DQ/obs/orquestração com IDs.

---

## Gaps vs sketch adversarial

| Capacidade | Estado | Prioridade |
|---|---|---|
| Modelo normativo (IDs, categorias) | Ausente | P0 |
| Perfis arquiteturais | Ausente | P0 |
| `canonical-data-check` | Ausente | P0 |
| CI + baseline + waiver | Ausente | P0 |
| Scaffolds A/B | Ausente | P1 |
| Skills P0 DE | Ausentes | P1 após kernel |
| Agents extras (drift, reviewer, sdp-builder…) | Parcial / faltam | P2 após checks |
| Pipeline Review lanes | Só `/sql-review` genérico | P1 |
| Propagação install dos agents/KBs DE | Parcial | P1 |
| Enforcement vs documentação | Só docs/prompts | Gap central |

---

## O que NÃO recriar no grill/design

1. Não criar novos agents DE genéricos até existir rule-schema + CLI mínima de checks.
2. Não reescrever Medallion/quarantine/lineage — promover `rules/pipeline.md` + `kb/pipeline/` a mandatos versionados.
3. Não duplicar ODCS — uma fonte normativa de contratos.
4. Não inventar segundo revisor SQL — estender `/sql-review` + `revisor-codigo` com lanes PASS/FAIL/WAIVED.
5. Não expandir `stack_map` copiando 10 agents sem perfil/checks.
6. Não tratar `kb/observabilidade` (Langfuse) como obs de lakehouse.
7. Sequência do sketch §3 é não negociável no curto prazo: **governance → validator MVP → baseline/waiver → scaffold → skills/agents**.

---

## Recomendação para o `/grill-me`

Priorizar perguntas sobre:

1. MVP do validator (quais 3–5 checks bloqueantes primeiro?)
2. Perfis mínimos (Databricks DAB+SDP vs Spark+Airflow) no dia 1
3. Política de waiver/baseline para brownfield (ex.: auditoria)
4. O que vira mandato Universal vs Condicional vs Recomendada
5. Como `install-harness` passa a instalar o pacote DE sem falsa conformidade
