# PRD — Silver Checklist ODCS (camada Silver prescritiva)

Slug: `silver-checklist-odcs`  
Repo: Agent Harness Canônico (framework — **não** produto ETL)  
Branch: `master` (evolução canônica — criar `feat/silver-checklist-odcs` no build)  
Data: 2026-08-19  
Tipo: **e** — evolução do harness canônico (KB pipeline DE)  
SI: **a** (dados sintéticos nos exemplos — sem PII)  
Fontes: `00-ideia.md`, `01-grill.md` (decisões 1–12 + MoSCoW + lentes I1–I10)  
Prior art: `pipeline/concepts/data-contracts.md`, `patterns/data-quality.md`, `patterns/solid-pipeline.md`

> Decisões do grill/define estão **fechadas** — este PRD as materializa; não reabre a matriz.  
> **Adversarial judge (PRD):** pulado **(b)** — sem `02b-judge.md` (mesmo padrão define).  
> Plano de extensão: `03-harness.md` (tipo e — canônico).

---

## Problem Statement

O harness documenta Medallion e contratos ODCS, mas a camada **Silver** permanece vaga:
“dedup, limpeza, validação” sem regras operacionais mapeadas às seções do contrato
(`schema.fields`, `quality`, `sla`, `versioning`). Engenheiros confundem **tipagem Bronze**
(com `.cast()` explícito) com **limpeza Silver** (trim, dedup, expectations). Agents DE
(`data-quality-analyst`, `data-contracts-engineer`) apontam para conceitos genéricos sem
checklist acionável por domínio.

O sintoma é prosa correta mas implementação inconsistente nos filhos. O problema real é a
ausência de um **KB pattern prescritivo** que ligue ODCS → 10–15 regras Silver com severidade
(`fail` | `quarantine` | `log`) e snippets PySpark + DLT — **sem** inflar o kernel DE com
checks não verificáveis no filesystem.

---

## Solution

Adicionar ao canônico o pattern **`silver-checklist-odcs.md`** em `kb/pipeline/patterns/`:

1. **Template genérico** — 10 regras core + até 5 opcionais; colunas:
   `regra_id`, categoria, mapeamento ODCS, severidade, PySpark, DLT
2. **Instância orders** — 15 regras derivadas do YAML exemplo em `data-contracts.md`
3. **Tabela de severidade padrão** — defaults por tipo de violação; domínio pode sobrescrever
4. **Seção Proibido no Silver** — fronteira Bronze/Silver/Gold (sem cast/inferSchema/raw/Gold agg)
5. **Campo template** `ingestion_mode: batch|cdc` — dedup batch vs CDC documentado
6. **Cross-links** — `data-contracts.md`, `pipeline/index.md`, `de-conformidade/references/`
7. **Agents JIT** — uma referência em `data-quality-analyst` e `data-contracts-engineer`
8. **Dual-tree** — espelho `.cursor/` na mesma sessão de ship
9. **Enforcement** — permanece DE-B003 (contrato versionado); **sem** novo rule_id DE

### Esboço de estrutura do KB pattern

```text
silver-checklist-odcs.md
├── Âncora normativa (DE-B003 ponte; YAML vence severidade DE)
├── Proibido no Silver (≥4 itens)
├── Tabela severidade padrão
├── Template genérico (10 core + 5 opcionais)
├── ingestion_mode: batch | cdc
├── Instância orders (SLV-ORD-001 … 015)
└── Ver também (medallion, quarantine, data-quality, data-contracts)
```

---

## Goals (MoSCoW)

### MUST

- KB `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` (+ espelho `.cursor/`)
- Template 10 core + opcionais; instância orders ≥10 regras preenchidas
- Tabela severidade padrão (fail / quarantine / log)
- Seção Proibido no Silver
- Snippets PySpark + DLT simétricos por regra aplicável
- Cross-links em `data-contracts.md`, `pipeline/index.md`, de-conformidade
- JIT refs nos 2 agents DE
- `/validar` verde; `data-engineering.yaml` **inalterado**
- Espelho `.claude` ↔ `.cursor`

### SHOULD

- `ingestion_mode` documentado no template contrato
- Colunas lineage medallion + contrato (`_contract_id`, `_contract_version`)
- Entrada em `kb/pipeline/_index.yaml` se o índice listar patterns

### COULD

- Example `examples/silver-checklist-orders-min/`
- Segundo domínio `customers` no KB

### WON'T (neste ship)

- Novo rule_id DE
- Gerador automático código ← contrato
- Inferência automática de tipos no Silver
- Command `/silver-checklist`
- Example executável obrigatório
- Alteração semântica de `medallion.md`
- Enforcement mecânico dedup linha a linha

---

## User Stories

### Mantenedor do canônico

1. As a mantenedor, I want a dedicated KB pattern for Silver checklist mapped to ODCS, so that
   concept (`data-contracts.md`) stays separate from executable guidance.
2. As a mantenedor, I want a reusable template plus a filled **orders** instance, so that filhos
   can copy the pattern for other domains.
3. As a mantenedor, I want default severity table by violation type, so that teams don't
   reinvent fail vs quarantine vs log per project.
4. As a mantenedor, I want explicit **Proibido no Silver** section, so that Bronze/Silver
   boundary is unambiguous (no cast/inferSchema in Silver).
5. As a mantenedor, I want PySpark and DLT snippets per rule, so that both spark-yarn and
   databricks profiles have reference code.
6. As CI do canônico, I want `/validar` green without changing `data-engineering.yaml`, so that
   this ship stays documentation-only for the DE kernel.
7. As a mantenedor, I want dual-tree mirror, so that Cursor and Claude stay in sync.

### Engenheiro DE / filho (consumidor do KB via install)

8. As an engenheiro DE, I want checklist rules mapped to ODCS sections I already declare in
   `data-contracts/*.yaml`, so that I know what to implement in Silver transforms.
9. As an engenheiro DE, I want dedup batch vs CDC documented, so that I pick the right pattern
   for my ingestion mode.
10. As an engenheiro DE, I want line-level quarantine vs batch fail for completeness, so that
    operational alerts match the severity table.

### Agents DE

11. As `data-quality-analyst`, I want a JIT link to the Silver checklist, so that expectations
    and quarantine align with contract fields.
12. As `data-contracts-engineer`, I want a JIT link from ODCS authoring to Silver rules, so that
    contracts include what Silver will enforce.

---

## Functional Requirements

| ID | Requisito |
|---|---|
| FR1 | KB pattern com template 10 core documentado |
| FR2 | Instância orders com ≥10 regras (SLV-ORD-*) |
| FR3 | Tabela severidade padrão com ≥6 tipos de violação |
| FR4 | Seção Proibido no Silver com ≥4 proibições |
| FR5 | Cada regra core com mapeamento ODCS explícito |
| FR6 | Regras aplicáveis com snippet PySpark **e** DLT |
| FR7 | Cross-link em `data-contracts.md` (Integração Silver) |
| FR8 | Entrada em `pipeline/index.md` tabela Padrões |
| FR9 | Ponte em `de-conformidade/references/` (DE-B003) |
| FR10 | Agents DE com referência JIT ao pattern |
| FR11 | Espelho byte-identical `.claude/` ↔ `.cursor/` nos paths tocados |
| FR12 | `data-engineering.yaml` sem diff neste ship |

---

## Acceptance Criteria (DoD ship)

| AC | Critério | Evidência |
|---|---|---|
| AC1 | KB pattern existe | `test` grep ou pytest path `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` |
| AC2 | Espelho Cursor | mesmo path sob `.cursor/kb/` |
| AC3 | Template 10 core | seção no KB com tabela template |
| AC4 | Instância orders | ≥10 linhas SLV-ORD-* no KB |
| AC5 | Severidade defaults | tabela no KB |
| AC6 | Proibido Silver | ≥4 bullets |
| AC7 | Cross-link data-contracts | link para pattern no concepts |
| AC8 | pipeline/index | linha na tabela Padrões |
| AC9 | de-conformidade | parágrafo em references |
| AC10 | Agents JIT | refs em 2 agents DE |
| AC11 | Gate verde | `/validar` exit 0 |
| AC12 | Kernel DE intacto | `git diff data-engineering.yaml` vazio |
| AC13 | Snippets dual | ≥3 regras orders com PySpark **e** DLT |
| AC14 | ingestion_mode | documentado no template |
| AC15 | Sem PII real | revisão manual KB (SI a) |

---

## Implementation Decisions

1. **Pattern separado** — não inflar `data-contracts.md` além de cross-link curto
2. **Documentação only** — enforcement mecânico continua DE-B003 + implementação filho
3. **Orders piloto** — único domínio preenchido neste ship
4. **Lineage** — medallion cols + `_contract_id` / `_contract_version` (não `_pipeline_run_id` duplicado; usar `_run_id` de `data-lineage.md`)
5. **SLV-ORD-005** — round/validate decimal no Silver; cast primário no Bronze
6. **Branch** — `feat/silver-checklist-odcs` no harness-build (não commitar em master)

---

## Testing Decisions

| Área | Como validar |
|---|---|
| KB presence + estrutura | pytest leve em `tests/data_engineering/` ou `tests/kb/` (grep seções obrigatórias) |
| Espelho dual-tree | pytest compara hash `.claude` vs `.cursor` nos paths tocados |
| Regressão DE | `/validar` suite global |
| Conteúdo prescritivo | review `revisor-codigo` soft + checklist AC manual |

---

## Out of Scope

Ver WON'T em Goals. Adicionalmente: mudar examples DE existentes; novo agent DE; integração
Great Expectations além de referência; alterar `rules/pipeline.md` além de link opcional.

---

## SI Considerations

- SI **a**: exemplos só IDs sintéticos (`order_id`, `customer_id` fictícios)
- Sem PII real em KB versionado
- Snippets não logam valores de campo — só metadados (`run_id`, `rule`, `count`)
- Filho com PII: contrato + `rules/pii.md` — fora deste ship canônico

---

## Further Notes

- Tasks sugeridas: 82+ em `tasks/silver-checklist-odcs/` (via `/to-tasks`)
- `/sync-context` no ship: citar pattern na tabela KB pipeline se aplicável
- Example stretch: `examples/silver-checklist-orders-min/` — backlog COULD

---

## Próximo passo

`/to-tasks` → `harness-build` na branch `feat/silver-checklist-odcs`.
