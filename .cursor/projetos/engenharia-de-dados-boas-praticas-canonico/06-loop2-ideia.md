# Loop 2 — Ideia (Databricks)

Slug (mesmo projeto): `engenharia-de-dados-boas-praticas-canonico`  
Iniciado em: 2026-08-06  
Branch: `feat/de-databricks-loop2` @ `3aa12f2` (base `master` pós-ship Loop 1)  
Estrutura: **a)** continua no mesmo slug (após Loop 1 arquivado)

## Ideia

Abrir o **Loop 2** do roadmap acordado no Loop 1: evoluir o kernel de conformidade DE no
canônico para **Databricks** (SDP/DLT, DAB, Unity Catalog), reusando
`data-engineering.yaml` + CLI `canonical-data-check` — sem segundo framework e **sem**
abrir ainda o Loop 3 (skills/agents/KBs DE novas).

## Herança do Loop 1 (não renegociar sem motivo)

| Item | Valor |
|---|---|
| Norma | `data-engineering.yaml` |
| CLI | `config.canonical_data_check` |
| Path filho | `.harness/data-check/` + seed-once |
| Install | pacote mínimo verificável; sem 10 agents DE |
| SI | **c + d** (confirmado Loop 2 — opção a) |
| Tipo | e — evolução do harness / framework |
| Fora | Loop 3 skills/agents/KBs DE |
| Branch | `feat/de-databricks-loop2` |
| Estrutura | **a)** mesmo slug |

## Escopo preliminar (a grillar)

- Perfis cloud no MVP: **`sdp-medallion` + `dlt-legacy`** (opção c — mesmo ship)
- Checks bloqueantes: **pacote c** — SDP/DLT essentials + schema rescue policy + Unity Catalog
  grants/linhagem checáveis em filesystem + DAB bundle validável
- Example greenfield: **dois** examples separados (opção **b**) — `…-sdp-min` e `…-dlt-min`
- Install: **a)** só estende norma YAML + checks na CLI; categoria `pipeline_dados` inalterada
- Seleção de perfil: **b)** auto-detect (DAB/DLT/SDP no tree) + override em `project_profile.yaml`
- Ambiguidade SDP+DLT: **b)** união dos checks; profile `databricks-multi` (ou similar)
- Pacote Universal A: **a)** sempre A + checks cloud (SDP e/ou DLT)
- Baseline/waiver: **b)** reusa Loop 1 + campo `profiles[]` no baseline
- `/validar`: **b)** marker **ou** auto-detect Databricks dispara data-check
- Pacotes checks cloud: **b)** pacote **D** `databricks-cloud` + regras condicionais SDP/DLT
- IDs de perfil: **b)** `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi`
- Quarentena DLT / schema rescue (incluídos no pacote c)

## Soft-blocks

- `git fetch` 403 no ambiente do agente — branch criada a partir de `master` local @ `3aa12f2`
  (usuário havia validado alinhamento com remote).
