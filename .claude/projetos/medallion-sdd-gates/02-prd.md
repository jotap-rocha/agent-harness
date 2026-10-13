# PRD — Medallion SDD Gates (processo harness)

Slug: `medallion-sdd-gates`  
Repo: Agent Harness Canônico (framework — **não** produto ETL)  
Branch: `feat/medallion-sdd-gates`  
Data: 2026-08-24  
Tipo: **e** — evolução do harness canônico (processo SDD/Dev Loop + KB pipeline)  
SI: **a** (dados sintéticos — sem PII)  
Fontes: `00-ideia.md`, `01-grill.md`  
Prior art: `silver-checklist-odcs.md`, `medallion.md`, `data-contracts.md`

> Decisões do grill estão **fechadas** — este PRD materializa o escopo.  
> **Adversarial judge (PRD):** pulado **(b)** — sem `02b-judge.md`.  
> Plano de extensão: `03-harness.md` (tipo e — canônico).

---

## Problem Statement

Projetos de pipeline Medallion iniciados via `/novo-projeto` ou evoluções via `/dev` não tinham
**gates de processo** que obrigassem, antes de codar:

- listar entidades/tabelas e colunas (ou amostra de dados);
- declarar `_source_system` por entidade;
- decidir postura JSON aninhado (Bronze fiel → Silver normaliza);
- contrato dual (ingestão Bronze + ODCS Silver);
- consumo NL (Genie), semântica e ontologia quando aplicável.

O sintoma é pipeline implementado sem contexto de camada, sem lineage completo e sem fronteira
Bronze/Silver/Gold clara. O problema real é a **ausência de checklist acionável no fluxo SDD
e Dev Loop** — não a falta de código ETL no canônico.

---

## Solution

Evoluir o canônico com **gates de entrada** referenciando KB único:

1. **`medallion-sdd-gates.md`** — checklist T1–T8 (transversal), B1–B4, S1–S8, G1–G7
2. **`harness-brainstorm` passo 4b** — hard-stop T1–T3; template Medallion Gates no `00-ideia.md`
3. **`harness-define` passo 2c** — validação antes de `01-grill.md`
4. **`prompt-crafter` passo 3b** — detecção pipeline no Dev Loop + seção Medallion Context
5. **`rules/pipeline.md`** — `_source_system`, contrato dual, link gates
6. **`commands/dev.md`** — nota gate medallion
7. **KB complementar** — `medallion.md`, `data-lineage.md`, `gold-analytic.md`, `genie-readiness.md`
8. **pytest** — `test_medallion_sdd_gates.py` dual-tree
9. **Enforcement** — processo agente only; **sem** novo rule_id DE

### Esboço de estrutura do KB gates

```text
medallion-sdd-gates.md
├── Quando acionar (SDD / Dev Loop)
├── Modelo Raw→Bronze→Silver→Gold→Diamond (ref)
├── Gate transversal T1–T8
├── Gate Bronze B1–B4
├── Gate Silver S1–S8 (ponte silver-checklist-odcs)
├── Gate Gold+NL G1–G7
├── Contrato dual
├── SDD por camada (3 branches recomendadas)
└── Dev Loop — Medallion Context no PROMPT
```

---

## Goals (MoSCoW)

### MUST

- KB `patterns/medallion-sdd-gates.md` (+ espelho `.cursor/`)
- Gates em `harness-brainstorm`, `harness-define`, `prompt-crafter`
- Hard-stop: tabelas + colunas/amostra + `_source_system`
- `rules/pipeline.md` atualizado
- `commands/dev.md` documenta gate
- pytest dual-tree verde
- `data-engineering.yaml` **inalterado**
- Tasks 88–93 implementadas

### SHOULD

- `medallion.md` + `data-lineage.md` + quick-reference com `_source_system`
- `gold-analytic.md` + `genie-readiness.md`
- Recomendação SDDs separados por camada no KB

### COULD

- Example JSON aninhado (stub)
- JIT refs em agents DE adicionais

### WON'T (neste ship)

- Novo rule_id DE
- Pipeline PySpark/DLT executável
- Enforcement mecânico dos gates (CLI)
- Alteração de `install-harness` stack_map obrigatória
- Camada Diamond implementada

---

## User Stories

### Mantenedor do canônico

1. As a mantenedor, I want SDD brainstorm to block without tables/columns/sample, so that
   pipeline projects start with concrete data context.
2. As a mantenedor, I want `_source_system` mandatory in Bronze/Silver lineage docs, so that
   business source is traceable separately from technical `_source`.
3. As a mantenedor, I want Dev Loop to detect pipeline tasks and ask reduced gates, so that
   point evolutions don't skip medallion context.
4. As a mantenedor, I want Genie/NL gate (T8, G1–G7, genie-readiness), so that NL rooms
   trigger semantic/ontology questions early.
5. As CI, I want pytest guarding dual-tree and agent references, so that drift is caught.

### Engenheiro DE / filho (consumidor via install)

6. As an engenheiro DE, I want a single KB for SDD entry gates, so that I know what the
   harness will ask before I implement bronze/silver/gold.
7. As an engenheiro DE, I want JSON nested documented as Bronze-faithful + Silver-normalize,
   so that I don't flatten too early or too late.
8. As an engenheiro DE, I want dual contract model documented, so that ingestion schema
   differs from Silver ODCS flat contract.

### Agents workflow / dev

9. As `harness-brainstorm`, I want step 4b pointing to KB without duplicating full checklist.
10. As `prompt-crafter`, I want redirect to `/novo-projeto` when multi-layer greenfield.

---

## Functional Requirements

| ID | Requisito |
|---|---|
| FR1 | KB gates com T, B, S, G completos |
| FR2 | Brainstorm 4b + template 00-ideia Medallion Gates |
| FR3 | Define 2c + bloco grill Medallion validation |
| FR4 | Prompt-crafter 3b + Medallion Context template |
| FR5 | rules/pipeline `_source_system` + Gates SDD section |
| FR6 | dev.md gate note |
| FR7 | pipeline/index + `_index.yaml` listam pattern |
| FR8 | medallion.md JSON fiel + contrato dual |
| FR9 | gold-analytic + genie-readiness KB |
| FR10 | Espelho `.claude/` ↔ `.cursor/` paths tocados |
| FR11 | `data-engineering.yaml` sem diff |
| FR12 | tasks/README 88–93 |

---

## Acceptance Criteria (DoD ship)

| AC | Critério | Evidência |
|---|---|---|
| AC1 | KB gates existe | `test_kb_pattern_file_exists` |
| AC2 | Espelho Cursor | `test_kb_pattern_dual_tree` |
| AC3 | Seções T/B/S/G | `test_kb_pattern_required_sections` |
| AC4 | Brainstorm 4b | `test_brainstorm_gate_section` |
| AC5 | Define 2c + template | `test_define_gate_section`, `test_define_grill_template` |
| AC6 | Prompt-crafter 3b | `test_prompt_crafter_gate_section` |
| AC7 | dev.md | `test_dev_command_gate_note` |
| AC8 | rules/pipeline | `test_pipeline_rule_gates` |
| AC9 | Index KB | `test_pipeline_index_lists_pattern` |
| AC10 | medallion + lineage `_source_system` | `test_medallion_concept_source_system`, `test_data_lineage_source_system` |
| AC11 | Gold + Genie KB | `test_gold_analytic_and_genie_kb` |
| AC12 | Gate verde | `/validar` exit 0 |
| AC13 | Kernel DE intacto | `git diff data-engineering.yaml` vazio |
| AC14 | Agents dual-tree | `test_agents_dual_tree` |
| AC15 | PRD + harness docs | `02-prd.md`, `03-harness.md` presentes |

---

## Implementation Decisions

1. **Process-only gates** — agents perguntam; não CLI enforcement (§1.3 honesty)
2. **KB fonte única** — agents linkam `medallion-sdd-gates.md`, não duplicam listas
3. **Contrato dual** — Bronze ingestão leve; Silver ODCS (`DE-B003` unchanged)
4. **JSON** — Bronze preserva struct/array; Silver explode/flatten
5. **Gold analítico** — subset negócio antes de Diamond; Genie checklist separado
6. **Tasks 88–93** — numeração global pós silver-checklist-odcs (82–87)
7. **Branch** — `feat/medallion-sdd-gates`; GIT_PREFLIGHT no brainstorm filho futuro

---

## Testing Decisions

| Área | Como validar |
|---|---|
| KB + wiring | `pytest tests/data_engineering/test_medallion_sdd_gates.py` |
| Espelho dual-tree | pytest filecmp agents + KB |
| Regressão global | `/validar` |
| Conteúdo prescritivo | `revisor-codigo` soft |
| Ship | evidence-gate tasks 88–93 |

---

## Out of Scope

Ver WON'T. Adicionalmente: mudar checks `package_b.py`/`package_d.py`; example JSON executável;
novo command `/medallion-gates`.

---

## SI Considerations

- SI **a**: gates e KB usam placeholders (`ERP`, `order_id` sintético)
- Patterns CPF/telefone/CEP são inferência documentada — filho com PII usa `rules/pii.md`
- Gates não coletam PII real na janela SDD — amostras devem ser mascaradas ou sintéticas

---

## Status de implementação (pré-PRD)

| Item | Status |
|---|---|
| Tasks 88–93 código | **done** (commits dfc8cfb, cc4ac2f) |
| pytest 25 tests | **green** |
| evidence-gate por task | **pendente** ship |
| revisor-codigo | **pendente** ship |
| `/validar` global | **pendente** ship |

---

## Próximo passo

Evidence-gate + `/validar` + `revisor-codigo` → `harness-ship` + retro (`05-retro.md`).
