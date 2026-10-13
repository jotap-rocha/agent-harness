"""Task 57 — context-rebind: README generate + banner anti-canônico + KEEP."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
)
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)

# Título/assinatura típica do CLAUDE.md do canônico — nunca deve ser título do filho.
CANONICAL_TITLE = "Agent Harness Canônico — guia do agente"
CONTEXT_FILES = ("CLAUDE.md", "AGENTS.md", "CONTEXT.md", "README.md")


def _load_install_module():
    spec = importlib.util.spec_from_file_location(
        "install_harness_context_rebind",
        INSTALL_SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _foundation_artifacts(stack_map: dict) -> dict[str, dict]:
    foundation = next(c for c in stack_map["categories"] if c["name"] == "foundation")
    return {str(a["path"]): a for a in foundation["artifacts"]}


def test_stack_map_foundation_declares_readme_generate() -> None:
    for path in STACK_MAP_PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        arts = _foundation_artifacts(data)
        assert "README.md" in arts, f"README.md ausente em {path}"
        assert arts["README.md"]["kind"] == "generate"


def test_generate_content_banner_and_readme_not_canonical() -> None:
    mod = _load_install_module()
    project = "meu-filho-app"
    stack = "python, fastapi"

    for rel in CONTEXT_FILES:
        text = mod.generate_content(rel, project, stack)
        # Não como título H1 (pode citar o canônico só em prosa de aviso)
        assert f"# {CANONICAL_TITLE}" not in text
        assert not any(
            line.strip().startswith("#") and CANONICAL_TITLE in line
            for line in text.splitlines()
        )
        assert project in text
        assert "não o Agent Harness Canônico" in text
        assert text.index("não o Agent Harness Canônico") < 200

    readme = mod.generate_content("README.md", project, stack)
    assert "make-readme" in readme.lower() or "/make-readme" in readme


def test_looks_like_canonical_context_helper() -> None:
    mod = _load_install_module()
    assert mod.looks_like_canonical_context(f"# {CANONICAL_TITLE}\n\nfoo") is True
    assert (
        mod.looks_like_canonical_context(
            "# meu-filho-app\n\n> não o Agent Harness Canônico\n"
        )
        is False
    )
    # Marcador genérico "(preencher)" sozinho NÃO força rebind (ressalva revisor)
    assert mod.needs_context_rebind("# Stub\n\n(preencher)\n") is False
    assert mod.needs_context_rebind("# Stub\n\n(preencher com /grill-me)\n") is True
    # Stub gerado com banner + placeholders ainda precisa de rebind
    stub = mod.generate_content("CLAUDE.md", "filho", "python")
    assert mod.looks_like_canonical_context(stub) is False
    assert mod.needs_context_rebind(stub) is True


def test_claude_cursor_install_scripts_mirrored() -> None:
    import filecmp

    pairs = (
        (
            "skills/install-harness/scripts/install_harness.py",
            "skills/install-harness/scripts/install_harness.py",
        ),
        (
            "skills/install-harness/scripts/stack_map.json",
            "skills/install-harness/scripts/stack_map.json",
        ),
        (
            "skills/install-harness/SKILL.md",
            "skills/install-harness/SKILL.md",
        ),
        (
            "skills/harness-architect/SKILL.md",
            "skills/harness-architect/SKILL.md",
        ),
        (
            "agents/workflow/harness-brainstorm.md",
            "agents/workflow/harness-brainstorm.md",
        ),
    )
    for rel in pairs:
        left = REPO_ROOT / ".claude" / rel[0]
        right = REPO_ROOT / ".cursor" / rel[1]
        assert left.is_file() and right.is_file(), rel
        assert filecmp.cmp(left, right, shallow=False), f"drift dual-tree: {rel[0]}"


def test_install_generate_destination_has_banner_readme_not_canonical(
    tmp_path: Path,
) -> None:
    target = tmp_path / "filho-rebind"
    target.mkdir()
    (target / "pyproject.toml").write_text(
        '[project]\nname = "filho-rebind"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(INSTALL_SCRIPT),
            str(target),
            "--canonical",
            str(REPO_ROOT),
            "--yes",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout

    for name in CONTEXT_FILES:
        path = target / name
        assert path.is_file(), f"faltou {name}"
        text = path.read_text(encoding="utf-8")
        assert f"# {CANONICAL_TITLE}" not in text, f"{name} ainda tem título canônico"
        assert not any(
            line.strip().startswith("#") and CANONICAL_TITLE in line
            for line in text.splitlines()
        )
        assert "não o Agent Harness Canônico" in text
        assert "filho-rebind" in text

    readme = (target / "README.md").read_text(encoding="utf-8")
    assert "make-readme" in readme.lower() or "/make-readme" in readme


def test_readme_keep_when_already_customized(tmp_path: Path) -> None:
    """Re-install com --yes não sobrescreve README já customizado (CONFLICT→keep)."""
    target = tmp_path / "filho-keep-readme"
    target.mkdir()
    (target / "pyproject.toml").write_text(
        '[project]\nname = "keep-readme"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    custom = "# README customizado do time\n\nNão tocar.\n"
    (target / "README.md").write_text(custom, encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(INSTALL_SCRIPT),
            str(target),
            "--canonical",
            str(REPO_ROOT),
            "--yes",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert (target / "README.md").read_text(encoding="utf-8") == custom
