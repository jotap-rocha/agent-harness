"""Task 54 — install foundation + seed KEEP evidence-gate."""

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
    REPO_ROOT / "config" / "evidence_gate" / "templates" / "evidencias"
)


def _load_install_module():
    spec = importlib.util.spec_from_file_location("install_harness", INSTALL_SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_seed_template_exists() -> None:
    assert (SEED_TEMPLATE / "SCHEMA.md").is_file()
    assert (SEED_TEMPLATE / "example-task.yaml").is_file()
    assert "audit.jsonl" in (SEED_TEMPLATE / "SCHEMA.md").read_text(encoding="utf-8")


def test_stack_map_foundation_lists_evidence_gate() -> None:
    for rel in (
        ".claude/skills/install-harness/scripts/stack_map.json",
        ".cursor/skills/install-harness/scripts/stack_map.json",
    ):
        stack = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        foundation = next(c for c in stack["categories"] if c["name"] == "foundation")
        paths = {a["path"]: a for a in foundation["artifacts"]}
        assert "evidence-gate.yaml" in paths
        seed = paths[".harness/evidence-gate"]
        assert seed.get("seed") is True
        assert seed.get("from") == "config/evidence_gate/templates/evidencias"


def test_install_foundation_has_evidence_gate(tmp_path: Path) -> None:
    target = tmp_path / "filho-eg"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='eg'\n", encoding="utf-8")
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
    assert (target / "evidence-gate.yaml").is_file()
    assert (target / ".harness" / "evidence-gate" / "SCHEMA.md").is_file()
    assert (target / "config" / "evidence_gate").is_dir()
    # CLI importável no filho (config copiado)
    import os

    env = os.environ.copy()
    env["PYTHONPATH"] = str(target)
    proc2 = subprocess.run(
        [
            sys.executable,
            "-c",
            ("from config.evidence_gate import EvidenceGateContract; "
            "print(EvidenceGateContract.load('evidence-gate.yaml').version)"),
        ],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert proc2.returncode == 0, proc2.stderr
    assert proc2.stdout.strip().isdigit()


def test_reinstall_keeps_evidence_gate_seed(tmp_path: Path) -> None:
    target = tmp_path / "filho-eg-re"
    target.mkdir()
    (target / "pyproject.toml").write_text("[project]\nname='eg2'\n", encoding="utf-8")
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
    schema = target / ".harness" / "evidence-gate" / "SCHEMA.md"
    schema.write_text(schema.read_text(encoding="utf-8") + "\n# CUSTOM\n", encoding="utf-8")

    install = _load_install_module()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    plan2 = install.build_plan(target, REPO_ROOT, stack_map, manifest, signals)
    seed_items = [i for i in plan2 if i["path"] == ".harness/evidence-gate"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    second = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert second.returncode == 0, second.stderr or second.stdout
    assert "# CUSTOM" in schema.read_text(encoding="utf-8")


def test_stack_map_claude_cursor_parity() -> None:
    a = (REPO_ROOT / ".claude/skills/install-harness/scripts/stack_map.json").read_text(
        encoding="utf-8"
    )
    b = (REPO_ROOT / ".cursor/skills/install-harness/scripts/stack_map.json").read_text(
        encoding="utf-8"
    )
    assert a == b
