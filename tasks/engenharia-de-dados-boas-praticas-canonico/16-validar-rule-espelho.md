# Validar condicional + rule espelho

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/11-example-spark-yarn-min.md, tasks/engenharia-de-dados-boas-praticas-canonico/15-install-pacote-minimo.md  
**Review:** aprovado com ressalvas ([revisor](a477f2a0-95c6-473d-b839-1d273a805899)); ressalvas leves de resolve/prosa aplicadas.

## What to build

Estender `/validar` para invocar o data-check **somente** se existir marker/perfil DE (preferência do plan: `.harness/data-check/project_profile.yaml`). Sem marker, `/validar` permanece ruff+mypy+pytest. Atualizar `rules/pipeline.md` (+ espelho `.mdc`) para declarar que IDs/severidade vêm de `data-engineering.yaml`. Garantir espelho `.claude` ↔ `.cursor` nas promoções deste ship.

## Acceptance criteria

- [x] Sem `project_profile` / marker DE → `/validar` **não** invoca data-check — tested by: `test_sem_marker_nao_invoca_data_check` + docs em `validar.md` (AC9)
- [x] Com marker DE → `/validar` invoca data-check — tested by: `test_com_marker_invoca_data_check` + example com seed (AC9)
- [x] `rules/pipeline.md` referencia `data-engineering.yaml` como fonte normativa de IDs — tested by: `test_pipeline_rule_referencia_norma_yaml` (AC10 parcial)
- [x] Espelho `.cursor/rules/pipeline.mdc` e commands tocados permanecem simétricos — tested by: `test_validar_commands_espelho_identico` + `test_pipeline_rule_corpo_espelhado` (AC10)
- [x] Nenhuma skill/agent/KB DE **nova** introduzida nesta task — revisão: só `de_marker.py` + commands/rules/example seed (AC11)

## Notes

- Helper: `config.canonical_data_check.de_marker` (`has_de_marker`, `data_check_validate_argv`).
- Hook `Stop` permanece só ruff/mypy/pytest (ship mínimo — harness plan).
- Example `spark-yarn-airflow-min` ganhou `.harness/data-check/` (marker para o gate condicional).
