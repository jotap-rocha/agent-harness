# Emit causal IDs

**Status:** done  
**Blocked by:** none

## What to build

Estender `ALLOWED_KEYS` com `event_id`, `run_id`, `parent_event_id`. Emits novos geram
UUID v4 para `event_id` (sempre se omitido) e `run_id` (se omitido). Load/render aceitam
eventos antigos sem esses campos. Fixtures só metadados (sem PII/prompt/secret).

## Acceptance criteria

- [x] `ALLOWED_KEYS` inclui os três campos — tested by: `tests/fluxo_events/test_emit_causal_ids.py::test_allowed_keys_include_causal`
- [x] Emit gera `event_id` UUID v4 se omitido — tested by: `tests/fluxo_events/test_emit_causal_ids.py::test_generates_event_id`
- [x] `run_id` auto se omitido; override respeitado — tested by: `tests/fluxo_events/test_emit_causal_ids.py::test_run_id_auto_and_override`
- [x] Evento antigo sem IDs ainda carrega/renderiza — tested by: `tests/fluxo_events/test_emit_causal_ids.py::test_legacy_events_without_ids`
- [x] Fixtures sem prompt/PII/secret — tested by: `tests/fluxo_events/test_emit_causal_ids.py::test_fixtures_metadata_only`

## Notes

Slug: `fluxo-grafo-causal`. Branch: `feat/fluxo-grafo-causal`. AC1–3, AC6, AC18. `version: 1` aditivo.

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
