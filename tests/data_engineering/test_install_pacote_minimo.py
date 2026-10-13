"""Testes do install pacote DE completo (Task 15 legado + Task 30 / AC6–AC7)."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_OK
from config.canonical_data_check.waivers_yaml import parse_waivers_document
from config.data_engineering.yaml_loader import load_mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
)
DATA_CHECK_DIR = Path(".harness") / "data-check"
AGENT_DIR = Path(".claude") / "agents" / "data-engineering"
COMMAND_DIR = Path(".claude") / "commands" / "data-engineering"

EXPECTED_PIPELINE_CORE = frozenset(
    {
        "data-engineering.yaml",
        ".claude/kb/pipeline",
        ".claude/kb/databricks",
        ".claude/rules/pipeline.md",
        ".claude/agents/data-engineering",
        ".claude/commands/data-engineering",
        ".claude/skills/de-conformidade",
        ".harness/data-check",
    }
)
EXPECTED_PIPELINE_KB_ADJACENT = frozenset(
    {
        ".claude/kb/airflow",
        ".claude/kb/spark",
        ".claude/kb/lakehouse",
        ".claude/kb/data-quality",
        ".claude/kb/dbt",
        ".claude/kb/data-modeling",
        ".claude/kb/sql-patterns",
        ".claude/kb/streaming",
        ".claude/kb/cloud-platforms",
    }
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


def _load_install_module():
    spec = importlib.util.spec_from_file_location(
        "install_harness_under_test",
        INSTALL_SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pipeline_category(stack_map: dict) -> dict:
    for category in stack_map["categories"]:
        if category["name"] == "pipeline_dados":
            return category
    raise AssertionError("categoria pipeline_dados ausente no stack_map")


def _write_pyproject_with_spark(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "pyproject.toml").write_text(
        '[project]\nname = "filho-de"\nversion = "0.0.1"\n'
        'dependencies = ["pyspark>=3.5"]\n',
        encoding="utf-8",
    )


def test_stack_map_pipeline_dados_declara_pacote_completo() -> None:
    """AC6: condition always + artefatos do pacote completo no stack_map (espelho .claude/.cursor)."""
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        category = _pipeline_category(data)
        condition = category["condition"]
        assert condition["type"] == "always"

        paths = {str(item["path"]) for item in category["artifacts"]}
        assert EXPECTED_PIPELINE_CORE.issubset(paths)
        assert EXPECTED_PIPELINE_KB_ADJACENT.issubset(paths)

        comment = str(category.get("_comment", "")).lower()
        assert "nao copiar" not in comment
        assert "agents" in comment or "data-engineering" in comment

        seed = next(
            item for item in category["artifacts"] if item["path"] == ".harness/data-check"
        )
        assert seed["kind"] == "copy"
        assert seed.get("from") == "config/canonical_data_check/templates/data-check"
        assert seed.get("seed") is True

        assert ".claude/agents/data-engineering" in paths
        assert ".claude/commands/data-engineering" in paths
        assert ".claude/skills/de-conformidade" in paths
        assert ".claude/kb/databricks" in paths


def test_stack_map_pipeline_dados_espelho_skill_prosa() -> None:
    """AC6: SKILL.md documenta pacote completo (sem proibição Loop 2)."""
    for skill_path in (
        REPO_ROOT / ".claude" / "skills" / "install-harness" / "SKILL.md",
        REPO_ROOT / ".cursor" / "skills" / "install-harness" / "SKILL.md",
    ):
        text = skill_path.read_text(encoding="utf-8")
        assert "pacote completo" in text.lower()
        assert "agents/data-engineering" in text
        assert "commands/data-engineering" in text
        assert "de-conformidade" in text
        assert "kb/databricks" in text or "`databricks`" in text
        assert "Não** copia" not in text
        assert "**Não** copia" not in text


def test_install_cria_harness_data_check_com_perfil_default(tmp_path: Path) -> None:
    """Install em dest mínimo cria `.harness/data-check/` com perfil spark-yarn-airflow."""
    target = tmp_path / "filho"
    _write_pyproject_with_spark(target)

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

    data_check = target / DATA_CHECK_DIR
    profile_path = data_check / "project_profile.yaml"
    baseline_path = data_check / "baseline.json"
    waivers_path = data_check / "waivers.yaml"

    assert profile_path.is_file()
    assert baseline_path.is_file()
    assert waivers_path.is_file()

    profile = load_mapping(profile_path)
    assert profile["profile"] == "spark-yarn-airflow"

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert baseline["version"] == 1
    assert baseline["findings"] == []
    assert baseline.get("profile") == "spark-yarn-airflow"

    waivers = parse_waivers_document(waivers_path.read_text(encoding="utf-8"))
    assert isinstance(waivers, list)
    assert waivers == []

    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    seed_entry = manifest["artefacts"][".harness/data-check"]
    assert seed_entry["customized"] is True
    assert seed_entry.get("seed") is True


def test_reinstall_preserva_baseline_e_waivers_do_filho(tmp_path: Path) -> None:
    """Seed: 2º install faz KEEP — não apaga baseline/waivers do filho."""
    target = tmp_path / "filho-reinstall"
    _write_pyproject_with_spark(target)

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

    data_check = target / DATA_CHECK_DIR
    baseline_path = data_check / "baseline.json"
    waivers_path = data_check / "waivers.yaml"
    baseline_path.write_text(
        json.dumps(
            {
                "version": 1,
                "profile": "spark-yarn-airflow",
                "findings": [{"code": "LAY.A.01", "severity": "blocker"}],
            }
        ),
        encoding="utf-8",
    )
    waivers_path.write_text(
        "schema_version: 1\nwaivers:\n"
        "  - code: LAY.A.01\n    reason: legado piloto\n"
        "    expires: '2099-01-01'\n    owner: equipe-de\n",
        encoding="utf-8",
    )

    install = _load_install_module()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    plan2 = install.build_plan(
        target, REPO_ROOT, stack_map, manifest, signals
    )
    seed_items = [i for i in plan2 if i["path"] == ".harness/data-check"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    second = subprocess.run(
        common, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    assert second.returncode == 0, second.stderr or second.stdout

    saved = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert saved["findings"][0]["code"] == "LAY.A.01"
    assert "LAY.A.01" in waivers_path.read_text(encoding="utf-8")

    manifest_after = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    seed_after = manifest_after["artefacts"][".harness/data-check"]
    assert seed_after["customized"] is True
    assert seed_after.get("seed") is True


def test_install_pacote_copia_agents_commands_skill_kb(tmp_path: Path) -> None:
    """AC6/AC7: CLI utilizável; copia 10 agents + 7 commands + skill + KB databricks."""
    target = tmp_path / "filho-cli"
    _write_pyproject_with_spark(target)

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

    assert (target / "data-engineering.yaml").is_file()
    assert (target / "config" / "canonical_data_check" / "__main__.py").is_file()
    assert (target / "config" / "data_engineering" / "yaml_loader.py").is_file()
    assert (target / ".claude" / "kb" / "pipeline").is_dir()
    assert (target / ".claude" / "kb" / "databricks").is_dir()
    assert (target / ".claude" / "rules" / "pipeline.md").is_file()
    assert (target / ".cursor" / "rules" / "pipeline.mdc").is_file()
    assert (target / ".claude" / "skills" / "de-conformidade" / "SKILL.md").is_file()

    agent_names = {p.name for p in (target / AGENT_DIR).glob("*.md")}
    command_names = {p.name for p in (target / COMMAND_DIR).glob("*.md")}
    assert agent_names == FROZEN_DE_AGENTS
    assert command_names == FROZEN_DE_COMMANDS
    assert (target / ".cursor" / "agents" / "data-engineering").is_dir()
    assert (target / ".cursor" / "commands" / "data-engineering").is_dir()

    validate = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "validate",
            str(target),
            "--contract",
            str(target / "data-engineering.yaml"),
            "--format",
            "json",
        ],
        cwd=target,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": str(target)},
    )
    # Dest mínimo sem layout A/B → blockers esperados; o que importa é a CLI rodar.
    assert validate.returncode in {EXIT_OK, 1, 2}, validate.stderr or validate.stdout
    payload = json.loads(validate.stdout)
    assert "exit_code" in payload
    assert "findings" in payload


def test_build_plan_seed_keep_mesmo_com_customized_false_legado(tmp_path: Path) -> None:
    """Bloqueante review: seed NUNCA vira AUTO_UPDATE mesmo com customized:false."""
    install = _load_install_module()
    target = tmp_path / "legado"
    target.mkdir()
    _write_pyproject_with_spark(target)
    data_check = target / DATA_CHECK_DIR
    data_check.mkdir(parents=True)
    (data_check / "baseline.json").write_text('{"version":1,"findings":[]}', encoding="utf-8")

    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    manifest = {
        "artefacts": {
            ".harness/data-check": {"source": "canonical", "customized": False},
        }
    }
    plan = install.build_plan(target, REPO_ROOT, stack_map, manifest, signals)
    seed_items = [i for i in plan if i["path"] == ".harness/data-check"]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "KEEP"
    assert seed_items[0].get("seed") is True

    apply_counts = install.apply_plan(
        seed_items,
        target,
        REPO_ROOT,
        "legado",
        "pipeline",
        "ATUALIZAÇÃO",
        manifest,
    )
    assert apply_counts["kept"] >= 1
    written = json.loads(
        (target / ".claude" / "harness-manifest.json").read_text(encoding="utf-8")
    )
    entry = written["artefacts"][".harness/data-check"]
    assert entry["customized"] is True
    assert entry.get("seed") is True


def test_build_plan_pipeline_dados_sempre_inclui_seed(tmp_path: Path) -> None:
    """pipeline_dados entra por padrão (always) mesmo sem keywords no destino."""
    install = _load_install_module()
    target = tmp_path / "sem-keyword"
    target.mkdir()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    plan = install.build_plan(
        target,
        REPO_ROOT,
        stack_map,
        None,
        signals,
    )
    seed_items = [
        item
        for item in plan
        if item["category"] == "pipeline_dados" and item["path"] == ".harness/data-check"
    ]
    assert len(seed_items) == 1
    assert seed_items[0]["action"] == "COPY"
    assert seed_items[0].get("from") == "config/canonical_data_check/templates/data-check"
    assert seed_items[0].get("seed") is True
    assert not seed_items[0].get("forced")

    agent_items = [
        item
        for item in plan
        if item["category"] == "pipeline_dados"
        and item["path"] == ".claude/agents/data-engineering"
    ]
    assert len(agent_items) == 1
    assert agent_items[0]["action"] == "COPY"
    assert not agent_items[0].get("forced")
