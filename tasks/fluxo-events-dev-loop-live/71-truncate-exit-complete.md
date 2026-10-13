# Truncate EXIT_COMPLETE

**Status:** done  
**Blocked by:** tasks/fluxo-events-dev-loop-live/69-render-dual-map-dev.md, tasks/fluxo-events-dev-loop-live/70-wiring-ux-crafter-executor.md

## What to build

No `EXIT_COMPLETE` do executor: emit exit + `truncate --keep 100` + re-render no slug
`dev-loop-*`. Fail soft se FS falhar.

## Acceptance criteria

- [x] Truncate no path Dev deixa ≤100 linhas e re-render — tested by: `tests/fluxo_events/test_dev_loop_truncate.py::test_truncate_keep_100_dev_slug`
- [x] Wiring executor documenta EXIT_COMPLETE → truncate — tested by: `tests/fluxo_events/test_dev_loop_truncate.py::test_executor_mentions_truncate`
- [x] Fail soft em erro de truncate — tested by: `tests/fluxo_events/test_dev_loop_truncate.py::test_truncate_fail_soft`

## Notes

AC8, AC9.
