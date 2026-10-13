# Fluxo — Grafo Causal Real — Decisões de Harness

Slug: `fluxo-grafo-causal`  
Branch: `feat/fluxo-grafo-causal`  
Data: 2026-08-18  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Lacunas de naming fechadas no architect (sem entrevista): ver seção abaixo  
Kernel base: ADR-005 + `fluxo-events.yaml` + `config/fluxo_events/`  
Prior art SVG: `build_flow_svg` (ship `fluxo-grafo-visual-agentes`)

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.
> Orthografia PT-BR: sempre **fluxo** (com **x**). Nunca **flujo** (com **j**) em
> artefatos do pacote.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **a** (só metadados — sem PII/prompts/secrets)
- Sem agent “fluxo officer” — estender emit/render/CLI + wiring SDD/Dev existentes
- Fluxo-events = **telemetria fail-soft**; evidence-gate = **hard**; agent-policies =
  freio Bash — kernels **não** unificados
- `/validar` permanece suite global; live **não** substitui STATUS.md / scorecard /
  evidence-gate
- Extensão do kernel existente — **não** fork / mini-app / SSE / Canvas
- Honesty §1.3: telemetria local ≠ fidelidade perfeita; emit/stack omitíveis/forjáveis
- SLA **best effort** — sem alvo numérico
- Append e stack **best-effort sem mutex** (corrida aceita)
- Cap log **2 MiB** rotate keep-tail + truncate **N=100** no ship / `EXIT_COMPLETE`
- Dual-map SDD / Dev Loop **inalterado** em semântica (`dev-loop-*` → `dev_loop_map`)
- `version: 1` **aditivo** (sem bump breaking)
- Stack em `projetos/{slug}/fluxo/stack.json` — **não versionada** (gitignore)
- Parent explícito = fonte de verdade; senão topo da stack; omitido = órfão
- Nós do SVG causal: `phase_enter` (raiz) + `agent_enter` + `task_enter`;
  `*_exit` / `ship_truncate` só na timeline
- Dois SVGs no `live.html` (canônico + causal); offline; sem JS obrigatório
- Guardrail PT-BR mecânico no pacote (`test_naming_ptbr.py`)
- Espelho `.claude` ↔ `.cursor` na mesma sessão de promoção
- Commit/push só com acordo explícito

## Naming fechado no architect (não bloqueava; alinhado ao padrão)

| Item | Escolha | Motivo |
|---|---|---|
| Contrato | `fluxo-events.yaml` — `version: 1` aditivo (docs/schema dos campos) | Grill #10; sem fork |
| Pacote engine | `config/fluxo_events/` | Kernel ADR-005 |
| Módulo stack | `config/fluxo_events/stack.py` (novo) | Grill #3/#7; fail-soft |
| Path stack | `projetos/{slug}/fluxo/stack.json` | Grill #7; local por slug |
| Gitignore | `**/fluxo/stack.json` (ou equivalente no `.gitignore` raiz) | Não versionar |
| Campos novos | `event_id`, `run_id`, `parent_event_id` | Grill #1; UUID v4 |
| ALLOWED_KEYS | estender frozenset em `emit.py` | Baseline + 3 keys |
| Geração UUID | emit gera `event_id` (sempre se omitido) e `run_id` (se omitido) | Grill #2/#5 |
| Override | CLI `--run-id` / `--parent-event-id` | Grill #2/#3 |
| Parent ordem | explícito > topo stack > omitido (órfão) | Grill #3 |
| Render canônico | `build_flow_svg` (existente; semântica intacta) | Prior art visual |
| Render causal | `build_causal_svg(events) -> str` (novo, puro) | Grill #4/#9 |
| HTML | dois blocos SVG em `build_html` / `live.html` | Grill #4 |
| `data-testid` canônico | manter `fluxograma` (ou legado) | Regressão |
| `data-testid` causal | `fluxograma-causal` | Assert estável AC7 |
| Truncate visual ID | primeiros 8 chars do UUID + `…` (SHOULD) | Grill #5 SHOULD |
| Event types | **reusar** lista atual — sem tipos novos | Dual-map intacto |
| CLI superfície | `python -m config.fluxo_events emit\|render\|truncate` | Sem CLI nova |
| Flags emit | `--run-id`, `--parent-event-id` | AC11 |
| Agent officer | **nenhum** | Gate de redundância |
| Docs SHOULD | `docs/fluxo-events-cheatsheet.md` + addendum ADR-005 | PRD SHOULD |
| Orthografia | sempre **fluxo** (x) | PT-BR; nunca flu+j+o |
| Seed install | foundation fluxo-events KEEP; propagar contrato no re-install | Sem categoria nova |

### Schema de evento (aditivo — metadados only)

```yaml
# Existentes (inalterados)
event_type: phase_enter | phase_exit | agent_enter | agent_exit | task_enter | task_exit | ship_truncate
ts: <ISO-8601>
phase: <int>                 # índice do mapa ativo (SDD 0–4 ou Dev 0–6)
agent: <str>
task_id: <str>               # opcional
slug: <str>
source: claude | cursor | cli  # opcional

# Novos (opcionais no load; emits novos preenchem)
event_id: <UUID v4>          # gerado no emit se omitido
run_id: <UUID v4>            # sessão/slug; auto se omitido; override ok
parent_event_id: <UUID|null> # explícito > stack; omitido = órfão
```

**Proibido:** prompt, message, content, diff, secret, password, token, api_key, CPF,
email, telefone, connection string (FORBIDDEN_KEY_PATTERNS existentes).

### Layout lógico (por slug)

```text
projetos/{slug}/fluxo/
├── events.jsonl      # append JSONL (versionado ou não — política atual do projeto)
├── live.html         # render: SVG canônico + SVG causal + timeline
└── stack.json        # NÃO versionar (gitignore); fail-soft
```

Espelho de paths de projeto sob `.claude/projetos/` e `.cursor/projetos/` quando dual-tree.

### Semântica da stack (contrato de comportamento)

```text
stack.json: lista de event_id (topo = parent implícito)
  agent_enter / task_enter / phase_enter:
    resolve parent → append event_id ao topo (best-effort)
  agent_exit / task_exit / phase_exit:
    pop do topo se bater com event_id conhecido (best-effort; sem mutex)
  FS erro → warning stderr; emit do evento segue (órfão ok)
```

Detalhe fino de push/pop fica no build; testes cobrem comportamento externo
(explícito > stack; órfão; fail-soft).

### SVG causal (contrato de nós)

```text
Incluir no grafo:  phase_enter (raiz) · agent_enter · task_enter
Excluir do grafo:  phase_exit · agent_exit · task_exit · ship_truncate
Arestas: parent_event_id → event_id (órfãos = nós soltos / sem aresta de entrada)
Labels: agent|task + ID truncado (SHOULD)
```

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Campos UUID aditivos | `emit.py` ALLOWED_KEYS + geração UUID | validação | CLI + agents |
| CLI flags | `config/fluxo_events/__main__.py` (ou CLI emit) | ferramentas | agents / scripts |
| Stack fail-soft | `config/fluxo_events/stack.py` + `stack.json` | execução | emit |
| Gitignore stack | `.gitignore` (`**/fluxo/stack.json`) | estado | git |
| SVG canônico | `build_flow_svg` (inalterado) | estado | humano |
| SVG causal | `build_causal_svg` | estado | humano + testes |
| Dois blocos HTML | `build_html` / `render_live` | estado | `/fluxo-live` |
| Wiring SDD+Dev | agents/commands (+ espelho `.cursor/`) | execução | SDD / `/dev` |
| Testes | `tests/fluxo_events/` (emit/stack/causal/CLI/legado) | validação | `/validar` |
| Cheatsheet | `docs/fluxo-events-cheatsheet.md` | estado | agente JIT |
| ADR addendum | `docs/adr/005-kernel-fluxo-events.md` | estado | humano + agent |
| Install | foundation re-copy contrato se docs no YAML mudarem | ferramentas | filhos |
| Contagem/docs | `CLAUDE.md` / `AGENTS.md` no ship (`/sync-context`) | estado | próximo agente |
| Ortogonalidade | cheatsheet cross-link | estado | SI + maintainer |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs listados abaixo — andaime real no `harness-build` após
`/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent “fluxo officer” / telemetria dedicada (gate de redundância)

### Agents / skills / commands / docs a estender (build)

**Kernel (MUST)**
- `fluxo-events.yaml` — documentar campos aditivos; manter `version: 1`
- `config/fluxo_events/emit.py` — ALLOWED_KEYS + UUID `event_id`/`run_id` + parent resolve
- `config/fluxo_events/stack.py` — load/save/push/pop fail-soft de `stack.json`
- `config/fluxo_events/render.py` — `build_causal_svg` + dois blocos no HTML
- CLI — `--run-id` / `--parent-event-id`
- `.gitignore` — `**/fluxo/stack.json` (ou path equivalente)
- `tests/fluxo_events/` — AC1–AC20 (emit IDs, stack, load legado, dois SVGs, nós causal,
  CLI, fail-soft, dual-map regressão, wiring presença)

**Wiring SDD + Dev Loop (MUST)**
- Agents/commands SDD (brainstorm→ship) — documentar/one-liner emit com run/parent + stack
- `prompt-crafter`, `dev-loop-executor`, `/dev`, `DEV-LOOP.md` — mesmo contrato fail-soft;
  dry-run **continua sem emit**
- Espelho `.cursor/` na mesma sessão de promoção

**Docs (SHOULD)**
- `docs/fluxo-events-cheatsheet.md` — campos novos, stack, dois SVGs, §1.3
- ADR-005 **addendum** — “Grafo causal real” (fecha o “fora deste ship” do addendum visual)

**Install / sync**
- Foundation fluxo-events already-on: se o YAML ganhar seção de schema docs, propagar no
  re-install; seed KEEP inalterado em stubs `fluxo/`
- Sem categoria nova; sem agent no `stack_map`
- `CLAUDE.md` / `AGENTS.md` no `/sync-context` do ship se a tabela “onde fica o quê”
  precisar citar stack/causal SVG

### Rules
- Sem rule nova `fluxo-events.md` obrigatória; cheatsheet basta
- **Não** tornar emit/stack bloqueante na DoD (fail soft ≠ evidence-gate)
- Ponte SI: nunca prompt/PII/secret no event log

### KBs
- **Nenhum** KB de domínio novo obrigatório neste ship

### Skills
- **Nenhuma** skill MUST nova de telemetria

## Ortogonalidade (obrigatória)

| Kernel / artefato | Concern | Relação com este ship |
|---|---|---|
| evidence-gate | Aceite hard por task | **Ortogonal** — telemetria ≠ manifesto |
| agent-policies | Freio Bash | **Ortogonal** |
| `/validar` | Suite global | Inclui novos testes `tests/fluxo_events/` |
| STATUS.md / scorecard | Checklist / métricas | Complementar; não substituídos |
| Dual-map SDD/Dev | Mapas de fase | Semântica **intacta**; só edges reais no SVG causal |
| `build_flow_svg` | Mapa canônico previsto | Preservado; causal é bloco adicional |

Cross-link: “telemetria ≠ aceite ≠ Bash deny”; grafo causal = execução real, não DoD.

## O que NÃO entra neste ship

- SSE / WebSocket / Canvas MUST
- Toggle JS canônico↔causal
- Mutex/lock no append ou na stack
- Backfill/migrar IDs em `events.jsonl` históricos
- Unificar com evidence-gate / agent-policies
- Persistência cross-machine da stack
- Key vault / pacote E
- Alvo de latência numérico; fork do kernel
- Agent “fluxo officer” / skill MUST nova
- Mudança semântica do dual-map
- Harness de produto-filho (agents/rules/KBs de app)
- `PRD.md` na raiz do canônico
- Tag `prod-*` / Fase 2 git hygiene

## Decisões contestáveis (ADR na implementação)

1. Estender o **mesmo** kernel com campos aditivos (não fork) — um painel, dois SVGs
2. Parent explícito > stack local — callers controlam; stack é conveniência fail-soft
3. `stack.json` não versionado — estado de sessão; §1.3 omitível
4. Nós causal só `*_enter` (+ `phase_enter` raiz) — exits/truncate não viram grafo
5. `version: 1` aditivo — sem breaking bump; load legado órfão ok
6. Sem mutex — corrida aceita (WON'T explícito)
7. Sem agent officer / skill MUST — wiring + cheatsheet bastam
8. Truncate visual de UUID no SVG (SHOULD) — legibilidade sem mudar schema

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local `feat/fluxo-grafo-causal`
- Working tree: artefatos untracked em `projetos/fluxo-grafo-causal/`
- Sem commit/push neste passo
- Sem implementação de código neste passo (só plano de harness)
- Adversarial judge define: **(b)** pulado (2026-08-18)
- Adversarial judge PRD: **(b)** pulado (2026-08-18) — sem `02b-judge.md`

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (AC1–AC20 / FRs do `02-prd.md`)
2. `harness-build` — implementar com `/validar` + `revisor-codigo` (sem agent officer)
3. Ao fechar: `/sync-context` + delivery records + evidence-gate das tasks (**ortogonal** à
   telemetria) + dogfood opcional no slug `fluxo-grafo-causal`
