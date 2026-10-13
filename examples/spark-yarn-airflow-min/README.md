# Example — spark-yarn-airflow-min

Greenfield mínimo do perfil `spark-yarn-airflow` para o DoD do Ship 1.
Dados são **sintéticos** (sem PII). Fora do install automático do harness.

## Validar

Na raiz do canônico:

```bash
python -m config.canonical_data_check validate examples/spark-yarn-airflow-min
```

Esperado: exit `0` (pacotes A+B PASS; C PASS com a DAG mínima em `dags/`).

`dags/orders_dag.py` é um **stub estático** para os checks C001–C003 (tags, fases,
referência a `config/spark.conf`). Não é uma DAG Airflow executável — o CI do
canônico não instala Airflow.

## Layout

| Path | Papel |
|---|---|
| `config/` | pipeline, camadas, `spark.conf` |
| `pipelines/` | transformação Spark (sem `SELECT *`) |
| `contracts/` | contrato versionado sintético |
| `dags/` | stub estático para checks C (não executável) |
| `tests/` | smoke test |
| `data/landing/` | CSV sintético |
| `.harness/data-check/` | marker/perfil + baseline/waivers (gate `/validar` condicional) |
| `OWNER` | ownership declarado |
