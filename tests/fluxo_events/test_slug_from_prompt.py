"""Task 68 — helper ``slug_from_prompt_path``."""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.emit import emit_event
from config.fluxo_events.paths import events_path
from config.fluxo_events.slug import slug_from_prompt_path


def test_slug_from_prompt_foo() -> None:
    assert slug_from_prompt_path("PROMPT_FOO.md") == "dev-loop-foo"
    assert slug_from_prompt_path(Path(".claude/dev/tasks/PROMPT_FOO.md")) == "dev-loop-foo"
    assert slug_from_prompt_path("PROMPT_FOO_BAR.md") == "dev-loop-foo-bar"


def test_slug_sanitizes() -> None:
    assert slug_from_prompt_path("PROMPT_Foo Bar!!.md") == "dev-loop-foo-bar"
    assert slug_from_prompt_path("PROMPT___X__Y.md") == "dev-loop-x-y"
    assert slug_from_prompt_path("PROMPT_--.md") == "dev-loop"
    assert re_only_allowed(slug_from_prompt_path("PROMPT_Áção@1.md"))


def re_only_allowed(slug: str) -> bool:
    import re

    return bool(re.fullmatch(r"dev-loop(-[a-z0-9]+)*", slug))


def test_emit_path_dev_loop(tmp_path: Path, contract_yaml_path: Path) -> None:
    slug = slug_from_prompt_path("PROMPT_CACHE.md")
    assert slug == "dev-loop-cache"
    result = emit_event(
        slug=slug,
        event_type="agent_enter",
        agent="dev-loop-executor",
        phase=0,
        contract_path=contract_yaml_path,
        projetos_root=tmp_path / "projetos",
        auto_render=False,
    )
    assert result.ok
    target = events_path(tmp_path / "projetos", slug)
    assert target.is_file()
    assert "dev-loop-cache" in str(target)
    assert target.parent.name == "fluxo"
    assert target.parent.parent.name == "dev-loop-cache"
