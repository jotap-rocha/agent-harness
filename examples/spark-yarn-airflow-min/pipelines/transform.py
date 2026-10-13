"""Transformação sintética — colunas explícitas (banimento de select-star)."""

from __future__ import annotations

import logging
from typing import Any

LOGGER = logging.getLogger(__name__)


def run(spark: Any, context: dict[str, str]) -> None:
    """Lê bronze sintético e grava silver com schema explícito.

    ``spark: Any`` — sem dependência hard de PySpark no canônico; o tipo concreto
    só existe em runtime do cluster.
    """
    run_id = context["run_id"]
    LOGGER.info("transform.start", extra={"run_id": run_id})
    df = spark.sql(
        "SELECT order_id, amount_cents, currency FROM bronze.orders_synth"
    )
    df.createOrReplaceTempView("silver_orders_synth")
    LOGGER.info("transform.done", extra={"run_id": run_id, "rows": df.count()})
