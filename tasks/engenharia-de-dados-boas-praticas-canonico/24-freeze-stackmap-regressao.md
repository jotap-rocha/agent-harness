# Freeze stackmap + regressão Loop 1

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/21-example-databricks-sdp-min.md, tasks/engenharia-de-dados-boas-praticas-canonico/22-example-databricks-dlt-min.md, tasks/engenharia-de-dados-boas-praticas-canonico/23-validar-autodetect-espelho.md

## What to build

Fechar o DoD do Loop 2: garantir que `pipeline_dados` no stack_map **não** ganhou keywords
Databricks nem artefatos novos indevidos; regressão verde do example
`spark-yarn-airflow-min` e suíte `tests/data_engineering/` Loop 1; confirmar ausência de
agents/skills/KBs DE **novas** neste ship.

## Acceptance criteria

- [x] `stack_map` `pipeline_dados` inalterado vs baseline Loop 1 (keywords + paths) — tested by: assert/freeze test (AC8)
- [x] `validate` em `examples/spark-yarn-airflow-min` continua PASS — tested by: pytest regressão
- [x] Nenhum path novo sob `agents/data-engineering` ou skill DE nova introduzido pelas tasks 17–23 — no test — revisão DoD (AC9) + inventário freeze
- [x] Suíte `tests/data_engineering/` verde no gate — tested by: pytest área

## Notes

- Fatia de fechamento / anti-regressão antes do ship Loop 2.
- Não implementar features novas aqui.
- GIT_PREFLIGHT: fetch Azure soft-block conhecido/autorizado; working tree 17–23 preservada;
  sem commit/push/stash/reset/clean. Delivery record / commit / ship → parent.
- Colisão `pytest -q` raiz (`test_smoke.py` ×3) corrigida renomeando smokes Databricks:
  `test_smoke_databricks_sdp.py` / `test_smoke_databricks_dlt.py` (spark-yarn mantém
  `test_smoke.py`). Sem mudar testpaths global; examples continuam coletados.
- Regressão `/validar` no canônico: sentinel conservador exige conjuntamente
  `data-engineering.yaml`, `config/canonical_data_check/`, `CLAUDE.md` e `AGENTS.md`.
  Somente esse root canônico não ativa por sinais internos; filhos/monorepos, inclusive
  pipelines sob `examples/`, preservam o auto-detect.
- Revisor: **aprovado com ressalvas** — 0 bloqueantes; correções solicitadas aplicadas.

### Evidências (Task 24)

| Etapa | Resultado |
|---|---|
| RED (test-first) | freeze: basename collision + canônico false-trigger (+ inventário KB ajustado) |
| GREEN focado | sentinel + freeze → **24 passed** |
| pytest raiz | `PYTHONPATH=. pytest -q` → **186 passed** |
| pytest DE | `PYTHONPATH=. pytest -q tests/data_engineering/` → **138 passed** |
| ruff focado | `de_marker.py` + testes da revisão/freeze → All checks passed |
| mypy focado | `de_marker.py` + testes da revisão/freeze → Success (3 arquivos) |
| data-check helper canônico | `data_check_validate_argv('.')` → **None** |
| Examples validate | spark-yarn / sdp / dlt → exit 0 |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; policy genérica removida e STATUS/Notes sincronizados |

### Sugestão de melhoria (SOLID)

Se outros repositórios canônicos surgirem, extrair um port `CanonicalRootDetector`
injetável evita ampliar o sentinel dentro da policy do `/validar`.
