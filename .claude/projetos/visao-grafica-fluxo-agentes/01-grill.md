# Visão Gráfica do Fluxo de Agentes — Grill & Requisitos

Slug: `visao-grafica-fluxo-agentes`  
Branch: `feat/visao-grafica-fluxo-agentes`  
Grill fechado em: 2026-08-13  
Define enriquecido em: 2026-08-13  
Fontes: `00-ideia.md`, `00b-codebase.md`, mockup aprovado, decisões do `/grill-me`, `harness-define`

## Checklist de completude (qualquer tipo)

| Dimensão | Status |
|---|---|
| Problema real (não sintoma) | ✅ sem telemetria de agent ativo; visuals só estáticos |
| Usuários / personas | ✅ maintainer SDD, agente canônico/filho, projeto-filho |
| Critérios de sucesso mensuráveis | ✅ (seção abaixo) |
| Out of scope | ✅ SSE/Canvas MUST, Dev Loop MVP, PII, misturar evidence-gate |
| Restrições técnicas | ✅ tipo e, SI a, fail soft, dual-tree, soft-block fetch |
| SLA / performance | ✅ G1-c — best effort, sem alvo numérico no MVP |

## Contexto (da sessão /grill-me)

### Problema

O SDD canônico (fases 0–4) existe só como prosa (`STATUS.md`, agents) e visuals
estáticos (HTML/Excalidraw). Não há painel live que mostre **todos** os agents por
fase e, em tempo quase real, **qual subagente está ativo** (ex.: Build →
`harness-build` / `revisor-codigo`). Sem event log de lifecycle de agent, a UI
não tem o que observar.

### Usuários

| Persona | Pain |
|---|---|
| Maintainer / humano no SDD | Quer ver o fluxo e o agent ativo sem ler só o chat |
| Agente no canônico/filho | Precisa emitir eventos de forma padronizada e fail-soft |
| Projeto-filho pós-install | Mesmo painel ao rodar `/novo-projeto` |

### Objetivos (MoSCoW)

**MUST:**
- Mapa estrutural SDD 0–4 com **todos** os agents/skills por fase (diagrama do usuário)
- Event log JSONL por projeto + CLI `emit` / `render` (módulo canônico)
- HTML `live.html` regenerado a cada emit; poll opcional via `http.server` no dir `fluxo/`
- Live em **todas** as fases 0–4 (não só Build)
- Artefatos em `.claude/projetos/{slug}/fluxo/` (+ espelho `.cursor/`)
- Wiring nos agents/skills SDD para chamar emit no enter/exit (fail soft)
- Install foundation always-on (CLI + template fluxo + wiring)
- Eventos = só metadados (agent, phase, task id, timestamps) — sem prompts/PII/secrets
- Testes do kernel + fixture de render
- Espelho `.claude` ↔ `.cursor`
- Cap do log **2 MiB** com rotate (manter tail) + warning soft (**G3-a**)
- Append best-effort sem lock (**G2-a**)
- No ship: truncar `events.jsonl` para últimos **N** eventos (**G4-b**; default N=100 no PRD)

**SHOULD:**
- Cheatsheet 1 página + ADR
- Comando `/fluxo-live` (atalho docs → abrir/render)
- Schema tipado `fluxo-events.yaml`

**COULD:**
- Cursor Canvas (quase-live) como superfície extra
- Mini-app SSE
- Dev Loop no mesmo mapa
- Hooks Session/Task nativos do IDE

### Out of Scope

- Mini-app SSE / WebSocket no MVP
- Canvas Cursor como MUST
- Dev Loop no mapa MVP (Fase 2)
- Prompts, diffs ou PII/secrets no event log
- Unificar com evidence-gate (aceite ≠ telemetria)
- Substituir STATUS.md / scorecard
- Key vault (SI a — N/A)
- Alvo de latência numérico no MVP (G1-c)

### Restrições

- Evolução de **framework** (tipo e); SI **a**
- Fail soft: emit/render **nunca** bloqueia o fluxo SDD
- Dual Claude↔Cursor via artefatos em disco (não depender de API de um IDE)
- Branch: `feat/visao-grafica-fluxo-agentes`
- Fetch Azure pode falhar 403 — soft-block didático
- Sem commit/push neste passo define

### Mockup aprovado

`assets/mockup-visao-grafica-fluxo-live.png` (+ diagrama SDD 0–4 do usuário)

### Mapa SDD obrigatório

```
Fase 0 IDEIA:        harness-brainstorm
Fase 1 REQUISITOS:   grill-me, harness-define
Fase 2 PRD+HARNESS:  harness-design, to-prd, harness-architect
Fase 3 IMPLEMENTAR:  to-tasks, harness-build, revisor-codigo
Fase 4 ENCERRAR:     harness-ship, /scorecard
```

## Decisões numeradas (grill — fechadas)

1. UI: **HTML local + event log em disco** (**a**); Canvas = COULD
2. Fonte: **novo event log** JSONL (**a**) — não só STATUS/entregas
3. Live em **todas as fases SDD 0–4** (**b**)
4. Emissão via **CLI/módulo canônico** (`emit`/`render`) (**b**)
5. Paths: `.claude/projetos/{slug}/fluxo/` (+ espelho) (**a**)
6. Live sem SSE: **híbrido** emit→render HTML + poll opcional http.server (**a**)
7. Fluxos: **SDD no MVP**; Dev Loop Fase 2 (**c**)
8. Falha emit/render: **fail soft** (**a**)
9. Install: **foundation always-on** (**a**)
10. Fora: sem SSE MUST, sem Canvas MUST, sem Dev Loop MVP, sem PII no log, ortogonal a evidence-gate (**a**)
11. SLA: **best effort** — sem alvo numérico no MVP (**G1-c**)
12. Concorrência: **append best-effort** sem lock (**G2-a**)
13. Cap do log: **2 MiB** — rotate (manter tail) + warning soft (**G3-a**)
14. Retenção: no ship, **truncar para últimos N eventos** (**G4-b**; default N=100 a cravar no PRD)
15. Adversarial judge (define): **(b)** pulado

### Inferidos (confirmados — não reabrir)

| # | Inferência | Status |
|---|---|---|
| I1 | Canvas Cursor não faz fetch/stream — quase-live só por rewrite do `.canvas.tsx` | Confirmado (skill canvas) |
| I2 | Mapa estrutural mostra TODOS os agents; live destaca o ativo | Confirmado (ideia + usuário) |
| I3 | Pacote: `config/fluxo_events/` + contrato `fluxo-events.yaml` na raiz | Confirmado no define |
| I4 | N=100 no truncate do ship até o PRD especificar outro | Proposto (G4-b) |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- N/A: SI **a** — só metadados de processo; sem secrets no fluxo

## Especificações implícitas detectadas

| Lente | Decisão |
|---|---|
| 1. Falha de dependência | Fail soft — emit/render falha → stderr/warning; SDD segue (decisão 8) |
| 2. Concorrência | Append best-effort sem lock (G2-a); corrida rara entre agents |
| 3. Idempotência | Re-emit do mesmo enter/exit = nova linha JSONL (timeline honesta); render LWW no HTML |
| 4. Auth / multi-tenant | N/A — disco local do workspace; single operator |
| 5. Dados sensíveis | Só metadados; SI a; nunca prompt/PII/secret no log |
| 6. Abuso / limites | Cap 2 MiB + rotate tail (G3-a); sem rate limit de emit |
| 7. Auditoria | `events.jsonl` = trilha de lifecycle; ortogonal a `evidencias/audit.jsonl` |
| 8. Erro visível | Warning soft no CLI/stderr; HTML pode mostrar “último render ok” se houver metadado |
| 9. Ciclo de vida | Truncate no ship para últimos N (G4-b); sem purge LGPD (sem PII) |
| 10. Contrato externo | N/A — sem API externa; HTML local + http.server opcional |

## Amarras a artefatos (previsto)

| Artefato | Onde | Nota |
|---|---|---|
| Contrato | `fluxo-events.yaml` | Schema de eventos + cap/rotate |
| Engine/CLI | `config/fluxo_events/` | emit, render (+ truncate no ship) |
| Por projeto | `projetos/{slug}/fluxo/events.jsonl` + `live.html` | Dual-tree |
| Wiring | agents workflow + skills SDD | enter/exit emit |
| Install | foundation stack_map | Always-on |
| Testes | `tests/fluxo_events/` | Kernel |
| Docs | cheatsheet + ADR | SHOULD |
| Comando | `/fluxo-live` | SHOULD |

## Critérios de sucesso mensuráveis

- `emit` appenda JSONL; `render` gera HTML com fases 0–4 e agents listados
- HTML destaca agent/fase ativos a partir do último evento
- Falha de emit não impede harness-build (teste fail-soft)
- Cap 2 MiB: rotate mantém tail; warning soft (teste)
- Ship: truncate deixa ≤ N linhas (default 100) e re-render
- Install fixture: CLI + template `fluxo/` no filho
- Zero prompt/PII em fixtures de eventos
- Espelho `.claude`↔`.cursor` dos artefatos de wiring

## Soft-blocks registrados

- `git fetch` Azure 403 — branch local `feat/visao-grafica-fluxo-agentes` (não sync remoto)
- Mockup aprovado antes do fechamento da fase 0
- Adversarial judge pulado (b)

## Próximo passo

Rode **`harness-design`** para gerar o PRD e montar o harness.
