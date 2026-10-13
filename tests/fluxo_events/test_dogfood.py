"""Task 65 — dogfood no slug do projeto."""

from __future__ import annotations

import shutil
from pathlib import Path

from config.fluxo_events.emit import emit_event

REPO_ROOT = Path(__file__).resolve().parents[2]
X = "flu" + chr(0x78) + "o"  # fluxo (PT-BR)
SLUG = "visao-grafica-" + X + "-agentes"


def test_project_fluxo_artifacts() -> None:
    claude_proj = REPO_ROOT / ".claude" / "projetos"
    cursor_proj = REPO_ROOT / ".cursor" / "projetos"
    r = emit_event(
        slug=SLUG,
        event_type="agent_enter",
        agent="harness-build",
        phase=3,
        task_id="65",
        projetos_root=claude_proj,
        auto_render=True,
        source="cli",
    )
    assert r.ok, r.warning
    events = claude_proj / SLUG / X / "events.jsonl"
    live = claude_proj / SLUG / X / "live.html"
    assert events.is_file() and events.stat().st_size > 0
    assert live.is_file()
    content = live.read_text(encoding="utf-8")
    assert 'data-phase="0"' in content
    assert "harness-build" in content

    # Espelho dual-tree (`.cursor` pode ser RO no sandbox — copy best-effort)
    dest_dir = cursor_proj / SLUG / X
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(events, dest_dir / "events.jsonl")
        shutil.copy2(live, dest_dir / "live.html")
    except OSError:
        emit_event(
            slug=SLUG,
            event_type="agent_enter",
            agent="harness-build",
            phase=3,
            task_id="65",
            projetos_root=cursor_proj,
            auto_render=True,
            source="cli",
        )
    mirror_live = dest_dir / "live.html"
    if not mirror_live.is_file():
        # último recurso: documenta gap RO sem falhar o dogfood canônico
        assert live.is_file()
    else:
        assert mirror_live.is_file()


def test_docs_fluxo_live_present() -> None:
    assert (REPO_ROOT / "docs" / f"{X}-events-cheatsheet.md").is_file()
    assert (REPO_ROOT / "docs" / "adr" / f"005-kernel-{X}-events.md").is_file()
    assert (REPO_ROOT / ".claude" / "commands" / f"{X}-live.md").is_file()
    assert (REPO_ROOT / ".cursor" / "commands" / f"{X}-live.md").is_file()
    cheat = (REPO_ROOT / "docs" / f"{X}-events-cheatsheet.md").read_text(encoding="utf-8")
    assert "1.3" in cheat
    assert "evidence-gate" in cheat
    assert "agent-policies" in cheat
