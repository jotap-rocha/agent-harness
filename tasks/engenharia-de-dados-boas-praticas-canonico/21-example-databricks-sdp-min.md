# Example databricks-sdp-min

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/19-checks-databricks-cloud.md

## What to build

Criar `examples/databricks-sdp-min/` greenfield (stubs estáticos, sem runtime Databricks)
que passa `validate` com A + D aplicável ao perfil `databricks-sdp-medallion`. Fora do
install automático. README curto de uso.

## Acceptance criteria

- [x] `validate` no example → PASS (exit 0) — tested by: pytest + subprocess (AC2)
- [x] Layout inclui sinais SDP/DAB mínimos exigidos pelo pacote D — tested by: asserts de layout + validate
- [x] Dados/stubs sem PII; sem secrets hardcoded — tested by: revisão + checks A
- [x] Example **não** está no `stack_map` — tested by: assert ausência (como spark-yarn-min)

## Notes

- Nome acordado `[inferido]`: `examples/databricks-sdp-min/`.
- CI do canônico não instala Databricks SDK.
- Sem `project_profile.yaml` de override — perfil vem só do auto-detect DAB+SDP
  (`databricks-sdp-medallion`). Marker separado fica para baseline futuro se necessário.
- GIT_PREFLIGHT: fetch Azure soft-block conhecido/autorizado; working tree das
  Tasks 17–20 preservada; sem commit/push/stash/reset/clean.
- Tasks 22–24 **não** implementadas neste turno.
- Smoke stub (`tests/test_smoke.py`) mantido como aceitável (espelha Loop 1).

### Evidências (Task 21)

| Etapa | Resultado |
|---|---|
| RED (test-first) | 5 falhas (layout/perfil/validate/CLI/PII) antes do example; stack_map já passava |
| GREEN focado | `test_example_databricks_sdp_min.py` → 6 passed |
| Gate DE | `pytest tests/data_engineering/` → 115+ passed |
| Lint focado | `ruff check` → OK |
| Tipos focado | `mypy --explicit-package-bases` → Success (teste + stub SDP) |
| CLI | `validate examples/databricks-sdp-min` → exit 0, profile `databricks-sdp-medallion`, D003 skip |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; ressalva acionável aplicada (assert D001/D002/D004/D005 não skip e sem fail); smoke stub aceito |
