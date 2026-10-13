# Loop 3 — Ideia (agents + skills + KBs DE + install)

Slug (mesmo projeto): `engenharia-de-dados-boas-praticas-canonico`  
Iniciado em: 2026-08-07  
Branch: `feat/de-agents-skills-loop3` @ `fa0ab0c` (base pós-ship Loop 2)  
Estrutura: **a)** continua no mesmo slug (Loops 1–2 arquivados/shipados)

## Ideia

Abrir o **Loop 3** do roadmap acordado: amarrar a camada agentic DE (10 agents + 7
commands + KBs) ao **kernel já executável** (norma + CLI A–D), criar a skill
`de-conformidade`, adicionar KB `databricks`, e **propagar tudo** via
`pipeline_dados` no `/install-harness` — sem segundo framework e **sem** live API.

## Herança dos Loops 1–2 (não renegociar)

| Item | Valor |
|---|---|
| Norma | `data-engineering.yaml` (perfis yarn + Databricks; pacotes A–D) |
| CLI | `config.canonical_data_check` (validate / baseline / compare / report / explain) |
| Path filho | `.harness/data-check/` + seed-once (`seed: true` → KEEP) |
| Examples | `spark-yarn-airflow-min`, `databricks-sdp-min`, `databricks-dlt-min` |
| SI | **c + d** |
| Tipo | e — evolução do harness / framework |
| Espelho | `.claude/` ↔ `.cursor/` obrigatório |
| Sem live API | checks só filesystem (UC/DAB/SDP/DLT) |
| Branch | `feat/de-agents-skills-loop3` |
| Estrutura | mesmo slug |

## Escopo fechado (decisões 1–4)

1. **Ship Loop 2 primeiro** — JÁ FEITO (PR 215002 / retro `10-loop2-retro.md`)
2. **Escopo:** agents + skills + KBs + propagar install
3. **Propagação:** TODOS os 10 agents + 7 commands DE em `pipeline_dados`
4. **Novos:** evoluir existentes + **1** skill DE (`de-conformidade`) + KB `databricks`

## Fora deste loop

- Live Databricks / workspace API no CI
- Quebrar seed KEEP / apagar baseline no re-install
- Segundo framework paralelo à CLI
- Renomear/remover agents existentes (só amarrar + evoluir)

## Soft-blocks

- `git fetch` 403 Azure — soft-block conhecido; continuar na branch local `feat/de-agents-skills-loop3`
