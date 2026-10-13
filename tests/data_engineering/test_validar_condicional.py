"""Testes do gate /validar condicional (Task 16 / AC9–AC10 + Task 23 / AC7, AC9)."""

from __future__ import annotations

from pathlib import Path

from config.canonical_data_check.de_marker import (
    DE_PROFILE_MARKER,
    data_check_validate_argv,
    has_de_marker,
    is_canonical_harness_root,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDAR_PATHS = (
    REPO_ROOT / ".claude" / "commands" / "validar.md",
    REPO_ROOT / ".cursor" / "commands" / "validar.md",
)
COMMANDS_README_PATHS = (
    REPO_ROOT / ".claude" / "commands" / "README.md",
    REPO_ROOT / ".cursor" / "commands" / "README.md",
)
PIPELINE_RULE_PATHS = (
    REPO_ROOT / ".claude" / "rules" / "pipeline.md",
    REPO_ROOT / ".cursor" / "rules" / "pipeline.mdc",
)

_VALIDATE_TAIL = ("config.canonical_data_check", "validate")


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _assert_validate_argv(project: Path) -> list[str]:
    argv = data_check_validate_argv(project)
    assert argv is not None
    assert argv[-3:-1] == list(_VALIDATE_TAIL)
    assert argv[-1] == str(project.resolve())
    return argv


def test_sem_marker_nem_sinal_nao_invoca_data_check(tmp_path: Path) -> None:
    """AC7: projeto comum (não-DE) → data_check_validate_argv é None."""
    _write(tmp_path / "README.md", "# app\n")
    assert has_de_marker(tmp_path) is False
    assert data_check_validate_argv(tmp_path) is None


def test_com_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC7 / Loop 1: com project_profile → argv aponta para validate no root."""
    marker = tmp_path / DE_PROFILE_MARKER
    marker.parent.mkdir(parents=True)
    marker.write_text("profile: spark-yarn-airflow\n", encoding="utf-8")

    assert has_de_marker(tmp_path) is True
    _assert_validate_argv(tmp_path)


def test_example_greenfield_tem_marker() -> None:
    """Example do Ship 1 carrega o marker (validate no /validar faz sentido)."""
    example = REPO_ROOT / "examples" / "spark-yarn-airflow-min"
    assert has_de_marker(example) is True
    assert data_check_validate_argv(example) is not None


def test_sdp_sem_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC7: auto-detect SDP (sem marker) → invoca data-check."""
    project = tmp_path / "sdp-only"
    _write(
        project / "pipelines" / "orders_sdp.py",
        (
            "from pyspark import pipelines as dp\n\n"
            "@dp.materialized_view()\n"
            "def orders():\n"
            "    return None\n"
        ),
    )
    assert has_de_marker(project) is False
    _assert_validate_argv(project)


def test_dlt_sem_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC7: auto-detect DLT (sem marker) → invoca data-check."""
    project = tmp_path / "dlt-only"
    _write(
        project / "pipelines" / "orders_dlt.py",
        "import dlt\n\n@dlt.table\ndef orders():\n    return None\n",
    )
    assert has_de_marker(project) is False
    _assert_validate_argv(project)


def test_multi_sdp_dlt_sem_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC7: SDP+DLT sem marker → invoca (perfil efetivo multi via engine)."""
    project = tmp_path / "multi"
    _write(
        project / "pipelines" / "orders_sdp.py",
        "from pyspark import pipelines as dp\n@dp.table\ndef orders(): pass\n",
    )
    _write(
        project / "pipelines" / "orders_dlt.py",
        "import dlt\n@dlt.table\ndef legacy(): pass\n",
    )
    assert has_de_marker(project) is False
    _assert_validate_argv(project)


def test_dab_isolado_sem_marker_nao_invoca_data_check(tmp_path: Path) -> None:
    """AC7: DAB isolado não escolhe perfil cloud e não ativa /validar."""
    project = tmp_path / "dab-only"
    _write(project / "databricks.yml", "bundle:\n  name: alone\n")
    assert has_de_marker(project) is False
    assert data_check_validate_argv(project) is None


def test_filho_pipeline_normal_invoca_data_check(tmp_path: Path) -> None:
    """Review Task 24: pipeline filho normal mantém auto-detect SDP."""
    project = tmp_path / "filho-pipeline"
    _write(
        project / "pipelines" / "orders_sdp.py",
        "from pyspark import pipelines as dp\n@dp.table\ndef orders(): pass\n",
    )

    assert is_canonical_harness_root(project) is False
    _assert_validate_argv(project)


def test_filho_monorepo_sob_examples_invoca_data_check(tmp_path: Path) -> None:
    """Review Task 24: paths examples/tests não são ignorados em filhos."""
    project = tmp_path / "filho-monorepo"
    _write(
        project / "examples" / "cloud-pipeline" / "orders_dlt.py",
        "import dlt\n@dlt.table\ndef orders(): pass\n",
    )

    assert is_canonical_harness_root(project) is False
    _assert_validate_argv(project)


def test_root_canonico_nao_invoca_por_sinais_internos() -> None:
    """Review Task 24: somente o sentinel completo desativa o root canônico."""
    assert is_canonical_harness_root(REPO_ROOT) is True
    assert has_de_marker(REPO_ROOT) is False
    assert data_check_validate_argv(REPO_ROOT) is None


def test_example_databricks_sdp_min_invoca_sem_marker() -> None:
    """Example SDP real: sem marker, com sinal SDP útil → invoca."""
    example = REPO_ROOT / "examples" / "databricks-sdp-min"
    assert example.is_dir()
    assert has_de_marker(example) is False
    assert data_check_validate_argv(example) is not None


def test_example_databricks_dlt_min_invoca_sem_marker() -> None:
    """Example DLT real: sem marker, com sinal DLT útil → invoca."""
    example = REPO_ROOT / "examples" / "databricks-dlt-min"
    assert example.is_dir()
    assert has_de_marker(example) is False
    assert data_check_validate_argv(example) is not None


def test_validar_command_documenta_marker_ou_autodetect() -> None:
    """Command /validar (espelho) declara marker OR auto-detect + helper."""
    for path in VALIDAR_PATHS:
        text = path.read_text(encoding="utf-8")
        assert ".harness/data-check/project_profile.yaml" in text
        assert "config.canonical_data_check validate" in text
        assert "data_check_validate_argv" in text
        assert "auto-detect" in text.lower() or "auto detect" in text.lower()
        assert "SDP" in text or "sdp" in text
        assert "DLT" in text or "dlt" in text
        assert "DAB" in text or "dab" in text
        assert "não" in text.lower() and "data-check" in text


def test_validar_commands_espelho_identico() -> None:
    """AC9: .claude e .cursor commands/validar.md simétricos."""
    a = VALIDAR_PATHS[0].read_text(encoding="utf-8")
    b = VALIDAR_PATHS[1].read_text(encoding="utf-8")
    assert a == b


def test_commands_readme_espelho_documenta_trigger() -> None:
    """README de commands (espelho) cita trigger marker ou auto-detect."""
    a = COMMANDS_README_PATHS[0].read_text(encoding="utf-8")
    b = COMMANDS_README_PATHS[1].read_text(encoding="utf-8")
    assert a == b
    assert "/validar" in a
    assert "auto-detect" in a.lower() or "SDP" in a or "sdp" in a


def test_pipeline_rule_referencia_norma_yaml() -> None:
    """AC9 parcial: rules/pipeline aponta data-engineering.yaml como fonte de IDs."""
    for path in PIPELINE_RULE_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "data-engineering.yaml" in text
        assert "IDs" in text or "ids" in text.lower()
        assert "canonical_data_check" in text
        assert "databricks" in text.lower()
        assert "auto-detect" in text.lower() or "SDP" in text or "sdp" in text


def test_pipeline_rule_corpo_espelhado() -> None:
    """Corpo da rule (após frontmatter) permanece alinhado entre .md e .mdc."""
    md = (REPO_ROOT / ".claude" / "rules" / "pipeline.md").read_text(encoding="utf-8")
    mdc = (REPO_ROOT / ".cursor" / "rules" / "pipeline.mdc").read_text(encoding="utf-8")

    def body_after_frontmatter(text: str) -> str:
        if text.startswith("---"):
            end = text.find("---", 3)
            assert end != -1
            return text[end + 3 :].lstrip("\n")
        return text

    assert body_after_frontmatter(md) == body_after_frontmatter(mdc)


# --- Task 34: /validar dispara pacote E -------------------------------------------------


def test_secret_store_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC8: marker com secret_store → argv validate (helper)."""
    project = tmp_path / "vault-marker"
    _write(
        project / DE_PROFILE_MARKER,
        "profile: spark-yarn-airflow\nsecret_store: oci\n",
    )
    assert has_de_marker(project) is True
    _assert_validate_argv(project)


def test_vault_autodetect_sem_marker_invoca_data_check(tmp_path: Path) -> None:
    """AC8: auto-detect vault (sem marker DE) → dispara data-check."""
    project = tmp_path / "vault-only"
    _write(
        project / "src" / "key_oci.py",
        "from oci.secrets import SecretsClient\n\ndef get_secret(sid: str) -> str:\n    return ''\n",
    )
    assert has_de_marker(project) is False
    _assert_validate_argv(project)


def test_sem_marker_sem_sdp_dlt_sem_vault_nao_invoca(tmp_path: Path) -> None:
    """AC8 negativo: sem DE, sem SDP/DLT, sem vault → argv None."""
    project = tmp_path / "plain-app"
    _write(project / "app.py", "print('hello')\n")
    assert data_check_validate_argv(project) is None


def test_dab_isolado_sem_vault_ainda_nao_invoca(tmp_path: Path) -> None:
    """DAB isolado sem vault continua sem ativar E/data-check."""
    project = tmp_path / "dab-no-vault"
    _write(project / "databricks.yml", "bundle:\n  name: alone\n")
    assert data_check_validate_argv(project) is None


def test_validar_command_documenta_aplicabilidade_e() -> None:
    """Docs /validar mencionam secret_store / pacote E (espelho)."""
    for path in VALIDAR_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "secret_store" in text
        assert "vault" in text.lower() or "keyvault" in text.lower() or "pacote E" in text
        assert "E" in text or "keyvault-cloud" in text
