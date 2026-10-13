# Silver Checklist ODCS

## Ideia

Criar um **checklist Silver concreto** (10–15 regras típicas por domínio) alinhado ao contrato
ODCS documentado em `.claude/kb/pipeline/concepts/data-contracts.md`.

Objetivo: documentar o que a camada Silver faz de fato — deduplicação, limpeza semântica,
validação contra contrato — **mapeado a campos e seções ODCS** (`schema.fields`, `quality`,
`sla`, `versioning`). **Não** inclui inferência automática de tipos (tipagem e cast ficam
no Bronze).

Entregável futuro provável:
- Novo artefato KB (ex.: `.claude/kb/pipeline/patterns/silver-checklist-odcs.md`)
- Espelho em `.cursor/kb/pipeline/patterns/`
- Possível example mínimo (`examples/silver-checklist-orders-min/` ou extensão de
  `data-contracts.md`)

Escopo explícito:
- Regras **prescritivas** (o que implementar), não gerador automático de código
- Cada regra referencia seção ODCS e severidade operacional (`fail` | `quarantine` | `log`)
- Domínio piloto: **orders** (`orders-v1.yaml` do KB data-contracts)
- Framework canônico — sem pipeline de produto neste fluxo SDD

## SI Assessment

Nível: **a** — Não — apenas dados abertos, sintéticos ou públicos

Implicações:
- Harness mínimo de SI (rules/seguranca.md já cobrem)
- Examples e checklist usam dados sintéticos (`order_id`, `customer_id` fictícios)
- Sem `[AVISO_LGPD]` / `rules/pii.md` neste escopo
- IDs em exemplos são placeholders — nunca PII real em KB versionado

## Tipo de Projeto

**e** — Outro: evolução do **harness canônico** (KB pipeline / engenharia de dados)

Stack prevista:
- KB existente: `.claude/kb/pipeline/concepts/data-contracts.md` (ODCS-style YAML)
- Novo padrão: `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` (ou extensão do concepts)
- Espelho dual-tree `.claude/` ↔ `.cursor/`
- Referência cruzada com skill `de-conformidade` e checks DE onde aplicável
- Implementação sugerida: PySpark / DLT (expectations, `merge`, quarantine table)
- Example opcional fora do `stack_map` (padrão canônico DE)

## Escopo do checklist (seções ODCS)

| Seção ODCS | O que Silver valida/implementa |
|---|---|
| `schema.fields` | Limpeza, required, enum, min — **não** cast de tipo (Bronze) |
| `quality.uniqueness` | Dedup por chave natural (`order_id`) |
| `quality.validity` | Regras de domínio (`amount > 0`, status in enum) |
| `quality.completeness` | % de nulls em campos required |
| `sla.freshness` | Metadado `_silver_processed_at` / watermark |
| `versioning` | Colunas `_contract_id`, `_contract_version`; política quarantine |

## Rascunho inicial — checklist orders (15 regras)

Contrato de referência: `orders-v1.yaml` em `data-contracts.md`  
Campos: `order_id`, `customer_id`, `amount`, `status`, `created_at`

| regra_id | categoria | mapeamento ODCS | implementação PySpark/DLT sugerida | severidade |
|---|---|---|---|---|
| SLV-ORD-001 | dedup | `quality.uniqueness.fields: [order_id]` | `dropDuplicates(["order_id"])` pós-merge ou `MERGE` com `whenMatchedUpdate` só se `source.created_at > target.created_at` | fail |
| SLV-ORD-002 | dedup | `quality.uniqueness.threshold: 100%` | Contagem `countDistinct(order_id) == count(*)` antes de write; DLT `@dlt.expect_or_fail("unique_order_id", "count(*) = count(distinct order_id)")` | fail |
| SLV-ORD-003 | limpeza | `schema.fields[order_id].required: true` | `trim(order_id)` + filtro `order_id IS NOT NULL AND length(trim(order_id)) > 0` | quarantine |
| SLV-ORD-004 | limpeza | `schema.fields[customer_id].required: true` | `trim(customer_id)`; null/blank → quarantine com `_quarantine_reason = 'customer_id_required'` | quarantine |
| SLV-ORD-005 | limpeza | `schema.fields[amount].type: decimal(10,2)` | `round(col("amount").cast("decimal(10,2)"), 2)` — cast **preservando** tipo já definido no Bronze | log |
| SLV-ORD-006 | validação | `schema.fields[amount].min: 0.01` + `quality.validity.amount_positive` | `filter(amount >= 0.01)` violações → quarantine; DLT `@dlt.expect_or_drop("amount_min", "amount >= 0.01")` ou expect quarantine | quarantine |
| SLV-ORD-007 | validação | `schema.fields[status].enum: [...]` | `status in ('pending','confirmed','shipped','delivered','cancelled')`; inválidos → quarantine | quarantine |
| SLV-ORD-008 | validação | `schema.fields[created_at].required: true` | Rejeitar `created_at IS NULL`; opcional: `created_at <= current_timestamp()` (anti-futuro) | quarantine |
| SLV-ORD-009 | validação | `quality.completeness: > 99%` | Métrica pré-write: `% non-null` em required fields; abaixo de 99% → `notify_owner` + fail job (SLA batch) | fail |
| SLV-ORD-010 | validação | `schema.fields[*].required` (conjunto) | `@dlt.expect_all_or_drop` por campo required; agregar violações em `_quarantine_reason` | quarantine |
| SLV-ORD-011 | lineage | `id` + `version` do contrato | Colunas `_contract_id = 'orders-contract-v1'`, `_contract_version = '1.0.0'` em todo write Silver | log |
| SLV-ORD-012 | lineage | `producer.service: orders-pipeline` | Coluna `_pipeline_run_id` (UUID run) + `_source_layer = 'bronze'` para rastreio | log |
| SLV-ORD-013 | sla | `sla.freshness: "< 24 hours"` | `_silver_processed_at = current_timestamp()`; alarme se `max(created_at)` do batch > 24h atrás vs clock ingest | fail |
| SLV-ORD-014 | sla | `versioning.breaking_change_policy: quarantine_and_notify` | `ContractValidator.load(...).validate(df)` — violação → append quarantine + `notify_owner` (padrão data-contracts.md) | quarantine |
| SLV-ORD-015 | dedup | CDC / late-arriving (implícito Silver) | Window `row_number() OVER (PARTITION BY order_id ORDER BY created_at DESC) = 1` antes do merge final | fail |

Notas do rascunho:
- **Bronze vs Silver:** casts de tipo (`string` → `decimal`) ficam no Bronze; Silver só arredonda/valida
- **Severidade:** `fail` interrompe o job; `quarantine` desvia linha; `log` registra métrica/auditoria
- Próxima fase (grill): generalizar template por domínio e decidir KB separado vs extensão

## Próximos passos

1. Rode `/grill-me` para aprofundar a ideia (template por domínio, severidade padrão, relação com DE checks)
2. Ao terminar, use `harness-define` para estruturar os requisitos (incluindo perguntas de pipeline DE)
3. Depois: `harness-design` → PRD + harness-architect
