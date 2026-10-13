# Bypass e fail modes

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/42-matcher-deny-ask.md

## What to build

Camada de guard sobre o matcher: `HARNESS_ALLOW_DESTRUCTIVE=1` short-circuita
deny-hard com trilha de log (sem secret/PII); falha do engine em deny-hard =
fail closed; falha em ask / opt-in = fail open.

## Acceptance criteria

- [x] Com env de bypass, deny-hard vira allow consciente + log sem secret — tested by: pytest guard + env
- [x] Engine quebrada / YAML ilegível em path deny-hard → bloqueia (fail closed) — tested by: pytest guard
- [x] Engine quebrada em path ask → não trava Dev Loop (fail open) + aviso — tested by: pytest guard
- [x] Sem bypass, deny-hard continua deny — tested by: pytest regressão

## Notes

Env canônica: `HARNESS_ALLOW_DESTRUCTIVE=1`. ADR prod/DDL continua na rule seguranca
(não substituído por bypass).
