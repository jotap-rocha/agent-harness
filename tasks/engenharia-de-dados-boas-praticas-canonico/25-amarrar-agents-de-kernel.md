# Amarrar agents DE ao kernel

**Status:** done  
**Blocked by:** none

## What to build

Evoluir os **10** agents em `agents/data-engineering/` para incluir uma seção **Kernel DE**
por domínio: amarras a pacotes/IDs (`DE-A*` para todos; A+B / A+B+C / A+D / D003–D004
conforme grill), obrigação de rodar `/validar` (ou CLI validate) em trees DE, e política
**corrigir** vs **baseline/waiver** (owner + expiry). Espelhar em `.cursor/agents/`.

## Acceptance criteria

- [x] Cada um dos 10 agents declara DE-A* + amarra de domínio do grill — tested by: inventário/grep estruturado (AC1)
- [x] Seção Kernel menciona `/validar` ou `canonical_data_check validate` — tested by: assert por arquivo
- [x] Texto cobre baseline/waiver vs corrigir (sem silenciar blocker sem owner+expiry) — tested by: âncora por agent
- [x] Espelho `.claude` ↔ `.cursor` idêntico para os 10 — tested by: assert espelho (AC10)

## Notes

- Fontes: `12-loop3-grill.md` (tabela amarras), `13-loop3-prd.md` AC1, `14-loop3-harness.md`.
- Não alterar checks Python do kernel.
- Amarras: spark→A+B; pipeline-architect→A+B+C; DQ→A+D003/D004; lakehouse/platform→A+D; schema→A+D004; demais→A (+D se cloud).
- **Evidência:** seção `## Conformidade DE (kernel)` + item de checklist em cada agent; testes em
  `tests/data_engineering/test_loop3_agents_commands_kb_bridges.py` (`test_ac1_*`) — 7 passed.
- **Revisor:** aprovado com ressalvas (lote integração Loop 3; 0 bloqueantes após entregas).
- Sem commit (acordo explícito não solicitado).
