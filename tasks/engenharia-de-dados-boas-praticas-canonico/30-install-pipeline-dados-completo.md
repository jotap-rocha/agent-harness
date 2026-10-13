# Install pipeline_dados completo

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/25-amarrar-agents-de-kernel.md, tasks/engenharia-de-dados-boas-praticas-canonico/26-amarrar-commands-de.md, tasks/engenharia-de-dados-boas-praticas-canonico/28-kb-databricks.md, tasks/engenharia-de-dados-boas-praticas-canonico/29-skill-de-conformidade.md

## What to build

Expandir a categoria `pipeline_dados` no `stack_map` (+ prosa em
`install-harness/SKILL.md`) para propagar **todos** os 10 agents e 7 commands DE, mais
artefatos da skill `de-conformidade` e KB `databricks` conforme plan. **Preservar**
`seed: true` / KEEP em `.harness/data-check`. Reescrever asserts de freeze/install que
hoje **proíbem** agents/commands.

## Acceptance criteria

- [x] `stack_map` `pipeline_dados` declara paths dos 10 agents + 7 commands (+ skill/KB acordados) — tested by: teste stack_map (AC6)
- [x] `SKILL.md` install-harness documenta o pacote completo (não mais “NÃO copiar agents”) — no test — revisão + grep prosa
- [x] Seed `.harness/data-check` permanece `seed: true` (KEEP no re-install) — tested by: testes KEEP existentes/adaptados (AC6)
- [x] Asserts de **ausência** de agents/commands DE removidos ou invertidos neste pacote de testes — tested by: suíte install atualizada (AC7 parcial)
- [x] Espelho `stack_map` / SKILL `.claude` ↔ `.cursor` — tested by: assert espelho

## Notes

- Keywords do detector permanecem `airflow|spark|dbt` (PRD: não exigir keywords Databricks).
- `_comment` do stack_map atualizado para política Loop 3 (pacote completo).
- KBs acordados: `databricks` + adjacentes (airflow, spark, lakehouse, data-quality, dbt,
  data-modeling, sql-patterns, streaming, cloud-platforms) + `pipeline` já existente.
- Freeze Loop 3 fechado na task 32; aqui `test_install_pacote_minimo.py` alinhado.
- Revisor (mental): aprovado com ressalvas — prosa CLAUDE/AGENTS/CONTEXT ainda Loop 2
  (sync no ship); inventário FROZEN duplicado em 2 arquivos de teste (aceitável).
