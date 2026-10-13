"""Task 61 — truncate ship + ship_truncate event."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import events_path, live_html_path
from config.fluxo_events.truncate import TruncateResult, truncate_events


def _seed_events(
    tmp_path: Path,
    contract_yaml_path: Path,
    n: int,
) -> None:
    for i in range(n):
        emit_event(
            slug="trunc-slug",
            event_type="task_enter",
            agent="harness-build",
            phase=3,
            task_id=str(i),
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            auto_render=False,
        )


def test_truncate_keep_100(tmp_path: Path, contract_yaml_path: Path) -> None:
    _seed_events(tmp_path, contract_yaml_path, 120)
    result = truncate_events(
        slug="trunc-slug",
        keep=100,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        emit_ship_event=True,
        auto_render=True,
    )
    assert result.ok
    assert result.kept <= 100
    target = events_path(tmp_path / "projetos", "trunc-slug")
    lines = [ln for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) <= 100
    assert live_html_path(tmp_path / "projetos", "trunc-slug").is_file()


def test_ship_truncate_event(tmp_path: Path, contract_yaml_path: Path) -> None:
    _seed_events(tmp_path, contract_yaml_path, 5)
    result = truncate_events(
        slug="trunc-slug",
        keep=100,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        emit_ship_event=True,
        auto_render=False,
    )
    assert result.ok
    target = events_path(tmp_path / "projetos", "trunc-slug")
    types = [
        json.loads(ln)["event_type"]
        for ln in target.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert "ship_truncate" in types


def test_truncate_fail_soft(tmp_path: Path, contract_yaml_path: Path) -> None:
    _seed_events(tmp_path, contract_yaml_path, 3)
    import config.fluxo_events.truncate as truncate_mod

    with patch.object(
        truncate_mod,
        "_truncate_file",
        side_effect=OSError("permission denied"),
    ):
        result = truncate_events(
            slug="trunc-slug",
            keep=2,
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            emit_ship_event=False,
            auto_render=False,
        )
    assert isinstance(result, TruncateResult)
    assert result.ok is False
    assert result.soft is True
    assert result.warning
