# Freeze Loop 3 + DoD gate

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/31-regressao-examples-install.md

## What to build

Fechar o DoD do Loop 3: **novo baseline de freeze** (inventário esperado: 10 agents,
7 commands, skill `de-conformidade`, KB `databricks`, `pipeline_dados` expandido) e
rodar o **gate completo** (ruff + mypy + pytest; validate nos 3 examples). Sem features
novas — só anti-regressão e inventário.

## Acceptance criteria

- [x] Freeze testa inventário Loop 3 (agents/commands/skill/KB/databricks + artefatos install) — tested by: `test_freeze_*` reescrito (AC9)
- [x] Freeze exige espelho `.claude`↔`.cursor` nos artefatos críticos — tested by: assert espelho (AC10)
- [x] Gate completo verde no canônico (área DE + regressões) — tested by: ruff/mypy/pytest + validate examples (AC9)
- [x] Sem live API / secrets introduzidos pelo Loop 3 — no test — revisão SI (AC11)

## Notes

- Substitui semanticamente o freeze “proibir agents/KB novas” do Loop 2
  (`test_stack_map_pipeline_dados_frozen_vs_loop3`, `test_inventario_agents_skills_kbs_loop3`).
- Delivery record gravado; commit / push / ship → parent com acordo explícito.
- Soft-block fetch Azure conhecido — não bloqueou o gate local.
- Revisor (mental): **aprovado com ressalvas** (0 bloqueantes):
  1. CLAUDE.md / AGENTS.md / CONTEXT.md ainda descrevem pacote mínimo Loop 2 — sync no
     `harness-ship` / `/sync-context`.
  2. Contagens inventário (20 skills / 19 KBs) espelhadas em mais de um módulo de teste.
