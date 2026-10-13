# Silver Checklist ODCS — Grill & Requisitos

Slug: `silver-checklist-odcs`  
Branch: `master` (evolução canônica)  
Data grill: 2026-08-19 · Define: 2026-08-19  
SI: **a** · Tipo: **e** (evolução do harness canônico — KB pipeline DE)  
Fontes: `00-ideia.md` · grill-me (12 decisões) · KB `pipeline/concepts/data-contracts.md`

> Decisões 1–12 fechadas no `/grill-me` — não reabrir sem novo grill.  
> Judge define: **pulado (b)** — sem `01b-judge.md`.

## Contexto (da sessão /grill-me)

### Problema

O harness **documenta** Medallion e contratos ODCS, mas a camada **Silver** fica abstrata:
“dedup, limpeza, validação” sem regras concretas mapeadas ao contrato. Engenheiros e agents
não sabem **o que implementar** vs o que fica no Bronze, nem qual severidade usar
(`fail` | `quarantine` | `log`).

Sintoma: confusão entre tipagem (Bronze) e limpeza (Silver); examples DE são stubs sem dedup real.

Problema real: falta de **padrão prescritivo reutilizável** ligando seções ODCS → checklist Silver
operacional, espelhado nos KBs/agents que o filho recebe via `pipeline_dados`.

### Usuários

| Persona | Pain / necessidade |
|---|---|
| **Engenheiro DE no filho** | Checklist acionável ao implementar Silver a partir de `data-contracts/*.yaml` |
| **Agent `data-quality-analyst`** | Referência JIT para expectations, quarantine e severidade |
| **Agent `data-contracts-engineer`** | Ponte contrato ODCS → regras Silver por campo |
| **Mantenedor do canônico** | KB versionado + espelho `.cursor/`; sem inflar kernel DE |

### Objetivos (MoSCoW)

**MUST:**
- KB pattern `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` (+ espelho `.cursor/`)
- Template genérico (10 core + até 5 opcionais; N/A documentado) mapeado a ODCS
- Instância **orders** (15 regras) alinhada ao YAML em `data-contracts.md`
- Tabela de **severidade padrão** por tipo de violação
- Seção **Proibido no Silver** (fronteira Bronze/Silver/Gold)
- Snippets **PySpark + DLT** simétricos por regra (quando aplicável)
- Cross-links: `data-contracts.md`, `pipeline/index.md`, `de-conformidade/references/`
- Referências JIT em `data-quality-analyst.md` e `data-contracts-engineer.md`
- Dual-tree `.claude/` ↔ `.cursor/` na mesma sessão de ship
- `/validar` verde (ruff + mypy + pytest) — regressão docs/espelho

**SHOULD:**
- Campo template `ingestion_mode: batch|cdc` no exemplo de contrato (documentação)
- Colunas lineage: medallion + contrato (`_contract_id`, `_contract_version`)
- Teste pytest de naming/guardrail se houver conteúdo indexável (opcional leve)

**COULD:**
- Example `examples/silver-checklist-orders-min/` (stretch futuro)
- Segundo domínio piloto (`customers`) no KB

**WON'T (neste ship):**
- Novo `rule_id` em `data-engineering.yaml`
- Gerador automático de código a partir do contrato
- Inferência automática de tipos no Silver
- Command novo (`/silver-checklist`)
- Example executável obrigatório

### Out of Scope

Tudo em WON'T; também: alteração semântica de `medallion.md`; enforcement mecânico de dedup
linha a linha; integração live API Databricks/Spark.

### Restrições

- Documentação prescritiva — enforcement continua DE-B003 (contrato) + implementação no filho
- SI **a**: só dados sintéticos nos exemplos (`order_id` fictício)
- Sem PII real em KB versionado
- Espelho dual-tree obrigatório
- Git: soft-block fetch Azure 403 neste ambiente — não fingir sync remoto

## Decisões (1–12) — fechadas no grill

| # | Tema | Escolha | Notas |
|---|---|---|---|
| 1 | Onde vive | **(b)** Pattern + cross-link `data-contracts.md` | Conceito vs padrão separados |
| 2 | Generalização | **(b)** Template + instância orders | |
| 3 | Enforcement | **(a)** Só KB — sem novo DE rule | DE-B003/D003 intactos |
| 4 | Snippets | **(c)** PySpark + DLT simétricos | |
| 5 | Example | **(a)** Sem example neste ship | |
| 6 | Severidade | **(a)** Tabela defaults ODCS | Domínio pode sobrescrever |
| 7 | Lineage cols | **(b)** Medallion + contrato | |
| 8 | Completeness | **(a)** Linha→quarantine; batch→fail | |
| 9 | Dedup | **(a)** Batch + CDC (`ingestion_mode`) | |
| 10 | Propagação | **(b)** KB + 2 agents DE | Sem command novo |
| 11 | Contagem | **(b)** 10–15 regras | 10 core + opcionais |
| 12 | Fronteira | **(a)** Seção Proibido no Silver | Sem cast/inferSchema |

## Tabela de severidade padrão (norma do KB)

| Tipo de violação | Default | Rationale |
|---|---|---|
| Uniqueness / dedup final falhou | **fail** | Duplicata corrompe downstream |
| Completeness batch abaixo do SLA | **fail** | Degradação sistêmica da fonte |
| Freshness batch violada | **fail** | SLA operacional |
| Required null / blank | **quarantine** | Linha recuperável |
| Enum / min / max inválido | **quarantine** | Regra por linha |
| Breaking change vs contrato | **quarantine** + notify | `versioning.breaking_change_policy` |
| Normalização cosmética (trim, round) | **log** | Auditoria sem bloquear |
| Lineage / metadados contrato | **log** | Falha técnica de write → fail |

## Pipeline — 10 perguntas

**N/A — tipo e (evolução KB canônico), não pipeline de produto.**

Respostas inferidas para contexto DE (filho que usará o checklist):

| # | Tema | Registro inferido |
|---|---|---|
| 1 | Fontes | Filho define; checklist assume Bronze já ingeriu |
| 2 | Schema | Contrato ODCS versionado; breaking → quarantine (SLV-ORD-014) |
| 3 | Volume | Filho define; dedup batch vs CDC via `ingestion_mode` |
| 4 | PII | SI **a** no canônico; filho com PII usa `rules/pii.md` |
| 5 | SLA | Exemplo orders: freshness `< 24h` no contrato |
| 6 | Gold consumers | Fora deste ship (checklist Silver only) |
| 7 | Owner | `producer` no contrato + `notify_owner` em quarantine |
| 8 | Ambiente | Snippets dual PySpark (spark-yarn) + DLT (databricks) |
| 9 | Qualidade fail vs log | Tabela severidade padrão acima |
| 10 | Portabilidade | Template por domínio; contrato por entidade |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- Provedor: **N/A**
- N/A: sem key vault neste escopo (SI **a**; KB só documentação)

## Especificações implícitas detectadas

| Lente | Registro |
|---|---|
| **I1** Falha dependência externa | **N/A** — KB estático; filho trata runtime |
| **I2** Concorrência | **N/A** — documentação; MERGE CDC descrito no checklist |
| **I3** Idempotência | Coberto no grill (#9): dedup batch + CDC late-arriving |
| **I4** Auth / multi-tenant | **N/A** — padrão genérico; filho aplica RBAC UC |
| **I5** PII não declarada | SI **a**; exemplos sintéticos; filho declara PII no contrato |
| **I6** Abuso / limites | **N/A** |
| **I7** Auditoria | Lineage cols + `_quarantine_reason`; logs estruturados (rule pipeline) |
| **I8** Erro visível | Severidade fail/quarantine/log documentada; filho implementa notify |
| **I9** Ciclo de vida | Quarantine reprocessável (KB `quarantine.md`); fora do ship canônico |
| **I10** Terceiro muda contrato | SLV-ORD-014 + schema evolution (merge/quarantine/fail) |

## Critérios de sucesso mensuráveis

| Critério | Evidência testável |
|---|---|
| KB pattern existe e espelhado | Arquivo em `.claude/` e `.cursor/` com mesma estrutura |
| Template 10 core documentado | Seção no KB com colunas regra_id, categoria, ODCS, severidade, PySpark, DLT |
| Instância orders ≥10 regras | Tabela preenchida referenciando YAML `orders-v1` |
| Cross-links presentes | Links em `data-contracts.md`, `pipeline/index.md`, de-conformidade |
| Agents atualizados | 1 linha JIT em `data-quality-analyst` + `data-contracts-engineer` |
| Proibido Silver explícito | Seção listando ≥4 proibições (cast, inferSchema, raw ingest, Gold agg) |
| Gate verde | `/validar` passa (pytest existente + espelho) |
| Sem novo DE rule | `data-engineering.yaml` inalterado neste ship |

## Entregáveis (design/build)

1. `.claude/kb/pipeline/patterns/silver-checklist-odcs.md`
2. Espelho `.cursor/kb/pipeline/patterns/silver-checklist-odcs.md`
3. Cross-link em `data-contracts.md` (§ Integração Silver)
4. Entrada em `pipeline/index.md` (tabela Padrões)
5. Parágrafo em `de-conformidade/references/` (ponte DE-B003 → checklist)
6. JIT refs nos 2 agents DE
7. `_index.yaml` pipeline se necessário (pattern registrado)

## Rascunho orders (referência — detalhe no KB)

Ver tabela completa em `00-ideia.md` (SLV-ORD-001 … 015). O KB final consolida template +
instância; ajuste SLV-ORD-012 para usar colunas medallion (`_run_id` já definido em
`data-lineage.md`) em vez de `_pipeline_run_id` duplicado.

## Próximo passo

1. Responder adversarial judge (define)
2. Rode **`harness-design`** para PRD (`02-prd.md`) + plano harness (`03-harness.md`)
