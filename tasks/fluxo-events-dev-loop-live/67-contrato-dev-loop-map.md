# Contrato dev-loop-map

**Status:** done  
**Blocked by:** none

## What to build

Estender `fluxo-events.yaml` com `dev_loop_map` (fases 0–6: LOAD→…→SYNC; agents
`prompt-crafter`, `dev-loop-executor`) e loader tipado. Preservar sdd_map, caps e
ausência de SLA numérico.

## Acceptance criteria

- [x] Contrato carrega `dev_loop_map` 0–6 com agents esperados — tested by: `tests/fluxo_events/test_dev_loop_map.py::test_loads_dev_loop_map`
- [x] Loader rejeita mapa Dev inválido — tested by: `tests/fluxo_events/test_dev_loop_map.py::test_invalid_dev_loop_map_fails`
- [x] Caps 2 MiB / truncate N=100 / sem latência preservados — tested by: `tests/fluxo_events/test_dev_loop_map.py::test_limits_unchanged`

## Notes

Slug: `fluxo-events-dev-loop-live`. Branch: `feat/fluxo-events-dev-loop-live`. AC1, AC16.
