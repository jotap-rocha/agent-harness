"""Freeze stack_map + inventário Loop 3 (Task 32 / AC9–AC11; Task 30 alinhar)."""

from __future__ import annotations

import json
from pathlib import Path

from config.canonical_data_check import EXIT_OK, validate_project
from config.canonical_data_check.de_marker import (
    data_check_validate_argv,
    has_de_marker,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)

# Baseline Loop 3 — `pipeline_dados` expandido (AC6/AC9). Instalado por padrão (always).
FROZEN_PIPELINE_ARTIFACT_PATHS = (
    "data-engineering.yaml",
    ".claude/kb/pipeline",
    ".claude/kb/databricks",
    ".claude/kb/airflow",
    ".claude/kb/spark",
    ".claude/kb/lakehouse",
    ".claude/kb/data-quality",
    ".claude/kb/dbt",
    ".claude/kb/data-modeling",
    ".claude/kb/sql-patterns",
    ".claude/kb/streaming",
    ".claude/kb/cloud-platforms",
    ".claude/rules/pipeline.md",
    ".claude/agents/data-engineering",
    ".claude/commands/data-engineering",
    ".claude/skills/de-conformidade",
    ".harness/data-check",
)

FROZEN_DE_AGENTS = frozenset(
    {
        "data-contracts-engineer.md",
        "data-platform-engineer.md",
        "data-quality-analyst.md",
        "dbt-specialist.md",
        "lakehouse-architect.md",
        "pipeline-architect.md",
        "schema-designer.md",
        "spark-engineer.md",
        "sql-optimizer.md",
        "streaming-engineer.md",
    }
)
FROZEN_DE_COMMANDS = frozenset(
    {
        "data-contract.md",
        "data-quality.md",
        "lakehouse.md",
        "migrate.md",
        "pipeline.md",
        "schema.md",
        "sql-review.md",
    }
)
# Loop 3: 18→19 KBs (databricks) · 19→20 skills (de-conformidade)
# Key Vault: 19→21 KBs (oci-vault, azure-keyvault) · 20→21 skills (cloud-secrets)
FROZEN_KB_DOMAINS = frozenset(
    {
        "airflow",
        "azure-keyvault",
        "cloud-platforms",
        "data-modeling",
        "data-quality",
        "databricks",
        "dbt",
        "design-instrucional",
        "fastapi",
        "lakehouse",
        "langgraph",
        "multi-tenant",
        "observabilidade",
        "oci-vault",
        "pipeline",
        "rag",
        "spark",
        "sql-patterns",
        "streaming",
        "supabase",
        "testing",
    }
)
FROZEN_SKILL_DIRS = frozenset(
    {
        "adversarial-judge",
        "cloud-secrets",
        "create-rag-pipeline",
        "de-conformidade",
        "documentation-writer",
        "excalidraw-diagram",
        "find-skills",
        "gen-tests",
        "grill-me",
        "grill-with-docs",
        "guia-architect",
        "handoff",
        "harness-architect",
        "install-harness",
        "make-readme",
        "new-adr",
        "search-strategy-check",
        "sync-context",
        "to-brd",
        "to-issues",
        "to-prd",
        "to-tasks",
        "visual-explainer",
        "write-a-skill",
    }
)
# Examples Databricks / keyvault ficam fora do install (não no stack_map).
FORBIDDEN_STACK_MAP_EXAMPLE_MARKERS = (
    "examples/databricks-sdp-min",
    "examples/databricks-dlt-min",
    "databricks-sdp-min",
    "databricks-dlt-min",
    "examples/keyvault-oci-min",
    "examples/keyvault-azure-min",
    "keyvault-oci-min",
    "keyvault-azure-min",
)


def _pipeline_category(stack_map: dict) -> dict:
    for category in stack_map["categories"]:
        if category["name"] == "pipeline_dados":
            return category
    raise AssertionError("categoria pipeline_dados ausente no stack_map")


def test_stack_map_pipeline_dados_frozen_vs_loop3() -> None:
    """AC9: condition always + paths do pacote completo Loop 3."""
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        category = _pipeline_category(data)
        condition = category["condition"]

        assert condition["type"] == "always"

        paths = tuple(str(item["path"]) for item in category["artifacts"])
        assert paths == FROZEN_PIPELINE_ARTIFACT_PATHS

        seed = next(
            item for item in category["artifacts"] if item["path"] == ".harness/data-check"
        )
        assert seed["kind"] == "copy"
        assert seed.get("from") == "config/canonical_data_check/templates/data-check"
        assert seed.get("seed") is True

        comment = str(category.get("_comment", "")).lower()
        assert "nao copiar" not in comment
        assert "agents" in comment or "data-engineering" in comment


def test_stack_map_pipeline_dados_espelho_identico() -> None:
    """AC10: categoria pipeline_dados idêntica em .claude e .cursor."""
    categories = []
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        categories.append(_pipeline_category(data))
    assert categories[0] == categories[1]


def test_stack_map_sem_artifacts_databricks_examples() -> None:
    """AC9: install não ganha examples Databricks (kb/databricks é permitido)."""
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        blob = json.dumps(data, ensure_ascii=False).lower()
        for marker in FORBIDDEN_STACK_MAP_EXAMPLE_MARKERS:
            assert marker.lower() not in blob, (
                f"{stack_map_path} não deve referenciar example {marker!r}"
            )
        assert ".claude/kb/databricks" in {
            str(item["path"]) for item in _pipeline_category(data)["artifacts"]
        }


def test_inventario_agents_skills_kbs_loop3() -> None:
    """Inventário canônico — 10 agents DE, 7 commands DE, 24 skills, 21 KBs."""
    for agents_root in (
        REPO_ROOT / ".claude" / "agents" / "data-engineering",
        REPO_ROOT / ".cursor" / "agents" / "data-engineering",
    ):
        names = {path.name for path in agents_root.glob("*.md")}
        assert names == FROZEN_DE_AGENTS

    for commands_root in (
        REPO_ROOT / ".claude" / "commands" / "data-engineering",
        REPO_ROOT / ".cursor" / "commands" / "data-engineering",
    ):
        names = {path.name for path in commands_root.glob("*.md")}
        assert names == FROZEN_DE_COMMANDS

    for skills_root in (REPO_ROOT / ".claude" / "skills", REPO_ROOT / ".cursor" / "skills"):
        skill_dirs = {path.name for path in skills_root.iterdir() if path.is_dir()}
        assert skill_dirs == FROZEN_SKILL_DIRS
        assert len(skill_dirs) == 24
        assert "de-conformidade" in skill_dirs
        assert "cloud-secrets" in skill_dirs

    for kb_root in (REPO_ROOT / ".claude" / "kb", REPO_ROOT / ".cursor" / "kb"):
        domains = {path.name for path in kb_root.iterdir() if path.is_dir()}
        assert domains == FROZEN_KB_DOMAINS
        assert len(domains) == 21
        assert "databricks" in domains
        assert "oci-vault" in domains and "azure-keyvault" in domains


def test_espelho_artefatos_criticos_loop3() -> None:
    """AC10: espelho .claude↔.cursor nos artefatos críticos (Loop 3 + keyvault)."""
    pairs = (
        (
            REPO_ROOT / ".claude" / "skills" / "de-conformidade" / "SKILL.md",
            REPO_ROOT / ".cursor" / "skills" / "de-conformidade" / "SKILL.md",
        ),
        (
            REPO_ROOT / ".claude" / "skills" / "cloud-secrets" / "SKILL.md",
            REPO_ROOT / ".cursor" / "skills" / "cloud-secrets" / "SKILL.md",
        ),
        (
            REPO_ROOT / ".claude" / "kb" / "databricks" / "index.md",
            REPO_ROOT / ".cursor" / "kb" / "databricks" / "index.md",
        ),
        (
            REPO_ROOT / ".claude" / "kb" / "oci-vault" / "index.md",
            REPO_ROOT / ".cursor" / "kb" / "oci-vault" / "index.md",
        ),
        (
            REPO_ROOT / ".claude" / "kb" / "azure-keyvault" / "index.md",
            REPO_ROOT / ".cursor" / "kb" / "azure-keyvault" / "index.md",
        ),
        (
            REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
            REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
        ),
        (
            REPO_ROOT / ".claude" / "skills" / "install-harness" / "SKILL.md",
            REPO_ROOT / ".cursor" / "skills" / "install-harness" / "SKILL.md",
        ),
    )
    for left, right in pairs:
        assert left.is_file(), left
        assert right.is_file(), right
        assert left.read_text(encoding="utf-8") == right.read_text(encoding="utf-8")


def test_example_smoke_basenames_unique_for_root_pytest_collection() -> None:
    """Regressão Tasks 21–22: basenames únicos sob examples/*/tests/."""
    smoke_files = sorted((REPO_ROOT / "examples").glob("*/tests/test_*.py"))
    assert smoke_files, "nenhum smoke encontrado em examples/*/tests/"
    basenames = [path.name for path in smoke_files]
    assert len(basenames) == len(set(basenames)), (
        "colisão de basename na coleta pytest raiz: " + ", ".join(basenames)
    )


def test_example_spark_yarn_airflow_min_validate_ainda_passa() -> None:
    """Regressão Loop 1: validate A/B(+C) no example spark-yarn continua PASS."""
    example = REPO_ROOT / "examples" / "spark-yarn-airflow-min"
    result = validate_project(example, contract_path=CONTRACT_PATH)
    failed = {
        finding.rule_id
        for finding in result.findings
        if finding.status == "fail" and finding.rule_id.startswith(("DE-A", "DE-B", "DE-C"))
    }
    assert result.exit_code == EXIT_OK
    assert not failed


def test_canonico_root_nao_dispara_data_check_por_examples_aninhados() -> None:
    """Gate /validar no canônico: examples Databricks aninhados não ativam data-check."""
    assert has_de_marker(REPO_ROOT) is False
    assert data_check_validate_argv(REPO_ROOT) is None
