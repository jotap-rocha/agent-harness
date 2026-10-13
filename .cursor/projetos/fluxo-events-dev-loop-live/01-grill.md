# Fluxo-events Dev Loop + backfill — Grill & Requisitos

Slug: `fluxo-events-dev-loop-live`  
Branch: `feat/fluxo-events-dev-loop-live`  
Grill fechado em: 2026-08-17  
Define enriquecido em: 2026-08-17  
Fontes: `00-ideia.md`, decisões do `/grill-me` (1–9, Q9→**b**), `harness-define`

## Checklist de completude (qualquer tipo)

| Dimensão | Status |
|---|---|
| Problema real (não sintoma) | ✅ Dev Loop sem live; entregas 58–65 pending; naming ES/PT |
| Usuários / personas | ✅ humano `/dev`, scorecard, agentes Dev Loop |
| Critérios de sucesso mensuráveis | ✅ (seção abaixo) |
| Out of scope | ✅ SSE/Canvas, evidence unify, skill MUST, mutex, script backfill, orthografia genérica |
| Restrições técnicas | ✅ tipo e, SI a, estender kernel, soft-block fetch |
| SLA / performance | ✅ best effort (igual G1-c do kernel) — sem alvo numérico |

## Contexto (da sessão /grill-me)

### Problema

1. O painel live (`fluxo-events`) cobre o SDD, mas o **Dev Loop** não emite telemetria nem
   avisa o usuário como abrir `live.html`.
2. Entregas **58–65** em `metrics/entregas.jsonl` ficaram com `"commit": "pending"` após o
   ship — scorecard/histórico inauditáveis.
3. Risco de regressão **flujo** (ES, j) vs **fluxo** (PT, x) em paths/seeds — sem check
   mecânico no gate (dívida da retro da visão gráfica).

### Usuários

| Persona | Pain |
|---|---|
| Humano no `/dev` | Quer ver o loop (LOAD→SYNC) e o agent/task ativo no mesmo estilo do SDD |
| Mantenedor / scorecard | Precisa de SHA real nas entregas 58–65 |
| Agente Dev Loop | Precisa de wiring fail-soft padronizado (como task 66 no SDD) |

### Objetivos (MoSCoW)

**MUST:**
- Slug sintético `dev-loop-{NOME}` sob `.claude/projetos/` (+ espelho `.cursor/`)
- `dev_loop_map` no `fluxo-events.yaml`; `render` escolhe mapa SDD vs Dev pelo slug `dev-loop-*`
- Reusar `event_type`s existentes; `phase` = índice do `dev_loop_map`
- Wiring + aviso UX em `prompt-crafter` e `dev-loop-executor`; docs `/dev` + `DEV-LOOP.md`
- Dry-run **não** emite; `EXIT_COMPLETE` → exit + `truncate --keep 100`
- Stem do PROMPT → NOME (lower, kebab, `[a-z0-9-]`)
- Backfill one-shot 58–65 → commit `e4dfc69`
- **Guardrail PT-BR**: artefatos do kernel/`tests/fluxo_events` / contrato / commands usam
  `fluxo` (x); teste mecânico falha se aparecer `flujo` (j) nos paths versionados do pacote
- Testes (mapa/render, wiring, backfill assert, naming) + dual-tree
- Fail soft (mesmo padrão SDD)

**SHOULD:**
- Cheatsheet seção Dev Loop + nota naming
- Addendum ADR-005 (ou ADR-006 se preferir no design) para `dev_loop_map` + guardrail

**COULD:**
- Canvas / SSE
- Orthografia genérica além do par `fluxo`/`flujo`

### Out of Scope

- SSE / Canvas MUST
- Unificar com evidence-gate
- Skill MUST nova
- Mutex no append
- Script genérico de backfill
- Substituir PROGRESS.md
- Orthografia genérica de todo o repo

### Restrições

- Tipo **e**; SI **a**
- Branch: `feat/fluxo-events-dev-loop-live`
- Soft-block fetch Azure 403
- Estender kernel existente — não fork
- Sem commit/push neste passo define

## Decisões numeradas (grill — fechadas)

1. Path: slug **`dev-loop-{NOME}`** sob `projetos/` (**a**)
2. UI: **`dev_loop_map`**; render por prefixo (**b**)
3. Emit/UX: **crafter + executor** + `/dev` + `DEV-LOOP.md` (**b**)
4. Backfill: **one-shot** (**a**)
5. SHA: **`e4dfc69`** (**a**)
6. `event_type`: **reusar**; phase = índice Dev (**a**)
7. Dry-run sem emit; complete + truncate 100 (**a**)
8. NOME: stem PROMPT → kebab (**a**)
9. Incluir guardrail PT-BR `fluxo`≠`flujo` (**b**); fora SSE/Canvas/etc.
10. Adversarial judge (define): **(b)** pulado

### Inferidos (define — não reabrir sem motivo)

| # | Inferência | Status |
|---|---|---|
| I1 | Fail soft idêntico ao SDD | Confirmado |
| I2 | Cap 2 MiB / append sem lock | Confirmado |
| I3 | `dev_loop_map` fases (proposta): 0 LOAD, 1 VALIDATE, 2 INIT_PICK, 3 EXECUTE_VERIFY, 4 UPDATE_CHECK, 5 LOOP_LOG, 6 SYNC — agents: prompt-crafter, dev-loop-executor | Proposto no define |
| I4 | Vault N/A | Confirmado SI a |
| I5 | SLA best effort (sem latência no yaml) | Confirmado define |
| I6 | Helper `slug_from_prompt_path(path) -> str` no pacote `fluxo_events` | Proposto |
| I7 | Guardrail: pytest varre paths do pacote + proíbe substring `flujo` em nomes de arquivo do tree `fluxo_events` / `fluxo-events*` | Proposto |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- N/A: SI **a** — metadados + SHAs públicos

## Especificações implícitas detectadas

| Lente | Decisão |
|---|---|
| 1. Falha dependência | Fail soft — emit/render/truncate não bloqueiam `/dev` |
| 2. Concorrência | Append best-effort sem lock (kernel) |
| 3. Idempotência | Re-emit = nova linha; truncate no EXIT_COMPLETE |
| 4. Auth | N/A — disco local |
| 5. Dados sensíveis | Só metadados / SHA — SI a |
| 6. Limites | Cap 2 MiB rotate; truncate N=100 no complete |
| 7. Auditoria | `events.jsonl` + `entregas.jsonl` (backfill) |
| 8. Erro visível | Warning soft stderr; aviso UX com path live.html |
| 9. Ciclo de vida | Truncate no complete; pastas `dev-loop-*` permanecem (sem purge auto) |
| 10. Contrato externo | N/A — HTML local |

## Amarras a artefatos (previsto)

| Artefato | Onde | Nota |
|---|---|---|
| Contrato | `fluxo-events.yaml` | + `dev_loop_map` |
| Engine | `config/fluxo_events/` | render dual-map; `slug_from_prompt_path` |
| Wiring | prompt-crafter, executor, `/dev`, DEV-LOOP.md | emit + UX |
| Backfill | `metrics/entregas.jsonl` | 58–65 → e4dfc69 |
| Guardrail | `tests/fluxo_events/test_naming_ptbr.py` | falha se `flujo` em artefatos do pacote |
| Docs | cheatsheet + ADR addendum | SHOULD |
| Testes | `tests/fluxo_events/` | mapa Dev, wiring, backfill, naming |

## Critérios de sucesso mensuráveis

- Slug `dev-loop-foo` a partir de `PROMPT_FOO.md`; HTML com mapa Dev Loop
- Crafter/executor + docs com emit/UX; testes de presença verdes
- Dry-run sem eventos; complete ≤100 linhas pós-truncate
- Entregas 58–65 com `"commit": "e4dfc69"`
- Pytest naming falha se introduzir `flujo` nos artefatos do pacote `fluxo-events`
- Espelho dual-tree do wiring

## Soft-blocks registrados

- `git fetch` Azure 403 — branch local `feat/fluxo-events-dev-loop-live`
- Judge define ainda não confirmado (a/b)

## Próximo passo

Rode **`harness-design`** para gerar o PRD (após judge a/b se desejado).
