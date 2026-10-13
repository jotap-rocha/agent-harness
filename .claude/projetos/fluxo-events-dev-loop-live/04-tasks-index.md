# Tasks index — Fluxo-events Dev Loop + backfill

Slug: `fluxo-events-dev-loop-live`  
Branch: `feat/fluxo-events-dev-loop-live`  
Fontes: `02-prd.md`, `03-harness.md`  
Aprovado: 2026-08-17

## Objetivo

Dev Loop → telemetria live (`dev-loop-{NOME}`); backfill commits 58–65 → `e4dfc69`;
guardrail PT-BR naming.

## Tasks (67–74)

| # | File | Status | Blocked by | AC |
|---|---|---|---|---|
| 67 | `tasks/fluxo-events-dev-loop-live/67-contrato-dev-loop-map.md` | done | none | AC1, AC16 |
| 68 | `tasks/fluxo-events-dev-loop-live/68-helper-slug-from-prompt.md` | done | 67 | AC3, AC4 |
| 69 | `tasks/fluxo-events-dev-loop-live/69-render-dual-map-dev.md` | done | 67, 68 | AC2, AC5 |
| 70 | `tasks/fluxo-events-dev-loop-live/70-wiring-ux-crafter-executor.md` | done | 68, 69 | AC6, AC7, AC13 |
| 71 | `tasks/fluxo-events-dev-loop-live/71-truncate-exit-complete.md` | done | 69, 70 | AC8, AC9 |
| 72 | `tasks/fluxo-events-dev-loop-live/72-backfill-commits-58-65.md` | done | none | AC10 |
| 73 | `tasks/fluxo-events-dev-loop-live/73-guardrail-naming-ptbr.md` | done | none | AC11 |
| 74 | `tasks/fluxo-events-dev-loop-live/74-docs-validar-dogfood.md` | done | 70–73 | AC14, AC15, AC17 |

### Ordem sugerida

```text
67 → 68 → 69 → 70 → 71
72 ∥ 73
(70 ∧ 71 ∧ 72 ∧ 73) → 74
```

## Próximo passo

Todas as tasks **done**. Diga **`harness-ship`** para fechar com scorecard e
`/sync-context` (CLAUDE.md / CONTEXT.md / AGENTS.md). Commit/push só com acordo explícito.
