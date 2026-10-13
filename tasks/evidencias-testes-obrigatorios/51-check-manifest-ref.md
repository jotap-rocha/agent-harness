# Check manifest ref

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/50-collect-run-logs.md

## What to build

`check` valida manifesto por task: cada critério tem ≥1 path de teste (ou waiver
humano), log existe, exit_code coerente, e `evidencias_ref` em delivery aponta o
manifesto. Sem prova válida → exit ≠ 0.

## Acceptance criteria

- [x] Manifesto válido + logs ok → check exit 0 — tested by: pytest check
- [x] Critério sem teste e sem waiver → check falha — tested by: pytest
- [x] Log ausente ou exit ≠ 0 → check falha — tested by: pytest
- [x] `evidencias_ref` quebrado/ausente em linha de entregas → check/ship path falha — tested by: pytest schema entregas ou check wiring

## Notes

Waiver: `waiver: { human: true, reason: "..." }` no critério (AC4 PRD).

Revisor: bloqueado (F841) → aprovado com ressalvas (`evidencias_ref` só com
`--entregas`; sem smoke CLI). Gate tentativas_ate_verde=2.
