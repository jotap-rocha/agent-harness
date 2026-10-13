"""Testes do adapter SCM — detecção por URL do remote (A9)."""

from __future__ import annotations

import pytest

from config.git_hygiene.scm import ScmKind, detect_scm


@pytest.mark.parametrize(
    "url",
    [
        "https://dev.azure.com/org/project/_git/repo",
        "https://org@dev.azure.com/org/project/_git/repo",
        "git@ssh.dev.azure.com:v3/org/project/repo",
        "https://org.visualstudio.com/DefaultCollection/project/_git/repo",
        "https://org.vs-ssh.visualstudio.com/org/project",
    ],
)
def test_detect_azure(url: str) -> None:
    assert detect_scm(url) == ScmKind.AZURE


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/org/repo.git",
        "git@github.com:org/repo.git",
        "https://www.github.com/org/repo",
        "ssh://git@github.com/org/repo.git",
    ],
)
def test_detect_github(url: str) -> None:
    assert detect_scm(url) == ScmKind.GITHUB


@pytest.mark.parametrize(
    "url",
    [
        "https://gitlab.com/org/repo.git",
        "https://bitbucket.org/org/repo.git",
        "https://git.example.com/org/repo.git",
        "",
        "not-a-url",
    ],
)
def test_detect_ambiguous(url: str) -> None:
    assert detect_scm(url) == ScmKind.AMBIGUOUS
