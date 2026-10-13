# 00b — Codebase map (pré-brainstorm)

Slug: `visao-grafica-fluxo-agentes`  
Workspace: `<raiz-do-clone>`  
Gerado por: codebase-explorer (2026-08-13)  
Foco: agents workflow, STATUS, visual-explainer, excalidraw, hooks, telemetria

## Executive Summary

- Framework canônico (não produto): agents/skills/rules/kernels; dual-tree `.claude/` ↔ `.cursor/`; sem app web/SSE.
- Progresso SDD = Markdown (`STATUS.md`) atualizado em fronteiras de fase + métricas/evidências **pós-fato**.
- Visuals existentes = **estáticos** (`visual-explainer` → HTML; Excalidraw → `.excalidraw`+PNG; `docs/guia/*.html`).
- Hooks = só freio de shell (PreToolUse / `beforeShellExecution`) — **sem** telemetria de agent/Task/subagent.
- **Gap principal para dashboard live:** event log de “qual agent está rodando agora”, stream/UI, hooks Session/Task/Subagent.

## Deep Dive

### Entry points / fluxos SDD

| Fase (checklist STATUS) | Agent / comando | Artefato típico |
|---|---|---|
| 0 Ideia | `/novo-projeto` → `harness-brainstorm` | `00-ideia.md` (+ `00b-codebase.md`) |
| 1 Grill | `/grill-me` → `harness-define` | `01-grill.md` |
| 2–3 PRD+Harness | `harness-design`, `/to-prd`, `/harness-architect` | `02-prd.md`, `03-harness.md` |
| 4 Tasks | `/to-tasks` | `04-tasks-index.md` + `tasks/` |
| 5 Build | `harness-build` (+ `revisor-codigo`) | tasks done + `entregas.jsonl` + evidencias |
| 6 Ship | `harness-ship` + `/scorecard` + `/sync-context` | `05-retro.md` |

Encadeamento humano (sem orquestrador runtime). Espelho: `.claude/agents/workflow/` ≡ `.cursor/agents/workflow/`. Match por `description:` no frontmatter — sem router central.

**Mapeamento à estrutura SDD 0–4 do usuário (ideia):**

```
Fase 0 IDEIA:        harness-brainstorm
Fase 1 REQUISITOS:   grill-me, harness-define
Fase 2 PRD+HARNESS:  harness-design, to-prd, harness-architect
Fase 3 IMPLEMENTAR:  to-tasks, harness-build, revisor-codigo
Fase 4 ENCERRAR:     harness-ship, /scorecard
```

### Artefatos de status

- **`STATUS.md`:** fase atual + checklist 0–6; **não live** (atualização manual pelo agent).
- **Evidence-gate:** `evidencias/audit.jsonl` = collects de critérios (não agent lifecycle).
- **`metrics/entregas.jsonl`:** 1 linha por task fechada; alimenta `/scorecard` (histórico).
- **Agent-policies:** deny/ask Bash; bypass → stderr; não é progresso SDD.
- **Dev Loop:** `PROGRESS.md` em `.claude/dev/progress/` — paralelo ao SDD, não unificado.

### Skills visuais

| Skill | Saída | Live? |
|---|---|---|
| `visual-explainer` | HTML em `~/.agent/diagrams/` | Não |
| `excalidraw-diagram` | `.excalidraw` + PNG | Não |
| Guias `docs/guia/` | HTML slides 01–16 | Não |

### Hooks e telemetria

- Claude: `.claude/hooks/agent_policies_pretooluse.sh`
- Cursor: `.cursor/hooks.json` → `beforeShellExecution`
- **Ausente:** SessionStart/Stop, SubagentStart/Stop, Task events, event bus, WebSocket/SSE, registry “current agent”.

### Convenções

- Dual-tree obrigatório; nenhum código de produto no canônico; DoD = gate + evidence-gate + revisor + entregas + sync-context no ship.
- Três níveis: vibe / Dev Loop (`/dev`) / harness completo (`/novo-projeto`).

## Gap analysis — visão gráfica live

| Já reusável | Falta |
|---|---|
| Grafo de fases SDD (docs + agents) como modelo de UI | Runtime emitindo `phase_enter` / `agent_start` / `agent_end` |
| `STATUS.md` como snapshot de fase | Watcher/API + push de updates |
| `entregas.jsonl` + scorecard (histórico) | Stream mid-task |
| `evidencias/audit.jsonl` (timeline de collects) | Eventos Task/subagent |
| Templates Mermaid/Excalidraw/HTML | UI live (SSE/WebSocket) + binding a eventos |
| Hooks shell (ponto de extensão) | Hooks além de Bash; telemetria de agent name/tools |
| `docs/guia/09-agentes-sdd.html` (mock visual) | Dados dinâmicos |

**Veredito:** canônico tem **estado de fase em Markdown** e **métricas/evidências pós-fato**. Não há telemetria de “qual agent está rodando agora”. Dashboard live exige camada nova (event log + transport + UI); reuso imediato = modelo de fases + STATUS/entregas/audit como fontes históricas.
