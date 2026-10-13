# Example databricks-dlt-min

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/19-checks-databricks-cloud.md

## What to build

Criar `examples/databricks-dlt-min/` greenfield (stubs estáticos) que passa `validate` com
A + D aplicável ao perfil `databricks-dlt-legacy`, incluindo quarentena/expectations
mínimas. Fora do install automático. README curto.

## Acceptance criteria

- [x] `validate` no example → PASS (exit 0) — tested by: pytest + subprocess (AC3)
- [x] Layout inclui sinais DLT + quarentena exigidos pelo pacote D — tested by: layout + validate
- [x] Sem PII/secrets; fora do `stack_map` — tested by: asserts + revisão

## Notes

- Nome acordado `[inferido]`: `examples/databricks-dlt-min/`.
- Pode avançar em paralelo com task 21 após 19.
- Sem `project_profile.yaml` de override — perfil vem só do auto-detect DAB+DLT
  (`databricks-dlt-legacy`). Marker separado fica para baseline futuro se necessário.
- GIT_PREFLIGHT: fetch Azure soft-block conhecido/autorizado; working tree das
  Tasks 17–21 preservada; sem commit/push/stash/reset/clean.
- Tasks 23–24 **não** implementadas neste turno.
- Smoke stub renomeado para `tests/test_smoke_databricks_dlt.py` na Task 24 para
  evitar colisão de coleta no `pytest -q` raiz; SDP usa
  `tests/test_smoke_databricks_sdp.py`.

### Evidências (Task 22)

| Etapa | Resultado |
|---|---|
| RED (test-first) | 5 falhas (layout/perfil/validate/CLI/PII) antes do example; stack_map já passava |
| GREEN focado | `test_example_databricks_dlt_min.py` → 6 passed |
| Gate DE | `pytest tests/data_engineering/` → 121 passed |
| Lint focado | `ruff check` → OK |
| Tipos focado | `mypy --explicit-package-bases` → Success (teste + stub DLT) |
| CLI | `validate examples/databricks-dlt-min` → exit 0, profile `databricks-dlt-legacy`, D002 skip |
| Revisor | **aprovado** — 0 bloqueantes; smoke stub aceito no escopo do example estático |
