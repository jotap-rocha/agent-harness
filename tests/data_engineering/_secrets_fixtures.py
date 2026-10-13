"""Fixtures de atribuição de credencial sem falso positivo no pre-commit.

O hook `.githooks/pre-commit` bloqueia literais de assignment de credencial no
diff. Os testes precisam gerar esses literais nos arquivos-alvo para a CLI DE
detectar — montamos a string em runtime a partir do nome do campo.
"""

from __future__ import annotations


def credential_assignment(name: str, value: str) -> str:
    """Retorna linha ``<name> = \"<value>\"`` (conteúdo do arquivo sob teste)."""
    return f'{name} = "{value}"\n'


def assignment_needle(name: str) -> str:
    """Retorna ``<name>=`` sem literal estático que o pre-commit bloqueia."""
    return f"{name}="


def forbidden_credential_needles() -> tuple[str, ...]:
    """Needles de scan PII/secrets para testes de example (montados em runtime)."""
    return (
        assignment_needle("password"),
        assignment_needle("api_key"),
        assignment_needle("secret_key"),
        "BEGIN PRIVATE KEY",
        "aws_secret_access_key",
    )