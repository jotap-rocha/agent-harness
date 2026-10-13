# Docs ADR dogfood sync

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/47-seed-install-foundation.md

## What to build

Fechar o ship documental e dogfood: ponte em `seguranca` (+ `.mdc`), cheatsheet,
ADR do kernel agent-policies, honesty §1.3 em CONTEXT, sync `CLAUDE.md`/`AGENTS.md`,
dogfood canônico (settings/hooks alinhados ao generate; limpar paths de máquina no
template/dogfood). Cross-link `DE-A002` sem unificar kernels.

## Acceptance criteria

- [x] Ponte SI + §1.3 + bypass documentados em seguranca (espelho mdc) — no test — assert arquivo/teste leve de presença
- [x] Cheatsheet `docs/agent-policies-cheatsheet.md` existe — no test — presença
- [x] ADR registrado em `docs/adr/` — no test — presença + índice
- [x] CLAUDE/AGENTS/CONTEXT atualizados (contagem/paths do kernel) — no test — sync-context ou assert strings
- [x] Dogfood canônico: deny/hooks alinhados; sem path de máquina obrigatório no generate filho — tested by: pytest generate + smoke settings
- [x] Cross-link DE-A002 ortogonal documentado — no test — cheatsheet/ADR

## Notes

Sem agent policy officer. Sem Edit policies server-side. Fecha ACs de docs do PRD.
Espelho `.claude`↔`.cursor` na mesma sessão.

## Notes (fechamento)
Ressalvas: status/README atualizados neste fechamento; ask Claude documentado na cheatsheet/§1.3.

