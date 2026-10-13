# PRD — Evidências e Testes Obrigatórios (evidence-gate)

Slug: `evidencias-testes-obrigatorios`  
Repo: Agent Harness Canônico (framework — **não** produto)  
Branch: `feat/evidencias-testes-obrigatorios`  
Data: 2026-08-13  
Tipo: **e** — evolução do harness canônico  
SI: **a** (sem dados sensíveis — logs de gate, paths, exit codes)  
Fontes: `00-ideia.md`, `00b-codebase.md`, `01-grill.md` (decisões 1–15 + G1–G4 fechados)

> Decisões do grill/define estão **fechadas** — este PRD as materializa; não reabre a matriz.

---

## Problem Statement

No ciclo harness (brainstorm → define → design → build → ship), “done” e critérios de
aceite ainda dependem de **claims em prosa**: DoD, test-first no `harness-build`,
`tested by` nas tasks, veredito do `revisor-codigo`, e campos de `metrics/entregas.jsonl`
preenchidos pelo próprio agente. O gate mecânico `/validar` (ruff + mypy + pytest) só
vale se alguém o executar; o Stop do Claude é parcial e condicionado a `backend/`/`src/`
(no canônico vira no-op); o Cursor não tem Stop equivalente de testes.

Não existe pasta `evidencias/`, manifesto que ligue critério → path(s) de teste → comando
→ exit_code → log, nem validador que bloqueie fechar task ou ship sem prova verificável.
O sintoma é alucinação de entrega e scorecard otimista. O problema real é a ausência de
um **kernel de framework** (contrato + engine `collect|check` + wiring DoD/agents +
install foundation) que torne a Definição de Pronto **auditável por artefato**, não por
texto do LLM.

§1.3 permanece: sem Edit policies / branch protection, nenhum gate impede de fato;
agente pode forjar manifesto à mão. O ship entrega o melhor freio **local e dogfoodável**
possível, com honesty explícita — não bloqueio server-side.

---

## Solution

Evoluir o canônico com um **kernel evidence-gate**, paralelo a `agent-policies` e ao
kernel DE (não unificado; concern distinto):

1. **Contrato** `evidence-gate.yaml` na raiz — schema do manifesto, regras de `check`,
   cap de log **2 MiB**, política de falha se exceder, alvo de latência do `collect`.
2. **Engine** `config/evidence_gate/` — load tipado + CLI
   `python -m config.evidence_gate collect|check`.
3. **`collect` executa** o comando referenciado, grava log + `exit_code`; **não** aceita
   só claim textual.
4. **`check` valida** manifesto (critério → ≥1 teste, comando, exit 0, path de log
   existente, tamanho ≤ cap) e o link `evidencias_ref` no delivery record.
5. **Pasta** `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/`) com manifesto
   por task, logs e trilha **append-only** de auditoria (`audit.jsonl` ou equivalente).
6. **`evidencias_ref` obrigatório** em `metrics/entregas.jsonl` apontando o manifesto.
7. **Bloqueio** no fechamento de **cada task** e **revalidação no ship**.
8. **Install foundation always-on** — schema + CLI + wiring de agents/commands/DoD nos
   filhos (mesmo padrão de propagação do freio, sem misturar com agent-policies).
9. **`revisor-codigo` ortogonal** — soft (cobertura/qualidade); evidence-gate = hard.
10. **`/validar` permanece** (suite global); evidence-gate prova aceite **por task** —
    não substitui o gate.
11. **G1–G4:** alvo `collect` ≤ **2×** o comando (sem hard timeout no yaml); concorrência
    **last-write-wins** na prova atual; cap **2 MiB** com **fail** se exceder (sem prova
    truncada silenciosa); auditoria **append-only** extra.
12. **Testes** em `tests/evidence_gate/` + fixture de install; E2E IDE fora do CI
    obrigatório.

---

## Goals (MoSCoW)

### MUST

- Contrato `evidence-gate.yaml` + engine `config/evidence_gate/` + CLI `collect|check`
- Manifesto por task: critério → path(s) de teste + comando + exit_code + path de log
- Pasta `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/`)
- Campo `evidencias_ref` obrigatório em `metrics/entregas.jsonl`
- Cada critério com ≥1 teste unitário no manifesto (demo sem teste = justificativa +
  marcador humano explícito)
- `collect` **executa** o comando e grava artefato; `check` valida
- Bloqueio no fechamento de **cada task** + **revalidação no ship**
- Install foundation always-on (schema + CLI + wiring agents/commands/DoD)
- `revisor-codigo` ortogonal (soft); evidence-gate = hard
- Atualizar DoD / harness-build / harness-ship / to-tasks / metrics schema
- Testes do próprio kernel (`tests/evidence_gate/`)
- Espelho `.claude` ↔ `.cursor` nos artefatos de projeto
- Cap de log **2 MiB**; `collect` **falha** se exceder (não truncar silenciosamente)
- Alvo `collect` ≤ **2×** o comando — **sem** hard timeout absoluto no yaml (G1)
- Concorrência **last-write-wins** na prova atual (G2)
- Trilha **append-only** de auditoria além de manifesto/log/ref (G4)

### SHOULD

- Template de manifesto + `SCHEMA.md` no seed/install
- Comando `/evidencias` (atalho docs) além da CLI
- Cheatsheet 1 página (`docs/evidence-gate-cheatsheet.md` ou equivalente)
- ADR do kernel evidence-gate (`docs/adr/`)
- Redaction leve se log parecer secret (heurística; SI a)

### COULD

- Hooks Stop dual Claude/Cursor (Fase 2)
- Screenshots/PDF para tasks UI
- Dashboard/portal de evidências
- Métricas agregadas de cobertura de evidência no `/scorecard`

### WON'T (neste ship)

- Hooks Stop dual obrigatórios no MVP
- Portal UI / dashboard
- E2E IDE obrigatório no CI
- Substituir `/validar` pelo evidence-gate
- Misturar com `agent-policies` (concern distinto — só cross-link se útil)
- Secrets/PII em logs de evidência
- Key vault / pacote E (SI a — N/A)
- Mutex cross-agent / hard timeout absoluto no yaml
- Prova truncada silenciosa acima do cap 2 MiB

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want a versioned `evidence-gate.yaml` contract at the repo root, so that manifesto schema and check rules are auditable like `git-hygiene.yaml` / `agent-policies.yaml`.
2. As a mantenedor do canônico, I want a typed loader under `config/evidence_gate/`, so that invalid contracts fail fast in CI instead of shipping a silent no-op gate.
3. As a mantenedor do canônico, I want `python -m config.evidence_gate collect` to **execute** the referenced command and persist log + exit_code, so that evidence is not a prose claim.
4. As a mantenedor do canônico, I want `python -m config.evidence_gate check` to validate manifesto ↔ tests ↔ log ↔ exit_code, so that close/ship can fail closed on missing proof.
5. As a mantenedor do canônico, I want each acceptance criterion mapped to ≥1 unit test path in the manifesto, so that “critério atendido” is mechanically cross-checked.
6. As a mantenedor do canônico, I want demo-only criteria to require an explicit human waiver marker in the manifesto, so that skipping tests is conscious and reviewable.
7. As a mantenedor do canônico, I want evidence stored under `projetos/{slug}/evidencias/` with `.claude`↔`.cursor` mirror, so that proof lives next to the project narrative.
8. As a mantenedor do canônico, I want `evidencias_ref` required on every `metrics/entregas.jsonl` line, so that delivery records link to verifiable manifests.
9. As a mantenedor do canônico, I want task close to invoke `check` and block on non-zero, so that harness-build cannot mark done without proof.
10. As a mantenedor do canônico, I want harness-ship to **re-run** `check` before closing the flow, so that stale or missing evidence cannot sneak past mid-cycle edits.
11. As a mantenedor do canônico, I want `/validar` to remain the global suite gate, so that evidence-gate complements rather than replaces ruff/mypy/pytest.
12. As a mantenedor do canônico, I want `revisor-codigo` to stay a soft orthogonal layer, so that hard proof (gate) and qualitative review (LLM) do not collapse into one mechanism.
13. As a mantenedor do canônico, I want DoD / harness-build / harness-ship / to-tasks / metrics README updated in the same ship, so that agents know when they are blocked.
14. As a mantenedor do canônico, I want install foundation always-on for evidence-gate, so that children inherit collect/check + schema without opt-in niche category.
15. As a mantenedor do canônico, I want a 2 MiB log cap with **fail** on exceed, so that oversized logs cannot produce silently truncated “green” proof.
16. As a mantenedor do canônico, I want collect latency target ≤ 2× the referenced command with **no** absolute hard timeout in YAML, so that long pytest suites are not arbitrarily killed by the contract.
17. As a mantenedor do canônico, I want last-write-wins on the current manifesto/log for a task, so that concurrent closes do not require a cross-agent mutex in MVP.
18. As a mantenedor do canônico, I want an append-only audit trail of collect events, so that LWW overwrites remain historically reconstructible.
19. As a mantenedor do canônico, I want pytest suite `tests/evidence_gate/` covering collect, check, cap, waiver, and install fixture, so that regressions fail CI without IDE E2E.
20. As CI do canônico, I want `/validar` green after this ship, so that the new kernel does not weaken existing gates.
21. As a mantenedor do canônico, I want docs to state §1.3 honesty (forged manifesto / skipped hooks possible), so that auditors are not promised server-side impossibility of fake evidence.
22. As a mantenedor do canônico, I want agent-policies left unchanged except optional cross-link, so that Bash anti-destruction stays a separate concern from acceptance proof.

### Agente / harness-build

23. As an agente em harness-build, I want a clear collect→check recipe before marking a task done, so that I know exactly what artifacts to produce.
24. As an agente em harness-build, I want `check` to fail with stderr naming missing criterion/test/log, so that I can remediate without guessing.
25. As an agente em harness-build, I want re-running `collect` on the same task to refresh the current proof deterministically, so that iteration stays idempotent for the “current” snapshot.
26. As an agente em harness-build, I want failed collect (non-zero command / missing binary) to block close, so that I cannot claim green without a real run.
27. As an agente em harness-build, I want `to-tasks` guidance to require test paths that evidence-gate can later verify, so that tasks are authored with mechanical proof in mind.
28. As an agente em harness-build, I want waiver markers only when a human explicitly allows demo-without-test, so that I do not self-waive silently.

### Revisor / ship / scorecard

29. As a revisor, I want to read manifesto + audit trail without trusting LLM prose alone, so that SI/DoD review has artifacts.
30. As a revisor, I want evidence-gate hard failures to be independent of my soft verdict, so that approving text cannot override missing proof.
31. As an operador de harness-ship, I want revalidation of all task evidences before EXIT_COMPLETE, so that the flow cannot close on stale refs.
32. As a leitor de `/scorecard`, I want `evidencias_ref` present on delivery lines, so that autonomy metrics remain tied to proof links (even if content quality is still human-audited).
33. As um responsável por SI (nível a), I want evidence logs free of secrets/PII by construction in fixtures and examples, so that LGPD/SI logging invariants hold.

### Projeto-filho / install

34. As an operador de `/install-harness`, I want foundation always-on for evidence-gate (schema + CLI + agent wiring), so that every child gets the freio without a niche category.
35. As an engenheiro no filho, I want the same `collect|check` UX as the canônico, so that dogfood and child behavior match.
36. As an engenheiro no filho, I want project evidence under `projetos/{slug}/evidencias/` mirrored when dual trees exist, so that Cursor and Claude stay in sync.
37. As an engenheiro no filho, I want SHOULD template + SCHEMA.md, so that writing a first manifesto does not require reading engine source.
38. As an engenheiro no filho, I want OPTIONAL `/evidencias` command as docs shortcut, so that agents discover the gate without memorizing the module path.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `evidence-gate.yaml` carrega no loader tipado; regras de manifesto/check presentes | pytest contrato / loader |
| AC2 | `collect` executa comando de fixture, grava log + exit_code | pytest collect |
| AC3 | `check` passa só com manifesto válido (critério→teste→log→exit 0) | pytest check |
| AC4 | Critério sem path de teste → check falha (salvo waiver humano explícito) | pytest matrix |
| AC5 | Cap 2 MiB: log maior → collect **falha** (sem prova truncada silenciosa) | pytest cap |
| AC6 | Alvo 2× documentado; **sem** hard timeout absoluto no yaml | assert contrato + docs |
| AC7 | LWW: segundo collect sobrescreve prova atual; audit append-only preserva histórico | pytest audit |
| AC8 | `evidencias_ref` obrigatório no schema de entregas; check falha se ausente/quebrado | pytest schema / check |
| AC9 | Fechar task sem manifesto/`check` verde → bloqueio (simulado no teste de wiring) | pytest wiring / agent contract |
| AC10 | Ship revalida evidências (comando/check documentado + teste de contrato) | pytest + review agents |
| AC11 | Install fixture: CLI + schema presentes no filho (foundation) | pytest install |
| AC12 | `/validar` permanece; evidence-gate não o remove/substitui | review + testes existentes |
| AC13 | `revisor-codigo` ortogonal (soft); docs não unificam com gate hard | review agent |
| AC14 | Zero secret/PII em fixtures/exemplos de evidência | grep + review SI |
| AC15 | Espelho `.claude`↔`.cursor` dos artefatos de projeto deste ship | checklist simétrica |
| AC16 | `/validar` verde no canônico com `tests/evidence_gate/` | ruff + mypy + pytest |
| AC17 | `check` &lt; 5 s em manifesto típico de fixture (regressão SLA) | pytest timing soft/assert oriente |
| AC18 | Docs §1.3 honesty: gate local ≠ impossibilidade de manifesto forjado | review cheatsheet/ADR |

---

## Functional Requirements

### FR1 — Contrato `evidence-gate.yaml`

- Fonte única de: schema do manifesto, regras de `check`, cap de log **2 MiB**, política
  **fail-on-exceed**, alvo de latência do `collect` (≤ 2× comando), ausência de hard
  timeout absoluto.
- Versionado na raiz do canônico (padrão `git-hygiene.yaml` / `agent-policies.yaml`).
- Mudanças breaking → bump + suite `tests/evidence_gate/` verde.

### FR2 — Engine `config/evidence_gate/`

- Load tipado (padrão loaders existentes).
- CLI: `python -m config.evidence_gate collect|check`.
- `collect`: executa comando do manifesto/critério, grava log sob `evidencias/`, registra
  exit_code, append na trilha de auditoria; atualiza prova “atual” (LWW).
- `check`: valida schema, cruzamento critério→teste, existência/tamanho do log, exit_code,
  `evidencias_ref`; exit ≠ 0 = bloqueante.
- Sem rede obrigatória; operação local FS + subprocess.

### FR3 — Manifesto e pasta de evidências

- Por task: manifesto ligando cada critério a ≥1 path de teste + comando + exit_code +
  path de log.
- Local: `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/projetos/...`).
- Waiver humano: marcador explícito no manifesto para demo sem teste; `check` aceita só
  com o marcador (e metadados mínimos exigidos pelo contrato).
- Ciclo de vida: evidências no git do projeto; sem TTL automático; exclusão = humano/git.

### FR4 — Delivery record e scorecard

- `metrics/entregas.jsonl` + README: campo **`evidencias_ref`** obrigatório (path relativo
  ao manifesto).
- Ship/scorecard leem o link; ausência ou path inválido → falha de `check` / contrato de
  fechamento.
- Não substitui campos existentes; adiciona prova ancorada.

### FR5 — Bloqueio task + ship

- harness-build: antes de marcar task done / append entregas → `collect` (se necessário) +
  `check` verde.
- harness-ship: revalida evidências das tasks do fluxo antes de fechar STATUS /
  EXIT_COMPLETE.
- Falha de dependência (comando inexistente / exit ≠ 0 / log &gt; 2 MiB) → bloqueio; sem
  retry automático no MVP; stderr claro.
- Sem Stop dual MUST neste ship (decisão 10 / WON'T).

### FR6 — Install foundation

- Foundation always-on: contrato/schema + engine CLI + wiring de DoD/agents/commands
  relevantes nos filhos.
- SHOULD: template de manifesto + SCHEMA.md no seed.
- Não acoplar a categoria `pipeline_dados` nem a agent-policies; concern próprio.
- Generate/portabilidade: sem paths de máquina obrigatórios nos templates.

### FR7 — Ortogonalidade

- `/validar` permanece suite global (ruff+mypy+pytest + DE condicional).
- `revisor-codigo` = soft (cobertura/qualidade/SI); não valida exit mecânico do manifesto.
- `agent-policies` = freio Bash destrutivo — não misturar kernels; cross-link opcional em
  docs.
- Soft policy DoD atualizada para exigir evidence-gate mecânico além de claims.

### FR8 — Auditoria e concorrência

- Prova “atual”: last-write-wins (G2).
- Trilha append-only extra (G4): cada `collect` registra evento (timestamp, task_id,
  comando resumido, exit_code, path log, resultado) sem apagar histórico.
- Formato concreto (`evidencias/audit.jsonl` vs histórico versionado) pode fechar na
  implementação desde que AC7 seja preservado.

### FR9 — Documentação (SHOULD)

- Cheatsheet 1 página; ADR do kernel; comando `/evidencias` como atalho.
- Honesty §1.3: manifesto forjável; gate local; sem Edit policies.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | SI **a**: sem PII/secrets em evidências; fixtures só paths/exit codes/logs sintéticos |
| NFR-SI2 | Sem `[AVISO_LGPD]` / `rules/pii.md` neste ship |
| NFR-SI3 | Key vault N/A — não introduzir wiring OCI/Azure |
| NFR-SI4 | Redaction leve de log = SHOULD se heurística achar secret |
| NFR-SI5 | Honesty §1.3: não prometer impossibilidade de prova forjada / bypass humano |
| NFR-Q1 | `check` &lt; 5 s para manifesto típico de 1 task (alvo Dev Loop) |
| NFR-Q2 | `collect` ≤ 2× tempo do comando referenciado; sem hard timeout no yaml |
| NFR-Q3 | Cap log 2 MiB; exceder → fail (não truncate silencioso) |
| NFR-Q4 | LWW na prova atual; audit append-only; sem mutex cross-agent no MVP |
| NFR-Q5 | Espelho `.claude`↔`.cursor` na mesma sessão de promoção |
| NFR-Q6 | Soft-block git: fetch Azure 403 → trabalho na branch local; sem inventar sync |
| NFR-Q7 | Fail closed no close/ship quando `check` ≠ 0; sem fallback silencioso |

---

## Architecture — artefatos canônicos

```text
┌─ evidence-gate.yaml ──► schema manifesto · regras check · cap 2MiB · alvo 2×
│
├─ config/evidence_gate/ ──► load · collect (executa) · check · (CLI)
│
├─ .claude/projetos/{slug}/evidencias/ ──► manifesto · logs · audit append-only
│         (+ espelho .cursor/projetos/...)
│
├─ metrics/entregas.jsonl ──► evidencias_ref → manifesto
│
├─ wiring: DoD · harness-build · harness-ship · to-tasks · revisor (soft)
├─ /validar ──► permanece (suite global; não substituído)
│
├─ install-harness foundation ──► schema + CLI + wiring
├─ docs: cheatsheet · ADR · /evidencias (SHOULD)
└─ tests/evidence_gate/ ──► collect · check · cap · waiver · install · audit
```

### Amarras a módulos lógicos

| Artefato | Módulo / superfície |
|---|---|
| Contrato | `evidence-gate.yaml` (raiz) |
| Engine / CLI | `config/evidence_gate/` |
| Evidências | `projetos/{slug}/evidencias/` (+ espelho) |
| Delivery | `metrics/entregas.jsonl` + `metrics/README.md` |
| DoD | `rules/definicao-de-pronto` (+ `.mdc`) |
| Agents | `harness-build`, `harness-ship`, `revisor-codigo` |
| Tasks skill | `to-tasks` |
| Install | foundation / `stack_map` (+ generate se couber) |
| Testes | `tests/evidence_gate/` |
| Docs | cheatsheet + ADR (+ `/evidencias` SHOULD) |
| Projeto | `.claude/projetos/evidencias-testes-obrigatorios/` (+ espelho `.cursor/`) |
| Ortogonal | `/validar`, `agent-policies`, DE kernel — sem unificar |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | Perímetro MVP: manifesto + validador; sem hooks MUST | FR5 / Out of Scope |
| 2 | Evidência mínima: critério→testes+comando+exit+log | FR3 / AC3 |
| 3 | Pasta evidencias/ + espelho + `evidencias_ref` | FR3–FR4 / AC8 |
| 4 | Unitários por critério; `/validar` segue | FR7 / AC4 / AC12 |
| 5 | Bloqueio task **e** ship | FR5 / AC9–AC10 |
| 6 | Install foundation always-on | FR6 / AC11 |
| 7 | Kernel yaml + `config/evidence_gate` + collect\|check | FR1–FR2 / AC1–AC3 |
| 8 | `collect` executa comando | FR2 / AC2 |
| 9 | Revisor ortogonal (soft) vs gate hard | FR7 / AC13 |
| 10 | Fora: Stop dual, portal, substituir `/validar`, misturar policies | Out of Scope |
| 11 / G1 | Só alvo 2×; sem hard timeout no yaml | NFR-Q2 / AC6 |
| 12 / G2 | Concorrência LWW | FR8 / AC7 |
| 13 / G3 | Cap 2 MiB; fail se exceder | FR1 / AC5 |
| 14 / G4 | Auditoria append-only extra | FR8 / AC7 |
| 15 | Judge define (b) pulado | Further Notes |
| I1 | `/validar` permanece; gate prova por task | FR7 |
| I2 | entregas ganha `evidencias_ref` | FR4 |
| I3 | Canônico dogfooda em tasks futuras | tipo e / Solution |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (exit codes CLI, conteúdo de manifesto/log,
falha de `check`, cap, waiver, fixture de install, presença de `evidencias_ref`), não
detalhes privados de helpers internos salvo o contrato documentado no YAML.

Alinhado às decisões 7–8 e critérios de sucesso do grill: suite dedicada
`tests/evidence_gate/`; E2E IDE = dogfood manual (fora do CI obrigatório).

| Área | O que testar | Prior art |
|---|---|---|
| Contrato YAML | load tipado; cap 2 MiB; ausência de hard timeout | `tests/git_hygiene/`, `tests/agent_policies/` contrato |
| collect | executa comando fixture; grava log + exit_code; audit append | subprocess + tmpdir |
| check | manifesto válido → 0; faltando teste/log/ref → ≠ 0 | unit FS |
| Waiver | sem marcador → fail; com marcador humano → pass controlado | matrix |
| Cap 2 MiB | overflow → collect fail (não truncate ok) | tmp file oversized |
| LWW + audit | segundo collect sobrescreve atual; audit cresce | pytest ordenado |
| entregas schema | `evidencias_ref` obrigatório | metrics README + teste schema |
| Wiring close/ship | contrato/docs/agents exigem check; teste de regressão de instrução ou helper | estilo wiring DE/`validar` |
| Install foundation | filho recebe CLI/schema | testes install (estilo policies/DE) |
| SI | fixtures sem secret/PII | grep + asserts de conteúdo |
| `/validar` | suite canônica verde com novos testes | gate existente |
| SLA check | manifesto típico &lt; 5 s | soft assert / benchmark leve |

### Plano de validação (DoD gate)

```bash
# Código (sempre)
uv run ruff check --fix . && uv run mypy . && uv run pytest -q

# Suite nova (quando existir)
uv run pytest -q tests/evidence_gate/

# CLI (quando existir)
python -m config.evidence_gate check --help
python -m config.evidence_gate collect --help
# collect/check contra fixture versionada sob tests/evidence_gate/fixtures/
```

Critério: gate **verde** no canônico; fixtures PASS; sem E2E IDE obrigatório no CI;
`/validar` e kernels ortogonais (DE, agent-policies) sem regressão.

---

## Out of Scope

Materializa a **decisão 10** + WON'T do grill:

- Hooks Stop dual Claude/Cursor obrigatórios no MVP (Fase 2 / COULD)
- Portal UI / dashboard de evidências
- E2E obrigatório Claude Code / Cursor IDE no CI
- Substituir `/validar` pelo evidence-gate
- Misturar/unificar com `agent-policies` ou DE kernel
- Secrets/PII em logs de evidência
- Key vault / pacote E
- Mutex cross-agent; hard timeout absoluto no yaml
- Prova truncada silenciosa acima de 2 MiB
- Screenshots/PDF como MUST de evidência UI
- Multi-tenant / RBAC / SIEM central de evidências
- Tag `prod-*` / Fase 2 git hygiene

---

## Risks

| Risco | Mitigação |
|---|---|
| Agente forja manifesto sem rodar collect | Docs §1.3; collect como path feliz documentado; dogfood; revisor soft ainda lê |
| Log gigante / DoS de disco | Cap 2 MiB + fail-on-exceed (AC5) |
| Collect trava Dev Loop em suite lenta | Alvo 2× sem hard kill no yaml; critério escopado no manifesto (não re-rodar monólito inteiro sem necessidade) |
| Drift Claude↔Cursor na pasta evidencias | Invariante de espelho + checklist AC15 |
| Confusão com `/validar` | FR7 / AC12 — suite global vs prova por task |
| Confusão com agent-policies | Out of Scope + cross-link “Bash deny ≠ aceite” |
| Install omite foundation | AC11 fixture bloqueante |
| LWW apaga prova anterior sem rastro | Audit append-only (G4 / AC7) |
| Fetch Azure 403 atrasa sync | Soft-block didático; branch local `feat/evidencias-testes-obrigatorios` |
| Promessa excessiva de “prova impossível de forjar” | AC18 + NFR-SI5 |

---

## SI Considerations

- **Nível a:** sem dados sensíveis de domínio; evidências = paths, comandos de teste,
  exit codes, logs de gate sintéticos/fixtures.
- Sem `[AVISO_LGPD]` / `rules/pii.md` / key vault neste ship.
- **Invariante:** evidências **nunca** incluem secrets, tokens, connection strings, PII.
  Exemplos e fixtures auditáveis por grep (AC14).
- Redaction leve = SHOULD se heurística detectar padrão de secret em log capturado.
- Rule `seguranca` transversal permanece; este ship não amplia superfície de escrita em
  produção.
- **Honesty §1.3:** gate local e dogfoodável; manifesto pode ser editado à mão; sem Edit
  policies o framework não impede fraude — reduz alucinação operacional e torna auditoria
  humana/CI possível.
- Revisor-codigo: SI bloqueante se o ship introduzir logging de secret/PII em evidências
  ou prometer impossibilidade server-side de prova falsa.

---

## Further Notes

- **Adversarial judge (grill/define):** pulado **(b)** — sem `01b-judge.md`.
- **Adversarial judge (PRD):** **pendente** — checkpoint obrigatório antes do
  `/harness-architect` (perguntar a/b mesmo após pulo no define).
- Naming exato de arquivos de manifesto (`task-<id>.yaml` vs `manifest.json`) e path do
  audit trail podem fechar na task de implementação desde que FR1–FR9 e ACs sejam
  preservados.
- Soft-blocks deste design: fetch 403; sem commit/push; **sem** `PRD.md` na raiz do
  canônico — apenas `02-prd.md` neste projeto (+ espelho `.cursor/`).
- Próximo artefato após judge/architect: `03-harness.md` → `/to-tasks` → `harness-build`.

---

## Próximo passo (após aceite do PRD + judge)

1. Checkpoint adversarial judge (a/b) — se (a), gerar `02b-judge.md` e opcionalmente
   ajustar o PRD
2. `/harness-architect` — montar/atualizar artefatos de harness desta evolução
3. Registrar `03-harness.md` → `/to-tasks` → `harness-build`
