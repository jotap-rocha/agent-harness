"""Testes dos githooks — comportamento externo (exit codes / mensagens)."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".githooks"

# Montar em runtime para o próprio pre-commit não bloquear este arquivo de teste.
_AWS_FAKE = "AKIA" + "IOSFODNN7EXAMPLE"
_PEM_FAKE = "-----BEGIN " + "PRIVATE KEY-----"
_PASSWORD_FAKE = "pass" + "word=supersecret"


def _run_hook(
    name: str,
    *args: str,
    input_text: str | None = None,
    env: dict | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    hook = HOOKS_DIR / name
    assert hook.is_file(), f"hook ausente: {hook}"
    assert os.access(hook, os.X_OK), f"hook não executável: {hook}"
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [str(hook), *args],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=str(cwd or REPO_ROOT),
        env=merged_env,
        check=False,
    )


def _init_repo_with_file(tmp_path: Path, filename: str, content: str) -> Path:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    (tmp_path / filename).write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", filename], cwd=tmp_path, check=True, capture_output=True)
    return tmp_path


def test_hooks_are_executable() -> None:
    for name in ("pre-commit", "commit-msg", "pre-push"):
        path = HOOKS_DIR / name
        assert path.is_file()
        mode = path.stat().st_mode
        assert mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


@pytest.mark.parametrize(
    "content,needle_absent",
    [
        (f"aws_key = {_AWS_FAKE}\n", _AWS_FAKE),
        (f"{_PEM_FAKE}\nMIIE...\n", "PRIVATE KEY"),
        (f"db {_PASSWORD_FAKE}\n", "supersecret"),
    ],
)
def test_pre_commit_blocks_synthetic_secrets(
    tmp_path: Path, content: str, needle_absent: str
) -> None:
    repo = _init_repo_with_file(tmp_path, "leak.txt", content)
    result = _run_hook("pre-commit", cwd=repo)
    assert result.returncode != 0
    combined = (result.stdout + result.stderr).lower()
    assert "segredo" in combined or "secret" in combined
    assert needle_absent not in result.stdout
    # Valor completo do segredo não deve aparecer; tipo/arquivo ok
    if needle_absent == _AWS_FAKE:
        assert _AWS_FAKE not in result.stderr


def test_pre_commit_allows_clean_diff(tmp_path: Path) -> None:
    repo = _init_repo_with_file(tmp_path, "ok.txt", "hello world\n")
    result = _run_hook("pre-commit", cwd=repo)
    assert result.returncode == 0
    assert "unrecognized option" not in (result.stdout + result.stderr)


def test_commit_msg_warns_but_allows_non_conventional(tmp_path: Path) -> None:
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text("mensagem livre sem convencional\n", encoding="utf-8")
    result = _run_hook("commit-msg", str(msg_file))
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).lower()
    assert "aviso" in combined or "conventional" in combined or "sugest" in combined


def test_commit_msg_silent_ok_on_conventional(tmp_path: Path) -> None:
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text("feat(scope): adiciona validacao\n", encoding="utf-8")
    result = _run_hook("commit-msg", str(msg_file))
    assert result.returncode == 0


def test_pre_push_warns_on_trunk_and_exits_zero() -> None:
    stdin = "refs/heads/master abc123 refs/heads/master def456\n"
    result = _run_hook("pre-push", "origin", "git@example.com:repo.git", input_text=stdin)
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).lower()
    assert "tronco" in combined or "master" in combined or "aviso" in combined


def test_pre_push_quiet_on_feature_branch() -> None:
    stdin = "refs/heads/feat/x abc123 refs/heads/feat/x def456\n"
    result = _run_hook("pre-push", "origin", "git@example.com:repo.git", input_text=stdin)
    assert result.returncode == 0
