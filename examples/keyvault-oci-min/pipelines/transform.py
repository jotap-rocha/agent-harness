"""Transformação sintética — colunas explícitas; secrets via facade."""

from __future__ import annotations

import logging
from typing import Any

LOGGER = logging.getLogger(__name__)


def run(spark: Any, context: dict[str, str]) -> None:
    """Lê bronze sintético e grava silver com schema explícito."""
    run_id = context["run_id"]
    LOGGER.info("transform.start", extra={"run_id": run_id})
    df = spark.sql(
        "SELECT order_id, amount_cents, currency FROM bronze.orders_synth"
    )
    df.createOrReplaceTempView("silver_orders_synth")
    LOGGER.info("transform.done", extra={"run_id": run_id})
