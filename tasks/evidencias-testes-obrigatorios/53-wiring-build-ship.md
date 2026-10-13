# Wiring build ship

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/51-check-manifest-ref.md, tasks/evidencias-testes-obrigatorios/52-audit-append-only.md

## What to build

Estender `harness-build` e `harness-ship`: fechar task exige collect→check verde e
append `entregas.jsonl` com `evidencias_ref`; ship revalida checks das tasks do
fluxo. Espelho `.claude`↔`.cursor` dos agents.

## Acceptance criteria

- [x] harness-build documenta bloqueio sem evidence-gate verde — no test — assert texto agent + teste de helper se houver API
- [x] Append entregas exige `evidencias_ref` no schema metrics — tested by: pytest schema/README ou validator
- [x] harness-ship documenta revalidação check antes de fechar — no test — assert texto agent
- [x] Helper/CLI usável pelos agents para close (smoke) — tested by: pytest integração mínima collect+check+ref

## Notes

Revisor permanece ortogonal (task 55). Sem Stop dual.

Revisor: bloqueado (ordem check/append) → aprovado com ressalvas. Gate
tentativas_ate_verde=2. Bug CLI `--command` vs dest subparser corrigido + teste regressão.
