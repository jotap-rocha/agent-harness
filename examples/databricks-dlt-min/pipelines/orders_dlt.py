"""Stub DLT estático — sinal import dlt / @dlt. (sem runtime Databricks)."""

from __future__ import annotations

import logging
from typing import Any

# Import tipicamente disponível só no runtime Databricks; stub para auto-detect.
import dlt  # type: ignore[import-not-found]

LOGGER = logging.getLogger(__name__)

quarantine_table = "ops.quarantine_orders"


@dlt.expect_or_drop("order_id_not_null", "order_id IS NOT NULL")
@dlt.table
def orders_synth() -> Any:
    """Tabela sintética de pedidos (order_id + amount — sem PII)."""
    run_id = "demo-run"
    LOGGER.info("dlt.orders.start", extra={"run_id": run_id})
    return None
