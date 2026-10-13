# Tasks index — Silver checklist ODCS

Slug: `silver-checklist-odcs`  
Branch: `feat/silver-checklist-odcs` (criar no build)  
Fontes: `02-prd.md`, `03-harness.md`  
Aprovado: 2026-08-19  
Implementação: pendente

## Objetivo

KB pattern prescritivo Silver ↔ ODCS (template + instância orders), cross-links,
agents JIT, pytest dual-tree, `/validar` verde, kernel DE intacto.

## Tasks (82–87)

| # | File | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 82 | `tasks/silver-checklist-odcs/82-kb-pattern-silver-checklist.md` | not started | none | AC1–6,13–14 |
| 83 | `tasks/silver-checklist-odcs/83-crosslinks-pipeline-de.md` | not started | 82 | AC7–9 |
| 84 | `tasks/silver-checklist-odcs/84-agents-jit-de.md` | not started | 82 | AC10 |
| 85 | `tasks/silver-checklist-odcs/85-pytest-kb-dual-tree.md` | not started | 82, 83, 84 | AC1–2,11 |
| 86 | `tasks/silver-checklist-odcs/86-validar-kernel-intacto.md` | not started | 85 | AC11–12 |
| 87 | `tasks/silver-checklist-odcs/87-docs-tasks-index.md` | not started | 86 | meta |

### Ordem sugerida

```text
82 → (83 ∥ 84) → 85 → 86 → 87
```

## Próximo passo

Diga **`harness-build`** ou `implement task 82` na branch `feat/silver-checklist-odcs`.
