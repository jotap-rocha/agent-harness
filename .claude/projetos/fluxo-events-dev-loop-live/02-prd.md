# PRD — Fluxo-events no Dev Loop + backfill de commits

Slug: `fluxo-events-dev-loop-live`  
Repo: Agent Harness Canônico (framework — **não** produto)  
Branch: `feat/fluxo-events-dev-loop-live`  
Data: 2026-08-17  
Tipo: **e** — evolução do harness canônico  
SI: **a** (só metadados de processo / SHAs públicos — sem PII)  
Fontes: `00-ideia.md`, `01-grill.md` (decisões 1–10 + define I1–I7)  
Kernel base: `fluxo-events.yaml` + `config/fluxo_events/` + ADR-005  
Conceito Dev Loop: `DEV-LOOP.md` · agents `prompt-crafter` / `dev-loop-executor` · `/dev`

> Decisões do grill/define estão **fechadas** — este PRD as materializa; não reabre a matriz.
> Orthografia PT-BR obrigatória: **fluxo** (com **x**). Nunca **flujo** (com **j**) em
> artefatos do pacote.
> **Adversarial judge (PRD):** pendente confirmação humana (a/b) — **não** rodar
> `/harness-architect` até o parent obter resposta do usuário.
> **Judge define:** pulado **(b)** — sem `01b-judge.md`.

---

## Problem Statement

O kernel `fluxo-events` (ship `visao-grafica-fluxo-agentes`) cobre o SDD 0–4 com
`emit`/`render`/`truncate` e aviso UX no enter de brainstorm/build. O **Dev Loop**
(`/dev`, `prompt-crafter`, `dev-loop-executor`, artefatos `PROMPT`/`PROGRESS`/`LOG`)
roda em paralelo sem alimentar o mesmo painel `live.html` e sem o aviso de como
abrir a telemetria.

Em paralelo, as entregas **58–65** em `metrics/entregas.jsonl` ficaram com
`"commit": "pending"` após o ship da visão gráfica — o scorecard/histórico deixam de
ser auditáveis embora o trabalho já esteja no git sob o SHA `e4dfc69`.

Há ainda risco de regressão de naming **flujo** (ES, j) vs **fluxo** (PT, x) em
paths/seeds do pacote, sem check mecânico no gate.

O sintoma é “Dev Loop invisível no painel + delivery records sujos”. O problema real
é a ausência de (1) extensão do kernel para um **mapa Dev Loop** com slug sintético
e wiring fail-soft nos agents `/dev`, (2) higiene pontual das entregas 58–65, e
(3) guardrail pytest de orthografia no pacote — sem fork do kernel, sem SSE, sem
misturar com evidence-gate.

§1.3 permanece: telemetria local best-effort; omissão/falha de emit não bloqueia `/dev`.

---

## Solution

Estender o kernel `fluxo-events` existente (não fork) para cobrir o Dev Loop com o
mesmo painel HTML, mais um backfill one-shot e um guardrail de naming:

1. **Slug sintético** `dev-loop-{NOME}` sob `.claude/projetos/` (+ espelho `.cursor/`),
   onde `NOME` = stem do `PROMPT_*.md` em lower kebab `[a-z0-9-]` via helper
   `slug_from_prompt_path(path) -> str` no pacote `fluxo_events`.
2. **Contrato** `fluxo-events.yaml` ganha `dev_loop_map` (fases 0–6). `render` escolhe
   mapa SDD vs Dev pelo prefixo do slug (`dev-loop-` → Dev; demais → SDD).
3. **Reusar** `event_types` existentes; `phase` = índice do `dev_loop_map` (não inventar
   `dev_loop_enter` etc.).
4. **Wiring + UX aviso** (1× no enter) em `prompt-crafter`, `dev-loop-executor`,
   comando `/dev` e `DEV-LOOP.md` — espelho da task 66 do SDD; fail soft.
5. **Dry-run** (`--dry-run`): **não** emite. **EXIT_COMPLETE**: `agent_exit`/`phase_exit`
   + `truncate --keep 100` + re-render (análogo ao ship SDD).
6. **Backfill one-shot**: linhas issue 58–65 em `metrics/entregas.jsonl` →
   `"commit": "e4dfc69"` (sem script genérico de backfill).
7. **Guardrail PT-BR**: pytest falha se substring `flujo` (j) aparecer em artefatos
   versionados do pacote `fluxo_events` / `fluxo-events*` / `tests/fluxo_events`.
8. **Fail soft** idêntico ao SDD; dual-tree; testes de mapa/render, wiring, backfill,
   naming.
9. **SHOULD:** cheatsheet seção Dev Loop + nota naming; addendum ADR-005 (ou ADR-006).

### Mapa Dev Loop obrigatório (estrutural — cravado neste PRD)

```
Fase 0 LOAD:            prompt-crafter, dev-loop-executor
Fase 1 VALIDATE:        prompt-crafter, dev-loop-executor
Fase 2 INIT_PICK:       prompt-crafter, dev-loop-executor
Fase 3 EXECUTE_VERIFY:  prompt-crafter, dev-loop-executor
Fase 4 UPDATE_CHECK:    prompt-crafter, dev-loop-executor
Fase 5 LOOP_LOG:        prompt-crafter, dev-loop-executor
Fase 6 SYNC:            prompt-crafter, dev-loop-executor
```

Agents canônicos do Dev Loop: **`prompt-crafter`**, **`dev-loop-executor`**.

Esboço de contrato (decisão-rich; loader tipado no build):

```yaml
# Acrescentar a fluxo-events.yaml (versão bump se breaking)
dev_loop_map:
  0: { slug: LOAD, agents: [prompt-crafter, dev-loop-executor] }
  1: { slug: VALIDATE, agents: [prompt-crafter, dev-loop-executor] }
  2: { slug: INIT_PICK, agents: [prompt-crafter, dev-loop-executor] }
  3: { slug: EXECUTE_VERIFY, agents: [prompt-crafter, dev-loop-executor] }
  4: { slug: UPDATE_CHECK, agents: [prompt-crafter, dev-loop-executor] }
  5: { slug: LOOP_LOG, agents: [prompt-crafter, dev-loop-executor] }
  6: { slug: SYNC, agents: [prompt-crafter, dev-loop-executor] }
# sdd_map + event_types + limits inalterados em semântica; render bifurca por slug
```

### Helper

```text
slug_from_prompt_path(path) -> "dev-loop-{nome}"
  stem "PROMPT_FOO_BAR.md" → nome "foo-bar" → slug "dev-loop-foo-bar"
  regras: lower; não alfanumérico → "-"; colapsar "--"; strip "-"; charset [a-z0-9-]
```

---

## Goals (MoSCoW)

### MUST

- Slug `dev-loop-{NOME}` sob `projetos/` (+ espelho `.cursor/`)
- `dev_loop_map` no `fluxo-events.yaml`; `render` escolhe SDD vs Dev por prefixo
  `dev-loop-`
- Reusar `event_types`; `phase` = índice do mapa Dev
- Helper `slug_from_prompt_path` no pacote `fluxo_events`
- Wiring + aviso UX: `prompt-crafter`, `dev-loop-executor`, `/dev`, `DEV-LOOP.md`
- Dry-run **sem** emit; `EXIT_COMPLETE` → exit + `truncate --keep 100` (+ re-render)
- Backfill entregas 58–65 → commit `e4dfc69`
- Guardrail PT-BR: **fluxo** (x) obrigatório; rejeitar **flujo** (j) em artefatos do
  pacote (pytest)
- Fail soft (mesmo padrão SDD); dual-tree; testes (mapa/render, wiring, backfill, naming)
- Eventos = só metadados (sem prompts/PII/secrets)
- Cap 2 MiB / append sem lock / SLA best effort herdados do kernel (inalterados)

### SHOULD

- Cheatsheet: seção Dev Loop + nota naming `fluxo`≠`flujo`
- Addendum ADR-005 (ou ADR-006) documentando `dev_loop_map` + guardrail

### COULD

- Canvas / SSE como superfície extra
- Orthografia genérica além do par `fluxo`/`fluxo` no repo inteiro

### WON'T (neste ship)

- SSE / Canvas MUST
- Unificar com evidence-gate
- Skill MUST nova
- Mutex no append
- Script genérico de backfill (além do one-shot 58–65)
- Substituir `PROGRESS.md` / `STATUS.md` / scorecard
- Orthografia genérica de todo o repo
- Key vault (SI a — N/A)
- Alvo de latência numérico; fork do kernel

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want `dev_loop_map` versioned in `fluxo-events.yaml`, so that Dev Loop phases 0–6 are auditable like the SDD map.
2. As a mantenedor do canônico, I want `render` to select `dev_loop_map` when the slug starts with `dev-loop-`, so that one engine serves both flows without forking.
3. As a mantenedor do canônico, I want existing `event_types` reused with `phase` as the Dev map index, so that schema churn stays minimal.
4. As a mantenedor do canônico, I want `slug_from_prompt_path` in the `fluxo_events` package, so that agents derive a deterministic synthetic slug from `PROMPT_*.md`.
5. As a mantenedor do canônico, I want emit/render under `.claude/projetos/dev-loop-{NOME}/fluxo/` (+ `.cursor/` mirror), so that Dev Loop live uses the same layout as SDD.
6. As a mantenedor do canônico, I want emit/render/truncate to **fail soft**, so that `/dev` never stalls on telemetry.
7. As a mantenedor do canônico, I want a pytest naming guard that fails on `flujo` (j) in package artifacts, so that ES spelling cannot regress into the kernel tree.
8. As a mantenedor do canônico, I want issues 58–65 in `metrics/entregas.jsonl` to store `"commit": "e4dfc69"`, so that scorecard history is auditable.
9. As a mantenedor do canônico, I want dual-tree mirror of Dev Loop wiring docs/agents/commands, so that Claude and Cursor stay in sync.
10. As CI do canônico, I want `/validar` green including `tests/fluxo_events/` extensions, so that this ship does not weaken gates.
11. As a mantenedor do canônico, I want docs to keep §1.3 honesty and orthogonality to evidence-gate / agent-policies, so that telemetry is not mistaken for acceptance or Bash deny.

### Agente / wiring Dev Loop

12. As `prompt-crafter`, I want a fail-soft emit on enter (and documented UX tip once), so that crafting sessions appear on the live panel.
13. As `dev-loop-executor`, I want fail-soft emit on enter/phase transitions using Dev map indices, so that LOAD→SYNC is visible like SDD 0–4.
14. As `dev-loop-executor`, I want `--dry-run` to skip all emits, so that plan-only runs leave no telemetry noise.
15. As `dev-loop-executor`, I want `EXIT_COMPLETE` to emit exit and run `truncate --keep 100` + re-render, so that closed loops keep a bounded trail.
16. As an agente Dev Loop, I want event fields limited to metadata, so that I never log prompts, PROGRESS contents, secrets, or PII.

### Humano / operador `/dev`

17. As a humano no `/dev`, I want a one-time enter tip pointing to `projetos/dev-loop-{NOME}/fluxo/live.html` (and `/fluxo-live` if applicable), so that I can open the panel without reading only the chat.
18. As a humano no `/dev`, I want `DEV-LOOP.md` and `/dev` docs to mention fluxo-events wiring, so that dogfood matches agent behavior.
19. As a leitor de PROGRESS/STATUS/scorecard, I want those artifacts unchanged as sources of truth, so that live telemetria complements rather than replaces them.

### Scorecard / higiene

20. As a mantenedor do scorecard, I want a one-shot backfill only for issues 58–65 → `e4dfc69`, so that the known debt is fixed without a generic backfill framework.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `fluxo-events.yaml` inclui `dev_loop_map` 0–6 com agents `prompt-crafter` e `dev-loop-executor` | pytest contrato / loader |
| AC2 | `render` com slug `dev-loop-*` usa mapa Dev; slug sem prefixo continua SDD | pytest render dual-map |
| AC3 | `slug_from_prompt_path("…/PROMPT_FOO.md")` → `dev-loop-foo` (kebab/lower/`[a-z0-9-]`) | pytest helper |
| AC4 | Paths `projetos/dev-loop-{NOME}/fluxo/{events.jsonl,live.html}` (+ espelho) | pytest emit/render path |
| AC5 | Eventos reusam `event_types`; `phase` ∈ 0..6 no Dev | pytest emit schema |
| AC6 | Wiring documentado em crafter, executor, `/dev`, `DEV-LOOP.md` (emit + aviso UX) | testes de presença + review |
| AC7 | Dry-run: zero linhas novas em `events.jsonl` | pytest / fixture dry-run |
| AC8 | `EXIT_COMPLETE`: truncate deixa ≤100 linhas + re-render | pytest truncate path Dev |
| AC9 | Fail soft: FS error em emit/render → warning; `/dev` não bloqueado | pytest fail-soft |
| AC10 | Entregas 58–65 com `"commit": "e4dfc69"` | assert sobre `metrics/entregas.jsonl` |
| AC11 | Pytest naming falha se `fluxo` (j) em artefatos do pacote `fluxo_events` / `fluxo-events*` / `tests/fluxo_events` | `test_naming_ptbr.py` |
| AC12 | Zero prompt/PII/secret em fixtures de eventos | grep + review SI |
| AC13 | Espelho `.claude`↔`.cursor` do wiring/docs deste ship | checklist simétrica |
| AC14 | `/validar` verde com suite `tests/fluxo_events/` estendida | ruff + mypy + pytest |
| AC15 | Ortogonalidade: não unifica evidence-gate / agent-policies; não substitui PROGRESS | review docs |
| AC16 | Cap 2 MiB / append sem lock / SLA best effort preservados | contrato + testes existentes verdes |
| AC17 | Docs §1.3 honesty + nota naming PT-BR (SHOULD cheatsheet/ADR) | review |

---

## Functional Requirements

### FR1 — Extensão do contrato

- Acrescentar `dev_loop_map` (fases 0–6, slugs LOAD…SYNC, agents listados acima).
- Preservar `sdd_map`, `event_types`, `limits` (2 MiB, N=100), `paths`.
- Sem campo de SLA numérico (G1-c herdado).

### FR2 — Engine / render dual-map

- `render(slug)`: se `slug.startswith("dev-loop-")` → `dev_loop_map`; senão → `sdd_map`.
- `emit` / `truncate` inalterados em semântica fail-soft; paths sob
  `projetos/{slug}/fluxo/`.
- Helper público `slug_from_prompt_path`.

### FR3 — Wiring Dev Loop

- `prompt-crafter`: enter → emit fail-soft + aviso UX 1× (path `live.html` / `/fluxo-live`).
- `dev-loop-executor`: enter/phase emits conforme mapa; dry-run silencioso; em
  `EXIT_COMPLETE` → exit emit + `truncate --keep 100` + re-render.
- `/dev` + `DEV-LOOP.md`: documentar telemetria e aviso (espelho dual-tree).
- Outros exits (`CIRCUIT_BREAKER`, `MAX_ITERATIONS`) podem emitir exit **sem** truncate
  obrigatório neste ship (truncate MUST só em `EXIT_COMPLETE`) — se o build quiser
  truncate também nesses exits, documentar como SHOULD sem quebrar AC8.

### FR4 — Backfill one-shot

- Editar somente issues **58–65** em `metrics/entregas.jsonl`.
- Valor fixo `"commit": "e4dfc69"`.
- Sem CLI genérica de backfill; teste assert pós-edição.

### FR5 — Guardrail naming PT-BR

- Suite `tests/fluxo_events/test_naming_ptbr.py` (nome sugerido).
- Escopo: tree versionada do pacote (`config/fluxo_events/`, `fluxo-events.yaml`,
  seeds/templates `fluxo*`, `tests/fluxo_events/`, commands/cheatsheet do kernel quando
  versionados sob esses globs).
- Falha se substring `flujo` (j) aparecer em **nomes de arquivo/path** ou conteúdo
  versionado do pacote conforme regra do teste (mínimo: paths/filenames; conteúdo de
  artefatos do pacote conforme I7 do define).
- Fora de escopo: orthografia genérica do repo inteiro.

### FR6 — Ortogonalidade

- Não misturar com evidence-gate (aceite) nem agent-policies (Bash deny).
- Não substituir `PROGRESS.md`, `STATUS.md`, `/scorecard`.
- Cross-link em cheatsheet/ADR addendum.

### FR7 — Documentação (SHOULD)

- Cheatsheet: seção Dev Loop + nota `fluxo`≠`fluxo`.
- Addendum ADR-005 ou ADR-006: `dev_loop_map`, slug sintético, guardrail, truncate no
  `EXIT_COMPLETE`.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | SI **a**: metadados + SHA públicos; sem PII/prompts/secrets no log |
| NFR-SI2 | Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault neste ship |
| NFR-SI3 | Fixtures auditáveis por grep — zero secret/PII |
| NFR-SI4 | Honesty §1.3: telemetria local ≠ fidelidade perfeita |
| NFR-Q1 | Fail soft: emit/render/truncate nunca bloqueia `/dev` |
| NFR-Q2 | SLA best effort — sem alvo numérico |
| NFR-Q3 | Append best-effort sem lock (herdado) |
| NFR-Q4 | Cap 2 MiB rotate keep-tail (herdado) |
| NFR-Q5 | Truncate N=100 no `EXIT_COMPLETE` |
| NFR-Q6 | Espelho `.claude`↔`.cursor` na mesma sessão |
| NFR-Q7 | Soft-block git: fetch Azure 403 → branch local; sem inventar sync |
| NFR-Q8 | Orthografia PT-BR **fluxo** (x) nos artefatos do pacote |

---

## Architecture — artefatos canônicos

```text
┌─ fluxo-events.yaml ──► sdd_map + dev_loop_map + event_types + limits
│
├─ config/fluxo_events/ ──► load · emit · render(dual) · truncate · slug_from_prompt_path
│
├─ .claude/projetos/dev-loop-{NOME}/fluxo/ ──► events.jsonl · live.html
│         (+ espelho .cursor/projetos/.../fluxo/)
│
├─ wiring: prompt-crafter · dev-loop-executor · /dev · DEV-LOOP.md
│         dry-run sem emit; EXIT_COMPLETE → truncate N=100
│
├─ metrics/entregas.jsonl ──► backfill 58–65 → e4dfc69
├─ tests/fluxo_events/ ──► dual-map · helper · wiring · backfill · naming PT-BR
├─ docs: cheatsheet Dev Loop · ADR addendum (SHOULD)
└─ ortogonal: evidence-gate · agent-policies · PROGRESS/STATUS/scorecard
```

### Amarras a módulos lógicos

| Artefato | Módulo / superfície |
|---|---|
| Contrato | `fluxo-events.yaml` (+ `dev_loop_map`) |
| Engine / CLI | `config/fluxo_events/` |
| Slug helper | `slug_from_prompt_path` |
| Por loop | `projetos/dev-loop-{NOME}/fluxo/` (+ espelho) |
| Wiring | prompt-crafter, dev-loop-executor, `/dev`, `DEV-LOOP.md` |
| Backfill | `metrics/entregas.jsonl` (58–65) |
| Guardrail | `tests/fluxo_events/test_naming_ptbr.py` |
| Docs | cheatsheet + ADR addendum (SHOULD) |
| Projeto SDD deste ship | `.claude/projetos/fluxo-events-dev-loop-live/` (+ espelho) |
| Ortogonal | evidence-gate, agent-policies, PROGRESS, STATUS, scorecard |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | Path `dev-loop-{NOME}` sob `projetos/` | FR2 / AC3–AC4 |
| 2 | `dev_loop_map`; render por prefixo | FR1–FR2 / AC1–AC2 |
| 3 | Emit/UX: crafter + executor + `/dev` + DEV-LOOP | FR3 / AC6 |
| 4 | Backfill one-shot | FR4 / AC10 |
| 5 | SHA `e4dfc69` | FR4 / AC10 |
| 6 | Reusar `event_type`; phase = índice Dev | FR1 / AC5 |
| 7 | Dry-run sem emit; complete + truncate 100 | FR3 / AC7–AC8 |
| 8 | NOME = stem PROMPT kebab | FR2 / AC3 |
| 9 | Guardrail PT-BR `fluxo`≠`fluxo` | FR5 / AC11 / NFR-Q8 |
| 10 | Judge define (b) pulado | Further Notes |
| I1 | Fail soft = SDD | AC9 / NFR-Q1 |
| I2 | Cap 2 MiB / append sem lock | AC16 |
| I3 | Fases Dev 0–6 cravadas | mapa acima / AC1 |
| I4 | Vault N/A | SI |
| I5 | SLA best effort | NFR-Q2 |
| I6 | Helper `slug_from_prompt_path` | AC3 |
| I7 | Pytest naming no pacote | AC11 |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (contrato YAML, escolha de mapa no render,
helper de slug, presença de wiring, dry-run silencioso, truncate no complete, conteúdo
de `entregas.jsonl`, falha do guardrail naming), não detalhes privados de HTML salvo
asserts de mapa/fase.

Prior art: `tests/fluxo_events/` (emit/render/rotate/truncate/wiring SDD),
`tests/evidence_gate/`, `tests/agent_policies/`.

| Área | O que testar | Prior art |
|---|---|---|
| Contrato | `dev_loop_map` 0–6 + agents | contrato SDD existente |
| Render dual | prefixo `dev-loop-` vs SDD | render fixtures |
| Helper slug | stem → kebab; charset | unit tmp paths |
| Emit Dev | phase 0–6; event_types reusados | emit tmpdir |
| Dry-run | zero append | fixture executor contrato |
| Truncate complete | ≤100 linhas | truncate SDD |
| Fail soft | FS error → warning | matrix SDD |
| Wiring presença | strings/one-liners nos 4 artefatos | testes presença SDD task 66 |
| Backfill | issues 58–65 == `e4dfc69` | assert arquivo |
| Naming PT-BR | introduz `flujo` → fail; baseline verde | novo teste |
| Dual-tree | espelho wiring | checklist / diff simétrico |
| `/validar` | suite canônica verde | gate existente |

### Plano de validação (DoD gate)

```bash
uv run ruff check --fix . && uv run mypy . && uv run pytest -q
uv run pytest -q tests/fluxo_events/
# asserts pontuais
python -c "from config.fluxo_events import slug_from_prompt_path; assert slug_from_prompt_path('PROMPT_FOO.md').startswith('dev-loop-')"
```

Critério: gate **verde**; AC1–AC17 com evidência; sem E2E IDE obrigatório; kernels
ortogonais sem regressão.

---

## Out of Scope

Materializa WON'T do grill (decisão 9 escopo + out-of-scope explícito):

- SSE / Canvas MUST
- Unificar / misturar com evidence-gate
- Skill MUST nova
- Mutex / lock de append
- Script genérico de backfill (qualquer `pending` além de 58–65)
- Substituir `PROGRESS.md` / `STATUS.md` / `/scorecard`
- Orthografia genérica de todo o repositório
- Key vault / pacote E
- Alvo de latência numérico
- Fork do kernel ou mini-app separado
- Tag `prod-*` / Fase 2 git hygiene
- Purge automático de pastas `dev-loop-*` após truncate

---

## Risks

| Risco | Mitigação |
|---|---|
| Agents omitem emit → painel stale | Fail soft + UX tip + testes de presença |
| Colisão de slug `dev-loop-*` com projeto SDD real | Convenção documentada; prefixo reservado |
| Stem ambíguo / caracteres especiais no PROMPT | Helper com charset estrito + testes |
| Truncate agressivo apaga debug mid-loop | Truncate só em `EXIT_COMPLETE` |
| Confusão evidence-gate ↔ telemetria | FR6 / AC15 |
| Drift Claude↔Cursor | AC13 dual-tree |
| Regressão `flujo` (j) | AC11 pytest |
| SHA `e4dfc69` errado vs histórico | Grill fechou SHA; assert AC10; não generalizar |
| Fetch Azure 403 | Soft-block didático; branch local |
| Architect cedo demais | Judge PRD a/b obrigatório antes do architect |

---

## SI Considerations

- **Nível a:** eventos = agent, phase (índice Dev), event_type, slug sintético,
  timestamps; backfill = short SHA já público no git.
- Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault.
- **Invariante:** event log **nunca** inclui texto de PROMPT, conteúdo de PROGRESS,
  diffs, secrets, tokens, PII.
- Rule `seguranca` transversal permanece.
- **Honesty §1.3:** telemetria local; emit omitível/forjável; sem Edit policies.
- Revisor-codigo: SI bloqueante se logging de prompt/PII/secret ou promessa de
  fidelidade server-side.

---

## Suggested task breakdown (tracer bullets)

Útil para `/to-tasks` depois do architect — fatias verticais sugeridas:

1. **T1 — Contrato `dev_loop_map` + loader** — YAML + testes AC1/AC16.
2. **T2 — Helper `slug_from_prompt_path` + paths Dev** — AC3/AC4.
3. **T3 — Render dual-map** — escolha SDD vs Dev por prefixo; HTML fases 0–6; AC2.
4. **T4 — Wiring + UX** — crafter, executor, `/dev`, `DEV-LOOP.md`; dry-run; AC6/AC7;
   espelho dual-tree.
5. **T5 — EXIT_COMPLETE truncate N=100** — AC8 + fail soft AC9.
6. **T6 — Backfill 58–65 → e4dfc69** — AC10 + teste assert.
7. **T7 — Guardrail naming PT-BR** — `test_naming_ptbr.py`; AC11.
8. **T8 — Docs SHOULD + /validar** — cheatsheet/ADR addendum; AC14/AC17; dogfood opcional
   com slug `dev-loop-*`.

Cada task declara ACs testáveis amarrados à tabela acima.

---

## Critérios de aceite do ship (fechamento)

O ship desta evolução só fecha quando:

1. AC1–AC17 atendidos com evidência (testes e/ou review documentada).
2. `/validar` verde no canônico (inclui extensões `tests/fluxo_events/`).
3. Evidence-gate das tasks deste fluxo verde quando aplicável — **ortogonal** à
   telemetria.
4. `revisor-codigo` sem bloqueante SI/wiring/naming.
5. Espelho `.claude`↔`.cursor` dos artefatos promovidos.
6. `03-harness.md` + tasks index + delivery records conforme DoD.
7. `/sync-context` no fechamento.
8. Entregas 58–65 com SHA `e4dfc69`; guardrail naming verde; truncate Dev testado.

---

## Further Notes

- **Adversarial judge (grill/define):** pulado **(b)** — sem `01b-judge.md`.
- **Adversarial judge (PRD):** **pendente confirmação humana** — checkpoint obrigatório
  antes do `/harness-architect`. **Esta invocação de harness-design NÃO roda
  harness-architect.**
- Soft-blocks: fetch Azure 403; sem commit/push; **sem** `PRD.md` na raiz do canônico —
  apenas `02-prd.md` neste projeto (+ espelho `.cursor/`).
- Pastas `dev-loop-*` sob `projetos/` **permanecem** após truncate (sem purge auto).
- Naming exato de campos HTML internos pode fechar no architect desde que FR/ACs sejam
  preservados.
- Próximo artefato após judge (a/b) + architect: `03-harness.md` → `/to-tasks` →
  `harness-build`.

---

## Próximo passo (após aceite do PRD + judge)

1. Checkpoint adversarial judge (a/b) — se (a), gerar `02b-judge.md` e opcionalmente
   ajustar o PRD; se (b), seguir
2. `/harness-architect` — montar/atualizar artefatos de harness desta evolução
3. Registrar `03-harness.md` → `/to-tasks` → `harness-build`
