"""Testes leves Tasks 36–38 — skill/KBs/grill + SI placeholders + espelho."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SKILL_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "cloud-secrets" / "SKILL.md",
    REPO_ROOT / ".cursor" / "skills" / "cloud-secrets" / "SKILL.md",
)
OCI_KB = (
    REPO_ROOT / ".claude" / "kb" / "oci-vault",
    REPO_ROOT / ".cursor" / "kb" / "oci-vault",
)
AZURE_KB = (
    REPO_ROOT / ".claude" / "kb" / "azure-keyvault",
    REPO_ROOT / ".cursor" / "kb" / "azure-keyvault",
)
DEFINE_PATHS = (
    REPO_ROOT / ".claude" / "agents" / "workflow" / "harness-define.md",
    REPO_ROOT / ".cursor" / "agents" / "workflow" / "harness-define.md",
)
GRILL_PATHS = (
    REPO_ROOT / ".claude" / "skills" / "grill-me" / "SKILL.md",
    REPO_ROOT / ".cursor" / "skills" / "grill-me" / "SKILL.md",
)

_KB_MIN = (
    "index.md",
    "quick-reference.md",
    "concepts",
    "patterns",
)

_REAL_SECRET_HEURISTIC = re.compile(
    r"(?i)(-----BEGIN (?:RSA )?PRIVATE KEY-----|sk-[a-zA-Z0-9]{20,})"
)


def test_cloud_secrets_skill_dual_and_mirror() -> None:
    texts = []
    for path in SKILL_PATHS:
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        texts.append(text)
        assert "description:" in text
        assert "facade" in text.lower()
        assert "oci" in text.lower() and "azure" in text.lower()
        assert "nunca logar" in text.lower() or "nunca" in text.lower()
        assert "oci-vault" in text and "azure-keyvault" in text
    assert texts[0] == texts[1]


def test_kbs_oci_azure_parity_and_mirror() -> None:
    for roots in (OCI_KB, AZURE_KB):
        for root in roots:
            assert root.is_dir(), root
            for name in _KB_MIN:
                target = root / name
                assert target.exists(), target
    oci_claude = (OCI_KB[0] / "index.md").read_text(encoding="utf-8")
    azure_claude = (AZURE_KB[0] / "index.md").read_text(encoding="utf-8")
    assert "DE-E" in oci_claude and "DE-E" in azure_claude
    assert "facade" in oci_claude.lower() and "facade" in azure_claude.lower()
    # espelho
    for claude_root, cursor_root in ((OCI_KB[0], OCI_KB[1]), (AZURE_KB[0], AZURE_KB[1])):
        for path in claude_root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(claude_root)
            other = cursor_root / rel
            assert other.is_file(), other
            assert path.read_text(encoding="utf-8") == other.read_text(encoding="utf-8")


def test_kb_and_skill_no_real_secrets() -> None:
    roots = [
        REPO_ROOT / ".claude" / "skills" / "cloud-secrets",
        REPO_ROOT / ".claude" / "kb" / "oci-vault",
        REPO_ROOT / ".claude" / "kb" / "azure-keyvault",
    ]
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            assert _REAL_SECRET_HEURISTIC.search(text) is None, path


def test_grill_define_vault_question_defaults_and_confirm() -> None:
    for path in DEFINE_PATHS + GRILL_PATHS:
        text = path.read_text(encoding="utf-8").lower()
        assert "vault" in text or "key vault" in text or "secret" in text
        assert "oci" in text and "azure" in text
        assert "confirma" in text or "confirmação" in text
    define = DEFINE_PATHS[0].read_text(encoding="utf-8").lower()
    assert "databricks" in define or "azure" in define
    assert "sem default" in define or "forçar" in define
    assert DEFINE_PATHS[0].read_text(encoding="utf-8") == DEFINE_PATHS[1].read_text(
        encoding="utf-8"
    )
    assert GRILL_PATHS[0].read_text(encoding="utf-8") == GRILL_PATHS[1].read_text(
        encoding="utf-8"
    )
