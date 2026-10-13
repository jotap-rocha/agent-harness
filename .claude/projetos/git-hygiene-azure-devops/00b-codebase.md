# Codebase map — agent-harness-canonico-v2

> Gerado no harness-brainstorm (passo 1) a partir do codebase-explorer.
> Data: 2026-08-06. Uso: contexto para `/grill-me` e harness-define.

## Executive Summary

Este repositório é o **framework canônico** do Agent Harness Method — fonte de verdade de
agents, skills, rules, KBs e commands. Não há produto/runtime HTTP. Propagação para
projetos-alvo ocorre exclusivamente via `/install-harness` (scripts + `stack_map.json`),
com espelhamento obrigatório `.claude/` ↔ `.cursor/`.

A capacidade de **Git hygiene / Azure DevOps** ainda **não está implementada**. Existe
apenas o plano em `sketch/portal-git/plan.md`. O MVP natural é a Fase 1 desse plano
(convenção: rule, yaml, `/nova-branch`, hooks, template PR), mais a correção da lacuna
de propagação dos agents `harness-*` no `stack_map.json`.

`config/pipeline_config.py` é **scaffold intencional** de engenharia de dados (não
resíduo a remover).

## Deep Dive

### Entry points do harness

| Comando / fluxo | Papel |
|---|---|
| `/novo-projeto` → harness-brainstorm | Captura ideia + SI + tipo |
| `/grill-me` → harness-define | Aprofunda requisitos |
| `/install-harness` | Detecta stack, Install Plan, copia artefatos |
| `/validar` | Gate de qualidade (hoje assume Python: ruff/mypy/pytest) |
| `/dev` / Dev Loop | Execução ágil de tarefa pontual |
| `/sync-context` | Drift de contexto vs código |
| `/scorecard` | Métricas de entrega |

### Propagação (`install-harness`)

- Fonte: `.claude/skills/install-harness/scripts/stack_map.json` + `install_harness.py`
- Mirror automático para `.cursor/`
- **Lacuna crítica:** agents `harness-*` (workflow) **não** estão no `stack_map.json` —
  mudanças neles **não chegam** aos projetos-filho via install. Qualquer wiring de
  GIT_PREFLIGHT / ship / build nesses agents precisa incluir a correção do mapa.

### O que já existe vs o que falta (Git / Azure)

| Artefato | Estado |
|---|---|
| `sketch/portal-git/plan.md` | Decisões e fases documentadas |
| `git-hygiene.yaml` | Ausente |
| Rule `git-hygiene` (+ espelho `.mdc`) | Ausente |
| Command `/nova-branch` | Ausente |
| `.githooks/` + bootstrap `core.hooksPath` | Ausente |
| `.azuredevops/pull_request_template.md` | Ausente |
| Adapter `scm: azure \| github` | Ausente |
| Baseline / pipeline guardrails / `metrics/git-hygiene.jsonl` | Ausente (Fase 2+) |
| `repo_profile` no CLAUDE.md filho | Ausente (`/validar` ainda Python-only) |

### Pontos de extensão (onde pluguar)

| Componente | Extensão prevista |
|---|---|
| `install-harness` + `stack_map.json` | Propagar rule, command, hooks, template Azure; incluir agents `harness-*` |
| `dev-loop-executor` | Step 0 `GIT_PREFLIGHT` (branch isolada + sync remoto) |
| `harness-build` / `harness-ship` | Preflicht de branch; título de PR + tag `prod-*` |
| `revisor-codigo` | Sinalizar (não bloquear) diff produzido no tronco |
| `prompt-crafter` | Seção `## Git` com branch sugerida |
| `to-issues` / scorecard | Hoje centrados em GitHub/`gh` — adapter Azure (`az`) no MVP ou depois |
| Rule transversal | Invariantes agnósticos; fornecedor via `scm` no CLAUDE.md filho |

### Riscos de SI e operação

- Secrets/PAT: somente env ou secret manager; nunca logs
- Sem `Edit policies`: gates locais são contornáveis — declarar isso explicitamente
- Espelhamento `.claude` ↔ `.cursor` é invariante; divergência quebra projetos Cursor
- Path canônico documentado em CLAUDE.md (`<raiz-do-canonico>`)
  diverge deste clone v2 — tratar no grill se necessário
- Hooks ausentes em clone limpo sem bootstrap do install

### Recomendação de escopo (MVP)

Fase 1 do plano (caminho fácil / convenção) **+** correção de propagação no
`stack_map.json`. Fora do MVP: portal UI, policies Azure, deploy automático,
rename `master→main`, pipeline de detecção completo, `repo_profile` (Fase 4).
