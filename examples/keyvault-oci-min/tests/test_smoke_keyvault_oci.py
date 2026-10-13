"""Smoke — example keyvault-oci-min (layout + facade sem live API)."""

from __future__ import annotations

from pathlib import Path

EXAMPLE_ROOT = Path(__file__).resolve().parents[1]


def test_facade_and_map_present() -> None:
    assert (EXAMPLE_ROOT / "src" / "key_oci.py").is_file()
    assert (EXAMPLE_ROOT / "config" / "secrets_map.yaml").is_file()
    marker = (
        EXAMPLE_ROOT / ".harness" / "data-check" / "project_profile.yaml"
    ).read_text(encoding="utf-8")
    assert "secret_store: oci" in marker
