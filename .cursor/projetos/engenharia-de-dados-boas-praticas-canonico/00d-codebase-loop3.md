# 00d — Codebase map (foco Loop 3 / agents · skills · KBs · install)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Repo: `<raiz-do-clone>`  
HEAD planejamento: `feat/de-agents-skills-loop3` @ `fa0ab0c`  
Pré-requisito: Loop 2 shipped (`10-loop2-retro.md`, tasks 17–24 done)  
Ideia Loop 3: `11-loop3-ideia.md` · mapas anteriores: `00b-codebase.md`, `00c-codebase-loop2.md`

> Mapeamento somente leitura. Não inventa artefatos ausentes; cita paths reais.

---

## Executive Summary

**O que o canônico tem hoje (pós Loop 2):** kernel de conformidade DE **executável**
(norma + CLI A–D + examples yarn/SDP/DLT + baseline `profiles[]` + `/validar` com
marker **ou** auto-detect SDP/DLT) **e**, em paralelo, uma camada agentic DE **rica em
prompts** mas **desacoplada** do kernel — install mínimo, freeze tests que **proíbem**
copiar agents/commands, e **zero** skill DE dedicada / **zero** KB `databricks`.

**Problema do Loop 3:** agents/commands/KBs não citam gate `/validar`, IDs DE-* nem
fluxo baseline/waiver; filhos `pipeline_dados` não recebem a camada agentic; não há
skill que leia findings da CLI nem domínio KB Databricks alinhado a DE-D001–005.

### Inventário agentic DE (existe, desacoplado)

| Peça | Path | Qtd | Ligação ao kernel |
|---|---|---|---|
| Agents | `.claude/agents/data-engineering/` (+ espelho `.cursor/`) | **10** | Nenhuma menção a DE-A*/CLI/`/validar` |
| Commands | `.claude/commands/data-engineering/` (+ espelho) | **7** | Acionam agents; sem ponte ao gate |
| Skills DE | — | **0** | `de-conformidade` **inexistente** |
| KB `databricks` | — | **0** | Domínio ausente em `_index.yaml` |
| KBs DE-adjacentes | `airflow`, `spark`, `lakehouse`, `pipeline`, `data-quality`, `dbt`, `data-modeling`, `sql-patterns`, `streaming`, `cloud-platforms` | **10** | Sem ponte curta a IDs DE-* |

**10 agents:** `data-contracts-engineer`, `data-platform-engineer`, `data-quality-analyst`,
`dbt-specialist`, `lakehouse-architect`, `pipeline-architect`, `schema-designer`,
`spark-engineer`, `sql-optimizer`, `streaming-engineer`.

**7 commands:** `data-contract`, `data-quality`, `lakehouse`, `migrate`, `pipeline`,
`schema`, `sql-review`.

### Kernel (herdado — não reabrir)

| Peça | Evidência |
|---|---|
| Norma | `data-engineering.yaml` — yarn + `databricks-*` + pacotes A–D |
| CLI | `python -m config.canonical_data_check` |
| Examples | `examples/spark-yarn-airflow-min`, `…-sdp-min`, `…-dlt-min` |
| Seed | `config/canonical_data_check/templates/data-check/` → `.harness/data-check/` (`seed: true`) |
| `/validar` | marker **ou** SDP/DLT; DAB isolado não ativa; sentinel canônico |

### Install `pipeline_dados` — pacote mínimo (Loop 1–2 freeze)

`stack_map.json` categoria `pipeline_dados`:

- Keywords: `airflow|spark|dbt` (sem Databricks keywords — Loop 2)
- Artifacts: `data-engineering.yaml` · `.claude/kb/pipeline` · `.claude/rules/pipeline.md` ·
  `.harness/data-check` (seed KEEP)
- Comentário explícito: **NÃO copiar agents/commands data-engineering**

### Freeze / asserts que o Loop 3 deve reescrever

| Teste | Comportamento atual | Gap Loop 3 |
|---|---|---|
| `test_freeze_stackmap_regressao.py` | Congela keywords + 4 paths; inventário 10 agents / skills / KBs **sem** `databricks` / `de-conformidade` | Novo baseline: agents+commands no stack_map; KB+skill permitidos |
| `test_install_pacote_minimo.py` | Assert **ausência** de `agents/data-engineering` e `commands/data-engineering` no plan | Inverter: fixture deve **provar cópia** dos 10+7 |
| Comentário `_comment` no stack_map | Proíbe cópia | Atualizar prosa + SKILL.md |

### Gaps óbvios para Loop 3

1. Agents sem seção **kernel DE-*** por domínio
2. Commands sem ponte ao gate + agent amarrado
3. KBs DE-adjacentes sem ponte curta a IDs (risco de duplicar norma se mal feito)
4. KB `databricks` inexistente (DE-D001–005 sem casa JIT)
5. Skill `de-conformidade` inexistente
6. Install mínimo ≠ propagação completa acordada
7. Freeze/install tests ainda codificam a política Loop 1–2 (proibir agents/commands)

---

## Deep Dive curto

### Mapa mental — herança → escopo Loop 3

```text
data-engineering.yaml / CLI / examples     ← INALTERADOS (salvo docs pontuais)
agents/data-engineering/* (10)             ← AMARRAR (seção kernel por domínio)
commands/data-engineering/* (7)            ← AMARRAR (gate + agent)
kb/{10 adjacentes}                         ← PONTE curta (sem duplicar norma)
kb/databricks/                             ← NOVO (index + QR + concepts + patterns)
skills/de-conformidade/                    ← NOVO (findings → remediação → baseline/waiver)
stack_map pipeline_dados                   ← EXPANDIR (10 agents + 7 commands + KB/skill)
tests freeze/install                       ← REESCREVER asserts
espelho .claude ↔ .cursor                  ← OBRIGATÓRIO em toda promoção
seed KEEP                                  ← PRESERVAR
```

### SI (c+d) — invariantes que permanecem

- Sem credenciais / live API no CI
- Findings sem dump de PII/payload sensível
- Operações destrutivas continuam bloqueadas no pacote A
- Seed KEEP: re-install não apaga baseline/waivers do filho
