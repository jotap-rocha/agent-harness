"""Stub SDP estático — sinal pyspark.pipelines / @dp. (sem runtime Databricks)."""

from __future__ import annotations

import logging
from typing import Any

# Import tipicamente disponível só no runtime Databricks; stub para auto-detect.
from pyspark import pipelines as dp  # type: ignore[import-not-found]

LOGGER = logging.getLogger(__name__)


@dp.materialized_view()
def bronze_orders_synth() -> Any:
    """View bronze sintética (pedido + valor — sem PII)."""
    run_id = "demo-run"
    LOGGER.info("sdp.bronze.start", extra={"run_id": run_id})
    return None


@dp.materialized_view()
def silver_orders_synth() -> Any:
    run_id = "demo-run"
    LOGGER.info("sdp.silver.start", extra={"run_id": run_id})
    return None


@dp.materialized_view()
def gold_orders_synth() -> Any:
    run_id = "demo-run"
    LOGGER.info("sdp.gold.start", extra={"run_id": run_id})
    return None
