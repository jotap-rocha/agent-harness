"""Task 71 — truncate EXIT_COMPLETE no path Dev Loop."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import events_path, live_html_path
from config.fluxo_events.truncate import TruncateResult, truncate_events

REPO_ROOT = Path(__file__).resolve().parents[2]
EXECUTOR = REPO_ROOT / ".claude/agents/dev/dev-loop-executor.md"


def _seed_dev(tmp_path: Path, contract_yaml_path: Path, n: int) -> str:
    slug = "dev-loop-cache"
    for i in range(n):
        emit_event(
            slug=slug,
            event_type="task_enter",
            agent="dev-loop-executor",
            phase=3,
            task_id=str(i),
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            auto_render=False,
        )
    return slug


def test_truncate_keep_100_dev_slug(tmp_path: Path, contract_yaml_path: Path) -> None:
    slug = _seed_dev(tmp_path, contract_yaml_path, 120)
    result = truncate_events(
        slug=slug,
        keep=100,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        emit_ship_event=True,
        auto_render=True,
        agent="dev-loop-executor",
        phase=6,
    )
    assert result.ok
    assert result.kept <= 100
    target = events_path(tmp_path / "projetos", slug)
    lines = [ln for ln in target.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) <= 100
    html = live_html_path(tmp_path / "projetos", slug).read_text(encoding="utf-8")
    assert "EXECUTE_VERIFY" in html or "Dev Loop" in html
    assert live_html_path(tmp_path / "projetos", slug).is_file()


def test_executor_mentions_truncate() -> None:
    text = EXECUTOR.read_text(encoding="utf-8")
    assert "EXIT_COMPLETE" in text
    assert "truncate" in text
    assert "--keep 100" in text
    assert "dev-loop-" in text


def test_truncate_fail_soft(tmp_path: Path, contract_yaml_path: Path) -> None:
    slug = _seed_dev(tmp_path, contract_yaml_path, 3)
    import config.fluxo_events.truncate as truncate_mod

    with patch.object(
        truncate_mod,
        "_truncate_file",
        side_effect=OSError("permission denied"),
    ):
        result = truncate_events(
            slug=slug,
            keep=100,
            contract_path=contract_yaml_path,
            projetos_root=tmp_path / "projetos",
            emit_ship_event=False,
            auto_render=False,
            agent="dev-loop-executor",
            phase=6,
        )
    assert isinstance(result, TruncateResult)
    assert result.ok is False
    assert result.soft is True
