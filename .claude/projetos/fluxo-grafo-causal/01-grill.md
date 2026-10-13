# Fluxo — Grafo Causal Real — Grill & Requisitos

Slug: `fluxo-grafo-causal`  
Branch: `feat/fluxo-grafo-causal`  
Data: 2026-08-18  
SI: **a** · Tipo: **e** (evolução do canônico)  
Fontes: `00-ideia.md` · kernel ADR-005 + fluxograma SVG (ship `fluxo-grafo-visual-agentes`)  
Define: 2026-08-18 (`harness-define`)

> Orthografia PT-BR: **fluxo** (x), nunca **flujo** (j).  
> Decisões 1–11 fechadas no `/grill-me` — não reabrir.  
> Judge define: **pulado (b)** — sem `01b-judge.md`.

## Contexto (da sessão /grill-me)

### Problema

O painel `live.html` mostra o fluxo **canônico previsto** (mapa do contrato). Não há
grafo **causal de execução** (quem chamou quem). Sem identidade de evento / parent,
o SVG não consegue desenhar arestas reais entre agentes/fases que de fato rodaram.

### Usuários

| Persona | Pain / necessidade |
|---|---|
| **Mantenedor do canônico** | Evoluir `fluxo-events` sem fork; gates pytest + ADR; install propaga seed KEEP |
| **Agents SDD / Dev Loop** | Emitir metadados com parent/run sem bloquear o fluxo (fail-soft) |
| **Humano no painel** | Ver, offline, o mapa canônico **e** o grafo causal real da execução do slug |

### Objetivos (MoSCoW)

**MUST:**
- Schema aditivo: `event_id` + `run_id` + `parent_event_id` (UUID v4; opcionais no load de eventos antigos)
- `run_id` por sessão/slug; UUID auto se omitido; override explícito ok
- Parent: explícito = fonte de verdade + stack fail-soft (`stack.json` local)
- Dois SVGs no `live.html`: canônico + causal (offline; sem JS obrigatório)
- Nós do SVG causal: `agent_enter` (+ `task_enter`) + `phase_enter` como raiz; exits/truncate só timeline
- Wiring: kernel + agents/commands SDD + Dev Loop (+ espelho `.cursor/`)
- `version: 1` aditivo + ADR-005 addendum
- Fail-soft; metadados only; dual-map intacto; cap 2 MiB / truncate N=100

**SHOULD:**
- Truncar IDs visualmente no SVG (legibilidade)
- Docs/cheatsheet atualizados com os campos novos e o stack

**COULD:**
- Toggle JS canônico↔causal (explícito WON'T neste ship; futuro)

**WON'T:**
- SSE / WebSocket / Canvas MUST
- Toggle JS canônico↔causal neste ship
- Mutex/lock no append ou na stack
- Backfill/migrar IDs em `events.jsonl` históricos (órfãos ok)
- Unificar com evidence-gate
- Persistência cross-machine da stack

### Out of Scope

Tudo listado em WON'T acima; também: unificação com evidence-gate/agent-policies; fork do
kernel; mudança semântica do dual-map SDD/Dev Loop; SLA numérico de latência do painel.

### Restrições

- Extensão do kernel existente — **não** fork
- Fail-soft: emit/render/stack nunca bloqueiam SDD / `/dev`
- Só metadados — sem prompt / PII / secret
- Cap 2 MiB (rotate keep-tail) e truncate N=100 no ship/EXIT_COMPLETE
- Sem SLA numérico — best effort
- Stack em `projetos/{slug}/fluxo/stack.json` — **não versionada** (gitignore)
- §1.3 honesty: telemetria local/forjável; stack omitível; painel pode ficar stale
- Soft-block git: fetch Azure 403 neste ambiente — não fingir sync; sem commit/push sem acordo

## Decisões (1–11) — fechadas no grill

| # | Tema | Escolha | Notas |
|---|---|---|---|
| 1 | Identidade | **b** `event_id` + `run_id` + `parent_event_id` | Parent aponta para `event_id` |
| 2 | Escopo `run_id` | **d** sessão/slug + UUID auto se omitido; override ok | Do phase 0 ao ship / EXIT_COMPLETE |
| 3 | Preenchimento parent | **d** explícito + stack fail-soft | Explícito = fonte de verdade |
| 4 | UX painel | **b** dois SVGs: canônico + causal | Offline; sem JS obrigatório |
| 5 | Formato IDs | **a** UUID v4 (ambos) | Truncar visualmente no SVG |
| 6 | Wiring | **b** kernel + SDD + Dev Loop | Docs agents/commands + espelho |
| 7 | Stack persistência | **d** `projetos/{slug}/fluxo/stack.json` não versionado | Fail-soft se FS falhar |
| 8 | WON'T | **a** tabela aceita | Ver MoSCoW WON'T |
| 9 | Nós do SVG causal | **d** `agent_enter` (+ `task_enter`) + `phase_enter` como raiz | Exits/truncate só timeline |
| 10 | Version contrato | **a** manter `version: 1` aditivo | ADR-005 addendum |
| 11 | Fechar grill | **a** → `harness-define` | Judge oferecido no define |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- Provedor: N/A
- N/A: **sem key vault** — SI nível **a**; telemetria só metadados locais em `projetos/{slug}/fluxo/`

## Especificações implícitas detectadas

| Lente | Registro |
|---|---|
| **I1** Falha de dependência (FS stack/emit) | Fail-soft: warning stderr; nunca bloqueia SDD/`/dev` (já no grill) |
| **I2** Concorrência (stack) | Best-effort **sem mutex** — WON'T explícito; corrida possível, aceita |
| **I3** Idempotência | Cada emit gera **novo** `event_id`; sem dedup / sem replay-id |
| **I4** Auth / multi-tenant | **N/A** — artefato local por slug; sem auth de painel |
| **I5** PII / dados sensíveis | SI **a**; IDs UUID não são PII; sem prompts/secrets nos eventos |
| **I6** Abuso / limites | Cap **2 MiB** herdado (rotate keep-tail); sem rate-limit novo |
| **I7** Auditoria | Trilha = `events.jsonl` (+ audit de truncate se aplicável); metadados only |
| **I8** Erro UX | Warning stderr; painel pode ficar stale (§1.3); sem retry automático de UI |
| **I9** Ciclo de vida | Truncate N=100 no ship/EXIT_COMPLETE; stack não versionada; órfãos ok (sem backfill) |
| **I10** Terceiros / contrato externo | **N/A** — sem integração externa; só kernel local |

## Esboço de contrato (aditivo)

```text
ALLOWED / payload (novos, opcionais no load):
  event_id: UUID v4          # gerado no emit se omitido (emits novos)
  run_id: UUID v4            # gerado/persistido por sessão se omitido
  parent_event_id: UUID|null # explícito ou topo da stack; omitido = órfão

Stack: .claude/projetos/{slug}/fluxo/stack.json  # gitignore / não versionar
       (.cursor/projetos/{slug}/fluxo/ espelho de paths de projeto)
```

## Critérios de sucesso mensuráveis

- **pytest** `tests/fluxo_events/`: emit gera `event_id`/`run_id`; parent explícito e via stack; load aceita eventos antigos sem os campos; fail-soft de stack/FS
- **HTML/render**: `live.html` contém **dois** SVGs (canônico + causal); nós causal = enters (+ `phase_enter` raiz); exits/truncate ausentes do grafo causal
- **IDs no emit**: novos emits trazem UUID v4; override de `run_id`/`parent_event_id` respeitado
- **SLA**: best effort / **sem alvo numérico** (herdado do kernel)

## Invariantes que se mantêm

- Fail-soft (emit/render/stack nunca bloqueiam SDD/`/dev`)
- Só metadados — sem prompt/PII/secret
- Ortogonal a evidence-gate e agent-policies
- Extensão do kernel — **não** fork
- Dual-map SDD / Dev Loop inalterado em semântica de fase
- Cap 2 MiB / truncate N=100 / sem SLA numérico
- §1.3 honesty: telemetria local/forjável; stack omitível

## Judge define

- Status: **pulado (b)** — sem `01b-judge.md`

## Próximo passo

Rode `harness-design` para gerar o PRD e montar o harness.
