# Fluxo-events Dev Loop + backfill — Decisões de Harness

Slug: `fluxo-events-dev-loop-live`  
Branch: `feat/fluxo-events-dev-loop-live`  
Data: 2026-08-17  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Lacunas de naming fechadas no architect (sem entrevista): ver seção abaixo  
Kernel base: ADR-005 + `fluxo-events.yaml` + `config/fluxo_events/`  
Conceito Dev Loop: `DEV-LOOP.md` · `prompt-crafter` · `dev-loop-executor` · `/dev`

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.
> Orthografia PT-BR: sempre **fluxo** (com **x**). Nunca **flujo** (com **j**) em
> artefatos do pacote.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **a** (só metadados de processo / SHAs públicos —
  sem PII/prompts/secrets)
- Sem agent “fluxo officer” / telemetria dedicada — estender agents/docs Dev Loop
  existentes + kernel já shipado
- Fluxo-events = **telemetria fail-soft**; evidence-gate = **hard**; agent-policies =
  freio Bash — kernels **não** unificados
- `/validar` permanece suite global; live **não** substitui `PROGRESS.md` / STATUS.md /
  scorecard / entregas (exceto backfill one-shot do campo `commit`)
- Extensão do kernel existente — **não** fork / mini-app / SSE
- Honesty §1.3: telemetria local ≠ fidelidade perfeita; emit omitível/forjável
- SLA **best effort** — sem alvo numérico (herdado G1-c)
- Append **best-effort sem lock** (herdado G2-a)
- Cap log **2 MiB** rotate keep-tail + warning soft (herdado G3-a)
- Dev Loop: dry-run **não** emite; `EXIT_COMPLETE` → exit + truncate **N=100** + re-render
- Slug sintético `dev-loop-{nome}` sob `projetos/` (+ espelho `.cursor/`)
- `render` escolhe `dev_loop_map` vs `sdd_map` pelo prefixo `dev-loop-`
- Reusar `event_types` existentes; `phase` = índice do mapa ativo
- Guardrail PT-BR mecânico no pacote (`test_naming_ptbr.py`)
- Espelho `.claude` ↔ `.cursor` na mesma sessão de promoção
- Commit/push só com acordo explícito

## Naming fechado no architect (não bloqueava; alinhado ao padrão)

| Item | Escolha | Motivo |
|---|---|---|
| Contrato | `fluxo-events.yaml` (raiz) — **estender** com `dev_loop_map` | Mesmo arquivo do kernel; sem segundo contrato |
| Pacote engine | `config/fluxo_events/` | Kernel já existente (ADR-005) |
| Helper | `slug_from_prompt_path(path) -> str` no pacote | Stem `PROMPT_*.md` → `dev-loop-{nome}` |
| Slug sintético | `dev-loop-{nome}` com `nome` lower kebab `[a-z0-9-]` | Grill #1/#8 |
| Pasta live Dev | `.claude/projetos/dev-loop-{nome}/fluxo/` (+ espelho `.cursor/`) | Mesmo layout SDD |
| Event log / UI | `fluxo/events.jsonl` · `fluxo/live.html` | Herdado; paths inalterados |
| `event_type` | **Reusar** lista atual (`phase_*`/`agent_*`/`task_*`/`ship_truncate`) | Grill #6 — sem `dev_loop_enter` |
| `phase` (Dev) | índice `0..6` do `dev_loop_map` | LOAD…SYNC |
| `render` | se `slug.startswith("dev-loop-")` → `dev_loop_map`; senão → `sdd_map` | Grill #2 |
| Dry-run | `--dry-run` → **zero** emit | Grill #7 |
| Complete | `EXIT_COMPLETE` → emit exit + `truncate --keep 100` + re-render | Grill #7 / G4-b análogo |
| Guardrail | `tests/fluxo_events/test_naming_ptbr.py` | Proíbe substring `flujo` (j) nos artefatos do pacote |
| Orthografia | sempre **fluxo** (x) | PT-BR; nunca flu+j+o |
| Backfill | editar `metrics/entregas.jsonl` issues **58–65** → `"commit": "e4dfc69"` | Grill #4/#5; one-shot |
| Docs SHOULD | seção Dev Loop + nota naming em `docs/fluxo-events-cheatsheet.md` | PRD SHOULD |
| ADR SHOULD | addendum ADR-005 **ou** ADR-006 (`dev_loop_map` + guardrail + truncate Dev) | PRD SHOULD |
| CLI | `python -m config.fluxo_events emit\|render\|truncate` (inalterada em superfície) | Sem CLI nova |
| Agent officer | **nenhum** | Gate de redundância |
| Seed install | seed `fluxo-events` já foundation; propagar YAML atualizado no re-install | Ver install abaixo |

### Mapa Dev Loop estrutural (obrigatório no contrato + render)

```
Fase 0 LOAD:            prompt-crafter, dev-loop-executor
Fase 1 VALIDATE:        prompt-crafter, dev-loop-executor
Fase 2 INIT_PICK:       prompt-crafter, dev-loop-executor
Fase 3 EXECUTE_VERIFY:  prompt-crafter, dev-loop-executor
Fase 4 UPDATE_CHECK:    prompt-crafter, dev-loop-executor
Fase 5 LOOP_LOG:        prompt-crafter, dev-loop-executor
Fase 6 SYNC:            prompt-crafter, dev-loop-executor
```

Esboço de contrato (build tipa no loader):

```yaml
dev_loop_map:
  0: { slug: LOAD, agents: [prompt-crafter, dev-loop-executor] }
  1: { slug: VALIDATE, agents: [prompt-crafter, dev-loop-executor] }
  2: { slug: INIT_PICK, agents: [prompt-crafter, dev-loop-executor] }
  3: { slug: EXECUTE_VERIFY, agents: [prompt-crafter, dev-loop-executor] }
  4: { slug: UPDATE_CHECK, agents: [prompt-crafter, dev-loop-executor] }
  5: { slug: LOOP_LOG, agents: [prompt-crafter, dev-loop-executor] }
  6: { slug: SYNC, agents: [prompt-crafter, dev-loop-executor] }
```

### Helper (contrato de comportamento)

```text
slug_from_prompt_path(path) -> "dev-loop-{nome}"
  stem "PROMPT_FOO_BAR.md" → nome "foo-bar" → "dev-loop-foo-bar"
  lower; non [a-z0-9] → "-"; colapsar "--"; strip "-"; charset final [a-z0-9-]
```

### Layout lógico (slug Dev)

```text
.claude/projetos/dev-loop-{nome}/fluxo/
├── events.jsonl
└── live.html
```

Espelho idêntico sob `.cursor/projetos/dev-loop-{nome}/fluxo/` quando dual-tree.
Pastas `dev-loop-*` **permanecem** após truncate (sem purge auto).

### Schema de evento (inalterado — metadados only)

```yaml
event_type: phase_enter | phase_exit | agent_enter | agent_exit | task_enter | task_exit | ship_truncate
ts: <ISO-8601>
phase: 0..6          # índice do mapa Dev quando slug é dev-loop-*
agent: prompt-crafter | dev-loop-executor | …
slug: dev-loop-{nome}
source: claude | cursor | cli   # opcional
```

**Proibido:** prompt, PROGRESS, diff, secret, PII, connection string.

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| `dev_loop_map` 0–6 | `fluxo-events.yaml` | validação | loader + render + CI |
| Render dual-map | `config/fluxo_events/` (render) | validação | CLI + agents Dev |
| Helper slug | `slug_from_prompt_path` em `config/fluxo_events/` | ferramentas | crafter / executor / testes |
| Paths live Dev | `projetos/dev-loop-{nome}/fluxo/` (+ espelho) | estado | humano + browser |
| Wiring + UX aviso | `prompt-crafter`, `dev-loop-executor`, `/dev`, `DEV-LOOP.md` | execução | agents Dev Loop |
| Dry-run silencioso | instruções executor + testes | execução | `/dev --dry-run` |
| Truncate no complete | wiring `EXIT_COMPLETE` + CLI truncate N=100 | validação | executor |
| Backfill 58–65 | `metrics/entregas.jsonl` → `e4dfc69` | estado | scorecard |
| Guardrail PT-BR | `tests/fluxo_events/test_naming_ptbr.py` | validação | `/validar` |
| Testes dual-map / wiring / backfill | `tests/fluxo_events/` | validação | CI |
| Cheatsheet Dev Loop + naming | `docs/fluxo-events-cheatsheet.md` | estado | agente JIT |
| ADR addendum | ADR-005 addendum ou ADR-006 | estado | humano + agent |
| Install propaga YAML | `install-harness` / foundation fluxo-events (re-copy contrato) | ferramentas | filhos no re-install |
| Contagem/docs canônico | `CLAUDE.md` / `AGENTS.md` no ship (`/sync-context`) | estado | próximo agente |
| Ortogonalidade | cheatsheet cross-link | estado | SI + maintainer |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs listados acima — andaime real no `harness-build` após
`/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent “fluxo officer” / telemetria dedicada no canônico (gate de redundância —
  responsabilidades cabem em crafter/executor + CLI existente)

### Agents / skills / commands / docs a estender (build)

**Dev Loop (MUST)**
- `prompt-crafter` — emit fail-soft no enter + aviso UX 1× (path `live.html` / `/fluxo-live`);
  derivar slug via `slug_from_prompt_path` quando houver path de PROMPT
- `dev-loop-executor` — emit enter/phase conforme `dev_loop_map`; **dry-run sem emit**;
  em `EXIT_COMPLETE` → exit + `truncate --keep 100` + re-render
- command `/dev` — documentar telemetria + aviso (espelho `.cursor/commands/`)
- `DEV-LOOP.md` — seção fluxo-events (enter tip, dry-run, truncate no complete)

**Kernel (MUST)**
- `fluxo-events.yaml` — acrescentar `dev_loop_map`
- `config/fluxo_events/` — render dual-map + `slug_from_prompt_path` (+ loader tipado)
- `tests/fluxo_events/test_naming_ptbr.py` — proíbe `flujo` (j) em artefatos do pacote
- demais testes: mapa Dev, helper, wiring presença, dry-run, truncate, backfill assert

**Higiene scorecard (MUST)**
- `metrics/entregas.jsonl` — issues 58–65 `"commit": "e4dfc69"` (one-shot; sem script genérico)

**Docs (SHOULD)**
- `docs/fluxo-events-cheatsheet.md` — seção Dev Loop + nota naming `fluxo`≠`flujo`
- ADR-005 addendum **ou** ADR-006 — `dev_loop_map`, slug sintético, guardrail, truncate Dev

**Install (se precisar propagar)**
- Foundation fluxo-events já always-on: no re-install / sync do contrato, garantir que o
  `fluxo-events.yaml` atualizado (com `dev_loop_map`) chegue aos filhos; seed KEEP inalterado
  em semântica (stubs `fluxo/`). Sem categoria nova; sem agent novo no `stack_map`.
- Atualizar menções em `CLAUDE.md` / `AGENTS.md` / `install-harness` só se a tabela
  “onde fica o quê” precisar citar `dev_loop_map` / Dev Loop live — no `/sync-context` do ship.

### Rules
- Sem rule nova `fluxo-events.md` obrigatória; cheatsheet basta
- **Não** tornar emit bloqueante na DoD (fail soft ≠ evidence-gate)
- Ponte SI: nunca prompt/PII/secret no event log

### KBs
- **Nenhum** KB de domínio novo obrigatório neste ship

## Ortogonalidade (obrigatória)

| Kernel / artefato | Concern | Relação com este ship |
|---|---|---|
| evidence-gate | Aceite hard por task | **Ortogonal** — telemetria ≠ manifesto |
| agent-policies | Freio Bash | **Ortogonal** |
| `/validar` | Suite global | Inclui novos testes `tests/fluxo_events/` |
| `PROGRESS.md` | Memory bridge Dev Loop | **Não** substituído |
| STATUS.md / scorecard | Checklist / métricas | Complementar; backfill só corrige SHA 58–65 |
| Kernel SDD fluxo-events | Telemetria 0–4 | Estendido; mapa SDD intacto |

Cross-link: “telemetria ≠ aceite ≠ Bash deny”; Dev Loop live = mesmo kernel, outro mapa.

## O que NÃO entra neste ship

- SSE / Canvas MUST
- Unificar com evidence-gate
- Skill MUST nova
- Mutex no append
- Script genérico de backfill
- Substituir `PROGRESS.md` / STATUS.md / scorecard
- Orthografia genérica de todo o repo
- Key vault / pacote E
- Alvo de latência numérico; fork do kernel
- Agent “fluxo officer”
- Purge automático de pastas `dev-loop-*`
- `PRD.md` na raiz do canônico
- Tag `prod-*` / Fase 2 git hygiene

## Decisões contestáveis (ADR na implementação)

1. Estender o **mesmo** kernel com `dev_loop_map` (não fork) — um painel, dois mapas
2. Bifurcação de render por **prefixo de slug** `dev-loop-` — zero flag extra no CLI
3. Reusar `event_types`; `phase` = índice Dev — schema estável
4. Truncate N=100 no `EXIT_COMPLETE` (análogo ship SDD) — bounded trail por loop
5. Dry-run sem emit — telemetria só em execução real
6. Guardrail pytest só no pacote `fluxo*` (não repo inteiro) — escopo MUST fechado
7. Backfill one-shot SHA fixo `e4dfc69` — dívida pontual sem framework de higiene
8. Sem agent officer / skill MUST — wiring + cheatsheet bastam

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local `feat/fluxo-events-dev-loop-live`
- Working tree: artefatos untracked em `projetos/fluxo-events-dev-loop-live/`
- Sem commit/push neste passo
- Sem implementação de código neste passo (só plano de harness)
- Adversarial judge define: **(b)** pulado (2026-08-17)
- Adversarial judge PRD: **(b)** pulado (2026-08-17) — sem `02b-judge.md`

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (tracer bullets T1–T8 do `02-prd.md`)
2. `harness-build` — implementar com `/validar` + `revisor-codigo` (sem agent officer)
3. Ao fechar: `/sync-context` + delivery records + evidence-gate das tasks (**ortogonal** à
   telemetria) + dogfood opcional com slug `dev-loop-*`
