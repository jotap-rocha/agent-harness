"""Task 67 — contrato ``dev_loop_map`` (fases 0–6)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.fluxo_events import FluxoEventsContract
from config.fluxo_events.contract import SddPhase

EXPECTED_DEV_SLUGS = (
    "LOAD",
    "VALIDATE",
    "INIT_PICK",
    "EXECUTE_VERIFY",
    "UPDATE_CHECK",
    "LOOP_LOG",
    "SYNC",
)
EXPECTED_AGENTS = ("prompt-crafter", "dev-loop-executor")


def test_loads_dev_loop_map(contract_yaml_path: Path) -> None:
    contract = FluxoEventsContract.load(contract_yaml_path)
    assert hasattr(contract, "dev_loop_map")
    assert len(contract.dev_loop_map) == 7
    phases = {phase.phase for phase in contract.dev_loop_map}
    assert phases == {0, 1, 2, 3, 4, 5, 6}
    by_phase = {p.phase: p for p in contract.dev_loop_map}
    for idx, slug in enumerate(EXPECTED_DEV_SLUGS):
        phase = by_phase[idx]
        assert isinstance(phase, SddPhase)
        assert phase.slug == slug
        assert list(phase.agents) == list(EXPECTED_AGENTS)


def test_invalid_dev_loop_map_fails(tmp_path: Path) -> None:
    bad = tmp_path / "bad-dev.yaml"
    bad.write_text(
        "version: 1\n"
        "limits:\n"
        "  max_events_bytes: 2097152\n"
        "  truncate_keep_default: 100\n"
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
        "dev_loop_map:\n"
        "  0:\n"
        "    slug: LOAD\n"
        "    agents:\n"
        "      - prompt-crafter\n"
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
    with pytest.raises(ValueError, match="dev_loop_map"):
        FluxoEventsContract.load(bad)


def test_limits_unchanged(contract_yaml_path: Path) -> None:
    contract = FluxoEventsContract.load(contract_yaml_path)
    assert contract.limits.max_events_bytes == 2_097_152
    assert contract.limits.truncate_keep_default == 100
    assert not hasattr(contract.limits, "latency_ms")
    assert not hasattr(contract.limits, "sla_ms")
    assert len(contract.sdd_map) == 5
