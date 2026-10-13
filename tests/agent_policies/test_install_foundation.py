"""Task 47 — seed KEEP + install foundation deny ≠ []."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "install-harness"
    / "scripts"
    / "install_harness.py"
)
SEED_TEMPLATE = (
    REPO_ROOT
    / "config"
    / "agent_policies"
    / "templates"
    / "policies"
)


def _load_install_module():
    spec = importlib.util.spec_from_file_location("install_harness", INSTALL_SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_seed_template_exists_with_marker() -> None:
    profile = SEED_TEMPLATE / "project_profile.yaml"
    schema = SEED_TEMPLATE / "SCHEMA.md"
    assert profile.is_file()
    assert schema.is_file()
    text = profile.read_text(encoding="utf-8")
    assert "families:" in text
    # valor real não pode ser inline []; comentário de aviso pode mencionar o anti-pattern
    data_lines = [
        line for line in text.splitlines() if line.strip() and not line.strip().startswith("#")
    ]
    assert not any(line.strip() == "families: []" for line in data_lines)
    schema_text = schema.read_text(encoding="utf-8")
    assert "KEEP" in schema_text or "seed" in schema_text.lower()
    from config.agent_policies.generate import generate_artifacts, load_profile_families

    assert load_profile_families(profile) == frozenset()
    # generate com seed vazio não falha
    result = generate_artifacts(
        contract_path=REPO_ROOT / "agent-policies.yaml",
        profile_path=profile,
    )
    assert result.claude_deny


def test_stack_map_foundation_lists_policies_seed() -> None:
    stack = json.loads(
        (
            REPO_ROOT
            / ".claude/skills/install-harness/scripts/stack_map.json"
        ).read_text(encoding="utf-8")
    )
    foundation = next(c for c in stack["categories"] if c["name"] == "foundation")
    paths = {a["path"]: a for a in foundation["artifacts"]}
    assert "agent-policies.yaml" in paths
    assert ".cursor/hooks.json" in paths
    assert paths[".cursor/hooks.json"]["kind"] == "generate"
    seed = paths[".harness/policies"]
    assert seed.get("seed") is True
    assert seed.get("from") == "config/agent_policies/templates/policies"


def test_install_foundation_deny_non_empty(tmp_path: Path) -> None:
    target = tmp_path / "filho"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
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

    settings = json.loads(
        (target / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    deny = settings["permissions"]["deny"]
    assert deny != []
    assert any("rm -rf" in d for d in deny)

    hooks = target / ".cursor" / "hooks.json"
    assert hooks.is_file()
    hooks_data = json.loads(hooks.read_text(encoding="utf-8"))
    assert "beforeShellExecution" in hooks_data["hooks"]

    profile = target / ".harness" / "policies" / "project_profile.yaml"
    assert profile.is_file()
    assert (target / "agent-policies.yaml").is_file()

    # PreToolUse presente
    assert "PreToolUse" in settings.get("hooks", {})


def test_reinstall_keeps_policies_profile_families(tmp_path: Path) -> None:
    target = tmp_path / "filho-re"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='y'\n", encoding="utf-8")
    common = [
        sys.executable,
        str(INSTALL_SCRIPT),
        str(target),
        "--canonical",
        str(REPO_ROOT),
        "--yes",
    ]
    first = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert first.returncode == 0, first.stderr or first.stdout

    profile = target / ".harness" / "policies" / "project_profile.yaml"
    profile.write_text(
        "families:\n  - cloud-cli-extra\n",
        encoding="utf-8",
    )

    install = _load_install_module()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    plan2 = install.build_plan(target, REPO_ROOT, stack_map, manifest, signals)
    seed_items = [i for i in plan2 if i["path"] == ".harness/policies"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    second = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert second.returncode == 0, second.stderr or second.stdout
    saved = profile.read_text(encoding="utf-8")
    assert "cloud-cli-extra" in saved
