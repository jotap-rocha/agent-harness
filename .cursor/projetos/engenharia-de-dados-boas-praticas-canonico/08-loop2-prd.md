# PRD — Kernel DE Databricks (Loop 2 / Ship 2)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Repo: Agent Harness Canônico (framework — **não** produto ETL de domínio)  
Branch: `feat/de-databricks-loop2`  
Data: 2026-08-07  
Tipo: **e** — evolução do framework de conformidade de Engenharia de Dados  
SI: **c + d** (confirmado)  
Fontes: `06-loop2-ideia.md`, `00c-codebase-loop2.md`, `07-loop2-grill.md` (15 decisões),  
`05-retro.md` (Loop 1), sketch `sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`

> Este PRD descreve **somente o Loop 2**. Loop 3 (skills/agents/KBs DE) e mudanças em
> `pipeline_dados` keywords/stack_map estão **fora**. Judge adversarial do grill: **pulado (b)**.

---

## Problem Statement

O Loop 1 entregou um kernel executável para o perfil on-prem `spark-yarn-airflow`
(norma + CLI A/B/C + example + baseline/waiver + install mínimo + `/validar` condicional).
Projetos Databricks (SDP/DLT/DAB/UC) ainda **não** são cobertos pelo validator: o YAML tem um
único perfil, o engine hardcoda A/B/C, não há examples cloud, o marker só testa existência de
arquivo e o baseline não registra múltiplos perfis.

Mantenedores do canônico e engenheiros DE em filhos cloud precisam do **mesmo** mecanismo de
prova (não um segundo framework), com DoD mensurável nos perfis `databricks-sdp-medallion` e
`databricks-dlt-legacy`, sem expandir o catálogo agentic (Loop 3).

---

## Solution

Entregar o **Ship 2 / Loop 2** estendendo o kernel existente:

1. **Estender `data-engineering.yaml`** com perfis
   `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` e pacote **D**
   `databricks-cloud` (regras condicionais por sinal SDP/DLT).
2. **Estender a CLI** `canonical-data-check`: dispatch/registry além de A/B/C; validate sempre
   roda **A + D** quando perfil cloud (ou multi); B/C permanecem para spark-yarn.
3. **Auto-detect** de sinais Databricks (DAB/DLT/SDP no tree) + override em
   `project_profile.yaml`; ambiguidade SDP+DLT → união de checks e profile `databricks-multi`.
4. **Dois examples greenfield** no canônico (fora do install auto):
   `examples/databricks-sdp-min/` e `examples/databricks-dlt-min/` — validate PASS (A+D aplicável).
5. **Baseline**: reusar ratchet/waivers Loop 1 + campo **`profiles[]`** (compat com `profile`
   singular legado).
6. **`/validar`**: data-check se marker **ou** auto-detect Databricks.
7. **Install `pipeline_dados` inalterado** — filhos recebem norma/CLI atualizados via foundation
   `config/` + `data-engineering.yaml`.
8. **Testes** no canônico + espelho `.claude/` ↔ `.cursor/` nas promoções de commands/rules tocados.
9. **Sem** novos agents/skills/KBs DE; **sem** brownfield RO Databricks neste ship.

Ordem: estender norma → engine/checks D → marker/auto-detect → baseline `profiles[]` →
examples → `/validar` → testes.

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want Databricks profiles in `data-engineering.yaml`, so that cloud rules share the same normative source as spark-yarn.
2. As a mantenedor do canônico, I want package D `databricks-cloud` with conditional SDP/DLT rules, so that one package covers both without duplicating Universal A.
3. As a mantenedor do canônico, I want the engine to dispatch packages by registry (not hardcode A/B/C only), so that D plugs in cleanly.
4. As a mantenedor do canônico, I want `examples/databricks-sdp-min` to PASS validate (A+D), so that SDP DoD is demonstrable.
5. As a mantenedor do canônico, I want `examples/databricks-dlt-min` to PASS validate (A+D), so that DLT DoD is demonstrable.
6. As a mantenedor do canônico, I want a fixture tree with both SDP and DLT signals to resolve as `databricks-multi` and run the union of checks, so that ambiguity is deterministic.
7. As a mantenedor do canônico, I want baseline snapshots to record `profiles[]`, so that multi-profile ratchet is auditable.
8. As a mantenedor do canônico, I want pytest covering new profiles + auto-detect + `/validar` trigger, so that Loop 2 regressions fail CI.
9. As a mantenedor do canônico, I want NOT to create new DE agents/skills/KBs, so that Loop 3 stays gated.
10. As CI do canônico, I want validate on each Databricks example within ~60s, so that the gate stays practical.

### Engenheiro DE / filho Databricks

11. As an engenheiro DE, I want auto-detect of DAB/DLT/SDP artifacts, so that I do not always hand-edit profile before first validate.
12. As an engenheiro DE, I want `project_profile.yaml` to override auto-detect, so that edge cases stay under human control.
13. As an engenheiro DE, I want `/validar` to run data-check when Databricks signals exist even without marker, so that cloud repos are gated earlier.
14. As an engenheiro DE, I want Universal A always with cloud checks, so that secrets/destructive gates still apply on Databricks projects.
15. As an engenheiro DE, I want waivers with owner+expiry to still silence blockers by rule_id, so that exception policy stays consistent with Loop 1.
16. As an engenheiro DE, I want `explain` / `report` to work for D rule IDs, so that failures stay actionable.
17. As CI do filho, I want `compare` against baseline with `profiles[]`, so that only new findings fail.

### Segurança / SI (c+d)

18. As a responsável por SI, I want Universal secret/destructive checks on Databricks trees, so that prod risk (d) remains covered.
19. As a responsável por SI, I want UC grants/linhagem checks to be filesystem-based (no live workspace credentials in CI), so that the canônico stays secret-free.
20. As a responsável por SI, I want findings without dumping sensitive notebook/table payloads, so that LGPD expectations (c) hold in reports.

### Aceite testável (DoD Ship 2)

| # | Critério | Evidência |
|---|---|---|
| AC1 | YAML declara perfis `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` + pacote D | teste contrato/loader |
| AC2 | `validate` em `examples/databricks-sdp-min` → PASS (A + D aplicável) | pytest + comando |
| AC3 | `validate` em `examples/databricks-dlt-min` → PASS (A + D aplicável) | pytest + comando |
| AC4 | Tree com sinais SDP+DLT → profile efetivo `databricks-multi` + união de checks | teste unitário |
| AC5 | Auto-detect DAB/DLT/SDP; override via `project_profile.yaml` vence | teste |
| AC6 | Baseline grava/lê `profiles[]` (compat com `profile` legado) | teste baseline/compare |
| AC7 | `/validar`: marker **ou** auto-detect Databricks dispara data-check; sem ambos → não dispara | teste condicional |
| AC8 | `pipeline_dados` / stack_map **inalterado** (sem keywords Databricks novas) | assert stack_map |
| AC9 | Nenhum agent/skill/KB DE **nova**; espelho `.claude`↔`.cursor` se commands/rules tocados | revisão + diff |
| AC10 | Pacote D cobre (MVP bloqueante): layout/DAB · quarentena DLT · schema rescue policy · UC grants/linhagem em FS · ban padrões destrutivos já em A | testes de regras D + docs YAML |

---

## Implementation Decisions

Referência às **15 decisões do grill**:

| # | Decisão | Escolha neste PRD |
|---|---|---|
| 1 | Estrutura | mesmo slug |
| 2 | SI | c + d |
| 3 | Perfis MVP | SDP **e** DLT no mesmo ship |
| 4 | Checks | pacote completo (SDP/DLT + schema rescue + UC FS + DAB) |
| 5 | Piloto | só examples greenfield |
| 6 | Examples | dois separados (`databricks-sdp-min`, `databricks-dlt-min`) |
| 7 | Install | YAML+CLI only; `pipeline_dados` inalterado |
| 8 | Seleção perfil | auto-detect + override |
| 9 | Ambiguidade | união → `databricks-multi` |
| 10 | Universal A | sempre A + cloud |
| 11 | Baseline | + `profiles[]` |
| 12 | `/validar` | marker **ou** auto-detect |
| 13 | Codebase map | `00c-codebase-loop2.md` |
| 14 | Profile IDs | `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` |
| 15 | Package | **D** `databricks-cloud` condicional |

### Pacote D (detalhe — decisão 4 + 15)

Checks bloqueantes no filesystem do repo-alvo (sem API Databricks autenticada no CI do canônico):

| Área | Exemplos de sinal / regra (IDs finais no YAML) |
|---|---|
| DAB / job config | bundle ou job YAML presente; owner/run identity declarado |
| SDP medallion | paths/camadas ou pipeline SDP declarados |
| DLT | pipeline DLT / expectations; **quarentena** declarada |
| Schema rescue | policy documentada (fail vs quarantine) |
| Unity Catalog | grants/linhagem **arquivos** versionados (YAML/SQL/md de política) — não live UC |
| SI | herda A (secrets, destrutivo) |

Sinais de auto-detect (mínimo): paths/arquivos típicos DAB (`databricks.yml` / `bundle*.yml`), DLT (`dlt`/`pipelines` com decorator/expectations), SDP (pastas/pipelines SDP acordadas no design). Heurística documentada no código + testes.

### Seams de teste (preferir existentes)

- Contrato YAML / loader (`tests/data_engineering/test_contract.py`)
- Engine validate + novos checks D
- `de_marker` / trigger `/validar`
- Baseline write/compare com `profiles[]`
- Examples SDP/DLT via subprocess CLI
- stack_map freeze (sem mudança `pipeline_dados`)

---

## Testing Decisions

- Testar **comportamento externo**: exit codes, profile efetivo, findings por `rule_id`, ausência de secret raw em report/baseline.
- Prior art: `tests/data_engineering/*` do Loop 1.
- Não mockar filesystem do example quando o real cabe em stubs estáticos (como DAG stub do Loop 1).
- Sem credenciais Databricks reais no CI.

---

## Out of Scope

- Loop 3: novos agents / skills / KBs DE
- Alterar keywords/categoria `pipeline_dados` no stack_map
- Brownfield RO Databricks; escrita em sql-capacity
- Validação live contra workspace Databricks / UC API
- Migrar filhos existentes automaticamente
- Segundo CLI ou norma paralela

---

## Further Notes

### Roadmap

| Loop | Foco |
|---|---|
| 1 (done) | `spark-yarn-airflow` |
| **2 (este PRD)** | Databricks SDP + DLT no mesmo kernel |
| 3 | skills / agents / KBs DE |

### Inferências `[inferido]`

- Nomes exatos dos examples: `examples/databricks-sdp-min/` e `examples/databricks-dlt-min/` `[inferido]` a partir do grill “…-sdp-min / …-dlt-min”.
- Lista precisa de globs de auto-detect será fechada no harness-design / implementação com testes `[inferido]`.
- Bump de baseline schema: preferir `profiles[]` adicional mantendo `profile` legado `[inferido]` (compat).

### Próximo passo

1. Aprovar este PRD  
2. `harness-design` → `09-loop2-harness.md`  
3. `/to-tasks` → tasks 17+  
4. `harness-build`
