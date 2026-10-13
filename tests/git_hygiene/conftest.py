"""Fixtures compartilhadas dos testes de contrato git-hygiene."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CONTRACT_YAML = REPO_ROOT / "git-hygiene.yaml"


def _read_cases(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def contract_yaml_path() -> Path:
    return CONTRACT_YAML


@pytest.fixture(scope="session")
def valid_branches() -> list[str]:
    return _read_cases(FIXTURES_DIR / "branches_valid.txt")


@pytest.fixture(scope="session")
def invalid_branches() -> list[str]:
    return _read_cases(FIXTURES_DIR / "branches_invalid.txt")


@pytest.fixture(scope="session")
def valid_pr_titles() -> list[str]:
    return _read_cases(FIXTURES_DIR / "pr_titles_valid.txt")


@pytest.fixture(scope="session")
def invalid_pr_titles() -> list[str]:
    return _read_cases(FIXTURES_DIR / "pr_titles_invalid.txt")
