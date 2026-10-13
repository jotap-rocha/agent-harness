# Tasks index — Silver checklist ODCS

Slug: `silver-checklist-odcs`  
Branch: `feat/silver-checklist-odcs`  
Fontes: `02-prd.md`, `03-harness.md`  
Aprovado: 2026-08-19  
Implementação: 2026-08-19 — **todas done**

## Objetivo

KB pattern prescritivo Silver ↔ ODCS (template + orders), cross-links,
agents JIT, pytest dual-tree, `/validar` verde, kernel DE intacto.

## Tasks (82–87)

| # | File | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 82 | `tasks/silver-checklist-odcs/82-kb-pattern-silver-checklist.md` | done | none | AC1–6,13–14 |
| 83 | `tasks/silver-checklist-odcs/83-crosslinks-pipeline-de.md` | done | 82 | AC7–9 |
| 84 | `tasks/silver-checklist-odcs/84-agents-jit-de.md` | done | 82 | AC10 |
| 85 | `tasks/silver-checklist-odcs/85-pytest-kb-dual-tree.md` | done | 82, 83, 84 | AC1–2,11 |
| 86 | `tasks/silver-checklist-odcs/86-validar-kernel-intacto.md` | done | 85 | AC11–12 |
| 87 | `tasks/silver-checklist-odcs/87-docs-tasks-index.md` | done | 86 | meta |

### Ordem sugerida

```text
82 → (83 ∥ 84) → 85 → 86 → 87
```

## Próximo passo

Diga **`harness-ship`** (após commit com acordo).
