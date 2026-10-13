# Example spark-yarn-airflow-min

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/10-cli-validate-abc.md

## What to build

Criar o projeto exemplo `examples/spark-yarn-airflow-min/` no canônico (fora do install automático) que passa `validate` nos pacotes **A+B**. Pode incluir DAG mínima opcional; se incluir, C pode PASS; se não, C skip.

Demonstra o DoD greenfield do Ship 1 no próprio framework.

## Acceptance criteria

- [x] Example existe com layout mínimo alinhado ao perfil (`config/`, jobs/pipelines, tests, owner, run_id/logging) — tested by: inspeção estrutural + validate
- [x] `canonical-data-check validate` no example → **PASS A+B** — tested by: pytest de integração (AC2)
- [x] Pacote C → skip ou PASS se DAG presente — tested by: pytest (AC3); stub em `dags/` → C aplicável sem skip/fail
- [x] README curto do example (COULD) descreve como rodar a CLI — no test — docs only
- [x] Example **não** é copiado pelo install automático — tested by: assert em config/stack_map (paths `.claude` e `.cursor`); Task 15 completa o install

## Notes

- Não usar dados reais/PII.
- Fora do `install-harness --scaffold` (Loop futuro).
- GIT_PREFLIGHT: `git fetch` HTTP 403 (proxy); branch local `feat/de-boas-praticas-canonico`. Working tree com mudanças 09/10 preservadas.
- RED test-first (prova nesta sessão): mover example → `python -m pytest -q tests/data_engineering/test_example_spark_yarn_min.py` → **4 failed, 1 passed** (stack_map já sem example); restaurado → 5 passed.
- GREEN: layout + validate A+B exit 0; C PASS silencioso com stub `dags/` (detect_airflow + sem skip); CLI subprocess; stack_map sem markers do example.
- Gate: verde (tentativas_ate_verde=1 após example+fixes). `ruff` OK; `mypy` OK; `pytest -q tests/data_engineering/` → 29 passed; suíte completa → 75 passed.
- Revisor: 1ª rodada `aprovado com ressalvas` (AC3 fraco no PASS silencioso, `Any` sem doc, stub DAG pouco explícito, notes). Corrigidas. 2ª rodada `aprovado`, 0 bloqueantes, 0 ressalvas.
- Revalidação final: revisor apontou AC3 permissivo e cabeçalho desatualizado no dashboard; corrigidos. Nova rodada `aprovado`, 0 bloqueantes, 0 ressalvas.
- Delivery record pendente: `metrics/entregas.jsonl` exige SHA do commit; commit não autorizado. Registrar só após acordo explícito (Tasks 09–11 pendentes de delivery record).
- `dags/orders_dag.py` é stub estático para heurísticas C001–C003 — não é DAG Airflow executável (CI sem Airflow).
