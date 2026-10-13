"""Task 63 — install foundation seed fluxo-events."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
X = "flu" + chr(0x78) + "o"  # fluxo (PT-BR)
PKG = f"{X}_events"
INSTALL_SCRIPT = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "install-harness"
    / "scripts"
    / "install_harness.py"
)
SEED_TEMPLATE = REPO_ROOT / "config" / PKG / "templates" / X


def _load_install_module():
    spec = importlib.util.spec_from_file_location("install_harness", INSTALL_SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_foundation_includes_fluxo() -> None:
    for rel in (
        ".claude/skills/install-harness/scripts/stack_map.json",
        ".cursor/skills/install-harness/scripts/stack_map.json",
    ):
        stack = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        foundation = next(c for c in stack["categories"] if c["name"] == "foundation")
        paths = {a["path"]: a for a in foundation["artifacts"]}
        assert f"{X}-events.yaml" in paths
        seed = paths[f".harness/{X}-events"]
        assert seed.get("seed") is True
        assert seed.get("from") == f"config/{PKG}/templates/{X}"
        assert f".claude/commands/{X}-live.md" in paths


def test_seed_keep(tmp_path: Path) -> None:
    target = tmp_path / "filho-fluxo"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='fl'\n", encoding="utf-8")
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
    schema = target / ".harness" / f"{X}-events" / "SCHEMA.md"
    assert schema.is_file()
    schema.write_text(schema.read_text(encoding="utf-8") + "\n# CUSTOM\n", encoding="utf-8")

    install = _load_install_module()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    plan2 = install.build_plan(target, REPO_ROOT, stack_map, manifest, signals)
    seed_items = [i for i in plan2 if i["path"] == f".harness/{X}-events"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    second = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert second.returncode == 0, second.stderr or second.stdout
    assert "# CUSTOM" in schema.read_text(encoding="utf-8")


def test_child_template_fluxo(tmp_path: Path) -> None:
    assert (SEED_TEMPLATE / "SCHEMA.md").is_file()
    assert (SEED_TEMPLATE / "events.jsonl").is_file()
    assert (SEED_TEMPLATE / "live.html").is_file()
    target = tmp_path / "filho-fluxo2"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='fl2'\n", encoding="utf-8")
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
    assert (target / f"{X}-events.yaml").is_file()
    assert (target / ".harness" / f"{X}-events" / "SCHEMA.md").is_file()
    assert (target / "config" / PKG).is_dir()
    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    proc2 = subprocess.run(
        [
            sys.executable,
            "-c",
            f"from config.{PKG} import FluxoEventsContract; "
            f"print(FluxoEventsContract.load('{X}-events.yaml').version)",
        ],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert proc2.returncode == 0, proc2.stderr
    assert proc2.stdout.strip().isdigit()
