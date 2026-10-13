"""Testes Task 39 — categoria cloud_secrets no stack_map / install."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
)

VAULT_ARTIFACTS = frozenset(
    {
        ".claude/skills/cloud-secrets",
        ".claude/kb/oci-vault",
        ".claude/kb/azure-keyvault",
    }
)
FORBIDDEN_EXAMPLE_MARKERS = (
    "keyvault-oci-min",
    "keyvault-azure-min",
    "examples/keyvault",
)


def _load_install():
    spec = importlib.util.spec_from_file_location(
        "install_harness_vault_test",
        INSTALL_SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _vault_category(stack_map: dict) -> dict:
    for category in stack_map["categories"]:
        if category["name"] == "cloud_secrets":
            return category
    raise AssertionError("categoria cloud_secrets ausente no stack_map")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_stack_map_declares_cloud_secrets_category() -> None:
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        category = _vault_category(data)
        condition = category["condition"]
        assert condition["type"] == "keyword_in_files"
        assert condition["type"] != "always"
        assert category["name"] != "pipeline_dados"
        keywords = {str(k).lower() for k in condition["keywords"]}
        assert "secret_store" in keywords or "keyvault" in keywords
        paths = {str(item["path"]) for item in category["artifacts"]}
        assert paths == VAULT_ARTIFACTS
        blob = json.dumps(data)
        for marker in FORBIDDEN_EXAMPLE_MARKERS:
            assert marker not in blob


def test_stack_map_cloud_secrets_espelho() -> None:
    a = json.loads(STACK_MAP_PATHS[0].read_text(encoding="utf-8"))
    b = json.loads(STACK_MAP_PATHS[1].read_text(encoding="utf-8"))
    assert _vault_category(a) == _vault_category(b)


def test_install_plan_includes_vault_with_secret_store_marker(tmp_path: Path) -> None:
    install = _load_install()
    target = tmp_path / "filho-vault"
    target.mkdir()
    _write(
        target / ".harness" / "data-check" / "project_profile.yaml",
        "profile: spark-yarn-airflow\nsecret_store: oci\n",
    )
    _write(target / "pyproject.toml", "[project]\nname='demo'\n")

    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    plan = install.build_plan(target, REPO_ROOT, stack_map, None, signals)
    planned = {
        item["path"]
        for item in plan
        if item["category"] == "cloud_secrets" and item["action"] != "SKIP_STACK"
    }
    assert planned == VAULT_ARTIFACTS


def test_install_plan_includes_vault_with_keyvault_dep(tmp_path: Path) -> None:
    install = _load_install()
    target = tmp_path / "filho-dep"
    target.mkdir()
    _write(
        target / "pyproject.toml",
        (
            "[project]\nname='demo'\ndependencies=["
            "'azure-keyvault-secrets>=4.0']\n"
        ),
    )
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    plan = install.build_plan(target, REPO_ROOT, stack_map, None, signals)
    planned = {
        item["path"]
        for item in plan
        if item["category"] == "cloud_secrets" and item["action"] != "SKIP_STACK"
    }
    assert planned == VAULT_ARTIFACTS


def test_install_plan_excludes_vault_without_flag(tmp_path: Path) -> None:
    install = _load_install()
    target = tmp_path / "filho-plain"
    target.mkdir()
    _write(
        target / "pyproject.toml",
        "[project]\nname='demo'\ndependencies=['fastapi']\n",
    )
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(target, install.collect_keywords(stack_map))
    plan = install.build_plan(target, REPO_ROOT, stack_map, None, signals)
    active = [
        item
        for item in plan
        if item["category"] == "cloud_secrets" and item["action"] != "SKIP_STACK"
    ]
    assert active == []
    assert all(
        item["action"] == "SKIP_STACK"
        for item in plan
        if item["category"] == "cloud_secrets"
    )


def test_pipeline_dados_nao_inclui_sempre_cloud_secrets() -> None:
    for stack_map_path in STACK_MAP_PATHS:
        data = json.loads(stack_map_path.read_text(encoding="utf-8"))
        pipeline = next(c for c in data["categories"] if c["name"] == "pipeline_dados")
        paths = {str(item["path"]) for item in pipeline["artifacts"]}
        assert ".claude/skills/cloud-secrets" not in paths
        assert ".claude/kb/oci-vault" not in paths
        assert ".claude/kb/azure-keyvault" not in paths
