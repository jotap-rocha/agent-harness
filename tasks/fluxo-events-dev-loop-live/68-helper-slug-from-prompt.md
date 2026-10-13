# Helper slug-from-prompt

**Status:** done  
**Blocked by:** tasks/fluxo-events-dev-loop-live/67-contrato-dev-loop-map.md

## What to build

Implementar `slug_from_prompt_path`: `PROMPT_FOO.md` → `dev-loop-foo` (lower, kebab,
só `[a-z0-9-]`). Emit/render sob `projetos/dev-loop-{NOME}/fluxo/`.

## Acceptance criteria

- [x] `PROMPT_FOO.md` → `dev-loop-foo` — tested by: `tests/fluxo_events/test_slug_from_prompt.py::test_slug_from_prompt_foo`
- [x] Caracteres inválidos sanitizados / rejeitados conforme contrato — tested by: `tests/fluxo_events/test_slug_from_prompt.py::test_slug_sanitizes`
- [x] Emit grava sob `projetos/dev-loop-*/fluxo/events.jsonl` — tested by: `tests/fluxo_events/test_slug_from_prompt.py::test_emit_path_dev_loop`

## Notes

AC3, AC4. Helper em `config/fluxo_events/`.
