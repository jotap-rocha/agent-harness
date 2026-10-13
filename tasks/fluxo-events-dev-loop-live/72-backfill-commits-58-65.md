# Backfill commits 58-65

**Status:** done  
**Blocked by:** none

## What to build

One-shot: em `metrics/entregas.jsonl`, issues 58–65 com `"commit": "pending"` passam a
`"commit": "e4dfc69"`. Não alterar outras linhas. Teste assertivo.

## Acceptance criteria

- [x] Issues 58–65 têm commit `e4dfc69` — tested by: `tests/fluxo_events/test_backfill_commits.py::test_entregas_58_65_sha`
- [x] Nenhuma outra issue foi alterada indevidamente — tested by: `tests/fluxo_events/test_backfill_commits.py::test_other_issues_untouched`
- [x] Não resta `pending` em 58–65 — tested by: `tests/fluxo_events/test_backfill_commits.py::test_no_pending_58_65`

## Notes

AC10. SHA fechado no grill. Pode paralelizar com 67–71.
