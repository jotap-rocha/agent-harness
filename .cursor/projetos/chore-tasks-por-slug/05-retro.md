# chore-tasks-por-slug — Retrospectiva de Ship

Ship em: 2026-08-17  
Branch: `chore/tasks-por-slug`

## Escopo

Chore de fechamento (não greenfield SDD completo):

1. **Layout** — `tasks/{slug}/NN-*.md` alinhado a `.claude/projetos/{slug}/` (`351d15e`)
2. **Task 66** — aviso UX painel live no SDD brainstorm/build + `/fluxo-live` (`779ca99`)

## Métricas de entrega (scorecard breve)

| Métrica | Valor |
|---|---|
| Tasks desta chore | 1 entregável formal (66) + layout (chore sem issue NN) |
| Critérios de aceite (66) | 100% (4/4) |
| Tentativas até gate verde | 1 |
| Evidence-gate 66 | ok (4 critérios: brainstorm, build, fluxo_live, dual_tree) |
| Suite `tests/fluxo_events/` | 30 passed |
| ruff / mypy (`config/fluxo_events` + tests) | verde |
| Intervenções humanas (linha 66) | 0 |
| Taxa de autonomia (66) | 100% |
| Commit feature UX | `779ca99` |
| Commit layout | `351d15e` |

Gaps de scorecard: `git fetch` 403 (sem sync remoto); Azure/`gh` PR não medidos neste ship;
entregas 58–65 ainda com `commit: "pending"` (herança do ship anterior da visão gráfica).

## O que funcionou bem

- Layout por slug remove ambiguidade path/`Blocked by` e espelha o modelo mental de projetos.
- Fatia UX 66 curta e testável (`test_ux_aviso_live`) sem reabrir o kernel.
- Evidence-gate collect/check da 66 coube no ship sem atrito.
- Sync-context mecânico + ajuste semântico (tasks por slug + aviso UX) alinhou CLAUDE/AGENTS/CONTEXT.

## O que melhorar

- Chore “layout” sem issue NN própria no `entregas.jsonl` — scorecard só vê a 66; documentar chores de higiene com linha ou ADR leve quando quiser rastreio.
- STATUS da visão gráfica ficou desatualizado até este ship citar a 66 — pós-ship fatias na mesma área pedem nota no STATUS antigo no mesmo commit.

## Armadilhas

- `git fetch` 403 via proxy: GIT_PREFLIGHT soft — não tratar working tree como sync com remoto.
- Emit `flujo-events` no enter do ship criou pasta `chore-tasks-por-slug/fluxo/` antes dos artefatos 00/STATUS/retro — ok fail-soft, mas o slug “aparece” cedo.

## ADRs

- Nenhum ADR novo nesta chore (sem decisão contestável além do já registrado em ADR-0005 para o kernel).

## Harness — o que aprendemos

- Capturou certo: dual-tree agents/commands; `/fluxo-live`; evidence-gate ortogonal.
- Faltou: invariante explícito “tasks por slug” no CLAUDE antes do layout — agora documentado.
- Drift sync: detector automático “em sync” não captura semântica (layout/aviso UX); ship precisa checar prosa além do script.
