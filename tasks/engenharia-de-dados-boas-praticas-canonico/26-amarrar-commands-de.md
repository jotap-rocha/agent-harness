# Amarrar commands DE ao gate

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/25-amarrar-agents-de-kernel.md

## What to build

Atualizar os **7** commands em `commands/data-engineering/` para apontar o **gate**
(`/validar` e/ou CLI validate) e o **agent amarrado** já evoluído na task 25. Espelhar
em `.cursor/commands/`.

## Acceptance criteria

- [x] Cada um dos 7 commands nomeia o agent DE correspondente — tested by: inventário commands (AC2)
- [x] Cada command aponta `/validar` ou `python -m config.canonical_data_check validate` — tested by: assert por arquivo (AC2)
- [x] Nenhum command inventa regra normativa nova (aponta YAML/skill) — no test — revisão DoD
- [x] Espelho `.claude` ↔ `.cursor` — tested by: assert espelho (AC10)

## Notes

- Commands: `data-contract`, `data-quality`, `lakehouse`, `migrate`, `pipeline`, `schema`, `sql-review`.
- Depende das amarras dos agents (25) para referências consistentes.
- **Evidência:** seção `## Gate DE (kernel)` em cada command; aponta `data-engineering.yaml` +
  skill `de-conformidade` (quando disponível); testes `test_ac2_*` + `test_migrate_command_*`.
- **Revisor:** aprovado com ressalvas (lote integração Loop 3; 0 bloqueantes após entregas).
- Sem commit.
