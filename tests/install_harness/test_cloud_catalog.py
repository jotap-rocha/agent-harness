"""Pacote multi-cloud: agnosticidade de agentes, contrato das KBs de serviço e detecção no install."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_SCRIPT = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "install_harness.py"
)
STACK_MAP_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "install-harness" / "scripts" / "stack_map.json",
    REPO_ROOT / ".cursor" / "skills" / "install-harness" / "scripts" / "stack_map.json",
)
TREES = (REPO_ROOT / ".claude", REPO_ROOT / ".cursor")

PROVIDERS = ("azure", "aws", "gcp")
ROLES = ("iac-provider", "warehouse", "streaming", "object-storage", "stream-processing")
ROLE_PATTERNS = {
    "iac-provider": ("provider-auth.md", "remote-state.md"),
    "warehouse": ("bulk-load.md", "merge-scd2.md"),
    "streaming": ("kafka-client-auth.md", "kafka-connect-sink.md"),
    "object-storage": ("service-identity-access.md",),
    "stream-processing": ("reference-data.md",),
}
REQUIRED_INDEX_SECTIONS = ("## Papel", "## Custo e free tier", "## SI", "## Por que este serviço")
CLOUD_AGENTS = ("cloud-data-engineer.md", "iac-engineer.md")

# Nomes de provider/serviço que nunca podem aparecer num agente de nuvem: a especialização
# mora só nas KBs (regra central do pacote).
FORBIDDEN_IN_AGENTS = re.compile(
    r"\b(azure|aws|amazon|gcp|google|microsoft|synapse|event ?hubs?|adls|redshift|msk|"
    r"bigquery|dataflow|kinesis|pub/?sub|s3|gcs|stream analytics|azurerm)\b",
    re.IGNORECASE,
)
# Placeholders permitidos (SI) não contam como acoplamento.
ID_LIKE = re.compile(r"\b\d{12}\b|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _load_install():
    spec = importlib.util.spec_from_file_location("install_harness_cloud_test", INSTALL_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _index() -> dict:
    return yaml.safe_load((REPO_ROOT / ".claude" / "kb" / "_index.yaml").read_text("utf-8"))


def _service_domains() -> dict[str, dict]:
    return {name: d for name, d in _index()["domains"].items() if "provider" in d}


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _active(plan: list[dict], category: str) -> set[str]:
    return {i["path"] for i in plan if i["category"] == category and i["action"] != "SKIP_STACK"}


# --- agnosticidade ---------------------------------------------------------------------


@pytest.mark.parametrize("tree", TREES, ids=lambda p: p.name)
@pytest.mark.parametrize("agent", CLOUD_AGENTS)
def test_agentes_de_nuvem_nao_citam_provider_nem_servico(tree: Path, agent: str) -> None:
    text = (tree / "agents" / "cloud" / agent).read_text(encoding="utf-8")
    hits = sorted({m.group(0).lower() for m in FORBIDDEN_IN_AGENTS.finditer(text)})
    assert hits == [], f"{agent} acoplado a provider/serviço: {hits}"


@pytest.mark.parametrize("agent", CLOUD_AGENTS)
def test_agentes_de_nuvem_fazem_passo_0_pela_kb(agent: str) -> None:
    text = (REPO_ROOT / ".claude" / "agents" / "cloud" / agent).read_text(encoding="utf-8")
    assert "Passo 0" in text
    assert "cloud-resolution" in text
    assert "_index.yaml" in text
    assert "kb-architect" in text  # caminho de saída quando não há KB para provider/role


# --- contrato das KBs de serviço --------------------------------------------------------


def test_matriz_completa_role_por_provider() -> None:
    pairs = [(d["provider"], d["role"]) for d in _service_domains().values()]
    assert sorted(pairs) == sorted((p, r) for p in PROVIDERS for r in ROLES)


@pytest.mark.parametrize("name", sorted(_service_domains()))
def test_kb_de_servico_cumpre_contrato(name: str) -> None:
    domain = _service_domains()[name]
    assert domain["provider"] in PROVIDERS
    assert domain["role"] in ROLES
    assert name.startswith(f"{domain['provider']}-")
    expected_agent = "iac-engineer" if domain["role"] == "iac-provider" else "cloud-data-engineer"
    assert expected_agent in domain["agents"]

    for tree in TREES:
        root = tree / "kb" / name
        index = (root / "index.md").read_text(encoding="utf-8")
        for section in REQUIRED_INDEX_SECTIONS:
            assert section in index, f"{root}/index.md sem {section!r}"
        assert (root / "quick-reference.md").is_file()
        for pattern in ROLE_PATTERNS[domain["role"]]:
            assert (root / "patterns" / pattern).is_file(), f"{root} sem patterns/{pattern}"
        for entry in domain["concepts"] + domain["patterns"]:
            assert (root / entry["path"]).is_file(), f"{root}/{entry['path']} no índice mas ausente"


@pytest.mark.parametrize("name", sorted(_service_domains()) + ["cloud-resolution", "terraform"])
def test_kb_de_nuvem_respeita_limites_e_si(name: str) -> None:
    limits = _index()["limits"]
    root = REPO_ROOT / ".claude" / "kb" / name
    for md in root.rglob("*.md"):
        lines = len(md.read_text(encoding="utf-8").splitlines())
        if md.name == "quick-reference.md":
            assert lines <= limits["quick_reference"], md
        elif md.parent.name == "concepts":
            assert lines <= limits["concept"], md
        elif md.parent.name == "patterns":
            assert lines <= limits["pattern"], md
        assert not ID_LIKE.search(md.read_text(encoding="utf-8")), f"ID real em {md}"


@pytest.mark.parametrize("name", sorted(_service_domains()) + ["cloud-resolution", "terraform"])
def test_kb_de_nuvem_espelhada_no_cursor(name: str) -> None:
    claude_root = REPO_ROOT / ".claude" / "kb" / name
    cursor_root = REPO_ROOT / ".cursor" / "kb" / name
    claude_files = {p.relative_to(claude_root) for p in claude_root.rglob("*") if p.is_file()}
    cursor_files = {p.relative_to(cursor_root) for p in cursor_root.rglob("*") if p.is_file()}
    assert claude_files == cursor_files
    for rel in claude_files:
        assert (claude_root / rel).read_bytes() == (cursor_root / rel).read_bytes(), rel


# --- stack_map ------------------------------------------------------------------------


@pytest.mark.parametrize("stack_map_path", STACK_MAP_PATHS, ids=lambda p: p.parts[-5])
def test_stack_map_declara_categorias_de_nuvem(stack_map_path: Path) -> None:
    data = json.loads(stack_map_path.read_text(encoding="utf-8"))
    categories = {c["name"]: c for c in data["categories"]}
    assert categories["cloud_core"]["condition"]["keywords"] == ["cloud_any"]
    for provider in PROVIDERS:
        category = categories[f"cloud_{provider}"]
        assert category["condition"]["keywords"] == [f"cloud_{provider}"]
        kbs = {a["path"] for a in category["artifacts"] if a["path"].startswith(".claude/kb/")}
        expected = {f".claude/kb/{n}" for n, d in _service_domains().items()
                    if d["provider"] == provider}
        assert kbs == expected
    for name in ("cloud_core", *(f"cloud_{p}" for p in PROVIDERS)):
        for artefact in categories[name]["artifacts"]:
            assert (REPO_ROOT / artefact["path"]).exists(), artefact["path"]


# --- detecção ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("tf_provider", "cloud"),
    [("azurerm", "azure"), ("aws", "aws"), ("google", "gcp"), ("google-beta", "gcp")],
)
def test_detecta_nuvem_por_provider_terraform(tmp_path: Path, tf_provider: str, cloud: str) -> None:
    install = _load_install()
    _write(tmp_path / "infra" / "main.tf", f'provider "{tf_provider}" {{\n}}\n')
    assert install.detect_clouds(tmp_path, set()) == {cloud}


def test_detecta_nuvem_por_dependencia(tmp_path: Path) -> None:
    install = _load_install()
    assert install.detect_clouds(tmp_path, {"boto3", "pandas"}) == {"aws"}
    assert install.detect_clouds(tmp_path, {"google-cloud-bigquery"}) == {"gcp"}
    assert install.detect_clouds(tmp_path, {"@azure/storage-blob"}) == {"azure"}


def test_campo_cloud_do_claude_md_vence_e_multi_ativa_todas(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "main.tf", 'provider "aws" {}\n')
    _write(tmp_path / "CLAUDE.md", "## Stack\ncloud: gcp   # declarado\n")
    assert install.detect_clouds(tmp_path, set()) == {"gcp"}
    _write(tmp_path / "CLAUDE.md", "## Stack\ncloud: multi\n")
    assert install.detect_clouds(tmp_path, set()) == set(PROVIDERS)


def test_linha_de_template_do_claude_md_nao_e_declaracao(tmp_path: Path) -> None:
    """O template traz `cloud: azure | aws | gcp | multi` — isso não pode ativar Azure."""
    install = _load_install()
    _write(tmp_path / "CLAUDE.md", "cloud: azure | aws | gcp | multi   # Passo 0\n")
    assert install.detect_clouds(tmp_path, set()) == set()


def test_install_plan_ativa_core_e_provider_detectado(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "terraform" / "main.tf", 'provider "azurerm" {\n  features {}\n}\n')
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    plan = install.build_plan(tmp_path, REPO_ROOT, stack_map, None, signals)
    assert ".claude/agents/cloud" in _active(plan, "cloud_core")
    assert ".claude/kb/azure-synapse" in _active(plan, "cloud_azure")
    assert _active(plan, "cloud_aws") == set()
    assert _active(plan, "cloud_gcp") == set()


def test_install_plan_sem_nuvem_nao_ativa_nada(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "pyproject.toml", "[project]\nname='demo'\ndependencies=['fastapi']\n")
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    plan = install.build_plan(tmp_path, REPO_ROOT, stack_map, None, signals)
    for name in ("cloud_core", *(f"cloud_{p}" for p in PROVIDERS)):
        assert _active(plan, name) == set(), name


def test_force_category_cloud_aws_sem_deteccao(tmp_path: Path) -> None:
    install = _load_install()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    plan = install.build_plan(tmp_path, REPO_ROOT, stack_map, None, signals,
                              force_categories=frozenset({"cloud_aws"}))
    assert ".claude/kb/aws-redshift" in _active(plan, "cloud_aws")
    assert _active(plan, "cloud_azure") == set()


# --- regressões do review (JSON, falsos positivos/negativos) ----------------------------


def test_plan_to_json_serializa_sinais_de_nuvem(tmp_path: Path) -> None:
    """Regressão: signals['clouds'] era set e quebrava `--json` em todo install."""
    install = _load_install()
    _write(tmp_path / "main.tf", 'provider "aws" {}\n')
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    plan = install.build_plan(tmp_path, REPO_ROOT, stack_map, None, signals)
    payload = json.loads(json.dumps(install.plan_to_json(plan, "NOVO", signals)))
    assert payload["stack_signals"]["clouds"] == ["aws"]


def test_plan_to_json_sem_nuvem_tambem_serializa(tmp_path: Path) -> None:
    install = _load_install()
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    plan = install.build_plan(tmp_path, REPO_ROOT, stack_map, None, signals)
    payload = json.loads(json.dumps(install.plan_to_json(plan, "NOVO", signals)))
    assert payload["stack_signals"]["clouds"] == []


def test_dependencia_transitiva_de_lockfile_nao_ativa_nuvem(tmp_path: Path) -> None:
    """dbt-snowflake puxa boto3 no uv.lock, mas o projeto declara só snowflake."""
    install = _load_install()
    _write(tmp_path / "pyproject.toml", "[project]\nname='x'\ndependencies=['dbt-snowflake']\n")
    _write(tmp_path / "uv.lock", '[[package]]\nname = "boto3"\nversion = "1.0"\n')
    stack_map = install.load_stack_map(REPO_ROOT)
    signals = install.detect_stack_signals(tmp_path, install.collect_keywords(stack_map))
    assert signals["clouds"] == []


def test_aws_sign2_nao_e_aws(tmp_path: Path) -> None:
    install = _load_install()
    assert install.detect_clouds(tmp_path, {"aws-sign2", "aws4"}) == set()
    assert install.detect_clouds(tmp_path, {"boto3"}) == {"aws"}


def test_terraform_recursivo_e_required_providers(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "infra" / "envs" / "dev" / "versions.tf",
           'terraform {\n  required_providers {\n    google = { source = "hashicorp/google" }\n  }\n}\n')
    assert install.detect_clouds(tmp_path, set()) == {"gcp"}


def test_terraform_ignora_comentario_e_dir_terraform(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "main.tf", '# provider "aws" {}\n// provider "google" {}\n')
    _write(tmp_path / ".terraform" / "x.tf", 'provider "azurerm" {}\n')
    assert install.detect_clouds(tmp_path, set()) == set()


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("cloud: aws, gcp", {"aws", "gcp"}),
        ("- cloud: azure", {"azure"}),
        ("**cloud:** gcp", {"gcp"}),
        ("cloud: none", set()),
    ],
)
def test_campo_cloud_formatos_aceitos(tmp_path: Path, line: str, expected: set[str]) -> None:
    install = _load_install()
    _write(tmp_path / "main.tf", 'provider "aws" {}\n')  # `cloud:` vence a inferência
    _write(tmp_path / "CLAUDE.md", f"## Stack\n{line}\n")
    assert install.detect_clouds(tmp_path, set()) == expected


def test_campo_cloud_em_bloco_de_codigo_nao_conta(tmp_path: Path) -> None:
    install = _load_install()
    _write(tmp_path / "CLAUDE.md", "```yaml\ncloud: aws\n```\n\ncloud: gcp\n")
    assert install.detect_clouds(tmp_path, set()) == {"gcp"}
