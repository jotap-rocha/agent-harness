"""Tasks 88–93 — Medallion SDD gates (KB + agents + rules + Dev Loop)."""

from __future__ import annotations

import filecmp
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

KB_REL = ".claude/kb/pipeline/patterns/medallion-sdd-gates.md"
KB_PATH = REPO_ROOT / KB_REL
CURSOR_KB = REPO_ROOT / KB_REL.replace(".claude/", ".cursor/", 1)

MIRROR_PATHS = [
    KB_REL,
    ".claude/kb/pipeline/index.md",
    ".claude/kb/_index.yaml",
    ".claude/agents/workflow/harness-brainstorm.md",
    ".claude/agents/workflow/harness-define.md",
    ".claude/agents/dev/prompt-crafter.md",
    ".claude/rules/pipeline.md",
    ".claude/commands/dev.md",
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
    assert "Gate transversal" in text
    assert "Gate Bronze" in text
    assert "Gate Silver" in text
    assert "Gate Gold + NL" in text
    assert "Contrato dual" in text
    assert "_source_system" in text
    assert "Medallion Context" in text


def test_brainstorm_gate_section() -> None:
    text = _read(".claude/agents/workflow/harness-brainstorm.md")
    assert "4b. Gate Medallion" in text
    assert "medallion-sdd-gates.md" in text
    assert "Hard-stop" in text
    assert "Medallion Gates (brainstorm)" in text


def test_define_gate_section() -> None:
    text = _read(".claude/agents/workflow/harness-define.md")
    assert "2c. Gate Medallion" in text
    assert "medallion-sdd-gates.md" in text
    assert "T1" in text and "T8" in text


def test_define_grill_template() -> None:
    text = _read(".claude/agents/workflow/harness-define.md")
    assert "Medallion Gates — validação" in text
    assert "### Bronze (se no escopo)" in text
    assert "### Silver (se no escopo)" in text
    assert "### Gold (se no escopo)" in text


def test_prompt_crafter_gate_section() -> None:
    text = _read(".claude/agents/dev/prompt-crafter.md")
    assert "3b. Gate Medallion" in text
    assert "medallion-sdd-gates.md" in text
    assert "Medallion Context" in text


def test_dev_command_gate_note() -> None:
    text = _read(".claude/commands/dev.md")
    assert "Gate Medallion" in text
    assert "medallion-sdd-gates.md" in text


def test_pipeline_rule_gates() -> None:
    text = _read(".claude/rules/pipeline.md")
    assert "_source_system" in text
    assert "Gates SDD e Dev Loop" in text
    assert "medallion-sdd-gates.md" in text
    assert "contrato de **ingestão**" in text


def test_pipeline_index_lists_pattern() -> None:
    text = _read(".claude/kb/pipeline/index.md")
    assert "medallion-sdd-gates.md" in text
    index_yaml = _read(".claude/kb/_index.yaml")
    assert "medallion-sdd-gates" in index_yaml


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
        (
            ".claude/agents/dev/prompt-crafter.md",
            ".cursor/agents/dev/prompt-crafter.md",
        ),
    ]
    for claude, cursor in pairs:
        assert filecmp.cmp(REPO_ROOT / claude, REPO_ROOT / cursor, shallow=False)


def test_project_ideia_exists() -> None:
    assert (REPO_ROOT / ".claude/projetos/medallion-sdd-gates/00-ideia.md").is_file()
    assert (REPO_ROOT / ".claude/projetos/medallion-sdd-gates/STATUS.md").is_file()


def test_readme_lists_slug() -> None:
    text = _read("tasks/README.md")
    assert "medallion-sdd-gates" in text


def test_medallion_concept_source_system() -> None:
    text = _read(".claude/kb/pipeline/concepts/medallion.md")
    assert "_source_system" in text
    assert "JSON aninhado" in text or "struct/array" in text


def test_data_lineage_source_system() -> None:
    text = _read(".claude/kb/pipeline/concepts/data-lineage.md")
    assert "_source_system" in text


def test_gold_analytic_and_genie_kb() -> None:
    gold = _read(".claude/kb/pipeline/concepts/gold-analytic.md")
    genie = _read(".claude/kb/pipeline/patterns/genie-readiness.md")
    assert "Diamond" in gold
    assert "Genie" in genie
    index = _read(".claude/kb/pipeline/index.md")
    assert "gold-analytic.md" in index
    assert "genie-readiness.md" in index


def test_grill_artifact_exists() -> None:
    assert (REPO_ROOT / ".claude/projetos/medallion-sdd-gates/01-grill.md").is_file()


def test_prd_and_harness_design_artifacts() -> None:
    assert (REPO_ROOT / ".claude/projetos/medallion-sdd-gates/02-prd.md").is_file()
    assert (REPO_ROOT / ".claude/projetos/medallion-sdd-gates/03-harness.md").is_file()
    prd = _read(".claude/projetos/medallion-sdd-gates/02-prd.md")
    assert "Problem Statement" in prd
    assert "medallion-sdd-gates.md" in prd
    harness = _read(".claude/projetos/medallion-sdd-gates/03-harness.md")
    assert "4b" in harness and "2c" in harness and "3b" in harness


@pytest.mark.parametrize("rel", MIRROR_PATHS)
def test_mirror_paths_exist(rel: str) -> None:
    assert (REPO_ROOT / rel).is_file()
