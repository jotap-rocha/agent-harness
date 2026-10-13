# Install pacote mínimo DE

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/09-yaml-contrato-loader.md, tasks/engenharia-de-dados-boas-praticas-canonico/12-baseline-compare-waiver.md  
**Review:** aprovado com ressalvas ([revisor](f12cd502-c578-452a-89b8-7ac960e9ea69)); ressalva de normalização do manifest no KEEP de seed aplicada.

## What to build

Ampliar a categoria `pipeline_dados` do `install-harness` / `stack_map` para propagar o **pacote mínimo verificável**: subset da norma, CLI utilizável, rule pipeline, KB pipeline, e seed de `.harness/data-check/` (`project_profile.yaml` + baseline vazio/template). **Não** copiar os 10 agents nem 7 commands DE.

## Acceptance criteria

- [x] Install (fixture/dry-run/teste) cria `.harness/data-check/` no destino com perfil default `spark-yarn-airflow` — tested by: `test_install_cria_harness_data_check_com_perfil_default` (AC8)
- [x] Pacote inclui artefatos necessários para rodar a CLI no filho — tested by: `test_install_pacote_permite_cli_e_nao_copia_agents_de`
- [x] Install **não** copia `agents/data-engineering/*` (10 agents) — tested by: assert ausência (AC8, AC11)
- [x] Keywords/detecção de pipeline_dados documentadas ou cobertas pelo stack_map existente ampliado — tested by: `test_stack_map_...` + `test_build_plan_force_...`
- [x] Seed-once: re-install **não** apaga baseline/waivers (`seed: true` → KEEP; manifest `customized: true`) — tested by: `test_reinstall_...` + `test_build_plan_seed_keep_...`

## Notes

- Sem `--scaffold` neste ship.
- Espelhar mudanças de skills/docs de install em `.claude` e `.cursor` se tocadas.
- Artefato seed: `from: config/canonical_data_check/templates/data-check`, `seed: true`.
