# PRD — Loop 3 / Ship 3 (agents · skills · KBs DE · install completo)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Repo: Agent Harness Canônico (framework — **não** produto ETL de domínio)  
Branch: `feat/de-agents-skills-loop3` @ `fa0ab0c`  
Data: 2026-08-07  
Tipo: **e** — evolução do framework de conformidade de Engenharia de Dados  
SI: **c + d**  
Fontes: `11-loop3-ideia.md`, `00d-codebase-loop3.md`, `12-loop3-grill.md`,
`10-loop2-retro.md`

> Este PRD descreve **somente o Loop 3**. Kernel A–D (Loops 1–2) é **pré-condição** e
> não é renegociado. Judge adversarial: **pulado** (decisões 1–4 já fechadas pelo
> mantenedor).

---

## Problem Statement

Loops 1–2 entregaram um kernel mensurável (norma + CLI + examples + `/validar`). A
camada agentic DE (10 agents, 7 commands, KBs) ainda opera **desacoplada**: não cita
IDs DE-*, não manda rodar o gate, não ensina baseline/waiver, e o install
`pipeline_dados` **proíbe** copiar agents/commands (freeze/tests reforçam isso).

Resultado: filhos recebem conformidade executável sem o “como agir” agentic; agentes
no canônico podem “resolver” fora do validator — falsa autonomia e DoD inauditável.

---

## Solution

Entregar o **Ship 3 / Loop 3**:

1. **Amarrar os 10 agents** com seção Kernel DE por domínio (tabela do grill).
2. **Amarrar os 7 commands** ao gate + agent atualizado.
3. **Pontes curtas** nos 10 KBs DE-adjacentes (IDs / pacotes — sem duplicar norma).
4. **Novo KB `databricks`** alinhado a DE-D001–005 + `_index.yaml`.
5. **Skill `de-conformidade`** (única skill DE nova) — findings → remediação →
   baseline/waiver.
6. **Install completo `pipeline_dados`**: propagar 10 agents + 7 commands (+ skill/KB
   conforme stack_map) e **reescrever** freeze/install asserts.
7. **Regressão**: examples verdes + fixture de install prova cópia.
8. **Freeze DoD Loop 3**: novo baseline de inventário + gate completo.
9. **Espelho** `.claude`↔`.cursor`; **seed KEEP** preservado; **sem live API**.

---

## User Stories

### Mantenedor do canônico

1. As a mantenedor, I want each DE agent to declare which DE-* packages/IDs it owns, so that advice stays grounded in the kernel.
2. As a mantenedor, I want DE commands to point at `/validar` and the wired agent, so that slash flows hit the gate.
3. As a mantenedor, I want KB bridges (not copies) to rule IDs, so that norma stays single-sourced in YAML.
4. As a mantenedor, I want a `databricks` KB domain for D001–D005, so that JIT docs match package D.
5. As a mantenedor, I want skill `de-conformidade` to turn CLI findings into remediation or waiver guidance, so that humans/agents share one playbook.
6. As a mantenedor, I want `pipeline_dados` to copy all 10 agents and 7 commands, so that filhos get the full agentic DE layer.
7. As a mantenedor, I want freeze/install tests updated to **require** that copy, so that Loop 2 “forbid agents” policy does not regress the new DoD.
8. As CI, I want examples yarn/SDP/DLT still PASS validate after Loop 3 docs/install changes.

### Engenheiro DE / filho

9. As an engenheiro DE, I want installed agents to tell me to run validate before “done”, so that DoD is the same as canônico.
10. As an engenheiro DE, I want `de-conformidade` to explain a failing `rule_id` and when to baseline vs fix, so that waivers stay owned+dated.
11. As an engenheiro DE, I want re-install to KEEP my `.harness/data-check` baseline/waivers, so that ratchet history survives harness updates.
12. As an engenheiro DE, I want Databricks concepts in KB without needing live workspace credentials.

### SI (c+d)

13. As SI owner, I want agents/skill to never suggest live UC API secrets in CI, so that (d) stays filesystem-only.
14. As SI owner, I want findings/remediation guidance without logging PII payloads, so that (c) holds.

### Aceite testável (DoD Ship 3)

| # | Critério | Evidência |
|---|---|---|
| AC1 | Cada um dos 10 agents DE tem seção Kernel com amarras do grill (todos DE-A*; domínio específico) | teste de inventário / grep estruturado + revisão |
| AC2 | Cada um dos 7 commands DE aponta gate (`/validar` ou CLI validate) + agent amarrado | teste inventário commands |
| AC3 | 10 KBs DE-adjacentes têm ponte curta a IDs/pacotes **sem** colar texto normativo | teste presença âncora + amostr de anti-duplicação leve |
| AC4 | Existe `kb/databricks/` (index + quick-ref + concepts + patterns) alinhado DE-D001–005; `_index.yaml` atualizado; espelho | pytest / file asserts |
| AC5 | Existe skill `de-conformidade` (SKILL.md + recursos) cobrindo findings → remediação → baseline/waiver; espelho | file asserts + smoke de estrutura write-a-skill |
| AC6 | `stack_map` `pipeline_dados` declara cópia dos 10 agents + 7 commands (e artefatos skill/KB acordados); `SKILL.md` install atualizado; seed KEEP intacto | teste stack_map + install plan |
| AC7 | Fixture install prova que agents/commands DE **são copiados** (asserts Loop 1–2 de ausência **removidos/invertidos**) | teste install |
| AC8 | `validate` nos 3 examples continua PASS | pytest regressão |
| AC9 | Novo freeze Loop 3: inventário agents/commands/skill/KB esperado; gate ruff+mypy+pytest (+ data-check examples) verde | freeze + gate |
| AC10 | Espelho `.claude`↔`.cursor` para todo artefato tocado em agents/commands/skills/kb/rules | diff/assert espelho |
| AC11 | Sem live API / secrets novos; SI c+d preservado | revisão SI + ausência de credenciais em artefatos |

---

## Implementation Decisions

| # | Decisão | Escolha |
|---|---|---|
| 1 | Ordem vs Loop 2 | Loop 2 já shipado — não reabrir |
| 2 | Escopo | agents + skills + KBs + install |
| 3 | Propagação | todos 10 + 7 em `pipeline_dados` |
| 4 | Novos | evoluir + skill `de-conformidade` + KB `databricks` |
| — | SI | c + d |
| — | Live API | não |
| — | Seed | KEEP preservado |
| — | Espelho | obrigatório |

### Amarras (resumo — detalhe no grill)

- todos → DE-A\*  
- spark-engineer → A+B  
- pipeline-architect → A+B+C  
- data-quality-analyst → A + D003/D004  
- lakehouse-architect / data-platform-engineer → A+D  
- schema-designer → A + D004  
- demais → A (+ D se cloud)

---

## Testing Decisions

- Preferir **testes de inventário** (existência de seções/âncoras, paths no stack_map,
  fixture install) — agents são markdown; não mockar LLM.
- Reusar suíte `tests/data_engineering/` para regressão de examples e seed KEEP.
- Reescrever `test_freeze_stackmap_regressao.py` e asserts de ausência em
  `test_install_pacote_minimo.py` como parte das tasks 30–32 (não “comentar” asserts).
- Gate final = `/validar` semantics do canônico + validate explícito nos 3 examples.

---

## Out of Scope

- Mudar regras/checks executáveis A–D (exceto docs que apontam a eles)
- Live Databricks API / sql-capacity write
- Remover agents/commands existentes
- Keywords Databricks obrigatórias no detector (opcional só se task 30 precisar —
  default: manter keywords yarn/dbt e forçar categoria / artefatos explícitos; **não**
  exigir keywords Databricks neste PRD)
- Loop 4+ (outros cloud vendors, brownfield RO Databricks)

---

## SI Considerations

| Tema | Tratamento Loop 3 |
|---|---|
| PII (c) | Skill/agents: não logar payloads; findings já sem `message` sensível no baseline |
| Prod write/delete (d) | Continuar apontando DE-A destrutivo; nunca sugerir credencial live para “passar o gate” |
| Secrets | Nenhum secret em KB/skill/agent; env/secret manager só como menção de anti-padrão |
| Seed KEEP | Re-install não apaga baseline/waivers do filho |

---

## Ordem sugerida de tasks

```text
25 agents → 26 commands → 27 KB pontes → 28 KB databricks → 29 skill
    → 30 install completo → 31 regressão examples+install → 32 freeze DoD
```

Numeração: **25–32**.
