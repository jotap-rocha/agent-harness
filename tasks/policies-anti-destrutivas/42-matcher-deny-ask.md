# Matcher deny vs ask

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/41-contrato-yaml-loader.md

## What to build

Engine de match compartilhada: dado um comando shell e as famílias ativas, retorna
decisão `deny` | `ask` | `allow` com family/pattern. Um pattern deny-hard e um ask
devem ser demonstráveis; Claude e Cursor usam a mesma decisão (adapters só depois).

## Acceptance criteria

- [x] Comando matching pattern deny → decisão deny — tested by: pytest matcher
- [x] Comando matching pattern ask → decisão ask — tested by: pytest matcher
- [x] Comando fora do catálogo → allow — tested by: pytest matcher
- [x] Decisão inclui identificadores de family/pattern (mensagem auditável) — tested by: pytest campos da decisão

## Notes

Severity classes: grill decisão 12. Sem hooks ainda — só engine pura.
