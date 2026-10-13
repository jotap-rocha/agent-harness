"""Testes do contrato git-hygiene — carregam regex apenas do YAML (fonte única)."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.git_hygiene.contract import GitHygieneContract


def test_contract_yaml_exists(contract_yaml_path: Path) -> None:
    assert contract_yaml_path.is_file(), (
        f"Fonte única ausente: {contract_yaml_path}. "
        "Crie git-hygiene.yaml na raiz do canônico."
    )


def test_contract_yaml_documents_schema(contract_yaml_path: Path) -> None:
    text = contract_yaml_path.read_text(encoding="utf-8")
    for marker in (
        "Schema mínimo",
        "branch.pattern",
        "pr_title.pattern",
        "person_name",
    ):
        assert marker in text, f"YAML deve documentar schema mínimo (faltou: {marker})"


def test_contract_documents_person_name_limit(contract_yaml_path: Path) -> None:
    """Nome de pessoa não deve ser fingido com regex impossível — limite documentado."""
    contract = GitHygieneContract.load(contract_yaml_path)
    note = contract.person_name_limit_note
    assert note, "limits.person_name deve existir no YAML"
    assert "regex" in note.lower()
    assert "confiáv" in note.lower() or "imposs" in note.lower() or "não" in note.lower()


@pytest.mark.parametrize(
    "branch",
    [
        "feat/gate-branch-isolada",
        "fix/parser-data-nula",
        "chore/atualiza-dependencias",
    ],
)
def test_acceptance_valid_branches(
    contract_yaml_path: Path,
    branch: str,
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert contract.is_valid_branch(branch), f"esperado válido: {branch!r}"


def test_fixture_valid_branches(
    contract_yaml_path: Path,
    valid_branches: list[str],
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert valid_branches, "fixture branches_valid.txt vazia"
    for branch in valid_branches:
        assert contract.is_valid_branch(branch), f"esperado válido: {branch!r}"


def test_fixture_invalid_branches(
    contract_yaml_path: Path,
    invalid_branches: list[str],
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert invalid_branches, "fixture branches_invalid.txt vazia"
    for branch in invalid_branches:
        assert not contract.is_valid_branch(branch), f"esperado inválido: {branch!r}"


@pytest.mark.parametrize(
    "branch,reason",
    [
        ("tmp", "sem tipo/escopo"),
        ("feat/tmp", "termo proibido"),
        ("feat/teste", "termo proibido"),
        ("feat/nova-branch", "termo proibido"),
        ("feat/configuração", "acento"),
        ("feat/escopo-com-mais-de-quarenta-caracteres-excedentes", ">40 chars"),
        ("docs/foo", "tipo fora da lista"),
        ("feat/2026-08-06", "data solta"),
    ],
)
def test_acceptance_invalid_branches(
    contract_yaml_path: Path,
    branch: str,
    reason: str,
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert not contract.is_valid_branch(branch), (
        f"esperado inválido ({reason}): {branch!r}"
    )


def test_fixture_valid_pr_titles(
    contract_yaml_path: Path,
    valid_pr_titles: list[str],
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert valid_pr_titles, "fixture pr_titles_valid.txt vazia"
    for title in valid_pr_titles:
        assert contract.is_valid_pr_title(title), f"esperado válido: {title!r}"


def test_fixture_invalid_pr_titles(
    contract_yaml_path: Path,
    invalid_pr_titles: list[str],
) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert invalid_pr_titles, "fixture pr_titles_invalid.txt vazia"
    for title in invalid_pr_titles:
        assert not contract.is_valid_pr_title(title), f"esperado inválido: {title!r}"


def test_pr_title_summary_max_72(contract_yaml_path: Path) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    ok = "feat(gate): " + ("x" * 72)
    bad = "feat(gate): " + ("x" * 73)
    assert contract.is_valid_pr_title(ok)
    assert not contract.is_valid_pr_title(bad)


def test_pr_title_rejects_blank_summary(contract_yaml_path: Path) -> None:
    """Resumo vazio/whitespace — fixture txt não preserva trailing space após strip."""
    contract = GitHygieneContract.load(contract_yaml_path)
    assert not contract.is_valid_pr_title("feat(gate): ")
    assert not contract.is_valid_pr_title("feat(gate):    ")


def test_validator_does_not_hardcode_branch_regex(
    contract_yaml_path: Path,
) -> None:
    """Garante que o módulo de validação não embute a regex — só o YAML."""
    source = (
        Path(__file__).resolve().parents[2]
        / "config"
        / "git_hygiene"
        / "contract.py"
    ).read_text(encoding="utf-8")
    forbidden_literals = (
        "^(feat|fix|chore)/",
        "^(feat|fix|chore)\\(",
    )
    for literal in forbidden_literals:
        assert literal not in source, (
            "Regex de contrato não deve estar hardcoded em contract.py; "
            f"encontrou {literal!r}. Carregue de git-hygiene.yaml."
        )


def test_types_feat_fix_chore_only(contract_yaml_path: Path) -> None:
    contract = GitHygieneContract.load(contract_yaml_path)
    assert set(contract.branch_types) == {"feat", "fix", "chore"}
    assert contract.is_valid_branch("feat/ok-scope")
    assert contract.is_valid_branch("fix/ok-scope")
    assert contract.is_valid_branch("chore/ok-scope")
    assert not contract.is_valid_branch("refactor/ok-scope")
