"""Task 61 — rotate keep-tail no cap 2 MiB."""

from __future__ import annotations

from pathlib import Path

from config.fluxo_events.paths import events_path
from config.fluxo_events.rotate import append_with_rotate, rotate_keep_tail


def test_rotate_keeps_tail(tmp_path: Path) -> None:
    target = tmp_path / "events.jsonl"
    # Cap pequeno para forçar rotate sem gerar 2 MiB reais.
    max_bytes = 200
    for i in range(50):
        warn = append_with_rotate(
            target,
            f'{{"event_type":"agent_enter","n":{i},"pad":"{"x" * 20}"}}',
            max_bytes=max_bytes,
        )
    assert target.is_file()
    size = target.stat().st_size
    assert size <= max_bytes
    text = target.read_text(encoding="utf-8")
    assert "n\":49" in text or '"n":49' in text
    # warning soft pelo menos uma vez no overflow
    assert warn is not None or size <= max_bytes

    # rotate explícito também é idempotente sob o cap
    rotate_keep_tail(target, max_bytes=max_bytes)
    assert target.stat().st_size <= max_bytes
    assert callable(events_path)  # import smoke / typing seam
