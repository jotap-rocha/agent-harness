# Docs ADR sync

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/54-install-foundation-seed.md, tasks/evidencias-testes-obrigatorios/55-dod-agents-totasks.md

## What to build

Fechar docs do ship: cheatsheet, ADR, command `/evidencias` (SHOULD), sync
CLAUDE/AGENTS/CONTEXT, cross-link ortogonal a agent-policies/`/validar`.

## Acceptance criteria

- [x] `docs/evidence-gate-cheatsheet.md` existe — no test — presença
- [x] ADR em `docs/adr/` + índice — no test — presença
- [x] Command evidencias (claude+cursor) aponta CLI — no test — presença
- [x] CLAUDE/AGENTS/CONTEXT listam kernel evidence-gate — no test — sync/assert strings
- [x] Cross-link: Bash deny ≠ aceite; `/validar` permanece — no test — cheatsheet/ADR

## Notes

Fecha ACs de docs do PRD. Dogfood: usar o gate nas próximas tasks do canônico.

Revisor: aprovado com ressalvas (commands 23 + `/evidencias` no stack_map — aplicados).
Gate tentativas_ate_verde=1.
