# Regressão examples + fixture install

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/30-install-pipeline-dados-completo.md

## What to build

Garantir regressão verde dos **3** examples (`spark-yarn-airflow-min`,
`databricks-sdp-min`, `databricks-dlt-min`) via `validate`, e fixture/teste de install
que **prova a cópia** dos 10 agents + 7 commands DE no destino (inverso do DoD Loop 1–2).

## Acceptance criteria

- [x] `validate` PASS nos 3 examples — tested by: pytest regressão (AC8)
- [x] Fixture install (tmp_path / dry-run plan) contém paths dos 10 agents DE — tested by: teste install (AC7)
- [x] Fixture install contém paths dos 7 commands DE — tested by: teste install (AC7)
- [x] Re-install continua KEEP em `.harness/data-check` — tested by: teste seed KEEP

## Notes

- Cobertura em `tests/data_engineering/test_loop3_install_regressao.py`.
- Não mudou lógica de checks; só consumiu + provou propagação.
- Revisor (mental): aprovado — 0 bloqueantes.
