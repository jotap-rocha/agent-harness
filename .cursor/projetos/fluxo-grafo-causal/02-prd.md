# PRD — Fluxo-events: grafo causal real

Slug: `fluxo-grafo-causal`  
Repo: Agent Harness Canônico (framework — **não** produto)  
Branch: `feat/fluxo-grafo-causal`  
Data: 2026-08-18  
Tipo: **e** — evolução do harness canônico  
SI: **a** (só metadados de processo — sem PII)  
Fontes: `00-ideia.md`, `01-grill.md` (decisões 1–11 + MoSCoW + lentes I1–I10)  
Kernel base: `fluxo-events.yaml` + `config/fluxo_events/` + ADR-005  
Prior art visual: ship `fluxo-grafo-visual-agentes` (`build_flow_svg` canônico)

> Decisões do grill/define estão **fechadas** — este PRD as materializa; não reabre a matriz.
> Orthografia PT-BR obrigatória: **fluxo** (com **x**). Nunca **flujo** (com **j**) em
> artefatos do pacote.
> **Adversarial judge (PRD):** pulado **(b)** — sem `02b-judge.md`.
> **Judge define:** pulado **(b)** — sem `01b-judge.md`.
> Plano de extensão: `03-harness.md` (tipo e — canônico).

---

## Problem Statement

O painel `live.html` do kernel `fluxo-events` já mostra um fluxograma SVG do mapa
**canônico previsto** (fases/agentes do contrato SDD ou Dev Loop). Esse grafo responde
“qual o fluxo esperado?”, não “quem chamou quem nesta execução”.

Sem identidade de evento (`event_id`), correlação de sessão (`run_id`) e aresta causal
(`parent_event_id`), o render não consegue desenhar a árvore real de
`agent_enter` / `task_enter` (com `phase_enter` como raiz). O sintoma é “painel bonito
mas cego à execução”. O problema real é a ausência de schema aditivo + stack fail-soft
+ segundo SVG causal — sem fork do kernel, sem SSE/Canvas, sem unificar com
evidence-gate / agent-policies.

§1.3 permanece: telemetria local best-effort; omissão/falha de emit/stack não bloqueia
SDD nem `/dev`.

---

## Solution

Estender o kernel `fluxo-events` existente (não fork) para gravar identidade causal e
renderizar dois SVGs no mesmo `live.html`:

1. **Schema aditivo** (`version: 1` mantida): campos opcionais no load de eventos antigos;
   emits novos geram UUID v4:
   - `event_id` — identidade do evento (gerado se omitido)
   - `run_id` — sessão/slug (UUID auto se omitido; override explícito ok)
   - `parent_event_id` — UUID do pai ou `null`/omitido (órfão)
2. **Parent**: valor **explícito** = fonte de verdade; senão topo da **stack fail-soft**
   em `projetos/{slug}/fluxo/stack.json` (não versionada / gitignore). FS falha → warning
   stderr; nunca bloqueia.
3. **Dois SVGs** no `live.html` (offline, sem JS obrigatório):
   - canônico: `build_flow_svg` (inalterado em semântica)
   - causal: `build_causal_svg` — nós = `agent_enter` (+ `task_enter`) + `phase_enter`
     como raiz; `*_exit` / `ship_truncate` só na timeline
4. **Wiring** SDD + Dev Loop (+ espelho `.cursor/`): agents/commands documentam
   `--run-id` / `--parent-event-id` (ou equivalente no emit) e stack.
5. **CLI**: flags `--run-id` / `--parent-event-id`; emit gera `event_id` UUID.
6. **Docs SHOULD**: cheatsheet + **addendum ADR-005** (campos + stack + dois SVGs).
7. **Fail-soft** idêntico; dual-map SDD/Dev intacto; cap 2 MiB / truncate N=100;
   sem mutex; sem backfill de IDs históricos (órfãos ok).

### Esboço de contrato (aditivo — decisão-rich)

```text
ALLOWED_KEYS (acrescentar):
  event_id: UUID v4          # emit gera se omitido (emits novos)
  run_id: UUID v4            # sessão/slug; auto se omitido; override ok
  parent_event_id: UUID|null # explícito > topo stack; omitido = órfão

Stack (local, não versionada):
  projetos/{slug}/fluxo/stack.json   # gitignore; fail-soft se FS falhar

Render HTML:
  [SVG canônico build_flow_svg] + [SVG causal build_causal_svg]
  Nós causal: phase_enter (raiz) · agent_enter · task_enter
  Fora do grafo causal: *_exit · ship_truncate (só timeline)
```

`ALLOWED_KEYS` atual (baseline a estender):
`event_type`, `ts`, `phase`, `agent`, `task_id`, `slug`, `source`.

---

## Goals (MoSCoW)

### MUST

- Schema aditivo: `event_id` + `run_id` + `parent_event_id` (UUID v4; opcionais no load
  de eventos antigos)
- `run_id` por sessão/slug; UUID auto se omitido; override explícito ok
- Parent: explícito = fonte de verdade + stack fail-soft (`stack.json` local)
- Dois SVGs no `live.html`: canônico + causal (offline; sem JS obrigatório)
- Nós do SVG causal: `agent_enter` (+ `task_enter`) + `phase_enter` como raiz;
  exits/truncate só timeline
- Wiring: kernel + agents/commands SDD + Dev Loop (+ espelho `.cursor/`)
- `version: 1` aditivo + ADR-005 addendum
- Fail-soft; metadados only; dual-map intacto; cap 2 MiB / truncate N=100
- Emit gera UUID; CLI `--run-id` / `--parent-event-id`
- Sem agent “fluxo officer”; extensão do kernel — **não** fork

### SHOULD

- Truncar IDs visualmente no SVG (legibilidade)
- Docs/cheatsheet atualizados com campos novos e o stack

### COULD

- Toggle JS canônico↔causal (explícito **WON'T** neste ship; futuro)

### WON'T (neste ship)

- SSE / WebSocket / Canvas MUST
- Toggle JS canônico↔causal
- Mutex/lock no append ou na stack
- Backfill/migrar IDs em `events.jsonl` históricos (órfãos ok)
- Unificar com evidence-gate
- Persistência cross-machine da stack
- Key vault (SI a — N/A)
- Alvo de latência numérico; fork do kernel
- Agent “fluxo officer” / skill MUST nova de telemetria

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want `event_id`/`run_id`/`parent_event_id` in the
   event schema as additive optional fields, so that old JSONL lines still load.
2. As a mantenedor do canônico, I want new emits to always get a UUID v4 `event_id`, so
   that causal edges have stable endpoints.
3. As a mantenedor do canônico, I want `run_id` scoped to sessão/slug with auto-UUID and
   explicit override, so that one live panel run is correlatable end-to-end.
4. As a mantenedor do canônico, I want `ALLOWED_KEYS` extended without breaking forbidden
   key patterns, so that SI metadados-only stays enforced.
5. As a mantenedor do canônico, I want `version: 1` kept additive, so that install/seed
   KEEP does not require a breaking bump.
6. As a mantenedor do canônico, I want an ADR-005 addendum documenting causal fields +
   stack + dual SVG, so that future ships do not invent a fork.
7. As CI do canônico, I want `/validar` green including extended `tests/fluxo_events/`,
   so that this ship does not weaken gates.
8. As a mantenedor do canônico, I want dual-tree mirror (`.claude`↔`.cursor`) of wiring
   docs, so that Claude and Cursor stay in sync.
9. As a mantenedor do canônico, I want orthography **fluxo** (x) preserved and `flujo`
   (j) rejected by existing naming guard, so that package naming does not regress.
10. As a mantenedor do canônico, I want orthogonality to evidence-gate and agent-policies
    preserved, so that telemetria ≠ aceite ≠ Bash deny.

### Engine / emit / stack

11. As the emit engine, I want explicit `parent_event_id` to win over stack top, so that
    callers remain the source of truth.
12. As the emit engine, I want a local `stack.json` push/pop (fail-soft) when parent is
    omitted, so that nested agent_enter can inherit parent without mutex.
13. As the emit engine, I want FS failures on stack/events to warn on stderr and continue,
    so that SDD/`/dev` never stall.
14. As the CLI, I want `--run-id` and `--parent-event-id`, so that scripts/agents can
    wire causality without editing code.
15. As a reader of old logs, I want load to accept events missing the new keys, so that
    historical JSONL remains renderable (órfãos ok).

### Render / humano no painel

16. As a humano no painel, I want two SVGs in `live.html` (canônico + causal), so that I
    can compare predicted map vs real execution offline.
17. As a humano no painel, I want causal nodes limited to `phase_enter` (root) +
    `agent_enter`/`task_enter`, so that exits/truncate do not clutter the graph.
18. As a humano no painel, I want truncated UUID labels on the causal SVG (SHOULD), so
    that the diagram stays readable.
19. As a leitor de timeline, I want exits and `ship_truncate` still listed chronologically,
    so that the causal graph does not replace the event log view.
20. As a operador, I want dual-map SDD/Dev Loop semantics unchanged, so that
    `dev-loop-*` slugs still pick `dev_loop_map`.

### Agents / wiring

21. As an agente SDD, I want documented fail-soft emit with run/parent, so that brainstorm
    → ship can populate the causal graph.
22. As an agente Dev Loop, I want the same wiring (and dry-run still silent), so that
    LOAD→SYNC can show real parent edges when emitted.
23. As an agente, I want events limited to metadata keys, so that I never log prompts,
    secrets, or PII.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `ALLOWED_KEYS` inclui `event_id`, `run_id`, `parent_event_id` | pytest contrato / emit |
| AC2 | Novo emit gera `event_id` UUID v4 se omitido | pytest emit |
| AC3 | `run_id` auto UUID se omitido; override CLI/payload respeitado | pytest emit + CLI |
| AC4 | `parent_event_id` explícito prevalece sobre stack | pytest stack |
| AC5 | Sem parent explícito → usa topo de `stack.json` (fail-soft) | pytest stack |
| AC6 | Load aceita eventos antigos sem os três campos | pytest load / render |
| AC7 | `live.html` contém **dois** SVGs (canônico + causal) | pytest render HTML |
| AC8 | Nós causal ⊆ `{phase_enter, agent_enter, task_enter}`; sem exits/truncate no SVG causal | pytest `build_causal_svg` |
| AC9 | `phase_enter` atua como raiz do grafo causal quando presente | pytest causal layout |
| AC10 | IDs truncados visualmente no SVG causal (SHOULD) | pytest substring/label |
| AC11 | CLI expõe `--run-id` e `--parent-event-id` | pytest CLI / help + emit |
| AC12 | `stack.json` sob `projetos/{slug}/fluxo/` e gitignored | pytest path + gitignore assert |
| AC13 | Fail-soft: FS error em stack/emit/render → warning; não bloqueia | pytest fail-soft |
| AC14 | Dual-map SDD/Dev inalterado (prefixo `dev-loop-`) | pytest render dual-map existentes verdes |
| AC15 | Cap 2 MiB / truncate N=100 / sem mutex preservados | contrato + testes existentes |
| AC16 | Wiring SDD + Dev Loop documentado (+ espelho `.cursor/`) | testes de presença + review |
| AC17 | ADR-005 addendum + cheatsheet (SHOULD) mencionam campos + stack + dois SVGs | review docs |
| AC18 | Zero prompt/PII/secret em fixtures de eventos | grep + review SI |
| AC19 | Sem agent “fluxo officer”; orthografia **fluxo** (x) | review + naming guard |
| AC20 | `/validar` verde com suite `tests/fluxo_events/` estendida | ruff + mypy + pytest |

---

## Functional Requirements

### FR1 — Schema aditivo

- Estender `ALLOWED_KEYS` / contrato tipado com `event_id`, `run_id`, `parent_event_id`.
- `version: 1` mantida (aditivo); load tolera ausência dos campos.
- Emits novos: gerar `event_id` (e `run_id` se omitido) como UUID v4.
- Preservar `event_types`, `sdd_map`, `dev_loop_map`, `limits` (2 MiB, N=100).

### FR2 — Stack fail-soft

- Path: `projetos/{slug}/fluxo/stack.json` (espelho de layout `.claude`/`.cursor` de projetos).
- Não versionar (gitignore); sem mutex (WON'T).
- Parent explícito > topo da stack; falha FS → warning stderr, emit segue (órfão ok).
- Semântica de push/pop alinhada a enter/exit de agent/task (detalhe no build; teste
  via comportamento externo).

### FR3 — Render dual SVG

- Manter `build_flow_svg` (mapa canônico previsto).
- Adicionar `build_causal_svg(events) -> str` (puro, testável).
- `build_html` inclui **dois** blocos SVG; timeline/painel de fases preservados.
- Offline; sem JS obrigatório; sem CDN.

### FR4 — CLI / API emit

- Flags `--run-id` / `--parent-event-id` (e geração interna de `event_id`).
- Superfície CLI permanece `python -m config.fluxo_events emit|render|truncate`.

### FR5 — Wiring SDD + Dev Loop

- Documentar/one-liners em agents/commands SDD e Dev Loop (+ espelho `.cursor/`).
- Dry-run Dev continua **sem** emit.
- Sem agent “fluxo officer”.

### FR6 — Documentação (SHOULD)

- Cheatsheet: campos novos, stack, dois SVGs, §1.3.
- Addendum ADR-005: grafo causal real (fecha o “fora deste ship” do addendum visual).

### FR7 — Ortogonalidade

- Não misturar com evidence-gate nem agent-policies.
- Não substituir STATUS/scorecard/evidence-gate.
- Cross-link em cheatsheet/ADR.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | SI **a**: só metadados; sem PII/prompts/secrets no log |
| NFR-SI2 | Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault neste ship |
| NFR-SI3 | UUID de evento **não** é PII; fixtures auditáveis por grep |
| NFR-SI4 | Honesty §1.3: telemetria local/forjável; stack omitível; painel pode ficar stale |
| NFR-Q1 | Fail soft: emit/render/stack nunca bloqueia SDD/`/dev` |
| NFR-Q2 | SLA best effort — sem alvo numérico |
| NFR-Q3 | Append e stack **sem** mutex (corrida aceita) |
| NFR-Q4 | Cap 2 MiB rotate keep-tail (herdado) |
| NFR-Q5 | Truncate N=100 no ship / `EXIT_COMPLETE` (herdado) |
| NFR-Q6 | Espelho `.claude`↔`.cursor` na mesma sessão |
| NFR-Q7 | Soft-block git: fetch Azure 403 → não fingir sync; sem commit/push sem acordo |
| NFR-Q8 | Orthografia PT-BR **fluxo** (x) nos artefatos do pacote |
| NFR-Q9 | Sem backfill de IDs históricos; órfãos ok |

---

## Architecture — artefatos canônicos

```text
┌─ fluxo-events.yaml ──► version 1 aditivo (schema/docs dos campos novos)
│
├─ config/fluxo_events/
│     emit (ALLOWED_KEYS + UUID + stack) · CLI flags
│     stack.py (stack.json fail-soft)
│     render: build_flow_svg + build_causal_svg → live.html
│
├─ projetos/{slug}/fluxo/
│     events.jsonl · live.html · stack.json (gitignore)
│
├─ wiring: agents/commands SDD + Dev Loop (+ espelho .cursor/)
├─ tests/fluxo_events/ ──► emit IDs · stack · causal SVG · load legado · CLI
├─ docs: cheatsheet · ADR-005 addendum (SHOULD)
└─ ortogonal: evidence-gate · agent-policies · STATUS/scorecard
```

### Amarras a módulos lógicos

| Artefato | Módulo / superfície |
|---|---|
| Contrato | `fluxo-events.yaml` (`version: 1` aditivo) |
| Emit / ALLOWED_KEYS | `config/fluxo_events/emit.py` |
| Stack | `config/fluxo_events/stack.py` (novo) + `stack.json` |
| Render canônico | `build_flow_svg` (existente) |
| Render causal | `build_causal_svg` (novo) |
| HTML | `build_html` / `render_live` — dois blocos SVG |
| CLI | `python -m config.fluxo_events` (`--run-id`, `--parent-event-id`) |
| Wiring | agents/commands SDD + Dev (+ espelho) |
| Docs | cheatsheet + ADR-005 addendum |
| Testes | `tests/fluxo_events/` |
| Projeto SDD deste ship | `.claude/projetos/fluxo-grafo-causal/` (+ espelho) |
| Ortogonal | evidence-gate, agent-policies, STATUS, scorecard |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | `event_id` + `run_id` + `parent_event_id` | FR1 / AC1–AC3 |
| 2 | `run_id` sessão/slug + auto UUID + override | FR1 / AC3 |
| 3 | Parent explícito + stack fail-soft | FR2 / AC4–AC5 |
| 4 | Dois SVGs canônico + causal | FR3 / AC7 |
| 5 | UUID v4 (+ truncar visual SHOULD) | FR1 / AC2 / AC10 |
| 6 | Wiring kernel + SDD + Dev Loop | FR5 / AC16 |
| 7 | `stack.json` local não versionado | FR2 / AC12 |
| 8 | WON'T (SSE, toggle JS, mutex, backfill, …) | Out of Scope |
| 9 | Nós causal: enters + `phase_enter` raiz | FR3 / AC8–AC9 |
| 10 | `version: 1` aditivo + ADR addendum | FR1 / FR6 / AC17 |
| 11 | Fechar grill → design | este PRD |
| I1 | Fail-soft FS | AC13 / NFR-Q1 |
| I2 | Sem mutex | NFR-Q3 / WON'T |
| I3 | Novo `event_id` por emit; sem dedup | FR1 |
| I4–I5 | Auth N/A; SI a | NFR-SI* |
| I6 | Cap 2 MiB herdado | AC15 |
| I7 | Trilha = `events.jsonl` | Architecture |
| I8 | Warning stderr; painel stale ok | NFR-SI4 |
| I9 | Truncate N=100; órfãos ok | AC15 / NFR-Q9 |
| I10 | Sem terceiros | N/A |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (keys no emit, UUID gerado, parent
explícito vs stack, load legado, presença de dois SVGs, conjunto de nós do causal,
CLI flags, gitignore de `stack.json`, fail-soft), não geometria privada salvo asserts
estáveis de `data-testid` / classes.

Prior art: `tests/fluxo_events/` (emit/render/rotate/truncate/dual-map/naming/wiring),
`tests/fluxo_events/test_render_graph.py` (`build_flow_svg`).

| Área | O que testar | Prior art |
|---|---|---|
| ALLOWED_KEYS / UUID | emit gera `event_id`/`run_id`; override | emit tmpdir |
| Parent | explícito > stack; órfão se ambos ausentes | novo stack tests |
| Load legado | JSONL sem campos novos renderiza | render fixtures |
| Causal SVG | nós ⊆ enters; sem exit/truncate; raiz phase | `test_render_graph` pattern |
| Dois SVGs no HTML | `data-testid` canônico + causal | render HTML |
| Truncate label | IDs curtos no SVG (SHOULD) | assert substring |
| CLI | `--run-id` / `--parent-event-id` | CLI emit tests |
| Fail-soft stack | FS error → warning, exit 0 path | matrix fail-soft |
| Dual-map | regressão SDD/Dev | testes existentes |
| Wiring presença | docs agents/commands | wiring SDD/Dev |
| Naming PT-BR | sem `flujo` (j) | `test_naming_ptbr.py` |
| `/validar` | suite canônica verde | gate existente |

### Plano de validação (DoD gate)

```bash
uv run ruff check --fix . && uv run mypy . && uv run pytest -q
uv run pytest -q tests/fluxo_events/
```

Critério: gate **verde**; AC1–AC20 com evidência; sem E2E IDE obrigatório; kernels
ortogonais sem regressão.

---

## Out of Scope

Materializa WON'T do grill (decisão 8 + out-of-scope):

- SSE / WebSocket / Canvas MUST
- Toggle JS canônico↔causal neste ship
- Mutex/lock no append ou na stack
- Backfill/migrar IDs em `events.jsonl` históricos
- Unificar com evidence-gate ou agent-policies
- Persistência cross-machine da stack
- Key vault / pacote E
- Alvo de latência numérico
- Fork do kernel ou mini-app separado
- Agent “fluxo officer” / skill MUST nova de telemetria
- Tag `prod-*` / Fase 2 git hygiene
- Mudança semântica do dual-map SDD/Dev Loop
- Harness de produto-filho (tipo **e** — só evolução do canônico)

---

## SI Considerations

| Tema | Decisão |
|---|---|
| Nível | **a** — metadados de processo / IDs sintéticos |
| Event log | só keys permitidas; forbidden patterns existentes |
| PII | UUID ≠ PII; sem prompts/secrets |
| LGPD | sem `[AVISO_LGPD]` / `rules/pii.md` neste escopo |
| Vault | N/A |
| Stack | local; pode conter só UUIDs/metadados de processo |
| Honesty | §1.3 — forjável/omitível; não é aceite |

---

## Orthografia

Sempre **fluxo** (x) em paths, seeds, docs e código do pacote. Nunca **flujo** (j).
Guardrail existente: `tests/fluxo_events/test_naming_ptbr.py`.

---

## Further Notes

- **Tipo e:** este PRD **não** pede geração de agents/rules/KBs de produto-filho. O
  passo harness-architect deve produzir `03-harness.md` como **plano de extensão do
  canônico** (o que o build vai tocar), não um `.claude/` de app.
- **Judge PRD:** pulado **(b)** — sem `02b-judge.md` (2026-08-18).
- **Judge define:** pulado **(b)** — sem `01b-judge.md`.
- Soft-block: fetch Azure **403** neste ambiente — branch local `feat/fluxo-grafo-causal`;
  sem commit/push sem acordo explícito.
- Referência de formato: `.claude/projetos/fluxo-events-dev-loop-live/02-prd.md`.
- ADR visual já antecipou este ship como “fora de escopo” do grafo canônico — este PRD
  fecha essa lacuna via addendum.

## Próximo passo

1. Plano de extensão em `03-harness.md` (harness-design fechado).
2. Rode `/to-tasks` → depois `harness-build`.
