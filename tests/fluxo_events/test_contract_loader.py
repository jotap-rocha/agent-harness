"""Task 58 — contrato tipado + loader (fluxo-events.yaml)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.fluxo_events import FluxoEventsContract
from config.fluxo_events.contract import (
    REQUIRED_EVENT_TYPES,
    FluxoLimits,
    SddPhase,
)


def test_loads_defaults(contract_yaml_path: Path) -> None:
    assert contract_yaml_path.is_file(), (
        f"Fonte única ausente: {contract_yaml_path}. "
        "Crie fluxo-events.yaml na raiz do canônico."
    )
    contract = FluxoEventsContract.load(contract_yaml_path)
    assert contract.version >= 1
    assert isinstance(contract.limits, FluxoLimits)
    assert contract.limits.max_events_bytes == 2_097_152
    assert contract.limits.truncate_keep_default == 100
    assert len(contract.sdd_map) == 5
    phases = {phase.phase for phase in contract.sdd_map}
    assert phases == {0, 1, 2, 3, 4}
    assert all(isinstance(phase, SddPhase) and phase.agents for phase in contract.sdd_map)
    assert set(REQUIRED_EVENT_TYPES) <= set(contract.event_types)
    assert contract.paths.events_file == "events.jsonl"
    assert contract.paths.live_html == "live.html"


def test_invalid_contract_fails(tmp_path: Path) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("version: 1\nlimits:\n", encoding="utf-8")
    with pytest.raises(ValueError, match="limits"):
        FluxoEventsContract.load(bad)

    missing = tmp_path / "missing.yaml"
    missing.write_text(
        "version: 1\n"
        "limits:\n"
        "  max_events_bytes: 2097152\n"
        "  truncate_keep_default: 100\n"
        "event_types:\n"
        "  - phase_enter\n"
        "paths:\n"
        "  events_file: events.jsonl\n"
        "  live_html: live.html\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="sdd_map"):
        FluxoEventsContract.load(missing)


def test_no_sla_latency_field(
    contract_yaml_path: Path,
    tmp_path: Path,
) -> None:
    """G1-c / AC15: sem alvo numérico de latência/SLA no contrato."""
    contract = FluxoEventsContract.load(contract_yaml_path)
    forbidden = {
        "sla",
        "sla_ms",
        "sla_seconds",
        "latency",
        "latency_ms",
        "max_latency",
        "target_latency",
        "latency_target",
    }
    assert not hasattr(contract.limits, "sla_ms")
    assert not hasattr(contract.limits, "latency_ms")
    raw_keys = set(contract.__dataclass_fields__) | set(
        contract.limits.__dataclass_fields__
    )
    assert forbidden.isdisjoint(raw_keys)

    polluted = tmp_path / "with-sla.yaml"
    polluted.write_text(
        "version: 1\n"
        "limits:\n"
        "  max_events_bytes: 2097152\n"
        "  truncate_keep_default: 100\n"
        "  latency_ms: 200\n"
        "sdd_map:\n"
        "  0:\n"
        "    slug: IDEIA\n"
        "    agents:\n"
        "      - harness-brainstorm\n"
        "  1:\n"
        "    slug: REQUISITOS\n"
        "    agents:\n"
        "      - grill-me\n"
        "  2:\n"
        "    slug: PRD_HARNESS\n"
        "    agents:\n"
        "      - harness-design\n"
        "  3:\n"
        "    slug: IMPLEMENTAR\n"
        "    agents:\n"
        "      - harness-build\n"
        "  4:\n"
        "    slug: ENCERRAR\n"
        "    agents:\n"
        "      - harness-ship\n"
        "event_types:\n"
        "  - phase_enter\n"
        "  - phase_exit\n"
        "  - agent_enter\n"
        "  - agent_exit\n"
        "  - task_enter\n"
        "  - task_exit\n"
        "  - ship_truncate\n"
        "paths:\n"
        "  events_file: events.jsonl\n"
        "  live_html: live.html\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="(?i)sla|latency"):
        FluxoEventsContract.load(polluted)


def test_package_importable() -> None:
    import config.fluxo_events as pkg

    assert hasattr(pkg, "FluxoEventsContract")
    assert pkg.__doc__
