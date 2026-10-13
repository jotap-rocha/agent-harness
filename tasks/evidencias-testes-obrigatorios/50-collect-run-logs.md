# Collect run logs

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/49-contrato-yaml-loader.md

## What to build

`collect` executa o comando do critério, grava log em
`evidencias/logs/<task>/<criterion>.log`, registra exit_code no manifesto atual
(LWW). Cap 2 MiB: se exceder → falha (sem prova truncada silenciosa). Alvo de tempo
≤ 2× o comando (sem hard kill absoluto no yaml).

## Acceptance criteria

- [x] Collect com comando ok → log + exit 0 no manifesto — tested by: pytest collect fixture
- [x] Collect com comando falho → exit ≠ 0 gravado; check posterior falha — tested by: pytest
- [x] Log > 2 MiB → collect falha (não grava prova válida truncada) — tested by: pytest cap
- [x] Re-collect na mesma task sobrescreve prova atual (LWW) — tested by: pytest

## Notes

G1: só alvo 2×. G3: fail se cap. Sem secrets/PII nos logs de fixture.

AC2 metade “check posterior falha” deferida à task 51 (`check_task`); aqui grava
exit ≠ 0 no manifesto. Audit append já no collect; cobertura explícita na task 52.

Revisor: bloqueado (F841) → corrigido → aprovado com ressalvas (paths hardcoded /
check deferido). Gate tentativas_ate_verde=2.
