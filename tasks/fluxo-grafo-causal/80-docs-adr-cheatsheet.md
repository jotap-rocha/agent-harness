# Docs ADR cheatsheet

**Status:** done  
**Blocked by:** tasks/fluxo-grafo-causal/75-emit-causal-ids.md

## What to build

SHOULD: atualizar `docs/fluxo-events-cheatsheet.md` e addendum ADR-005 com campos
causais, stack, dois SVGs, §1.3. Orthografia **fluxo** (x). Sem agent “fluxo officer”.

## Acceptance criteria

- [x] Cheatsheet menciona event_id/run_id/parent, stack, dois SVGs — tested by: `tests/fluxo_events/test_docs_causal.py::test_cheatsheet_causal`
- [x] ADR-005 addendum presente — tested by: no test — docs review + waiver humano
- [x] Sem “fluxo officer”; naming PT-BR ok nos docs tocados — tested by: `tests/fluxo_events/test_naming_ptbr.py` (regressão) + review

## Notes

AC17, AC19 (docs). Pode paralelizar com 76–78.

Auto-revisão (revisor-codigo estilo): **aprovado**. Sem bloqueantes.
