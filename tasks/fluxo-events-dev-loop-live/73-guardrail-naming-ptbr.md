# Guardrail naming PT-BR

**Status:** done  
**Blocked by:** none

## What to build

Pytest `test_naming_ptbr.py`: falha se substring `flujo` (j) aparecer em nomes/paths
versionados do pacote `fluxo-events` / `config/fluxo_events` / `tests/fluxo_events` /
commands `fluxo-live`. Escopo = pacote, não repo inteiro.

## Acceptance criteria

- [x] Suite verde no tree atual (só `fluxo` com x) — tested by: `tests/fluxo_events/test_naming_ptbr.py::test_no_spanish_flujo_in_package_paths`
- [x] Fixture negativa: path com j seria detectado pela função de scan — tested by: `tests/fluxo_events/test_naming_ptbr.py::test_scan_detects_spanish_flujo`
- [x] Escopo documentado (não varre repo inteiro) — tested by: `tests/fluxo_events/test_naming_ptbr.py::test_scan_roots_are_scoped`

## Notes

AC11. Orthografia: flu+x+o vs flu+j+o. Pode paralelizar com 67–72.
