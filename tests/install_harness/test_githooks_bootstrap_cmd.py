"""`_githooks_bootstrap_cmd`: escolha do comando de bootstrap dos githooks por SO."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
)


@pytest.fixture(scope="module")
def mod():
    spec = importlib.util.spec_from_file_location("install_harness_githooks", INSTALL_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def target(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    return tmp_path


def _touch(target: Path, name: str) -> Path:
    path = target / "scripts" / name
    path.write_text("", encoding="utf-8")
    return path


def _which(mapping: dict[str, str]):
    return lambda name: mapping.get(name)


def test_windows_prefere_pwsh(mod, monkeypatch, target):
    ps1 = _touch(target, "bootstrap-githooks.ps1")
    monkeypatch.setattr(mod.os, "name", "nt")
    monkeypatch.setattr(
        mod.shutil, "which", _which({"pwsh": "C:/pwsh.exe", "powershell": "C:/powershell.exe"})
    )
    assert mod._githooks_bootstrap_cmd(target) == [
        "C:/pwsh.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1), str(target),
    ]


def test_windows_cai_para_powershell(mod, monkeypatch, target):
    _touch(target, "bootstrap-githooks.ps1")
    monkeypatch.setattr(mod.os, "name", "nt")
    monkeypatch.setattr(mod.shutil, "which", _which({"powershell": "C:/powershell.exe"}))
    cmd = mod._githooks_bootstrap_cmd(target)
    assert cmd is not None and cmd[0] == "C:/powershell.exe"


def test_windows_nunca_usa_bash(mod, monkeypatch, target):
    """bash do PATH no Windows costuma ser o stub do WSL: não pode ser escolhido."""
    _touch(target, "bootstrap-githooks.sh")
    monkeypatch.setattr(mod.os, "name", "nt")
    monkeypatch.setattr(mod.shutil, "which", _which({"bash": "C:/Windows/System32/bash.exe"}))
    assert mod._githooks_bootstrap_cmd(target) is None


def test_windows_sem_ps1_retorna_none(mod, monkeypatch, target):
    monkeypatch.setattr(mod.os, "name", "nt")
    monkeypatch.setattr(mod.shutil, "which", _which({"pwsh": "C:/pwsh.exe"}))
    assert mod._githooks_bootstrap_cmd(target) is None


def test_windows_sem_powershell_retorna_none(mod, monkeypatch, target):
    _touch(target, "bootstrap-githooks.ps1")
    monkeypatch.setattr(mod.os, "name", "nt")
    monkeypatch.setattr(mod.shutil, "which", _which({}))
    assert mod._githooks_bootstrap_cmd(target) is None


def test_posix_usa_bash_com_sh(mod, monkeypatch, target):
    sh = _touch(target, "bootstrap-githooks.sh")
    monkeypatch.setattr(mod.os, "name", "posix")
    monkeypatch.setattr(mod.shutil, "which", _which({"bash": "/bin/bash"}))
    assert mod._githooks_bootstrap_cmd(target) == ["/bin/bash", str(sh), str(target)]


def test_posix_sem_script_ou_bash_retorna_none(mod, monkeypatch, target):
    monkeypatch.setattr(mod.os, "name", "posix")
    monkeypatch.setattr(mod.shutil, "which", _which({"bash": "/bin/bash"}))
    assert mod._githooks_bootstrap_cmd(target) is None
    _touch(target, "bootstrap-githooks.sh")
    monkeypatch.setattr(mod.shutil, "which", _which({}))
    assert mod._githooks_bootstrap_cmd(target) is None
