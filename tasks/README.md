# Tasks — Agent Harness Canônico

Dashboard local (skill `to-tasks`).

## Layout (por slug de projeto)

Tasks **não** ficam na raiz de `tasks/`. Cada pacote vive em:

```text
tasks/{slug}/NN-short-title.md
```

O `{slug}` é o **mesmo** de `.claude/projetos/{slug}/`.  
Numeração global `NN` permanece (issue / evidence-gate / entregas).

| Pacote (pasta) | Issues | Status |
|---|---|---|
| [`git-hygiene-azure-devops/`](git-hygiene-azure-devops/) | 01–08 | done |
| [`engenharia-de-dados-boas-praticas-canonico/`](engenharia-de-dados-boas-praticas-canonico/) | 09–32 | done |
| [`keyvault-oci-azure-choice/`](keyvault-oci-azure-choice/) | 33–40 | done |
| [`policies-anti-destrutivas/`](policies-anti-destrutivas/) | 41–48 | done |
| [`evidencias-testes-obrigatorios/`](evidencias-testes-obrigatorios/) | 49–56 | done |
| [`context-rebind-filho/`](context-rebind-filho/) | 57 | done |
| [`visao-grafica-fluxo-agentes/`](visao-grafica-fluxo-agentes/) | 58–66 | done* |
| [`fluxo-events-dev-loop-live/`](fluxo-events-dev-loop-live/) | 67–74 | done |
| [`fluxo-grafo-causal/`](fluxo-grafo-causal/) | 75–81 | done |
| [`silver-checklist-odcs/`](silver-checklist-odcs/) | 82–87 | done |
| [`medallion-sdd-gates/`](medallion-sdd-gates/) | 88–93 | done |

\*66 = aviso UX painel live (pós-ship, branch `chore/tasks-por-slug`).

**Blocked by** usa path completo, ex.: `tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md`.

---


## Git Hygiene (01–08) — done

Pasta: `tasks/git-hygiene-azure-devops/`  
Objetivo: Camada Convenção no canônico (dogfood + `/install-harness`).  
Fonte: `.claude/projetos/git-hygiene-azure-devops/`.

| # | Title | Status | Blocked by | Aceite |
|---|---|---|---|---|
| 01 | contrato-regex-testes | done | none | A1 (yaml), A3 |
| 02 | cheatsheet-rule-ajuda | done | 01 | A13, A1 (rule), A15 (rule) |
| 03 | template-pr-azure | done | none | A4 |
| 04 | githooks-bootstrap | done | 01 | A5–A7, A14 |
| 05 | comando-nova-branch | done | 01, 02 | A2, A3 (uso) |
| 06 | adapter-pr-hibrido | done | 01, 05 | A9, A10 |
| 07 | wiring-git-preflight | done | 02, 05 | A8, A15 |
| 08 | stack-map-install | done | 02–07 | A11, A12, fecha A14 |

---

## Engenharia de Dados — Loop 1 kernel (09–16) — done

Pasta: `tasks/engenharia-de-dados-boas-praticas-canonico/`  
**Objetivo:** norma + CLI A/B/C + example spark-yarn + baseline/waiver + install mínimo + `/validar` condicional.

Fontes: `.claude/projetos/engenharia-de-dados-boas-praticas-canonico/` (`02-prd.md`, `03-harness.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 09 | yaml-contrato-loader | done | none | AC1 |
| 10 | cli-validate-abc | done | 09 | AC2 parcial, AC3 |
| 11 | example-spark-yarn-min | done | 10 | AC2, AC3 |
| 12 | baseline-compare-waiver | done | 10 | AC4, AC5 |
| 13 | report-explain | done | 10 | stories 16–17 |
| 14 | relatorio-ro-sql-capacity | done | 10, 13 | AC6, AC7 |
| 15 | install-pacote-minimo | done | 09, 12 | AC8 |
| 16 | validar-rule-espelho | done | 11, 15 | AC9, AC10 |

---

## Engenharia de Dados — Loop 2 Databricks (17–24) — done

Pasta: `tasks/engenharia-de-dados-boas-praticas-canonico/`  
**Objetivo:** perfis Databricks + pacote D + auto-detect/multi + baseline `profiles[]` + 2 examples + `/validar` ampliado — **sem** mudar `pipeline_dados`, **sem** agents/KBs novas.

Fontes: `08-loop2-prd.md`, `09-loop2-harness.md`, `07-loop2-grill.md`.

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 17 | yaml-perfis-pacote-d | done | none | AC1 |
| 18 | engine-registry-detect | done | 17 | AC4, AC5 |
| 19 | checks-databricks-cloud | done | 18 | AC10 |
| 20 | baseline-profiles-array | done | 18 | AC6 |
| 21 | example-databricks-sdp-min | done | 19 | AC2 |
| 22 | example-databricks-dlt-min | done | 19 | AC3 |
| 23 | validar-autodetect-espelho | done | 18, 21 | AC7, AC9 |
| 24 | freeze-stackmap-regressao | done | 21, 22, 23 | AC8, AC9 |

### Ordem sugerida (histórica)

```text
17 → 18 → (19 ∥ 20) → (21 ∥ 22) → 23 → 24
```

---

## Engenharia de Dados — Loop 3 agents/skills/KBs/install (25–32)

Pasta: `tasks/engenharia-de-dados-boas-praticas-canonico/`  
**Objetivo:** amarrar 10 agents + 7 commands ao kernel; pontes KB + KB `databricks`;
skill `de-conformidade`; propagar **tudo** em `pipeline_dados`; novo freeze DoD —
**sem** live API; seed KEEP; espelho `.claude`↔`.cursor`.

Fontes: `11-loop3-ideia.md`, `00d-codebase-loop3.md`, `12-loop3-grill.md`,
`13-loop3-prd.md`, `14-loop3-harness.md`.

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 25 | amarrar-agents-de-kernel | done | none | AC1, AC10 |
| 26 | amarrar-commands-de | done | 25 | AC2, AC10 |
| 27 | kbs-de-ponte-ids | done | 25 | AC3, AC10 |
| 28 | kb-databricks | done | 27 | AC4, AC10, AC11 |
| 29 | skill-de-conformidade | done | 25 | AC5, AC10, AC11 |
| 30 | install-pipeline-dados-completo | done | 25, 26, 28, 29 | AC6, AC7 |
| 31 | regressao-examples-install | done | 30 | AC7, AC8 |
| 32 | freeze-loop3-dod | done | 31 | AC9, AC10, AC11 |

### Ordem sugerida

```text
25 → 26
25 → 27 → 28
25 → 29
(26 ∧ 28 ∧ 29) → 30 → 31 → 32
```

### Fora deste pacote

- Reabrir checks/perfis A–D do kernel  
- Live Databricks API / sql-capacity write  
- Segunda skill DE  

---

## Key Vault OCI vs Azure (33–40) — done

Pasta: `tasks/keyvault-oci-azure-choice/`  
**Objetivo:** pergunta OCI/Azure no grill → skill `cloud-secrets` + KBs → pacote E
(`DE-E*`) + marker/auto-detect → examples min + install condicional (categoria vault) —
sem agent canônico; sem live API; espelho `.claude`↔`.cursor`.

Fontes: `.claude/projetos/keyvault-oci-azure-choice/` (`02-prd.md`, `03-harness.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 33 | kernel-pacote-e-marker | done | none | AC4–AC7, AC9–AC10 |
| 34 | validar-dispara-e | done | 33 | AC8 |
| 35 | scaffold-examples-min | done | 33 | AC11–AC12 |
| 36 | skill-cloud-secrets | done | none | AC2 |
| 37 | kbs-oci-azure-vault | done | none | AC3, AC14 (SI) |
| 38 | grill-pergunta-vault | done | none | AC1 |
| 39 | install-categoria-vault | done | 36, 37 | AC13 |
| 40 | si-bridge-adr-sync | done | 33–39 | AC14–AC16 + docs |

### Ordem sugerida

```text
33 → 34
33 → 35
36 ∥ 37 ∥ 38 ∥ 33
(36 ∧ 37) → 39
(33…39) → 40
```

### Fora deste pacote

- Agent `key-oci-expert` no canônico  
- Live OCI/Azure Vault API  
- Outros cofres (AWS/HashiCorp)  
- Install sempre via `pipeline_dados`  

---

## Policies anti-destrutivas (41–48) — done

Pasta: `tasks/policies-anti-destrutivas/`  
**Objetivo:** kernel `agent-policies.yaml` + engine + paridade Claude↔Cursor
(PreToolUse / `beforeShellExecution`) + install foundation (deny ≠ `[]`) + seed
`.harness/policies` KEEP + docs/ADR/dogfood — SI **d**; sem Edit policies server-side;
`DE-A002` ortogonal.

Fontes: `.claude/projetos/policies-anti-destrutivas/` (`02-prd.md`, `03-harness.md`).

| # | Title | Status | Blocked by | Foco |
|---|---|---|---|---|
| 41 | contrato-yaml-loader | done | none | YAML + loader + CLI check |
| 42 | matcher-deny-ask | done | 41 | matcher compartilhado |
| 43 | bypass-fail-modes | done | 42 | bypass + fail closed/open |
| 44 | catalog-core-families | done | 41 | core shell…k8s |
| 45 | generate-dual-artifacts | done | 42, 44 | generate Claude+Cursor |
| 46 | hooks-dual-runtime | done | 43, 45 | PreToolUse + beforeShell |
| 47 | seed-install-foundation | done | 45, 46 | seed KEEP + install |
| 48 | docs-adr-dogfood-sync | done | 47 | SI, ADR, dogfood, sync |

### Ordem sugerida

```text
41 → 42 → 43
41 → 44
(42 ∧ 44) → 45
(43 ∧ 45) → 46
(45 ∧ 46) → 47 → 48
```

### Fora deste pacote

- Edit policies / branch protection server-side  
- Agent “policy officer”  
- Unificar/deprecar `DE-A002`  
- E2E obrigatório Claude/Cursor IDE no CI  

---

## Evidências e testes obrigatórios (49–56) — done

Pasta: `tasks/evidencias-testes-obrigatorios/`  
**Objetivo:** kernel `evidence-gate` (`collect|check`) + manifesto/logs/`audit.jsonl`
+ `evidencias_ref` + bloqueio build/ship + install foundation + DoD/agents —
SI **a**; sem Stop dual; `/validar` permanece.

Fontes: `.claude/projetos/evidencias-testes-obrigatorios/` (`02-prd.md`, `03-harness.md`).

| # | Title | Status | Blocked by | Foco |
|---|---|---|---|---|
| 49 | contrato-yaml-loader | done | none | YAML + loader |
| 50 | collect-run-logs | done | 49 | collect + cap 2 MiB |
| 51 | check-manifest-ref | done | 50 | check + evidencias_ref |
| 52 | audit-append-only | done | 50 | audit.jsonl |
| 53 | wiring-build-ship | done | 51, 52 | agents build/ship |
| 54 | install-foundation-seed | done | 51 | install always-on |
| 55 | dod-agents-totasks | done | 53 | DoD + to-tasks + revisor |
| 56 | docs-adr-sync | done | 54, 55 | docs + ADR + sync |

### Ordem sugerida

```text
49 → 50 → 51
50 → 52
(51 ∧ 52) → 53 → 55
51 → 54
(54 ∧ 55) → 56
```

### Fora deste pacote

- Hooks Stop dual Claude/Cursor  
- Portal UI de evidências  
- Substituir `/validar`  
- Misturar com agent-policies  

---

## Context-rebind filho (57) — done

Pasta: `tasks/context-rebind-filho/`  
**Objetivo:** install foundation gera README do filho + banner anti-canônico;
passo CONTEXT_REBIND no 1º round (brainstorm/architect/install).

| # | Title | Status | Blocked by | Foco |
|---|---|---|---|---|
| 57 | context-rebind-filho | done | none | README + banner + soft-block |

---

## Visão gráfica fluxo de agentes (58–66) — done

Pasta: `tasks/visao-grafica-fluxo-agentes/`  
**Objetivo:** kernel `fluxo-events` (contrato + emit/render/truncate + `live.html`
SDD 0–4) + wiring agents + install foundation + docs + dogfood + aviso UX ao usuário.

Fontes: `.claude/projetos/visao-grafica-fluxo-agentes/` (`02-prd.md`, `03-harness.md`,
`04-tasks-index.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 58 | contrato-yaml-loader | done | none | AC1, AC15 |
| 59 | cli-emit-jsonl | done | 58 | AC2, AC5, AC7, AC10 |
| 60 | render-live-html | done | 58 | AC3, AC4, AC5, AC17 |
| 61 | rotate-truncate-ship | done | 59, 60 | AC6, AC8 |
| 62 | wiring-sdd-emit | done | 59–61 | AC11, AC14, AC16 |
| 63 | install-foundation-seed | done | 58–61 | AC9 |
| 64 | docs-adr-fluxo-live | done | 58 | AC13, AC18 |
| 65 | validar-dogfood-slug | done | 62, 63, 64 | AC11, AC12 |
| 66 | aviso-ux-painel-live | done | none | UX aviso SDD |

### Ordem sugerida

```text
58 → (59 ∥ 60) → 61 → 62
58 → 64
(58–61) → 63
(62 ∧ 63 ∧ 64) → 65
```

### Fora deste pacote

- SSE / Canvas MUST / Dev Loop no mapa  
- Unificar com evidence-gate ou agent-policies  
- Substituir STATUS.md / scorecard  

---

## Fluxo-events Dev Loop + backfill (67–74) — done

Pasta: `tasks/fluxo-events-dev-loop-live/`  
**Objetivo:** telemetria live no Dev Loop (`dev-loop-{NOME}` + `dev_loop_map`);
backfill commits 58–65 → `e4dfc69`; guardrail PT-BR naming (fluxo≠flujo).

Fontes: `.claude/projetos/fluxo-events-dev-loop-live/` (`02-prd.md`, `03-harness.md`,
`04-tasks-index.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 67 | contrato-dev-loop-map | done | none | AC1, AC16 |
| 68 | helper-slug-from-prompt | done | 67 | AC3, AC4 |
| 69 | render-dual-map-dev | done | 67, 68 | AC2, AC5 |
| 70 | wiring-ux-crafter-executor | done | 68, 69 | AC6, AC7, AC13 |
| 71 | truncate-exit-complete | done | 69, 70 | AC8, AC9 |
| 72 | backfill-commits-58-65 | done | none | AC10 |
| 73 | guardrail-naming-ptbr | done | none | AC11 |
| 74 | docs-validar-dogfood | done | 70–73 | AC14, AC15, AC17 |

### Ordem sugerida

```text
67 → 68 → 69 → 70 → 71
72 ∥ 73
(70 ∧ 71 ∧ 72 ∧ 73) → 74
```

---

## Fluxo grafo causal (75–81) — done

Pasta: `tasks/fluxo-grafo-causal/`  
**Objetivo:** schema aditivo (`event_id`/`run_id`/`parent_event_id`) + stack fail-soft +
dois SVGs (canônico + causal) + wiring SDD/Dev.

Fontes: `.claude/projetos/fluxo-grafo-causal/` (`02-prd.md`, `03-harness.md`,
`04-tasks-index.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 75 | emit-causal-ids | done | none | AC1–3,6,18 |
| 76 | stack-parent-gitignore | done | 75 | AC4,5,12,13 |
| 77 | cli-run-parent-flags | done | 75, 76 | AC11 |
| 78 | render-causal-svg | done | 75 | AC7–10,14 |
| 79 | wiring-sdd-dev-causal | done | 75–77 | AC16 |
| 80 | docs-adr-cheatsheet | done | 75 | AC17,19 |
| 81 | validar-dogfood-causal | done | 76–80 | AC15,19,20 |

### Ordem sugerida

```text
75 → 76 → 77 → 79
75 → 78
75 → 80
(77 ∧ 78 ∧ 79 ∧ 80) → 81
```

---

## Silver checklist ODCS (82–87) — done

Pasta: `tasks/silver-checklist-odcs/`  
**Objetivo:** KB pattern Silver ↔ ODCS (template + orders), cross-links, agents JIT,
pytest dual-tree, `/validar` verde, `data-engineering.yaml` intacto.

Fontes: `.claude/projetos/silver-checklist-odcs/` (`02-prd.md`, `03-harness.md`,
`04-tasks-index.md`).

| # | Title | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 82 | kb-pattern-silver-checklist | done | none | AC1–6,13–14 |
| 83 | crosslinks-pipeline-de | done | 82 | AC7–9 |
| 84 | agents-jit-de | done | 82 | AC10 |
| 85 | pytest-kb-dual-tree | done | 82, 83, 84 | AC1–2,11 |
| 86 | validar-kernel-intacto | done | 85 | AC11–12 |
| 87 | docs-tasks-index | done | 86 | meta |

### Ordem sugerida

```text
82 → (83 ∥ 84) → 85 → 86 → 87
```

---

## Medallion SDD gates (88–93) — done

Pasta: `tasks/medallion-sdd-gates/`  
**Objetivo:** Gates de processo SDD/Dev Loop para pipelines Medallion (KB + agents + rules).

Fontes: `.claude/projetos/medallion-sdd-gates/` (`00-ideia.md`, `STATUS.md`).

| # | Title | Status | Blocked by |
|---|---|---|---|
| 88 | kb-pattern-medallion-gates | done | none |
| 89 | gates-harness-brainstorm | done | 88 |
| 90 | gates-harness-define | done | 88 |
| 91 | gates-prompt-crafter | done | 88 |
| 92 | rules-pipeline-index | done | 88 |
| 93 | pytest-wiring | done | 89, 90, 91, 92 |

### Ordem sugerida

```text
88 → (89 ∥ 90 ∥ 91 ∥ 92) → 93
```

---

## Pipeline runtime + AI-DEV-KIT gates (94–98) — done

Pasta: `tasks/pipeline-runtime-gates/`  
**Objetivo:** Gates humanos Spark local vs Databricks + AI-DEV-KIT no brainstorm SDD.

Fontes: `.claude/projetos/pipeline-runtime-gates/` (`00-ideia.md`, `STATUS.md`).

| # | Title | Status | Blocked by |
|---|---|---|---|
| 94 | kb-ai-dev-kit-gate | done | none |
| 95 | gates-brainstorm-4a | done | 94 |
| 96 | gates-define-2a | done | 94 |
| 97 | rules-index-crossrefs | done | 94 |
| 98 | pytest-ship | done | 95, 96, 97 |

### Ordem sugerida

```text
94 → (95 ∥ 96 ∥ 97) → 98
```

---

## Como implementar

Diga `harness-build` ou `implement task 75` / `start task 75` (resolve `tasks/{slug}/NN-*.md`). Siga a skill `to-tasks`
(testes primeiro quando houver, espelho `.claude`↔`.cursor`, gate, delivery record,
commit só com acordo).
