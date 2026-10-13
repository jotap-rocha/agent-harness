# CLI validate A+B+C

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/09-yaml-contrato-loader.md

## What to build

Entregar a CLI `canonical-data-check` (ou nome acordado no ADR leve) com o comando `validate` que executa checks **A** (Universal blockers) e **B** (perfil `spark-yarn-airflow` blockers) e trata **C** (Airflow) como condicional: skip se não houver DAG/orquestração Airflow detectada.

Usar fixtures de diretório (mínimas) para provar PASS/FAIL por pacote — o example completo vem na task 11.

## Acceptance criteria

- [x] Entrypoint CLI expõe `validate` apontando a um path de projeto — tested by: invocação CLI em teste de integração (subprocess ou API pública)
- [x] Pacote A bloqueia violações Universal (secrets, destrutivo sem gate, layout mínimo, run_id/logging, owner) em fixtures — tested by: pytest com fixture “ruim” → exit/fail com rule_ids
- [x] Pacote B bloqueia violações de medalhão/contrato/`select *` no perfil — tested by: pytest com fixture de perfil
- [x] Pacote C faz skip (não falha) quando Airflow/DAG ausente — tested by: pytest AC3
- [x] Exit codes estáveis e findings com `rule_id` — tested by: assert na API de resultado

## Notes

- Reutilizar IDs do YAML da task 09.
- Não gravar baseline ainda (task 12).
- SI c+d: checks estáticos; não ler dados de negócio sensíveis além de paths/conteúdo necessário à heurística.
- GIT_PREFLIGHT: `git fetch` HTTP 403 (proxy); execução na branch local `feat/de-boas-praticas-canonico`.
- RED test-first: `python -m pytest -q tests/data_engineering/test_validate_cli.py` falhou na coleta com `ModuleNotFoundError: No module named 'config.canonical_data_check'` (exit 2, 1 error).
- GREEN: 24 testes em `tests/data_engineering/`; suíte completa 69 passed.
- Gate: verde (tentativas_ate_verde=2 — 1ª verde da área após implementação; 2ª após corrigir ressalvas do revisor). Comandos: `ruff check` área OK; `mypy` área OK; `pytest -q tests/data_engineering/` + suíte completa.
- Revisor: 1ª rodada `aprovado com ressalvas` (MULTILINE Airflow, OWNER vazio, help exit, .env.example, A001 JSON); corrigidas. 2ª rodada `aprovado`, 0 bloqueantes, 0 ressalvas.
- Delivery record pendente: `metrics/entregas.jsonl` exige SHA do commit; commit não autorizado. Registrar só após acordo explícito (Task 09 e 10 pendentes de delivery record).
- Entrypoint: `python -m config.canonical_data_check validate <path>` · API: `validate_project` / `cli.main`.
