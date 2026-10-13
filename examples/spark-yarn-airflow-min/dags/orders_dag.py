"""Stub estático de DAG para checks C001–C003 (não é DAG Airflow executável).

Em runtime Airflow, o equivalente seria::

    from airflow import DAG
    with DAG(dag_id="orders_synth_min", tags=["example", "orders"]) as dag:
        pre_process >> load >> post_process

O arquivo vive em ``dags/`` para ativar o pacote C; checks estáticos
leem tags, fases pré/carga/pós e referência a ``config/spark.conf``.
O CI do canônico não instala Airflow — este módulo só alimenta heurísticas.
"""

from __future__ import annotations

# Metadados lidos pelos checks C001–C003 (heurística estática).
tags = ["example", "orders", "spark-yarn"]
pre_process = "prepare synthetic landing"
load = "spark-submit --properties-file config/spark.conf pipelines/transform.py"
post_process = "validate silver contract"

__all__ = ["tags", "pre_process", "load", "post_process"]
