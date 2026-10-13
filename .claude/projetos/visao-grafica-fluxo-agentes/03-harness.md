# Visão Gráfica do Fluxo de Agentes — Decisões de Harness

Slug: `visao-grafica-fluxo-agentes`  
Branch: `feat/visao-grafica-fluxo-agentes`  
Data: 2026-08-13  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Lacunas de naming fechadas no architect (sem entrevista): ver seção abaixo  
Mockup: `assets/mockup-visao-grafica-fluxo-live.png`

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **a** (só metadados de processo — sem PII/prompts/secrets)
- Sem agent “fluxo officer” / telemetria dedicada no canônico — estender agents/skills SDD existentes
- Fluxo-events = **telemetria fail-soft**; evidence-gate = **hard** (aceite); agent-policies = freio Bash — kernels **não** unificados
- `/validar` permanece suite global; live **não** substitui STATUS.md / scorecard / entregas
- Install foundation **sempre-on** (contrato + CLI + template `fluxo/` + wiring agents)
- Honesty §1.3: telemetria local ≠ fidelidade perfeita; emit omitível/forjável; sem Edit policies
- SLA **best effort** — sem alvo numérico no contrato (G1-c)
- Append **best-effort sem lock** (G2-a)
- Cap log **2 MiB** com **rotate manter tail** + warning soft (G3-a) — **não** fail hard no cap
- Ship: truncar para últimos **N=100** eventos + re-render (G4-b)
- Live em **todas** as fases SDD 0–4; mapa mostra **todos** os agents; live destaca o **ativo**
- Sem SSE MUST; híbrido emit→render HTML; `http.server` opcional
- Espelho `.claude` ↔ `.cursor` na mesma sessão de promoção (artefatos de projeto + wiring)
- Commit/push só com acordo explícito

## Naming fechado no architect (não bloqueava; alinhado ao padrão)

| Item | Escolha | Motivo |
|---|---|---|
| Contrato | `fluxo-events.yaml` (raiz) | Espelha `git-hygiene.yaml` / `agent-policies.yaml` / `evidence-gate.yaml` |
| Pacote engine | `config/fluxo_events/` (`contract.py`, `yaml_loader.py`, emit, render, truncate, `__main__`) | Padrão `git_hygiene` / `agent_policies` / `evidence_gate` |
| CLI | `python -m config.fluxo_events emit\|render\|truncate` | Espelha kernels existentes; truncate explícito no ship |
| Pasta por projeto | `.claude/projetos/{slug}/fluxo/` (+ espelho `.cursor/projetos/.../fluxo/`) | Grill decisão 5 / PRD FR4 |
| Event log | `fluxo/events.jsonl` (1 JSON/linha) | Fonte live; append best-effort |
| UI live | `fluxo/live.html` (LWW a cada render) | Híbrido sem SSE; mockup como referência visual |
| `event_type` | `phase_enter` · `phase_exit` · `agent_enter` · `agent_exit` · `task_enter` · `task_exit` · `ship_truncate` | Naming cravado no architect (PRD sugeria start/end — unificado em enter/exit) |
| `emit` | append JSONL + **auto-render default**; opt-out `--no-render` | Path feliz = 1 comando atualiza painel |
| `render` | regenera `live.html` a partir do mapa estrutural + eventos | Mapa completo mesmo com log vazio |
| `truncate` | `--keep N` default **100** (ship); emite `ship_truncate` + re-render | G4-b |
| Cap no contrato | `limits.max_events_bytes: 2097152` (2 MiB); rotate keep-tail + soft warning | G3-a (≠ evidence-gate fail-on-exceed) |
| SLA | **ausente** no yaml (best effort documentado) | G1-c |
| Concorrência | append sem lock file | G2-a |
| Seed / SCHEMA | `config/fluxo_events/templates/fluxo/` → SCHEMA.md + `events.jsonl` vazio + stub `live.html` (`seed: true` KEEP no filho sob `.harness/fluxo-events/`) | Como policies / evidence-gate |
| Docs SHOULD | `docs/fluxo-events-cheatsheet.md` + ADR em `docs/adr/` | Como kernels irmãos |
| Command SHOULD | `.claude/commands/fluxo-live.md` (+ `.cursor/commands/`) | Atalho docs → emit/render/http.server; não substitui o módulo |
| Testes | `tests/fluxo_events/` (+ fixtures sob `tests/fluxo_events/fixtures/`) | Espelha `tests/evidence_gate/` |
| Cross-link | cheatsheet: “telemetria ≠ aceite ≠ Bash deny” | Ortogonalidade FR8 |
| Mockup | `assets/mockup-visao-grafica-fluxo-live.png` | Aceite visual de referência |

### Layout lógico da pasta `fluxo/` (por projeto)

```text
.claude/projetos/{slug}/fluxo/
├── events.jsonl    # append-only operacional (rotate G3 / truncate G4)
└── live.html       # regenerado por render (LWW); mapa SDD 0–4 + ativo + timeline
```

Espelho idêntico sob `.cursor/projetos/{slug}/fluxo/` quando dual-tree.

### Schema de evento (mínimo — metadados only)

```yaml
# Uma linha JSON em events.jsonl
event_type: phase_enter | phase_exit | agent_enter | agent_exit | task_enter | task_exit | ship_truncate
ts: <ISO-8601>
phase: 0 | 1 | 2 | 3 | 4   # ou slug canônico IDEIA|REQUISITOS|PRD_HARNESS|IMPLEMENTAR|ENCERRAR
agent: <nome canônico>      # ex.: harness-build
task_id: <opcional>         # fase Implementar quando conhecido
slug: <projeto-slug>
source: claude | cursor | cli   # opcional
```

**Proibido:** prompt, conteúdo de mensagem, diff, secret, PII, connection string.

### Mapa SDD estrutural (obrigatório no contrato + render)

```
Fase 0 IDEIA:        harness-brainstorm
Fase 1 REQUISITOS:   grill-me, harness-define
Fase 2 PRD+HARNESS:  harness-design, to-prd, harness-architect
Fase 3 IMPLEMENTAR:  to-tasks, harness-build, revisor-codigo
Fase 4 ENCERRAR:     harness-ship, /scorecard
```

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Contrato schema/cap/N/mapa 0–4 | `fluxo-events.yaml` (raiz) | validação | loader + CI + CLI |
| Engine load/emit/render/truncate | `config/fluxo_events/` | validação | CLI + agents + install |
| CLI emit\|render\|truncate | `python -m config.fluxo_events` | ferramentas | agents SDD / ship / maintainer |
| Event log + live HTML | `projetos/{slug}/fluxo/` (+ espelho) | estado | humano + browser |
| Auto-render no emit | flag default; `--no-render` | ferramentas | agents |
| Cap 2 MiB rotate tail | contrato + engine | validação | emit path |
| Truncate N=100 no ship | CLI truncate + wiring `harness-ship` | validação | agente ship |
| Wiring enter/exit fail-soft | agents/skills/commands SDD 0–4 | execução | todo agent SDD |
| Install foundation | `install-harness` / `stack_map` + seed `.harness/fluxo-events/` | ferramentas | `/install-harness` |
| Seed SCHEMA + stubs | `config/fluxo_events/templates/fluxo/` | ferramentas | install + filho |
| Cheatsheet + `/fluxo-live` | `docs/fluxo-events-cheatsheet.md` + command SHOULD | estado | agente JIT |
| Testes kernel | `tests/fluxo_events/` | validação | `/validar` |
| Contagem/docs canônico | `CLAUDE.md` / `AGENTS.md` no ship (`/sync-context`) | estado | próximo agente |
| ADR | `docs/adr/` (kernel fluxo-events + fail-soft/cap/truncate) na implementação | estado | humano + agent |
| Cross-link evidence-gate/policies | cheatsheet (sem unificar) | estado | SI + maintainer |
| STATUS / scorecard intactos | sem substituição | estado | checklist / métricas pós-fato |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs listados acima — andaime real no `harness-build` após
`/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent “fluxo officer” / telemetria dedicada no canônico (gate de redundância —
  responsabilidades cabem nos agents SDD existentes + CLI)

### Agents / skills / commands a estender (build)

**Fase 0 — IDEIA**
- `harness-brainstorm` — emit `phase_enter`/`agent_enter` no início; `agent_exit`/`phase_exit` ao fechar ideia

**Fase 1 — REQUISITOS**
- skill `grill-me` — emit enter/exit
- `harness-define` — emit enter/exit (+ phase transitions se aplicável)

**Fase 2 — PRD+HARNESS**
- `harness-design` — emit enter/exit
- skill `to-prd` — emit enter/exit
- skill `harness-architect` (instruções) — emit enter/exit quando invocada no fluxo

**Fase 3 — IMPLEMENTAR**
- skill `to-tasks` — emit enter/exit
- `harness-build` — emit enter/exit + `task_enter`/`task_exit` com `task_id` quando conhecido
- `revisor-codigo` — emit enter/exit (soft review; **não** valida telemetria como aceite)

**Fase 4 — ENCERRAR**
- `harness-ship` — emit enter/exit + **`truncate --keep 100`** + re-render antes/ao fechar
- command `/scorecard` — emit enter/exit (opcional se for só leitura; preferível para timeline completa)

**Install / foundation**
- skill `install-harness` / `stack_map` — foundation always-on: contrato + engine + wiring + seed KEEP

**Docs / atalho (SHOULD)**
- command `/fluxo-live` — docs → render / abrir `live.html` / `http.server` opcional
- sem skill MUST nova no MVP (playbook = cheatsheet)

### Rules
- Sem rule nova `fluxo-events.md` obrigatória; cheatsheet em `docs/` (SHOULD)
- Ponte curta opcional em `seguranca` (nunca prompt/PII/secret em event log) — SI a
- **Não** alterar DoD para tornar emit bloqueante (fail soft ≠ evidence-gate)

### KBs
- **Nenhum** KB de domínio novo obrigatório neste ship (framework de telemetria, não stack de produto)

### Kernel / seed / testes (a criar no build)
- `fluxo-events.yaml` + `config/fluxo_events/` (emit auto-render; render; truncate)
- Seed `config/fluxo_events/templates/fluxo/` → `.harness/fluxo-events/` (SCHEMA + stubs, KEEP)
- Layout `fluxo/events.jsonl` + `live.html`
- Testes `tests/fluxo_events/` (emit, render, rotate, truncate, fail-soft, install fixture, SI grep)
- Dogfood: wiring no canônico; uso real neste/outros ships SDD

## Ortogonalidade (obrigatória)

| Kernel | Concern | Relação com fluxo-events |
|---|---|---|
| evidence-gate | Prova mecânica de aceite por task (hard) | **Ortogonal** — telemetria mid-run ≠ manifesto/check |
| agent-policies | Freio Bash deny/ask | **Ortogonal** — Bash deny ≠ progresso SDD |
| `/validar` | Suite global ruff+mypy+pytest (+ DE) | Permanece; testes `tests/fluxo_events/` entram no gate |
| STATUS.md | Checklist prosa de fase | Complementar; **não** substituído |
| `/scorecard` + `entregas.jsonl` | Métricas pós-fato | Complementar; **não** substituído |

Cross-link em cheatsheet/ADR: “telemetria ≠ aceite ≠ Bash deny”.

## O que NÃO entra neste ship

- SSE / WebSocket como MUST
- Canvas Cursor como MUST
- Dev Loop no mapa MVP (Fase 2 / COULD)
- Prompts, diffs, PII ou secrets no event log
- Unificar / misturar com evidence-gate ou agent-policies
- Substituir STATUS.md / scorecard / entregas
- Key vault / pacote E
- Alvo de latência numérico; mutex de append
- Fail hard no cap 2 MiB (aqui é rotate soft — ≠ evidence-gate)
- Hooks Session/Task nativos do IDE como MUST
- Agent dedicado “fluxo officer”
- Tag `prod-*` / Fase 2 git hygiene
- Skill MUST `fluxo-events` (cheatsheet basta no MVP)
- `PRD.md` na raiz do canônico

## Decisões contestáveis (ADR na implementação)

1. Kernel **separado** `fluxo-events` (não fundir com evidence-gate, agent-policies ou `/validar`) —
   telemetria de processo ≠ prova de aceite ≠ freio Bash ≠ suite global
2. Install **foundation always-on** (não categoria opt-in) — painel live default nos filhos
3. Live **sem SSE**: emit→render HTML + http.server opcional — dual-tree em disco, IDE-agnóstico
4. Cap **2 MiB** com **rotate keep-tail** (não fail-on-exceed) — telemetria degradável ≠ prova truncada inválida
5. Append **sem lock** + fail soft — SDD nunca bloqueia por telemetria
6. Ship truncate **N=100** + evento `ship_truncate` — retenção bounded no fechamento
7. `emit` **auto-render** default (`--no-render` opt-out) — path feliz de um comando
8. Sem skill MUST no MVP (cheatsheet + wiring agents) — evitar proliferação
9. Seed sob `config/fluxo_events/templates/fluxo/` → `.harness/fluxo-events/` — pacote dono do contrato

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local `feat/visao-grafica-fluxo-agentes`
- Working tree: artefatos untracked em `projetos/visao-grafica-fluxo-agentes/`
- Sem commit/push neste passo
- Adversarial judge define: **(b)** pulado (2026-08-13)
- Adversarial judge PRD: **(b)** pulado (2026-08-13) — sem `02b-judge.md`

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (tracer bullets T1–T8 do PRD)
2. `harness-build` — implementar com `/validar` + `revisor-codigo`
3. Ao fechar: `/sync-context` + delivery record em `metrics/entregas.jsonl` (com
   `evidencias_ref` via evidence-gate — **ortogonal** à telemetria fluxo) + truncate N=100
   no path de ship
