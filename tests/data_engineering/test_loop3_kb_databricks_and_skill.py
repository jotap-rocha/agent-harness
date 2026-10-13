"""Loop 3 Tasks 28–29: KB databricks + skill de-conformidade + espelho."""

from __future__ import annotations

from pathlib import Path

import yaml  # type: ignore[import-untyped]

REPO_ROOT = Path(__file__).resolve().parents[2]

DE_D_IDS = ("DE-D001", "DE-D002", "DE-D003", "DE-D004", "DE-D005")

DATABRICKS_REQUIRED_RELATIVE = (
    "index.md",
    "quick-reference.md",
    "concepts/dab-bundle-identity.md",
    "concepts/sdp-medallion.md",
    "concepts/dlt-quarantine-expectations.md",
    "concepts/schema-rescue.md",
    "concepts/unity-catalog-fs-grants-lineage.md",
    "patterns/greenfield-sdp-min.md",
    "patterns/dlt-quarantine.md",
    "patterns/dab-identity.md",
)

SECRET_MARKERS = (
    "DATABRICKS_TOKEN=",
    "password:",
    "api_key:",
    "Bearer ",
    "sk-",
)

EXPECTED_INDEX_AGENTS = {
    "lakehouse-architect",
    "data-platform-engineer",
    "data-quality-analyst",
    "schema-designer",
}


def _kb_roots() -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "kb" / "databricks",
        REPO_ROOT / ".cursor" / "kb" / "databricks",
    )


def _skill_roots() -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "skills" / "de-conformidade",
        REPO_ROOT / ".cursor" / "skills" / "de-conformidade",
    )


def _index_yaml_paths() -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "kb" / "_index.yaml",
        REPO_ROOT / ".cursor" / "kb" / "_index.yaml",
    )


def _walk_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file())


def test_ac4_kb_databricks_arvore_minima() -> None:
    """AC4: árvore kb/databricks com index, quick-ref, concepts e patterns."""
    claude, _ = _kb_roots()
    assert claude.is_dir(), "domínio .claude/kb/databricks/ ausente"
    for rel in DATABRICKS_REQUIRED_RELATIVE:
        path = claude / rel
        assert path.is_file(), f"faltando {rel}"
        assert path.stat().st_size > 0, f"arquivo vazio: {rel}"


def test_ac4_kb_cita_de_d001_a_d005_sem_secrets() -> None:
    """AC4/AC11: conteúdo cita DE-D001…005; sem live API/credenciais."""
    claude, _ = _kb_roots()
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in _walk_files(claude))
    for rule_id in DE_D_IDS:
        assert rule_id in corpus, f"KB databricks não cita {rule_id}"
    lower = corpus.lower()
    assert "data-engineering.yaml" in corpus
    assert "live api" in lower or "sem api live" in lower or "não consulta" in lower
    for marker in SECRET_MARKERS:
        assert marker not in corpus, f"possível secret no KB: {marker!r}"


def test_ac4_index_yaml_declara_dominio_databricks() -> None:
    """AC4: _index.yaml lista domínio databricks com entry_points e agents."""
    claude_idx, _ = _index_yaml_paths()
    data = yaml.safe_load(claude_idx.read_text(encoding="utf-8"))
    domains = data["domains"]
    assert "databricks" in domains
    entry = domains["databricks"]
    assert entry["path"] == "databricks/"
    assert "index" in entry["entry_points"]
    assert "quick_reference" in entry["entry_points"]
    agents = set(entry["agents"])
    assert EXPECTED_INDEX_AGENTS <= agents
    concept_names = {c["name"] for c in entry["concepts"]}
    assert {
        "dab-bundle-identity",
        "sdp-medallion",
        "dlt-quarantine-expectations",
        "schema-rescue",
        "unity-catalog-fs-grants-lineage",
    } <= concept_names
    pattern_names = {p["name"] for p in entry["patterns"]}
    assert {"greenfield-sdp-min", "dlt-quarantine", "dab-identity"} <= pattern_names


def test_ac4_kb_databricks_espelho_identico() -> None:
    """AC10: espelho byte-a-byte .claude/kb/databricks ↔ .cursor/kb/databricks."""
    claude, cursor = _kb_roots()
    claude_files = {p.relative_to(claude): p for p in _walk_files(claude)}
    cursor_files = {p.relative_to(cursor): p for p in _walk_files(cursor)}
    assert set(claude_files) == set(cursor_files)
    for rel, cpath in claude_files.items():
        assert cpath.read_bytes() == cursor_files[rel].read_bytes(), rel
    claude_idx, cursor_idx = _index_yaml_paths()
    assert claude_idx.read_text(encoding="utf-8") == cursor_idx.read_text(
        encoding="utf-8"
    )


def test_ac5_skill_de_conformidade_existe_com_description() -> None:
    """AC5: SKILL.md com frontmatter description acionável."""
    claude, _ = _skill_roots()
    skill = claude / "SKILL.md"
    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "name: de-conformidade" in text
    assert "description:" in text
    # description deve orientar quando usar
    assert "Use when" in text or "Use quando" in text
    assert "canonical_data_check" in text


def test_ac5_skill_cobre_findings_remediacao_baseline_waiver() -> None:
    """AC5: skill cobre findings → remediação → baseline/waiver."""
    claude, _ = _skill_roots()
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in _walk_files(claude))
    for token in (
        "canonical_data_check",
        "validate",
        "report",
        "explain",
        "rule_id",
        "remediation",
        "baseline",
        "waiver",
        "owner",
        "expiry",
        "corrigir",
    ):
        assert token in corpus.lower() or token in corpus, f"faltando âncora {token!r}"
    for marker in SECRET_MARKERS:
        assert marker not in corpus


def test_ac5_skill_espelho_identico() -> None:
    """AC10: espelho .claude/skills/de-conformidade ↔ .cursor/..."""
    claude, cursor = _skill_roots()
    claude_files = {p.relative_to(claude): p for p in _walk_files(claude)}
    cursor_files = {p.relative_to(cursor): p for p in _walk_files(cursor)}
    assert set(claude_files) == set(cursor_files)
    for rel, cpath in claude_files.items():
        assert cpath.read_bytes() == cursor_files[rel].read_bytes(), rel
