# YAML contrato + loader DE

**Status:** done  
**Blocked by:** none

## What to build

Criar a fonte normativa `data-engineering.yaml` na raiz do canônico (Universal + perfil `spark-yarn-airflow`, IDs, categorias, severidades) e o pacote loader/contrato em `config/data_engineering/` no mesmo padrão de `git-hygiene` (carregar YAML, validar schema mínimo, expor API tipada para a CLI).

Esta fatia fecha o caminho: arquivo normativo → load → teste de contrato verde — sem ainda implementar checks reais.

## Acceptance criteria

- [x] `data-engineering.yaml` existe na raiz com `version` e perfil `spark-yarn-airflow` declarado — tested by: pytest de contrato/loader (AC1)
- [x] Loader rejeita YAML inválido / campos obrigatórios ausentes — tested by: testes unitários de contrato (casos negativos)
- [x] Pacote Python espelha o padrão `config/git_hygiene/` (load from path, from_mapping) — tested by: import + testes unitários
- [x] IDs de regras A (Universal), B (perfil) e C (Airflow condicional) estão presentes no YAML mesmo que checks ainda sejam stubs — tested by: assert de presença de IDs no contrato carregado

## Notes

- Loop 1 only; sem perfis Databricks.
- Não criar agents/skills/KBs novas.
- Fonte: `02-prd.md`, `03-harness.md`, decisões 1–3 e 12 do grill.
- GIT_PREFLIGHT: `git fetch` falhou com HTTP 403 no proxy; execução autorizada na branch local isolada `feat/de-boas-praticas-canonico`.
- RED test-first: `python -m pytest -q tests/data_engineering` falhou antes da implementação com 1 erro de coleta (`ModuleNotFoundError: config.data_engineering`), exit code 2.
- GREEN da área: 10 testes passaram após implementação e reforços da revisão.
- Gate: verde na 1ª tentativa (`ruff` e `mypy` da área; 10 testes da área; suíte completa com 55 testes). Gate repetido após ressalvas e permaneceu verde.
- Revisor: primeira rodada `aprovado com ressalvas`; ressalvas corrigidas. Segunda rodada `aprovado`, 0 bloqueantes e 0 ressalvas.
- Delivery record pendente: `metrics/entregas.jsonl` exige o SHA da entrega, mas commit não foi autorizado. Registrar somente após acordo explícito e commit desta task.
