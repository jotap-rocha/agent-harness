# PRD — Visão Gráfica do Fluxo de Agentes (fluxo-events)

Slug: `visao-grafica-fluxo-agentes`  
Repo: Agent Harness Canônico (framework — **não** produto)  
Branch: `feat/visao-grafica-fluxo-agentes`  
Data: 2026-08-13  
Tipo: **e** — evolução do harness canônico  
SI: **a** (só metadados de processo — agent, phase, task id, timestamps; sem PII)  
Fontes: `00-ideia.md`, `00b-codebase.md`, `01-grill.md` (decisões 1–15 + G1–G4 fechadas)  
Mockup aprovado: `assets/mockup-visao-grafica-fluxo-live.png`  
  (path absoluto de sessão: `<cursor-projects>/<workspace-slug>/assets/mockup-visao-grafica-fluxo-live.png`)

> Decisões do grill/define estão **fechadas** — este PRD as materializa; não reabre a matriz.
> **Adversarial judge (PRD):** pendente confirmação humana (a/b) — **não** rodar
> `/harness-architect` até o parent obter resposta do usuário.

---

## Problem Statement

O SDD canônico (fases 0–4) existe como prosa (`STATUS.md`, agents workflow) e visuals
estáticos (HTML/Excalidraw/`docs/guia`). Hooks cobrem só freio de shell
(PreToolUse / `beforeShellExecution`). Não há event log de lifecycle de agent, nem painel
que mostre **todos** os papéis por fase e, em tempo quase real, **qual subagente está
ativo** (ex.: Build → `harness-build` / `revisor-codigo`).

O sintoma é “só dá pra acompanhar pelo chat”. O problema real é a ausência de um
**kernel de telemetria de fluxo** (contrato + engine `emit|render` + artefatos por projeto
+ wiring fail-soft nos agents SDD + install foundation) ortogonal a evidence-gate
(aceite) e agent-policies (Bash). Sem isso, mapa e live não têm o que observar.

§1.3 permanece: emit/render são best-effort locais; falha ou omissão de wiring não
impede o SDD — honesty explícita, sem prometer telemetria server-side.

---

## Solution

Evoluir o canônico com um **kernel fluxo-events**, paralelo a evidence-gate e
agent-policies (não unificado; concern distinto — telemetria de processo ≠ prova de
aceite ≠ freio Bash):

1. **Contrato** `fluxo-events.yaml` na raiz — schema de evento, cap do log **2 MiB**,
   política de rotate (manter tail) + warning soft, default de truncate no ship
   (**N=100**), mapa estrutural SDD 0–4.
2. **Engine** `config/fluxo_events/` — load tipado + CLI
   `python -m config.fluxo_events emit|render` (+ truncate no ship).
3. **`emit`** appenda uma linha JSONL (metadados only) em
   `.claude/projetos/{slug}/fluxo/events.jsonl` (+ espelho `.cursor/`); **fail soft**.
4. **`render`** regenera `live.html` a partir do JSONL + mapa estrutural (todas as
   fases/agents); destaca agent/fase ativos pelo último evento relevante; **fail soft**.
5. **Live sem SSE:** híbrido emit→render HTML; `python -m http.server` **opcional** no
   dir `fluxo/` para poll/refresh no browser.
6. **Live em TODAS as fases SDD 0–4** — não só Build.
7. **Mapa estrutural** mostra **todos** os agents; live destaca o **ativo**.
8. **Wiring** nos agents/skills SDD (enter/exit → emit) — nunca bloqueia o fluxo.
9. **Install foundation always-on** — CLI + template `fluxo/` + wiring nos filhos.
10. **G1–G4:** SLA best effort sem alvo numérico (G1-c); append best-effort sem lock
    (G2-a); cap **2 MiB** com rotate manter tail + warning soft (G3-a); no ship truncar
    para últimos **N=100** eventos e re-render (G4-b).
11. **Testes** em `tests/fluxo_events/` + fixture de render; E2E IDE fora do CI
    obrigatório.
12. **UI alvo:** alinhada ao mockup aprovado (fases, agent ativo, timeline).

### Mapa SDD obrigatório (estrutural)

```
Fase 0 IDEIA:        harness-brainstorm
Fase 1 REQUISITOS:   grill-me, harness-define
Fase 2 PRD+HARNESS:  harness-design, to-prd, harness-architect
Fase 3 IMPLEMENTAR:  to-tasks, harness-build, revisor-codigo
Fase 4 ENCERRAR:     harness-ship, /scorecard
```

---

## Goals (MoSCoW)

### MUST

- Contrato `fluxo-events.yaml` + engine `config/fluxo_events/` + CLI `emit|render`
  (+ truncate no ship)
- Paths: `.claude/projetos/{slug}/fluxo/events.jsonl` + `live.html` (+ espelho `.cursor/`)
- Mapa estrutural SDD 0–4 com **todos** os agents listados (diagrama acima)
- Live em **todas** as fases 0–4; destaque do agent/fase ativos
- Híbrido emit→render HTML; `http.server` opcional (sem SSE MUST)
- Fail soft: emit/render **nunca** bloqueia SDD
- Wiring enter/exit nos agents/skills SDD relevantes
- Install foundation always-on (CLI + template fluxo + wiring)
- Eventos = só metadados (agent, phase, task id, timestamps) — sem prompts/PII/secrets
- Cap **2 MiB** — rotate manter tail + warning soft (G3-a)
- Append best-effort sem lock (G2-a)
- Ship: truncar `events.jsonl` para últimos **N=100** e re-render (G4-b)
- SLA best effort — sem alvo numérico no MVP (G1-c)
- Testes do kernel + fixture de render (`tests/fluxo_events/`)
- Espelho `.claude` ↔ `.cursor`
- Ortogonal a evidence-gate e agent-policies (só cross-link em docs)

### SHOULD

- Cheatsheet 1 página (`docs/fluxo-events-cheatsheet.md` ou equivalente)
- ADR do kernel fluxo-events (`docs/adr/`)
- Comando `/fluxo-live` (atalho docs → abrir/render / http.server opcional)
- Schema tipado completo no yaml (campos obrigatórios/opcionais documentados)

### COULD

- Cursor Canvas (quase-live) como superfície extra
- Mini-app SSE / WebSocket
- Dev Loop no mesmo mapa (Fase 2)
- Hooks Session/Task nativos do IDE

### WON'T (neste ship)

- SSE / WebSocket como MUST
- Canvas Cursor como MUST
- Dev Loop no mapa MVP
- Prompts, diffs, PII ou secrets no event log
- Unificar / misturar com evidence-gate (aceite ≠ telemetria)
- Substituir `STATUS.md` / `/scorecard`
- Key vault (SI a — N/A)
- Alvo de latência numérico no MVP
- Mutex / lock de append no MVP

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want a versioned `fluxo-events.yaml` at the repo root, so that event schema, cap/rotate and SDD map are auditable like other kernels.
2. As a mantenedor do canônico, I want a typed loader under `config/fluxo_events/`, so that invalid contracts fail fast in CI.
3. As a mantenedor do canônico, I want `python -m config.fluxo_events emit` to append one JSONL line of process metadata, so that agents share one telemetry seam.
4. As a mantenedor do canônico, I want `python -m config.fluxo_events render` to regenerate `live.html` from events + structural map, so that the UI always reflects disk state without SSE.
5. As a mantenedor do canônico, I want the structural map to list **all** SDD 0–4 agents even with an empty log, so that the catalog is visible before any run.
6. As a mantenedor do canônico, I want live highlight of the active agent/phase from the latest relevant event, so that operators see “who is running now”.
7. As a mantenedor do canônico, I want live coverage for **all** phases 0–4, so that Build is not a special case.
8. As a mantenedor do canônico, I want emit/render to **fail soft** (stderr warning, exit non-blocking for callers), so that SDD never stalls on telemetry.
9. As a mantenedor do canônico, I want append best-effort without file locks, so that rare concurrent agents do not block each other (G2-a).
10. As a mantenedor do canônico, I want a 2 MiB cap with rotate-keeping-tail + soft warning, so that logs cannot grow unbound while still remaining usable (G3-a).
11. As a mantenedor do canônico, I want ship to truncate `events.jsonl` to the last **N=100** events and re-render, so that closed projects keep a bounded trail (G4-b).
12. As a mantenedor do canônico, I want install foundation always-on for fluxo-events, so that children inherit CLI + template + wiring without opt-in niche.
13. As a mantenedor do canônico, I want evidence-gate and agent-policies left as separate kernels, so that telemetry does not become acceptance proof or Bash deny.
14. As a mantenedor do canônico, I want pytest suite `tests/fluxo_events/` covering emit, render, cap/rotate, truncate, fail-soft, and install fixture, so that regressions fail CI without IDE E2E.
15. As CI do canônico, I want `/validar` green after this ship, so that the new kernel does not weaken existing gates.
16. As a mantenedor do canônico, I want docs to state §1.3 honesty (omitted emit / forged events possible), so that auditors are not promised perfect live fidelity.
17. As a mantenedor do canônico, I want the rendered HTML to follow the approved mockup intent (phases, active agent, timeline), so that visual acceptance is grounded.

### Agente / wiring SDD

18. As an agente SDD (brainstorm→ship), I want a one-liner emit on enter/exit, so that I can report lifecycle without inventing formats.
19. As an agente SDD, I want emit failure to never abort my phase work, so that telemetry outages are non-blocking.
20. As an agente em harness-ship, I want a documented truncate→render step, so that closing a flow bounds the event log.
21. As an agente, I want event fields limited to metadata (agent, phase, task_id, timestamps, event_type), so that I never log prompts/secrets/PII.
22. As harness-build / revisor-codigo, I want task_id optional on events when known, so that Build timeline can correlate with tasks without requiring it in early phases.

### Humano / operador

23. As a maintainer watching SDD, I want to open `fluxo/live.html` (file:// or optional http.server) and see the map + active agent + timeline, so that I need not read only the chat.
24. As a maintainer, I want optional `python -m http.server` in `fluxo/` for browser refresh, so that I get near-live without SSE.
25. As a maintainer, I want `/fluxo-live` (SHOULD) as a docs shortcut, so that agents discover emit/render without memorizing the module path.
26. As a leitor de STATUS/scorecard, I want those artifacts unchanged as sources of truth for checklist/metrics, so that live telemetria complements rather than replaces them.

### Projeto-filho / install

27. As an operador de `/install-harness`, I want foundation always-on for fluxo-events, so that every child gets the same live panel capability.
28. As an engenheiro no filho, I want the same `emit|render` UX and `projetos/{slug}/fluxo/` layout, so that dogfood and child behavior match.
29. As an engenheiro no filho, I want dual-tree mirror of `fluxo/` when both trees exist, so that Claude and Cursor stay in sync.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `fluxo-events.yaml` carrega no loader tipado; schema + cap + N=100 + mapa 0–4 presentes | pytest contrato / loader |
| AC2 | `emit` appenda 1 linha JSONL válida (metadados) sob `fluxo/events.jsonl` | pytest emit |
| AC3 | `render` gera `live.html` com fases 0–4 e **todos** os agents listados (mesmo com log vazio) | pytest render + fixture HTML |
| AC4 | HTML destaca agent/fase ativos a partir do último evento relevante | pytest render / assert conteúdo |
| AC5 | Falha de emit/render (FS error simulado) → warning soft; caller SDD não bloqueado | pytest fail-soft |
| AC6 | Cap 2 MiB: overflow → rotate mantém tail + warning soft (não fail hard) | pytest rotate |
| AC7 | Append sem lock: dois emits sequenciais/concorrentes best-effort não exigem mutex | pytest append / docs G2 |
| AC8 | Ship truncate: `events.jsonl` fica com ≤ **100** linhas; re-render ok | pytest truncate |
| AC9 | Install fixture: CLI + template `fluxo/` no filho (foundation) | pytest install |
| AC10 | Zero prompt/PII/secret em fixtures de eventos | grep + review SI |
| AC11 | Espelho `.claude`↔`.cursor` dos artefatos de wiring/projeto deste ship | checklist simétrica |
| AC12 | `/validar` verde no canônico com `tests/fluxo_events/` | ruff + mypy + pytest |
| AC13 | Ortogonalidade: docs não unificam com evidence-gate nem agent-policies | review + cheatsheet |
| AC14 | STATUS.md / scorecard **não** substituídos; live é complementar | review agents/docs |
| AC15 | SLA: sem alvo numérico no contrato (G1-c documentado) | assert contrato + docs |
| AC16 | Wiring documentado/instruído nos agents SDD 0–4 (enter/exit emit) | review agents + teste de contrato de instrução |
| AC17 | Mockup referenciado; HTML cobre fases + ativo + timeline (aceitação visual) | review + fixture |
| AC18 | Docs §1.3 honesty: telemetria local ≠ fidelidade perfeita / omitir emit possível | review cheatsheet/ADR |

---

## Functional Requirements

### FR1 — Contrato `fluxo-events.yaml`

- Fonte única de: schema de evento, cap **2 MiB**, rotate (manter tail) + warning soft,
  default truncate ship **N=100**, mapa estrutural SDD 0–4 (agents por fase), política
  fail-soft, ausência de SLA numérico (G1-c).
- Versionado na raiz do canônico (padrão `git-hygiene.yaml` / `agent-policies.yaml` /
  `evidence-gate.yaml`).
- Mudanças breaking → bump + suite `tests/fluxo_events/` verde.

### FR2 — Engine `config/fluxo_events/`

- Load tipado (padrão loaders existentes).
- CLI: `python -m config.fluxo_events emit|render` (+ truncate exposto à CLI ou helper
  usado pelo ship).
- `emit`: valida campos mínimos → append JSONL best-effort → opcionalmente dispara
  `render` (ou o wiring chama render em seguida); erros → stderr + exit não bloqueante
  para o fluxo SDD (contrato de fail-soft documentado).
- `render`: lê mapa estrutural + `events.jsonl` → escreve `live.html` (LWW no HTML).
- Truncate (ship): mantém últimas **N=100** linhas de `events.jsonl` → re-render.
- Sem rede obrigatória; operação local FS.

### FR3 — Schema de evento (sugerido)

Campos mínimos (metadados only) — naming exato pode fechar no architect desde que ACs
sejam preservados:

```yaml
# Exemplo de linha em events.jsonl (JSON, um objeto por linha)
event_type: phase_enter | phase_exit | agent_start | agent_end | task_start | task_end | info
ts: ISO-8601
phase: 0|1|2|3|4   # ou slug IDEIA|REQUISITOS|PRD_HARNESS|IMPLEMENTAR|ENCERRAR
agent: harness-build  # nome canônico do agent/skill/comando
task_id: optional     # quando conhecido (fase Implementar)
slug: projeto-slug
source: optional      # claude|cursor|cli
```

**Proibido no evento:** prompt, conteúdo de mensagem, diff, secret, PII, connection string.

### FR4 — Pasta por projeto

```text
.claude/projetos/{slug}/fluxo/
├── events.jsonl    # append-only operacional (rotate/truncate conforme G3/G4)
└── live.html       # regenerado por render (LWW)
```

Espelho idêntico sob `.cursor/projetos/{slug}/fluxo/` quando dual-tree.

### FR5 — Live sem SSE

- Path feliz: agent chama `emit` → `render` → humano abre `live.html`.
- Opcional: `python -m http.server` no dir `fluxo/` para refresh no browser.
- Sem WebSocket/SSE no MVP (WON'T).

### FR6 — Wiring SDD

- Agents/skills/commands do mapa 0–4 instruídos a emitir enter/exit (e task_* na fase
  Implementar quando houver task_id).
- Falha de emit **não** altera STATUS, DoD, evidence-gate ou build.
- harness-ship: passo truncate N=100 + render antes/ao fechar o fluxo (documentado).

### FR7 — Install foundation

- Foundation always-on: contrato/schema + engine CLI + template `fluxo/` + wiring de
  agents/commands relevantes nos filhos.
- Não acoplar a `pipeline_dados` nem a evidence-gate/agent-policies; concern próprio.
- Generate/portabilidade: sem paths de máquina obrigatórios nos templates.

### FR8 — Ortogonalidade

- **evidence-gate** = prova de aceite por task (hard) — não é telemetria mid-run.
- **agent-policies** = freio Bash destrutivo — não é progresso SDD.
- **STATUS.md** / **scorecard** / **entregas.jsonl** permanecem fontes de checklist e
  métricas pós-fato; live complementar.
- Cross-link em cheatsheet: “telemetria ≠ aceite ≠ Bash deny”.

### FR9 — Documentação (SHOULD)

- Cheatsheet 1 página; ADR do kernel; comando `/fluxo-live` como atalho.
- Honesty §1.3: emit omitível; HTML pode ficar stale; sem Edit policies.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | SI **a**: só metadados de processo; sem PII/prompts/secrets no log |
| NFR-SI2 | Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault neste ship |
| NFR-SI3 | Fixtures auditáveis por grep — zero secret/PII |
| NFR-SI4 | Honesty §1.3: não prometer fidelidade perfeita nem telemetria server-side |
| NFR-Q1 | Fail soft: emit/render nunca bloqueia SDD |
| NFR-Q2 | SLA best effort — **sem** alvo numérico no contrato (G1-c) |
| NFR-Q3 | Append best-effort sem lock (G2-a) |
| NFR-Q4 | Cap 2 MiB; rotate manter tail + warning soft (G3-a) — **não** fail hard no cap |
| NFR-Q5 | Ship truncate últimos **N=100** + re-render (G4-b) |
| NFR-Q6 | Espelho `.claude`↔`.cursor` na mesma sessão de promoção |
| NFR-Q7 | Soft-block git: fetch Azure 403 → trabalho na branch local; sem inventar sync |
| NFR-Q8 | UI alinhada ao mockup aprovado (fases, ativo, timeline) |

---

## Architecture — artefatos canônicos

```text
┌─ fluxo-events.yaml ──► schema evento · cap 2MiB rotate · N=100 · mapa SDD 0–4
│
├─ config/fluxo_events/ ──► load · emit · render · truncate · (CLI)
│
├─ .claude/projetos/{slug}/fluxo/ ──► events.jsonl · live.html
│         (+ espelho .cursor/projetos/.../fluxo/)
│
├─ wiring: agents/skills SDD 0–4 (enter/exit emit, fail soft)
├─ harness-ship ──► truncate N=100 + render
│
├─ install-harness foundation ──► CLI + template fluxo + wiring
├─ docs: cheatsheet · ADR · /fluxo-live (SHOULD)
└─ tests/fluxo_events/ ──► emit · render · rotate · truncate · fail-soft · install
```

### Amarras a módulos lógicos

| Artefato | Módulo / superfície |
|---|---|
| Contrato | `fluxo-events.yaml` (raiz) |
| Engine / CLI | `config/fluxo_events/` |
| Por projeto | `projetos/{slug}/fluxo/` (+ espelho) |
| Wiring | agents workflow + skills/commands do mapa SDD |
| Ship | `harness-ship` (truncate + render) |
| Install | foundation / `stack_map` (+ seed template se couber) |
| Testes | `tests/fluxo_events/` |
| Docs | cheatsheet + ADR (+ `/fluxo-live` SHOULD) |
| Mockup | `assets/mockup-visao-grafica-fluxo-live.png` |
| Projeto | `.claude/projetos/visao-grafica-fluxo-agentes/` (+ espelho `.cursor/`) |
| Ortogonal | evidence-gate, agent-policies, STATUS, scorecard — sem unificar |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | UI HTML local + event log em disco | FR4–FR5 / AC3–AC4 |
| 2 | Novo event log JSONL (não só STATUS) | FR2–FR3 / AC2 |
| 3 | Live em todas as fases 0–4 | FR6 / AC3 / AC16 |
| 4 | CLI/módulo canônico emit\|render | FR2 / AC2–AC3 |
| 5 | Paths `projetos/{slug}/fluxo/` + espelho | FR4 / AC11 |
| 6 | Híbrido emit→render; http.server opcional | FR5 |
| 7 | SDD no MVP; Dev Loop Fase 2 | Out of Scope |
| 8 | Fail soft | FR2 / AC5 / NFR-Q1 |
| 9 | Install foundation always-on | FR7 / AC9 |
| 10 | Fora: SSE/Canvas MUST, Dev Loop, PII, misturar evidence-gate | Out of Scope |
| 11 / G1-c | SLA best effort sem alvo numérico | NFR-Q2 / AC15 |
| 12 / G2-a | Append sem lock | NFR-Q3 / AC7 |
| 13 / G3-a | Cap 2 MiB rotate tail + warning soft | NFR-Q4 / AC6 |
| 14 / G4-b | Ship truncar últimos N=100 | NFR-Q5 / AC8 |
| 15 | Judge define (b) pulado | Further Notes |
| I1 | Canvas = COULD (quase-live só por rewrite) | WON'T MVP |
| I2 | Mapa = todos; live = ativo | AC3–AC4 |
| I3 | Pacote `config/fluxo_events/` + `fluxo-events.yaml` | FR1–FR2 |
| I4 | N=100 no truncate | AC8 |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (CLI exit/warnings, conteúdo JSONL/HTML,
rotate, truncate, fail-soft, fixture de install), não detalhes privados de helpers
internos salvo o contrato documentado no YAML.

Alinhado às decisões do grill: suite dedicada `tests/fluxo_events/`; E2E IDE = dogfood
manual (fora do CI obrigatório). Prior art: `tests/evidence_gate/`,
`tests/agent_policies/`, `tests/git_hygiene/`.

| Área | O que testar | Prior art |
|---|---|---|
| Contrato YAML | load tipado; cap 2 MiB; N=100; mapa 0–4; sem SLA numérico | contrato evidence-gate / policies |
| emit | append JSONL; campos mínimos; rejeita payload com campos proibidos se validar | tmpdir |
| render | HTML com todas fases/agents; highlight ativo; LWW | fixture HTML |
| Fail soft | FS error → warning; não propaga bloqueio ao caller de teste | matrix |
| Cap / rotate | arquivo > 2 MiB → tail preservado + warning | tmp oversized |
| Truncate ship | >100 linhas → ≤100 após truncate + re-render | pytest |
| Append sem lock | dois emits não exigem lock file | docs + teste sequencial |
| Install foundation | filho recebe CLI/template | testes install |
| SI | fixtures sem secret/PII/prompt | grep + asserts |
| `/validar` | suite canônica verde com novos testes | gate existente |
| Ortogonalidade | docs não misturam kernels | review |

### Plano de validação (DoD gate)

```bash
# Código (sempre)
uv run ruff check --fix . && uv run mypy . && uv run pytest -q

# Suite nova (quando existir)
uv run pytest -q tests/fluxo_events/

# CLI (quando existir)
python -m config.fluxo_events emit --help
python -m config.fluxo_events render --help
# emit/render contra fixture versionada sob tests/fluxo_events/fixtures/
```

Critério: gate **verde** no canônico; fixtures PASS; sem E2E IDE obrigatório no CI;
kernels ortogonais (evidence-gate, agent-policies, DE) sem regressão.

---

## Out of Scope

Materializa a **decisão 10** + WON'T do grill:

- Mini-app SSE / WebSocket no MVP
- Canvas Cursor como MUST
- Dev Loop no mapa MVP (Fase 2 / COULD)
- Prompts, diffs, PII ou secrets no event log
- Unificar / misturar com evidence-gate ou agent-policies
- Substituir `STATUS.md` / `/scorecard` / `entregas.jsonl`
- Key vault / pacote E
- Alvo de latência numérico; mutex de append
- Hooks Session/Task nativos do IDE como MUST
- Tag `prod-*` / Fase 2 git hygiene
- Orquestrador runtime central de agents (continua match por `description:`)

---

## Risks

| Risco | Mitigação |
|---|---|
| Agents omitem emit → painel stale | Fail soft + docs §1.3; wiring explícito; dogfood |
| Corrida de append corrompe JSONL | G2-a consciente; linhas curtas; render tolerante a linha inválida (skip + warning) |
| Log gigante | Cap 2 MiB + rotate tail (AC6); truncate no ship (AC8) |
| Confusão com evidence-gate | FR8 / AC13 — telemetria ≠ aceite |
| Confusão com STATUS/scorecard | AC14 — complementar, não substitui |
| Drift Claude↔Cursor em `fluxo/` | Invariante de espelho + AC11 |
| Install omite foundation | AC9 fixture bloqueante |
| Expectativa de SSE “tempo real” | FR5 + Out of Scope; http.server opcional |
| Vazamento de prompt/PII no evento | Schema + validação + AC10 SI |
| Fetch Azure 403 atrasa sync | Soft-block didático; branch local feat |
| Judge ainda não confirmado no design | STATUS: pendente a/b; **não** architect até parent perguntar |

---

## SI Considerations

- **Nível a:** sem dados sensíveis de domínio; eventos = agent name, phase, task id,
  timestamps, event_type, slug.
- Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault neste ship.
- **Invariante:** event log **nunca** inclui prompts, conteúdo de usuário, diffs,
  secrets, tokens, connection strings, PII. Exemplos e fixtures auditáveis por grep
  (AC10).
- Rule `seguranca` transversal permanece; este ship não amplia superfície de escrita em
  produção.
- **Honesty §1.3:** telemetria local e dogfoodável; emit pode ser omitido ou forjado;
  sem Edit policies o framework não garante fidelidade — reduz cegueira operacional e
  torna o fluxo legível para humano/CI.
- Revisor-codigo: SI bloqueante se o ship introduzir logging de prompt/PII/secret em
  eventos ou prometer telemetria server-side infalsificável.

---

## Suggested task breakdown (tracer bullets)

Útil para `/to-tasks` depois do architect — fatias verticais sugeridas:

1. **T1 — Contrato + loader** — `fluxo-events.yaml` + load tipado + testes de contrato
   (mapa 0–4, cap, N=100, G1-c).
2. **T2 — emit** — append JSONL + validação de campos + fail-soft + testes.
3. **T3 — render** — `live.html` com mapa completo + highlight ativo + fixture alinhada
   ao mockup + testes.
4. **T4 — rotate + truncate** — cap 2 MiB rotate tail; ship truncate N=100 + re-render
   + testes.
5. **T5 — wiring SDD** — instruções enter/exit nos agents/skills 0–4 + harness-ship
   truncate; espelho `.cursor/`.
6. **T6 — install foundation** — stack_map + template `fluxo/` + teste install.
7. **T7 — docs SHOULD** — cheatsheet + ADR + `/fluxo-live` + honesty §1.3.
8. **T8 — /validar + dogfood** — suite verde; emit/render no próprio projeto slug
   (opcional mas desejável).

Cada task deve declarar critérios de aceite testáveis amarrados a AC1–AC18.

---

## Critérios de aceite do ship (fechamento)

O ship desta evolução só fecha quando:

1. AC1–AC18 atendidos com evidência (testes e/ou review documentada).
2. `/validar` verde no canônico (inclui `tests/fluxo_events/`).
3. Evidence-gate das tasks deste fluxo verde (quando o kernel evidence-gate estiver em
   uso nas tasks) — **ortogonal**: telemetria fluxo ≠ prova de aceite.
4. `revisor-codigo` sem bloqueante SI/wiring.
5. Espelho `.claude`↔`.cursor` dos artefatos promovidos.
6. `03-harness.md` + tasks index + delivery records conforme DoD.
7. `/sync-context` no fechamento (CLAUDE.md/AGENTS.md refletem o kernel novo).
8. Truncate N=100 documentado e testado no path de ship.

---

## Further Notes

- **Adversarial judge (grill/define):** pulado **(b)** — sem `01b-judge.md`.
- **Adversarial judge (PRD):** **pendente confirmação humana** — checkpoint obrigatório
  antes do `/harness-architect` (perguntar a/b mesmo após pulo no define). **Esta
  invocação de harness-design NÃO roda harness-architect.**
- Naming exato de `event_type`, layout interno do HTML e se `emit` auto-chama `render`
  podem fechar no architect desde que FR1–FR9 e ACs sejam preservados.
- Soft-blocks deste design: fetch 403; sem commit/push; **sem** `PRD.md` na raiz do
  canônico — apenas `02-prd.md` neste projeto (+ espelho `.cursor/`).
- Working tree com untracked `projetos/visao-grafica-fluxo-agentes/` — OK; não
  stash/commit neste passo.
- Próximo artefato após judge (a/b) + architect: `03-harness.md` → `/to-tasks` →
  `harness-build`.

---

## Próximo passo (após aceite do PRD + judge)

1. Checkpoint adversarial judge (a/b) — se (a), gerar `02b-judge.md` e opcionalmente
   ajustar o PRD; se (b), seguir
2. `/harness-architect` — montar/atualizar artefatos de harness desta evolução
3. Registrar `03-harness.md` → `/to-tasks` → `harness-build`
