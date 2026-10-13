# Tasks index — Fluxo grafo causal

Slug: `fluxo-grafo-causal`  
Branch: `feat/flujo-grafo-causal`  
Fontes: `02-prd.md`, `03-harness.md`  
Aprovado: 2026-08-18  
Implementação: 2026-08-18 — **todas done**

## Objetivo

Schema aditivo (`event_id`/`run_id`/`parent_event_id`) + stack fail-soft + dois SVGs
(canônico + causal) + wiring SDD/Dev.

## Tasks (75–81)

| # | File | Status | Blocked by | AC |
|---|---|---|---|---|
| 75 | `tasks/fluxo-grafo-causal/75-emit-causal-ids.md` | done | none | AC1–3,6,18 |
| 76 | `tasks/fluxo-grafo-causal/76-stack-parent-gitignore.md` | done | 75 | AC4,5,12,13 |
| 77 | `tasks/fluxo-grafo-causal/77-cli-run-parent-flags.md` | done | 75, 76 | AC11 |
| 78 | `tasks/fluxo-grafo-causal/78-render-causal-svg.md` | done | 75 | AC7–10,14 |
| 79 | `tasks/fluxo-grafo-causal/79-wiring-sdd-dev-causal.md` | done | 75–77 | AC16 |
| 80 | `tasks/fluxo-grafo-causal/80-docs-adr-cheatsheet.md` | done | 75 | AC17,19 |
| 81 | `tasks/fluxo-grafo-causal/81-validar-dogfood-causal.md` | done | 76–80 | AC15,19,20 |

### Ordem sugerida

```text
75 → 76 → 77 → 79
75 → 78
75 → 80
(77 ∧ 78 ∧ 79 ∧ 80) → 81
```

## Próximo passo

Todas as tasks concluídas. Diga **`harness-ship`** (após commit com acordo).
