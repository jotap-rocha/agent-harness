"""Pipeline runtime + AI-DEV-KIT gates (brainstorm 4a/4a-bis, define 2a)."""

from __future__ import annotations

import filecmp
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

KB_REL = ".claude/kb/databricks/patterns/ai-dev-kit-gate.md"
KB_PATH = REPO_ROOT / KB_REL
CURSOR_KB = REPO_ROOT / KB_REL.replace(".claude/", ".cursor/", 1)

MIRROR_PATHS = [
    KB_REL,
    ".claude/kb/databricks/index.md",
    ".claude/kb/_index.yaml",
    ".claude/agents/workflow/harness-brainstorm.md",
    ".claude/agents/workflow/harness-define.md",
    ".claude/rules/pipeline.md",
    ".claude/kb/pipeline/patterns/medallion-sdd-gates.md",
]


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def test_ai_dev_kit_kb_exists() -> None:
    assert KB_PATH.is_file()
    text = KB_PATH.read_text(encoding="utf-8")
    assert "AI-DEV-KIT" in text
    assert "Hard-stop" in text or "hard-stop" in text
    assert "administrador" in text


def test_ai_dev_kit_kb_dual_tree() -> None:
    assert CURSOR_KB.is_file()
    assert filecmp.cmp(KB_PATH, CURSOR_KB, shallow=False)


def test_brainstorm_runtime_gate() -> None:
    text = _read(".claude/agents/workflow/harness-brainstorm.md")
    assert "4a. Gate Runtime Pipeline" in text
    assert "Spark LOCAL" in text
    assert "Databricks CLOUD" in text
    assert "resposta humana obrigatória" in text
    assert "Hard-stop" in text


def test_brainstorm_ai_dev_kit_gate() -> None:
    text = _read(".claude/agents/workflow/harness-brainstorm.md")
    assert "4a-bis. Gate AI-DEV-KIT" in text
    assert "ai-dev-kit-gate.md" in text
    assert "Não sei do que se trata" in text
    assert "Encerre o brainstorm" in text
    assert "Runtime Pipeline (gate 4a)" in text
    assert "AI-DEV-KIT (gate 4a-bis" in text


def test_define_runtime_validation() -> None:
    text = _read(".claude/agents/workflow/harness-define.md")
    assert "2a. Gate Runtime + AI-DEV-KIT" in text
    assert "ai-dev-kit-gate.md" in text
    assert "HARD-STOP" in text


def test_pipeline_rule_references_gates() -> None:
    text = _read(".claude/rules/pipeline.md")
    assert "4a" in text and "4a-bis" in text and "2a" in text
    assert "ai-dev-kit-gate.md" in text


def test_databricks_index_lists_ai_dev_kit() -> None:
    text = _read(".claude/kb/databricks/index.md")
    assert "ai-dev-kit-gate.md" in text
    index_yaml = _read(".claude/kb/_index.yaml")
    assert "ai-dev-kit-gate" in index_yaml


def test_medallion_gates_prerequisite_runtime() -> None:
    text = _read(".claude/kb/pipeline/patterns/medallion-sdd-gates.md")
    assert "4a-bis" in text
    assert "AI-DEV-KIT" in text


@pytest.mark.parametrize("rel", MIRROR_PATHS)
def test_mirror_paths_exist(rel: str) -> None:
    assert (REPO_ROOT / rel).is_file()


def test_agents_dual_tree() -> None:
    pairs = [
        (
            ".claude/agents/workflow/harness-brainstorm.md",
            ".cursor/agents/workflow/harness-brainstorm.md",
        ),
        (
            ".claude/agents/workflow/harness-define.md",
            ".cursor/agents/workflow/harness-define.md",
        ),
    ]
    for claude, cursor in pairs:
        assert filecmp.cmp(REPO_ROOT / claude, REPO_ROOT / cursor, shallow=False)


def test_sdd_project_artifacts_exist() -> None:
    base = REPO_ROOT / ".claude/projetos/pipeline-runtime-gates"
    for name in (
        "00-ideia.md",
        "STATUS.md",
        "01-grill.md",
        "02-prd.md",
        "03-harness.md",
        "04-tasks-index.md",
    ):
        assert (base / name).is_file()


def test_tasks_readme_lists_slug() -> None:
    text = _read("tasks/README.md")
    assert "pipeline-runtime-gates" in text
