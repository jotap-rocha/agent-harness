# Fluxo-events no Dev Loop + backfill de commits

## Ideia

Fechar duas dívidas de processo deixadas pelo ship da visão gráfica / chore tasks-por-slug:

1. **Dev Loop live** — hoje só o SDD (brainstorm→ship) emite telemetria `fluxo-events` e
   avisa o usuário sobre `live.html`. O Dev Loop (`prompt-crafter`, `dev-loop-executor`,
   artefatos `PROMPT`/`PROGRESS`/`LOG`) **não** alimenta o painel gráfico. Incluir emit
   fail-soft + aviso UX no enter do Dev Loop, reutilizando o kernel existente
   (`fluxo-events.yaml` + `config/fluxo_events/`), sem mini-app SSE e sem misturar com
   evidence-gate.

2. **Backfill de commits** — linhas 58–65 em `metrics/entregas.jsonl` ainda têm
   `"commit": "pending"` embora o trabalho já tenha sido commitado/mergeado. Corrigir os
   SHAs reais para o scorecard/histórico ficarem auditáveis.

Em resumo: **mesmo painel live cobrindo Dev Loop + higiene de delivery records** — evolução
do harness canônico (não produto).

### Escopo explícito (desta ideia)

- Wiring Dev Loop → `emit`/`render` (+ path de `fluxo/` — decidir no grill: slug do
  projeto SDD ativo vs pasta `.claude/dev/` vs outro)
- Aviso UX ao usuário no enter do Dev Loop (espelho da task 66 do SDD)
- Backfill mecânico ou documentado dos `commit` em entregas 58–65
- Testes de presença/wiring + espelho `.claude`↔`.cursor`
- Docs: cheatsheet / DEV-LOOP.md / ADR se houver decisão contestável

### Fora (não reabrir sem grill)

- SSE / Canvas MUST
- Unificar com evidence-gate
- Substituir PROGRESS.md / STATUS.md
- Guardrail orthografia PT-BR genérico (dívida separada, opcional se couber)

### Contexto / débitos que motivam

- Grill/PRD `visao-grafica-fluxo-agentes`: Dev Loop = Fase 2 / COULD
- Retro chore: entregas 58–65 com `commit: "pending"`
- Task 66 já avisou UX só no SDD (brainstorm/build)

## SI Assessment

Nível: **a** — Não — apenas metadados de processo / paths / SHAs de commit (sem PII)

Implicações:
- Harness mínimo de SI (rules/seguranca.md)
- Eventos: só metadados (agent, phase/loop, task id, timestamps) — nunca prompts/PII/secrets
- Backfill: só short SHA já públicos no git — sem secrets

## Tipo de Projeto

**e** — Evolução do **harness canônico** / ferramenta transversal

Stack prevista:
- Kernel existente `fluxo-events` (sem novo pacote, salvo helpers mínimos)
- Agents/skills Dev Loop: `prompt-crafter`, `dev-loop-executor`, `DEV-LOOP.md`, `.claude/dev/`
- `metrics/entregas.jsonl` + possivelmente script/one-shot de backfill
- Espelho dual-tree

## Soft-blocks registrados

- `git fetch` Azure 403 — branch local a partir de `master` @ `b4f6c86`
- CONTEXT_REBIND: N/A (evolução do canônico)
- Codebase-explorer: **não** solicitado (gap já conhecido)

## Próximos passos

1. Rode `/grill-me` para fechar: onde gravar `fluxo/` no Dev Loop, schema de `event_type`
   (ex. `dev_loop_enter`), escopo do backfill (só 58–65 vs todas `pending`), MoSCoW
2. Depois: `harness-define` → `harness-design` → `/to-tasks` → `harness-build`
