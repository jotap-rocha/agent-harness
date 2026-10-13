# PRD — Pipeline Runtime + AI-DEV-KIT Gates

Slug: `pipeline-runtime-gates`  
Repo: Agent Harness Canônico (framework)  
Branch: `feat/pipeline-runtime-gates`  
Data: 2026-08-24  
Tipo: **e** — evolução harness (SDD + KB Databricks)  
SI: **a**  
Fontes: `00-ideia.md`, `01-grill.md`  
Prior art: `medallion-sdd-gates`, `de_marker.py`, pesquisa `ai-dev-kit-main-databricks`

---

## Problem Statement

O fluxo `/novo-projeto` não **obrigava** resposta humana sobre runtime (Spark local vs Databricks)
antes de avançar para Medallion e artefatos SDD. Projetos Databricks sem **AI-DEV-KIT** instalado
violam pré-requisito organizacional. Analistas sem conhecimento do kit não devem continuar o
brainstorm.

## Solution

1. **`harness-brainstorm` passo 4a** — hard-stop runtime (Spark LOCAL | Databricks CLOUD)
2. **`harness-brainstorm` passo 4a-bis** — AI-DEV-KIT (sim → continua; não/não-sei → encerra)
3. **KB `ai-dev-kit-gate.md`** — fonte única de regras e mensagem de encerramento
4. **`harness-define` passo 2a** — valida runtime + kit no `00-ideia.md`
5. **Cross-links** — `rules/pipeline.md`, `medallion-sdd-gates.md`, `databricks/index.md`
6. **pytest** — `test_pipeline_runtime_gates.py`

### Fluxo

```text
Passo 4 (tipo pipeline) → 4a runtime humano
  ├─ spark-local → 4b Medallion → continua
  └─ databricks → 4a-bis AI-DEV-KIT
        ├─ sim → 4b → continua
        ├─ não → STOP (sem 00-ideia.md)
        └─ não sei → STOP + administrador
```

## Goals (MoSCoW)

### MUST

- Gates 4a e 4a-bis no brainstorm com hard-stop
- KB + espelho `.cursor/`
- Define 2a validação
- pytest verde
- Tasks 94–98

### SHOULD

- Template `00-ideia.md` com seções Runtime e AI-DEV-KIT

### WON'T

- Auto-detect substituindo resposta humana
- Novo rule_id DE

---

## User Stories

1. Como analista, quero ser perguntado explicitamente se o pipeline é Spark local ou Databricks.
2. Como analista Databricks, quero confirmar AI-DEV-KIT antes de continuar o SDD.
3. Como analista sem conhecimento do kit, quero orientação para falar com o administrador.
4. Como revisor, quero pytest que prova wiring dual-tree dos gates.

---

## Acceptance Criteria

| ID | Critério | Teste |
|---|---|---|
| AC1 | KB ai-dev-kit-gate existe + dual-tree | `test_ai_dev_kit_kb_*` |
| AC2 | Brainstorm 4a hard-stop runtime | `test_brainstorm_runtime_gate` |
| AC3 | Brainstorm 4a-bis AI-DEV-KIT stop | `test_brainstorm_ai_dev_kit_gate` |
| AC4 | Define 2a validação | `test_define_runtime_validation` |
| AC5 | Rules/index cross-links | `test_pipeline_rule_*`, `test_databricks_index_*` |

---

## Tasks

94 → (95 ∥ 96 ∥ 97) → 98
