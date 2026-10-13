# 00c — Codebase map (foco Loop 2 / Databricks)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Repo: `<raiz-do-clone>`  
Pré-requisito: Loop 1 shipped (`05-retro.md`, tasks 09–16 done)  
Ideia Loop 2: `06-loop2-ideia.md` · STATUS: `STATUS.md`  
Sketch adversarial: `sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`  
Mapa pré-kernel (histórico): `00b-codebase.md`

> Mapeamento somente leitura via `codebase-explorer`. Não inventa artefatos ausentes; cita paths reais.

---

## Executive Summary — Agent Harness Canônico

**O que faz:** Framework do Agent Harness Method — fonte de verdade de agents, skills, KBs, rules e (desde o Loop 1) um **kernel executável** de conformidade DE. Não é produto de pipeline; propaga artefatos via `/install-harness` para projetos-filho.

**Stack:** Python 3.11+ (stdlib + CLI `config.canonical_data_check`) · YAML normativo · pytest · espelho `.claude/` ↔ `.cursor/`. Sem `docker-compose`, sem `pyproject.toml`/`package.json` na raiz; `requirements.txt` é marcador (install usa só stdlib).

**Entry point (kernel DE):** `python -m config.canonical_data_check` → `config/canonical_data_check/__main__.py` → `cli.main` (`config/canonical_data_check/cli.py`).

**Portas expostas:** nenhuma (não há app HTTP).

**Convenções notáveis:**
1. Norma em `data-engineering.yaml`; loader tipado em `config/data_engineering/`; checks em `config/canonical_data_check/checks/`.
2. Runtime no filho: `.harness/data-check/` (seed-once, `seed: true` no install).
3. Install `pipeline_dados` **não** copia agents/commands DE — só norma + rule + KB pipeline + seed.
4. `/validar` só chama data-check se existir marker `project_profile.yaml` (Loop 2: ampliar para auto-detect).
5. Espelho obrigatório `.claude/` ↔ `.cursor/` (rules `.md` → `.mdc`).

### O que o Loop 1 deixou implementado

| Peça | Path / evidência |
|---|---|
| Norma | `data-engineering.yaml` — perfil único `spark-yarn-airflow`, pacotes A/B/C, regras DE-A001…DE-C003 |
| Loader | `config/data_engineering/contract.py`, `yaml_loader.py` |
| CLI | `validate` / `baseline` / `compare` / `report` / `explain` em `config/canonical_data_check/cli.py` |
| Checks | `checks/package_a.py`, `package_b.py`, `package_c.py` (C condicional via `detect_airflow`) |
| Example | `examples/spark-yarn-airflow-min/` (fora do stack_map) |
| Baseline/waiver | `baseline.py` + templates em `templates/data-check/` + `SCHEMA.md` |
| Install mínimo | `stack_map.json` categoria `pipeline_dados` + seed `.harness/data-check` |
| `/validar` | `.claude/commands/validar.md` + `de_marker.py` |
| RO sql-capacity | `ro_report.py` → `reports/sql-capacity-compliance.json` (somente leitura) |
| Testes | `tests/data_engineering/` (8 módulos) |
| Tasks | `tasks/09`…`16` marcadas done em `tasks/README.md` |

### O que já existe de Databricks/DE fora do kernel normativo

Camada rica de **prompts/docs** (não enforcement Databricks):

- **10 agents** em `.claude/agents/data-engineering/` (espelho `.cursor/`)
- **7 commands** em `.claude/commands/data-engineering/`
- **KBs** DE-adjacentes: `airflow`, `spark`, `lakehouse`, `pipeline`, `data-quality`, `dbt`, `data-modeling`, `sql-patterns`, `streaming`, `cloud-platforms`
- **Rule** `pipeline.md` / `.mdc` — Medallion + ponte para a norma YAML
- **Nenhuma skill DE dedicada**
- Sketch + PRD/grill do projeto já separam Databricks como **Loop 2**

### Gaps óbvios para Loop 2

1. Só um perfil no YAML (`spark-yarn-airflow`); ausentes `sdp-medallion` / `dlt-legacy` (e `databricks-multi`)
2. Engine hardcoda A/B/C (`engine.py`) — precisa registry/dispatch
3. `DEFAULT_PROFILE = "spark-yarn-airflow"` em CLI, constants, templates, seed
4. Sem examples Databricks
5. `de_marker` só testa existência do arquivo — sem ler `profile:` e sem auto-detect DAB/DLT/SDP
6. Baseline schema `version: 1` com `"profile"` singular — **não existe `profiles[]`**
7. `pipeline_dados` keywords = `airflow|spark|dbt` — inalterado por acordo Loop 2
8. Naming sketch vs ideia: sketch `databricks-sdp-medallion` / `databricks-dlt-legacy`; ideia `sdp-medallion` / `dlt-legacy`
9. Loop 2 **não** deve criar agents/skills/KBs novas (Loop 3)

---

## Deep Dive

### 1. Entry points relevantes

| Peça | Path | Papel |
|---|---|---|
| Norma | `data-engineering.yaml` | `profiles` + `packages` A/B/C |
| Contrato | `config/data_engineering/contract.py` | load tipado |
| CLI | `config/canonical_data_check/cli.py` | subcomandos + `--profile` |
| Engine | `config/canonical_data_check/engine.py` | orquestra A/B/C |
| Baseline | `config/canonical_data_check/baseline.py` | ratchet + waivers |
| Marker | `config/canonical_data_check/de_marker.py` | gate `/validar` |
| Seed | `config/canonical_data_check/templates/data-check/` | → `.harness/data-check/` |
| Example | `examples/spark-yarn-airflow-min/` | greenfield A+B(+C stub) |
| Install | `.claude/skills/install-harness/scripts/stack_map.json` | `pipeline_dados` |
| `/validar` | `.claude/commands/validar.md` | ruff/mypy/pytest + DE condicional |

### 2. Perfis/checks A/B/C — extensibilidade

- YAML: `profiles.<id>.packages` + pacotes com `applicability` / `severity`
- Engine: dispatch **hardcoded** `check_package_a|b|c` — gap para registry
- Acordo Loop 2: sempre A + checks cloud; ambiguidade → união + `databricks-multi`

### 3. Baseline / waiver

- Layout: `project_profile.yaml` + `baseline.json` + `waivers.yaml`
- `baseline.json` v1: `profile` **singular**; findings sem `message` (SI)
- Waivers: por `rule_id` + owner + expiry
- `profiles[]`: **ainda não existe** — acordo Loop 2 para adicionar

### 4. Agents / commands / KBs DE (não tocar no Loop 2)

Ver lista completa no Executive Summary. Install **não** propaga agents/commands DE.

### 5. Espelho `.claude` ↔ `.cursor`

Invariante em `CLAUDE.md`. Kernel Python não duplica em `.cursor/`.

### 6. Testes

`tests/data_engineering/` — cobertura alta do perfil piloto; **zero** para Databricks ainda.

### 7. Docs / projeto

```
.claude/projetos/engenharia-de-dados-boas-praticas-canonico/
  00-ideia.md … 05-retro.md, 06-loop2-ideia.md, STATUS.md
  00c-codebase-loop2.md  ← este arquivo
```

### Mapa mental — herança Loop 1 → escopo Loop 2

```text
data-engineering.yaml          ← ESTENDER (novos profiles + rules)
config/canonical_data_check/   ← ESTENDER (checks, engine, marker, baseline)
examples/                      ← ADICIONAR sdp-min + dlt-min
tests/data_engineering/        ← ADICIONAR cobertura novos perfis
stack_map pipeline_dados       ← INALTERADO (acordo)
agents/skills/KBs DE           ← NÃO TOCAR (Loop 3)
```
