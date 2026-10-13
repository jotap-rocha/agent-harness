"""Loop 3 Tasks 25–27: amarras agents/commands DE + pontes KB + espelho."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DE_AGENTS = {
    "spark-engineer.md": ("DE-B", "pacote **B**", "DE-B*"),
    "pipeline-architect.md": ("DE-C", "pacote **C**", "DE-C*"),
    "data-quality-analyst.md": ("DE-D003", "DE-D004"),
    "lakehouse-architect.md": ("pacote **D**", "DE-D*"),
    "data-platform-engineer.md": ("pacote **D**", "DE-D*"),
    "schema-designer.md": ("DE-D004",),
    "dbt-specialist.md": ("DE-A*",),
    "sql-optimizer.md": ("DE-A*",),
    "streaming-engineer.md": ("DE-A*",),
    "data-contracts-engineer.md": ("DE-A*",),
}

DE_COMMANDS: dict[str, str] = {
    "data-contract.md": "data-contracts-engineer",
    "data-quality.md": "data-quality-analyst",
    "lakehouse.md": "lakehouse-architect",
    "migrate.md": "spark-engineer",  # also dbt/pipeline; any DE agent named is enough for AC
    "pipeline.md": "pipeline-architect",
    "schema.md": "schema-designer",
    "sql-review.md": "sql-optimizer",
}

DE_KB_DOMAINS: dict[str, tuple[str, ...]] = {
    "airflow": ("DE-A*", "DE-C*", "data-engineering.yaml"),
    "spark": ("DE-A*", "DE-B*", "data-engineering.yaml"),
    "lakehouse": ("DE-A*", "DE-D*", "data-engineering.yaml"),
    "pipeline": ("DE-A*", "data-engineering.yaml"),
    "data-quality": ("DE-A*", "DE-D003", "DE-D004", "data-engineering.yaml"),
    "dbt": ("DE-A*", "data-engineering.yaml"),
    "data-modeling": ("DE-A*", "DE-D004", "data-engineering.yaml"),
    "sql-patterns": ("DE-A*", "data-engineering.yaml"),
    "streaming": ("DE-A*", "data-engineering.yaml"),
    "cloud-platforms": ("DE-A*", "DE-D*", "data-engineering.yaml"),
}

GATE_MARKERS = ("/validar", "canonical_data_check")
WAIVER_MARKERS = ("baseline", "waiver", "corrigir", "owner")
ANTI_DUP_MARKERS = (
    "não duplica severidade",
    "nao duplica severidade",
    "fonte: `data-engineering.yaml`",
    "Fonte: `data-engineering.yaml`",
    "Fonte normativa: `data-engineering.yaml`",
)


def _agent_paths(name: str) -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "agents" / "data-engineering" / name,
        REPO_ROOT / ".cursor" / "agents" / "data-engineering" / name,
    )


def _command_paths(name: str) -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "commands" / "data-engineering" / name,
        REPO_ROOT / ".cursor" / "commands" / "data-engineering" / name,
    )


def _kb_index_paths(domain: str) -> tuple[Path, Path]:
    return (
        REPO_ROOT / ".claude" / "kb" / domain / "index.md",
        REPO_ROOT / ".cursor" / "kb" / domain / "index.md",
    )


def test_ac1_dez_agents_declaram_kernel_de_a_e_yaml() -> None:
    """AC1: cada agent cita DE-A*, data-engineering.yaml e amarra de domínio."""
    assert len(DE_AGENTS) == 10
    for name, domain_tokens in DE_AGENTS.items():
        claude, _ = _agent_paths(name)
        text = claude.read_text(encoding="utf-8")
        assert "Conformidade DE (kernel)" in text, name
        assert "data-engineering.yaml" in text, name
        assert "DE-A" in text, name
        assert any(token in text for token in GATE_MARKERS), name
        assert all(m in text.lower() for m in ("baseline", "waiver", "corrigir")), name
        assert "owner" in text.lower(), name
        for token in domain_tokens:
            assert token in text, f"{name} missing domain token {token!r}"


def test_ac1_agents_espelho_identico() -> None:
    """AC10: espelho .claude ↔ .cursor dos 10 agents DE."""
    for name in DE_AGENTS:
        claude, cursor = _agent_paths(name)
        assert claude.read_text(encoding="utf-8") == cursor.read_text(encoding="utf-8"), name


def test_ac2_sete_commands_apontam_gate_e_agent() -> None:
    """AC2: cada command nomeia agent DE + gate validate."""
    assert len(DE_COMMANDS) == 7
    for name, agent in DE_COMMANDS.items():
        claude, _ = _command_paths(name)
        text = claude.read_text(encoding="utf-8")
        assert agent in text, f"{name} must name {agent}"
        assert "Gate DE (kernel)" in text or "/validar" in text, name
        assert any(m in text for m in GATE_MARKERS), name
        assert "DE-" in text or "data-engineering.yaml" in text, name


def test_ac2_commands_espelho_identico() -> None:
    """AC10: espelho dos 7 commands DE tocados."""
    for name in DE_COMMANDS:
        claude, cursor = _command_paths(name)
        assert claude.read_text(encoding="utf-8") == cursor.read_text(encoding="utf-8"), name


def test_ac3_dez_kbs_tem_ponte_curta() -> None:
    """AC3: 10 KBs DE-adjacentes com âncora a IDs/pacotes sem colar norma."""
    assert len(DE_KB_DOMAINS) == 10
    for domain, tokens in DE_KB_DOMAINS.items():
        claude, _ = _kb_index_paths(domain)
        text = claude.read_text(encoding="utf-8")
        assert "Conformidade DE (ponte)" in text, domain
        for token in tokens:
            assert token in text, f"{domain} missing {token!r}"
        assert any(m.lower() in text.lower() for m in ANTI_DUP_MARKERS), domain
        # anti-duplicação leve: ponte curta (não cola YAML inteiro)
        ponte_start = text.index("## Conformidade DE (ponte)")
        rest = text[ponte_start:]
        next_h2 = rest.find("\n## ", 1)
        ponte = rest if next_h2 < 0 else rest[:next_h2]
        assert len(ponte) < 900, f"{domain} ponte demasiado longa ({len(ponte)} chars)"
        assert "severity:" not in ponte.lower()


def test_ac3_kb_espelho_identico() -> None:
    """AC10: espelho index.md dos 10 KBs tocados."""
    for domain in DE_KB_DOMAINS:
        claude, cursor = _kb_index_paths(domain)
        assert claude.read_text(encoding="utf-8") == cursor.read_text(encoding="utf-8"), domain


def test_migrate_command_cita_agents_amarrados() -> None:
    """migrate deve citar dbt-specialist e/ou spark-engineer + pipeline-architect."""
    text = (REPO_ROOT / ".claude/commands/data-engineering/migrate.md").read_text(
        encoding="utf-8"
    )
    assert "dbt-specialist" in text
    assert "spark-engineer" in text
    assert "pipeline-architect" in text