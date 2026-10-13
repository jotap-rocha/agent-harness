"""Tasks 82–87 — KB Silver checklist ODCS + cross-links + dual-tree."""

from __future__ import annotations

import filecmp
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

KB_REL = ".claude/kb/pipeline/patterns/silver-checklist-odcs.md"
KB_PATH = REPO_ROOT / KB_REL
CURSOR_KB = REPO_ROOT / KB_REL.replace(".claude/", ".cursor/", 1)

MIRROR_PATHS = [
    KB_REL,
    ".claude/kb/pipeline/concepts/data-contracts.md",
    ".claude/kb/pipeline/index.md",
    ".claude/kb/_index.yaml",
    ".claude/skills/de-conformidade/references/rule-ids-remediation.md",
    ".claude/agents/data-engineering/data-quality-analyst.md",
    ".claude/agents/data-engineering/data-contracts-engineer.md",
]


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def test_kb_pattern_file_exists() -> None:
    assert KB_PATH.is_file()


def test_kb_pattern_dual_tree() -> None:
    assert CURSOR_KB.is_file()
    assert filecmp.cmp(KB_PATH, CURSOR_KB, shallow=False)


def test_kb_pattern_required_sections() -> None:
    text = KB_PATH.read_text(encoding="utf-8")
    assert "Proibido no Silver" in text
    assert "Severidade padrão" in text
    assert "Template genérico" in text
    assert "Instância orders" in text
    assert "ingestion_mode" in text


def test_orders_instance_rule_count() -> None:
    text = KB_PATH.read_text(encoding="utf-8")
    rules = re.findall(r"SLV-ORD-\d{3}", text)
    assert len(set(rules)) >= 10


def test_orders_dual_snippets() -> None:
    text = KB_PATH.read_text(encoding="utf-8")
    blocks = text.split("### SLV-ORD-")
    dual = 0
    for block in blocks[1:]:
        has_pyspark = "**PySpark:**" in block or "```python" in block
        has_dlt = "**DLT:**" in block or "@dlt." in block
        if has_pyspark and has_dlt:
            dual += 1
    assert dual >= 3


def test_data_contracts_links_pattern() -> None:
    text = _read(".claude/kb/pipeline/concepts/data-contracts.md")
    assert "silver-checklist-odcs.md" in text
    assert "Integração Silver" in text


def test_pipeline_index_lists_pattern() -> None:
    text = _read(".claude/kb/pipeline/index.md")
    assert "silver-checklist-odcs.md" in text


def test_de_conformidade_references_checklist() -> None:
    text = _read(".claude/skills/de-conformidade/references/rule-ids-remediation.md")
    assert "DE-B003" in text
    assert "silver-checklist-odcs.md" in text


def test_kb_index_lists_pattern_or_skip_documented() -> None:
    text = _read(".claude/kb/_index.yaml")
    assert "silver-checklist-odcs" in text


def test_data_quality_analyst_jit_link() -> None:
    text = _read(".claude/agents/data-engineering/data-quality-analyst.md")
    assert "silver-checklist-odcs.md" in text


def test_data_contracts_engineer_jit_link() -> None:
    text = _read(".claude/agents/data-engineering/data-contracts-engineer.md")
    assert "silver-checklist-odcs.md" in text


def test_agents_dual_tree() -> None:
    for rel in (
        ".claude/agents/data-engineering/data-quality-analyst.md",
        ".claude/agents/data-engineering/data-contracts-engineer.md",
    ):
        claude = REPO_ROOT / rel
        cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
        assert filecmp.cmp(claude, cursor, shallow=False), rel


def test_data_engineering_yaml_unchanged() -> None:
    path = REPO_ROOT / "data-engineering.yaml"
    result = subprocess.run(
        ["git", "show", "HEAD:data-engineering.yaml"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
    )
    # Checkout Windows pode converter para CRLF (autocrlf); o conteúdo é o que importa.
    working = path.read_bytes().decode("utf-8").replace("
", "
")
    assert working == result.stdout.decode("utf-8").replace("
", "
")


def test_tasks_index_file_exists() -> None:
    index = REPO_ROOT / ".claude/projetos/silver-checklist-odcs/04-tasks-index.md"
    assert index.is_file()
    text = index.read_text(encoding="utf-8")
    assert "82" in text and "87" in text


def test_readme_lists_silver_checklist_slug() -> None:
    text = _read("tasks/README.md")
    assert "silver-checklist-odcs" in text


@pytest.mark.parametrize("rel", MIRROR_PATHS)
def test_mirror_paths_dual_tree(rel: str) -> None:
    claude = REPO_ROOT / rel
    cursor = REPO_ROOT / rel.replace(".claude/", ".cursor/", 1)
    assert claude.is_file(), rel
    assert cursor.is_file(), rel
    assert filecmp.cmp(claude, cursor, shallow=False), rel
