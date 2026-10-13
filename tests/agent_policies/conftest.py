"""Fixtures compartilhadas dos testes de agent-policies."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_YAML = REPO_ROOT / "agent-policies.yaml"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def contract_yaml_path() -> Path:
    return CONTRACT_YAML
