"""Task 40 — SI bridge, ADR, de-conformidade DE-E*, docs sync leve."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DE_E_IDS = ("DE-E001", "DE-E002", "DE-E003")

SEGURANCA_PATHS = (
    REPO_ROOT / ".claude" / "rules" / "seguranca.md",
    REPO_ROOT / ".cursor" / "rules" / "seguranca.mdc",
)
DE_SKILL_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "de-conformidade" / "SKILL.md",
    REPO_ROOT / ".cursor" / "skills" / "de-conformidade" / "SKILL.md",
)
DE_REMEDIATION_PATHS = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "de-conformidade"
    / "references"
    / "rule-ids-remediation.md",
    REPO_ROOT
    / ".cursor"
    / "skills"
    / "de-conformidade"
    / "references"
    / "rule-ids-remediation.md",
)
ADR_PATH = REPO_ROOT / "docs" / "adr" / "002-pacote-e-keyvault-cloud-dual-install.md"
ADR_INDEX = REPO_ROOT / "docs" / "adr" / "README.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"
STATUS_PATHS = (
    REPO_ROOT / ".claude" / "projetos" / "keyvault-oci-azure-choice" / "STATUS.md",
    REPO_ROOT / ".cursor" / "projetos" / "keyvault-oci-azure-choice" / "STATUS.md",
)


def _body_after_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        assert end != -1
        return text[end + 3 :].lstrip("\n")
    return text


def test_seguranca_ponte_vault_espelhada() -> None:
    bodies = []
    for path in SEGURANCA_PATHS:
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        assert "nunca logar" in lower
        assert "placeholder" in lower
        assert "key vault" in lower or "keyvault" in lower or "vault" in lower
        assert "de-e" in lower or "DE-E" in text
        bodies.append(_body_after_frontmatter(text))
    assert bodies[0] == bodies[1]


def test_adr_002_keyvault_registrado() -> None:
    assert ADR_PATH.is_file()
    text = ADR_PATH.read_text(encoding="utf-8")
    assert "Pacote E" in text or "keyvault-cloud" in text
    assert "cloud-secrets" in text
    assert "cloud_secrets" in text or "install" in text.lower()
    assert "Impacto em SI" in text or "SI/LGPD" in text
    index = ADR_INDEX.read_text(encoding="utf-8")
    assert "002-pacote-e-keyvault-cloud-dual-install.md" in index


def test_de_conformidade_mapeia_de_e() -> None:
    for path in DE_SKILL_PATHS + DE_REMEDIATION_PATHS:
        text = path.read_text(encoding="utf-8")
        for rule_id in DE_E_IDS:
            assert rule_id in text, f"{rule_id} ausente em {path}"
        assert "keyvault" in text.lower() or "vault" in text.lower()
    assert DE_SKILL_PATHS[0].read_text(encoding="utf-8") == DE_SKILL_PATHS[1].read_text(
        encoding="utf-8"
    )
    assert DE_REMEDIATION_PATHS[0].read_text(
        encoding="utf-8"
    ) == DE_REMEDIATION_PATHS[1].read_text(encoding="utf-8")


def test_claude_agents_refletem_pacote_e_contagens() -> None:
    claude = CLAUDE_MD.read_text(encoding="utf-8")
    agents = AGENTS_MD.read_text(encoding="utf-8")
    for text in (claude, agents):
        assert "| 38 |" in text or "38 domínios" in text  # 21 + 17 multi-cloud
        assert "cloud-secrets" in text or "keyvault" in text.lower() or "pacote E" in text
        assert "DE-E" in text or "keyvault-cloud" in text or "secret_store" in text
    # tabela skills/KBs
    assert "38" in claude and "38" in agents


def test_status_projeto_pronto_para_ship() -> None:
    for path in STATUS_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "Implementação concluída" in text or "[x] 5." in text
        assert "pronto para ship" in text.lower() or "fase atual: 5" in text.lower()
