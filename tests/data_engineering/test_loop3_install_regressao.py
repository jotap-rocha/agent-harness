"""Regressão Loop 3 — examples validate + fixture install completo (Task 31)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_OK, validate_project

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
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
EXAMPLES = (
    "spark-yarn-airflow-min",
    "databricks-sdp-min",
    "databricks-dlt-min",
)


def _load_install_module():
    spec = importlib.util.spec_from_file_location(
        "install_harness_loop3_regressao",
        INSTALL_SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_tres_examples_exit_ok() -> None:
    """AC8: validate PASS nos 3 examples oficiais."""
    for name in EXAMPLES:
        example = REPO_ROOT / "examples" / name
        result = validate_project(example, contract_path=CONTRACT_PATH)
        assert result.exit_code == EXIT_OK, (
            f"{name}: exit={result.exit_code} findings="
            f"{[f.rule_id for f in result.findings if f.status == 'fail']}"
        )


def test_pipeline_dados_copia_camada_agentic_completa(tmp_path: Path) -> None:
    """AC7: install padrão copia 10 agents + 7 commands + skill/KB (sem --force-category)."""
    target = tmp_path / "filho-default"
    target.mkdir()
    (target / "README.md").write_text("# filho default\n", encoding="utf-8")

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

    agents = target / ".claude" / "agents" / "data-engineering"
    commands = target / ".claude" / "commands" / "data-engineering"
    assert agents.is_dir()
    assert commands.is_dir()
    assert {p.name for p in agents.glob("*.md")} == FROZEN_DE_AGENTS
    assert {p.name for p in commands.glob("*.md")} == FROZEN_DE_COMMANDS
    assert (target / ".claude" / "skills" / "de-conformidade" / "SKILL.md").is_file()
    assert (target / ".claude" / "kb" / "databricks" / "index.md").is_file()
    assert (target / ".cursor" / "agents" / "data-engineering").is_dir()
    assert (target / ".cursor" / "commands" / "data-engineering").is_dir()
    assert (target / ".harness" / "data-check" / "baseline.json").is_file()


def test_reinstall_pipeline_dados_keep_seed(tmp_path: Path) -> None:
    """AC7: re-install padrão continua KEEP em `.harness/data-check`."""
    target = tmp_path / "filho-reinstall-default"
    target.mkdir()
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

    baseline = target / ".harness" / "data-check" / "baseline.json"
    marker = {"version": 1, "profile": "spark-yarn-airflow", "findings": [{"code": "DE-A001"}]}
    baseline.write_text(json.dumps(marker), encoding="utf-8")

    install = _load_install_module()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    plan = install.build_plan(
        target,
        REPO_ROOT,
        stack_map,
        manifest,
        signals,
    )
    seed_items = [i for i in plan if i["path"] == ".harness/data-check"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    second = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert second.returncode == 0, second.stderr or second.stdout
    saved = json.loads(baseline.read_text(encoding="utf-8"))
    assert saved["findings"][0]["code"] == "DE-A001"
