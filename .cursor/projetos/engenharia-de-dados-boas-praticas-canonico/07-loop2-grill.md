# Grill — Loop 2 Databricks (kernel DE canônico)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Branch: `feat/de-databricks-loop2`  
Contexto: Loop 1 shipped · `06-loop2-ideia.md` · `00c-codebase-loop2.md` · sketch DE

## Entendimento compartilhado

Estender o **mesmo** kernel normativo (`data-engineering.yaml` + `canonical-data-check`) para
perfis Databricks, com examples greenfield e baseline/`/validar` evoluídos — **sem** segundo
framework e **sem** Loop 3 (agents/skills/KBs DE novas).

## Decisões

| # | Tema | Escolha |
|---|---|---|
| 1 | Estrutura projeto | **a)** mesmo slug |
| 2 | SI | **a)** permanece **c + d** |
| 3 | Perfis MVP | **c)** `sdp` **e** `dlt` no mesmo ship |
| 4 | Checks bloqueantes | **c)** completo do grill (SDP/DLT + schema rescue + UC FS + DAB) |
| 5 | Piloto prova | **a)** só example greenfield no canônico |
| 6 | Layout examples | **b)** dois examples (`…-sdp-min` e `…-dlt-min`) |
| 7 | Install | **a)** só YAML + CLI; `pipeline_dados` inalterado |
| 8 | Seleção de perfil | **b)** auto-detect + override em `project_profile.yaml` |
| 9 | Ambiguidade SDP+DLT | **b)** união dos checks; profile `databricks-multi` |
| 10 | Pacote Universal A | **a)** sempre A + checks cloud |
| 11 | Baseline / waiver | **b)** reusa Loop 1 + campo `profiles[]` |
| 12 | `/validar` | **b)** marker **ou** auto-detect Databricks |
| 13 | Codebase-explorer | **a)** `00c-codebase-loop2.md` |
| 14 | IDs de perfil YAML | **b)** `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` |
| 15 | Pacotes checks cloud | **b)** pacote **D** `databricks-cloud` + regras condicionais SDP/DLT |

## IDs canônicos (acordados)

| Profile ID | Uso |
|---|---|
| `databricks-sdp-medallion` | Example / projeto SDP |
| `databricks-dlt-legacy` | Example / projeto DLT |
| `databricks-multi` | Tree com sinais SDP **e** DLT (união de checks) |

| Package | Papel |
|---|---|
| A | Universal (sempre) |
| B | Perfil `spark-yarn-airflow` (Loop 1 — inalterado) |
| C | Airflow condicional (Loop 1 — inalterado) |
| D | `databricks-cloud` — regras condicionais por sinal SDP/DLT |

## Fora deste loop

- Loop 3: skills / agents / KBs DE novas
- Ampliar categoria `pipeline_dados` / keywords Databricks no stack_map
- Brownfield RO Databricks / sql-capacity write
- Segundo framework paralelo à CLI

## Riscos / atenção (do `00c`)

- Engine hoje hardcoda A/B/C → precisa dispatch/registry para pacote D
- Baseline v1 só tem `profile` singular → adicionar `profiles[]` com compat
- `de_marker` hoje só existência de arquivo → auto-detect DAB/DLT/SDP
- DEFAULT_PROFILE / seed templates ainda spark-yarn

## Próximo passo

1. (Opcional) adversarial judge no grill  
2. `harness-define` / PRD Loop 2 → `08-loop2-prd.md`  
3. Harness plan → `09-loop2-harness.md` → `/to-tasks`
