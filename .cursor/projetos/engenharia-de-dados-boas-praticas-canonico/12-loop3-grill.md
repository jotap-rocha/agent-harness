# Grill — Loop 3 (agents · skills · KBs · install)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Branch: `feat/de-agents-skills-loop3` @ `fa0ab0c`  
Contexto: Loop 2 shipped · `11-loop3-ideia.md` · `00d-codebase-loop3.md`

## Entendimento compartilhado

Com o kernel A–D verde, o Loop 3 amarra a camada agentic DE ao gate executável,
adiciona skill `de-conformidade` + KB `databricks`, e propaga **todos** os 10 agents
e 7 commands via `pipeline_dados` — sem live API, com espelho `.claude`↔`.cursor` e
seed KEEP preservado.

## Decisões fechadas (não reabrir)

| # | Tema | Escolha |
|---|---|---|
| 1 | Ship Loop 2 primeiro | **Feito** — não reabrir kernel Databricks neste loop |
| 2 | Escopo | agents + skills + KBs + propagar install |
| 3 | Propagação | **TODOS** 10 agents + 7 commands DE em `pipeline_dados` |
| 4 | Novos | evoluir existentes + **1** skill DE + KB `databricks` |

### Metadados

| Item | Valor |
|---|---|
| Slug | `engenharia-de-dados-boas-praticas-canonico` |
| SI | **c + d** |
| Branch | `feat/de-agents-skills-loop3` |
| Skill name | `de-conformidade` |
| Live API | **não** |
| Espelho | `.claude` ↔ `.cursor` na mesma sessão |
| Seed | `seed: true` → KEEP no re-install (preservar) |

## Amarras por domínio (agents → pacotes / IDs)

| Agent | Amarras obrigatórias |
|---|---|
| **todos** (10) | **DE-A\*** (Universal) + invocar `/validar` / CLI quando houver tree DE; baseline/waiver vs corrigir |
| `spark-engineer` | A + **B** |
| `pipeline-architect` | A + **B** + **C** (Airflow condicional) |
| `data-quality-analyst` | A + **DE-D003** / **DE-D004** (quarentena DLT · schema rescue) |
| `lakehouse-architect` | A + **D** (pacote cloud) |
| `data-platform-engineer` | A + **D** |
| `schema-designer` | A + **DE-D004** |
| `dbt-specialist` | A (+ D se tree cloud / multi) |
| `sql-optimizer` | A (+ D se cloud) |
| `streaming-engineer` | A (+ D se cloud) |
| `data-contracts-engineer` | A (+ D se cloud) |

Cada agent ganha seção **Kernel DE** (não prosa solta): quando rodar validate, quais IDs
são do seu domínio, e política **corrigir** vs **baseline/waiver** (owner + expiry).

## Amarras commands (7)

Cada command DE deve:

1. Apontar o **gate** (`/validar` e/ou `python -m config.canonical_data_check validate`)
2. Nomear o **agent amarrado** já atualizado
3. Não duplicar a norma — apontar YAML / skill `de-conformidade` para remediação

## KBs

| Ação | Alvo |
|---|---|
| Ponte curta | 10 KBs DE-adjacentes — link a IDs DE-* / pacotes, **sem** copiar texto da norma |
| Novo domínio | `kb/databricks/` — `index` + `quick-reference` + concepts + patterns alinhados **DE-D001–005**; registrar em `_index.yaml` |

## Skill `de-conformidade`

- Pattern `write-a-skill` (SKILL.md + progressive disclosure)
- Lê findings da CLI (validate/compare/report/explain)
- Orienta remediação por `rule_id`
- Guia baseline/waiver (nunca silenciar sem owner+expiry)
- Espelho `.claude/skills/de-conformidade/` ↔ `.cursor/skills/de-conformidade/`

## Install

- Expandir `pipeline_dados` no `stack_map` (+ prosa `SKILL.md` install-harness)
- Copiar 10 agents + 7 commands (+ skill + KB databricks conforme plan)
- Reescrever freeze/install asserts (deixam de proibir; passam a exigir cópia)
- Preservar seed KEEP

## Fora deste loop

- Live Databricks API / credenciais no CI
- Alterar semântica dos checks A–D (só consumir)
- Apagar/renomear agents existentes
- Quebrar KEEP de `.harness/data-check`

## Próximo passo

1. PRD Loop 3 → `13-loop3-prd.md`  
2. Harness plan → `14-loop3-harness.md` (aprovado por decisão fechada)  
3. Tasks `25`–`32` + `tasks/README.md`
