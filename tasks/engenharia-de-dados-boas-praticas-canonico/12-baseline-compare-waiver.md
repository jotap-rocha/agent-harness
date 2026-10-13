# Baseline compare waiver

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/10-cli-validate-abc.md

## What to build

Implementar na CLI os comandos `baseline` e `compare` com **ratchet**: findings já baselineados não quebram; finding **novo** falha. Suportar waiver pontual com **owner + expiry** obrigatórios; sem isso o waiver não silencia blocker.

Artefatos de runtime no projeto-alvo: `.harness/data-check/` (`project_profile.yaml`, `baseline.json`, waivers). Templates/seed no canônico para o install (consumidos na task 15).

## Acceptance criteria

- [x] `baseline` grava snapshot de findings no path `.harness/data-check/` do alvo — tested by: teste de integração em tmp dir
- [x] `compare` falha só em finding novo vs baseline — tested by: pytest ratchet (AC4)
- [x] Waiver sem owner ou sem expiry **não** silencia blocker — tested by: pytest (AC5)
- [x] Waiver válido (owner + expiry futuro) silencia o rule_id correspondente até expiry — tested by: pytest
- [x] Schema/template do baseline documentado no canônico (não baseline do sql-capacity) — no test — template/docs; coberto indiretamente pelo install na 15 (+ assert estrutural de templates)

## Notes

- sql-capacity: **não** gravar baseline lá.
- Idempotência: reexecutar baseline/compare no mesmo estado é seguro.
- GIT_PREFLIGHT: soft-block `git fetch`/sync remoto ACKNOWLEDGED (Azure 403); execução na branch local `feat/de-boas-praticas-canonico`. Tasks 09–11 preservadas (untracked/modificadas).
- RED test-first: `PYTHONPATH=. python -m pytest -q tests/data_engineering/test_baseline_compare_waiver.py` → **12 failed** (ModuleNotFoundError `baseline`, CLI sem subcomandos, templates ausentes). Evidência em sessão.
- GREEN: 14 testes no arquivo Task 12; área DE 43 passed; suíte completa 89 passed.
- Gate: verde (tentativas_ate_verde=2 — 1ª após implementação; 2ª após ressalvas do revisor: fingerprint sem `:linha`, UTC expiry, baseline corrompido → EXIT_USAGE, SCHEMA). `ruff` OK; `mypy` OK.
- Revisor: 1ª rodada `aprovado com ressalvas` (fingerprint+linha, waiver path-scope, baseline silencioso, UTC, DoD). Corrigidas as relevantes + doc SCHEMA. 2ª rodada `aprovado com ressalvas` leves (SCHEMA DE-USAGE — documentado; DoD — fechado agora). 0 bloqueantes.
- Delivery record pendente: `metrics/entregas.jsonl` exige SHA do commit; commit não autorizado. Registrar só após acordo explícito (Tasks 09–12 pendentes de delivery record).
- API: `write_baseline` / `compare_project` · CLI: `python -m config.canonical_data_check {baseline|compare} <path>` · runtime `.harness/data-check/` · seed `config/canonical_data_check/templates/data-check/`.
