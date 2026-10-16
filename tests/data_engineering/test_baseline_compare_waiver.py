"""Testes baseline/compare/waiver — ratchet e schema de waiver (Task 12)."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from config.canonical_data_check import EXIT_BLOCKERS, EXIT_OK
from config.canonical_data_check.cli import main as cli_main
from config.canonical_data_check.de_marker import (
    DATABRICKS_DLT_PROFILE,
    DATABRICKS_MULTI_PROFILE,
    DATABRICKS_SDP_PROFILE,
)
from config.canonical_data_check.waivers_yaml import parse_waivers_document
from config.data_engineering.yaml_loader import load_mapping
from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
DATA_CHECK_DIR = ".harness/data-check"
TEMPLATES_DIR = (
    REPO_ROOT / "config" / "canonical_data_check" / "templates" / "data-check"
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _minimal_good_project(root: Path) -> Path:
    """Projeto mínimo que passa A+B (C=SKIP)."""
    _write(
        root / "config" / "pipeline.yaml",
        "owner: data-platform\nrun_id_field: run_id\nlogging: structured\n",
    )
    _write(
        root / "config" / "layers.yaml",
        "layers:\n  - landing\n  - bronze\n  - silver\n  - gold\n",
    )
    _write(root / "config" / "spark.conf", "spark.executor.memory=2g\n")
    _write(
        root / "pipelines" / "transform.py",
        (
            "import logging\n"
            "run_id = context['run_id']\n"
            "logging.getLogger(__name__).info('start', extra={'run_id': run_id})\n"
            "df = spark.sql('SELECT id, amount FROM bronze.orders')\n"
        ),
    )
    _write(
        root / "contracts" / "orders.v1.yaml",
        "version: 1\nfields:\n  - name: id\n    type: string\n",
    )
    _write(root / "tests" / "test_smoke.py", "def test_ok() -> None:\n    assert True\n")
    _write(root / "OWNER", "data-platform\n")
    return root


def _brownfield_with_known_debt(root: Path) -> Path:
    """Projeto com dívida conhecida (select *) e layout mínimo A."""
    project = _minimal_good_project(root)
    _write(
        project / "pipelines" / "legacy.sql",
        "SELECT * FROM bronze.orders;\n",
    )
    return project


def _cloud_project(root: Path, *, include_dlt: bool = False) -> Path:
    """Projeto cloud mínimo com blockers D determinísticos para baseline."""
    project = _minimal_good_project(root)
    _write(
        project / "pipelines" / "orders_sdp.py",
        (
            "from pyspark import pipelines as dp\n\n"
            "@dp.materialized_view()\n"
            "def orders():\n"
            "    return None\n"
        ),
    )
    if include_dlt:
        _write(
            project / "pipelines" / "orders_dlt.py",
            (
                "import dlt\n\n"
                "@dlt.table\n"
                "def legacy_orders():\n"
                "    return None\n"
            ),
        )
    return project


def _future_expiry() -> str:
    return (date.today() + timedelta(days=30)).isoformat()


def _past_expiry() -> str:
    return (date.today() - timedelta(days=1)).isoformat()


def test_baseline_writes_snapshot_under_harness_data_check(tmp_path: Path) -> None:
    """AC: baseline grava snapshot em `.harness/data-check/` do alvo."""
    from config.canonical_data_check.baseline import write_baseline

    project = _brownfield_with_known_debt(tmp_path / "target")
    result = write_baseline(project, contract_path=CONTRACT_PATH)

    data_check = project / DATA_CHECK_DIR
    baseline_path = data_check / "baseline.json"
    profile_path = data_check / "project_profile.yaml"

    assert result.exit_code == EXIT_OK
    assert baseline_path.is_file()
    assert profile_path.is_file()

    payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert payload["version"] == 1
    assert "profiles" not in payload
    assert "findings" in payload
    rule_ids = {item["rule_id"] for item in payload["findings"]}
    assert "DE-B002" in rule_ids

    profile = load_mapping(profile_path)
    assert profile["profile"] == "spark-yarn-airflow"


@pytest.mark.parametrize(
    ("include_dlt", "expected_profile", "expected_profiles"),
    [
        (False, DATABRICKS_SDP_PROFILE, [DATABRICKS_SDP_PROFILE]),
        (
            True,
            DATABRICKS_MULTI_PROFILE,
            sorted([DATABRICKS_DLT_PROFILE, DATABRICKS_SDP_PROFILE]),
        ),
    ],
)
def test_baseline_writes_deterministic_profiles_for_cloud_and_multi(
    tmp_path: Path,
    *,
    include_dlt: bool,
    expected_profile: str,
    expected_profiles: list[str],
) -> None:
    """AC6: cloud/multi persiste perfil efetivo e componentes determinísticos."""
    from config.canonical_data_check.baseline import write_baseline

    project = _cloud_project(tmp_path / "cloud", include_dlt=include_dlt)

    result = write_baseline(project, contract_path=CONTRACT_PATH)
    baseline_path = project / DATA_CHECK_DIR / "baseline.json"
    first = json.loads(baseline_path.read_text(encoding="utf-8"))
    write_baseline(project, contract_path=CONTRACT_PATH)
    second = json.loads(baseline_path.read_text(encoding="utf-8"))

    assert result.profile == expected_profile
    assert first["profile"] == expected_profile
    assert first["profiles"] == expected_profiles
    assert second["profiles"] == expected_profiles


def test_compare_accepts_legacy_baseline_with_singular_profile(tmp_path: Path) -> None:
    """AC6 compat: baseline Loop 1 sem profiles[] continua válido."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _brownfield_with_known_debt(tmp_path / "legacy")
    write_baseline(project, contract_path=CONTRACT_PATH)
    baseline_path = project / DATA_CHECK_DIR / "baseline.json"
    payload = json.loads(baseline_path.read_text(encoding="utf-8"))
    payload.pop("profiles", None)
    payload["profile"] = "spark-yarn-airflow"
    baseline_path.write_text(json.dumps(payload), encoding="utf-8")

    result = compare_project(project, contract_path=CONTRACT_PATH)

    assert result.exit_code == EXIT_OK
    assert any(
        finding.rule_id == "DE-B002" and finding.status == "baseline"
        for finding in result.findings
    )


def test_baseline_writes_dlt_cloud_profile_array(tmp_path: Path) -> None:
    """Ressalva revisão: cobre explicitamente o ramo cloud DLT-only."""
    from config.canonical_data_check.baseline import write_baseline

    project = _minimal_good_project(tmp_path / "dlt-cloud")
    _write(
        project / "pipelines" / "orders_dlt.py",
        (
            "import dlt\n\n"
            "@dlt.table\n"
            "def orders():\n"
            "    return None\n"
        ),
    )

    result = write_baseline(project, contract_path=CONTRACT_PATH)
    payload = json.loads(
        (project / DATA_CHECK_DIR / "baseline.json").read_text(encoding="utf-8")
    )

    assert result.profile == DATABRICKS_DLT_PROFILE
    assert payload["profiles"] == [DATABRICKS_DLT_PROFILE]


def test_cloud_compare_ratchet_new_finding_fails_baselined_does_not(
    tmp_path: Path,
) -> None:
    """AC6: ratchet cloud mantém dívida conhecida e bloqueia finding novo."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _cloud_project(tmp_path / "cloud-ratchet")
    write_baseline(project, contract_path=CONTRACT_PATH)

    same = compare_project(project, contract_path=CONTRACT_PATH)
    assert same.exit_code == EXIT_OK
    assert any(
        finding.rule_id == "DE-D004" and finding.status == "baseline"
        for finding in same.findings
    )

    _write(
        project / "pipelines" / "new_debt.py",
        credential_assignment("password", "cloud-secret-must-not-leak"),
    )
    regress = compare_project(project, contract_path=CONTRACT_PATH)

    assert regress.exit_code == EXIT_BLOCKERS
    assert any(
        finding.rule_id == "DE-A001" and finding.status == "fail"
        for finding in regress.findings
    )
    assert any(
        finding.rule_id == "DE-D004" and finding.status == "baseline"
        for finding in regress.findings
    )


def test_cli_baseline_entrypoint(tmp_path: Path) -> None:
    project = _brownfield_with_known_debt(tmp_path / "cli-base")
    code = cli_main(
        ["baseline", str(project), "--contract", str(CONTRACT_PATH)]
    )
    assert code == EXIT_OK
    assert (project / DATA_CHECK_DIR / "baseline.json").is_file()


def test_compare_ratchet_new_finding_fails_baselined_does_not(
    tmp_path: Path,
) -> None:
    """AC4: compare falha só em finding novo; baselineado não quebra."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _brownfield_with_known_debt(tmp_path / "ratchet")
    write_baseline(project, contract_path=CONTRACT_PATH)

    # Mesmo estado → ratchet passa (dívida conhecida)
    same = compare_project(project, contract_path=CONTRACT_PATH)
    assert same.exit_code == EXIT_OK
    baselined = {f.rule_id for f in same.findings if f.status == "baseline"}
    assert "DE-B002" in baselined
    assert not any(f.status == "fail" and f.severity == "blocker" for f in same.findings)

    # Nova regressão → falha
    _write(
        project / "pipelines" / "new_debt.py",
        credential_assignment("password", "another-secret-value"),
    )
    regress = compare_project(project, contract_path=CONTRACT_PATH)
    assert regress.exit_code == EXIT_BLOCKERS
    failed = {f.rule_id for f in regress.findings if f.status == "fail"}
    assert "DE-A001" in failed
    # Dívida antiga continua baselineada, não fail
    assert any(
        f.rule_id == "DE-B002" and f.status == "baseline" for f in regress.findings
    )


def test_cli_compare_entrypoint_ratchet(tmp_path: Path) -> None:
    from config.canonical_data_check.baseline import write_baseline

    project = _brownfield_with_known_debt(tmp_path / "cli-cmp")
    write_baseline(project, contract_path=CONTRACT_PATH)
    assert (
        cli_main(["compare", str(project), "--contract", str(CONTRACT_PATH)])
        == EXIT_OK
    )
    _write(project / "pipelines" / "extra.sql", "SELECT * FROM silver.x;\n")
    assert (
        cli_main(["compare", str(project), "--contract", str(CONTRACT_PATH)])
        == EXIT_BLOCKERS
    )


def test_waiver_without_owner_or_expiry_does_not_silence(tmp_path: Path) -> None:
    """AC5: waiver incompleto não silencia blocker."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _brownfield_with_known_debt(tmp_path / "bad-waiver")
    write_baseline(project, contract_path=CONTRACT_PATH)

    # Nova dívida + waiver inválido (sem owner)
    _write(
        project / "pipelines" / "secret.py",
        credential_assignment("api_key", "sk-live-should-not-leak"),
    )
    _write(
        project / DATA_CHECK_DIR / "waivers.yaml",
        (
            "waivers:\n"
            "  - rule_id: DE-A001\n"
            "    expiry: "
            f"{_future_expiry()}\n"
            "    reason: incompleto sem owner\n"
        ),
    )
    result = compare_project(project, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_BLOCKERS
    assert any(f.rule_id == "DE-A001" and f.status == "fail" for f in result.findings)
    assert not any(f.rule_id == "DE-A001" and f.status == "waived" for f in result.findings)

    # Sem expiry
    _write(
        project / DATA_CHECK_DIR / "waivers.yaml",
        (
            "waivers:\n"
            "  - rule_id: DE-A001\n"
            "    owner: data-platform\n"
            "    reason: incompleto sem expiry\n"
        ),
    )
    result2 = compare_project(project, contract_path=CONTRACT_PATH)
    assert result2.exit_code == EXIT_BLOCKERS
    assert any(f.rule_id == "DE-A001" and f.status == "fail" for f in result2.findings)


def test_valid_waiver_silences_until_expiry(tmp_path: Path) -> None:
    """Waiver válido (owner + expiry futuro) silencia rule_id até expiry."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _brownfield_with_known_debt(tmp_path / "good-waiver")
    write_baseline(project, contract_path=CONTRACT_PATH)
    _write(
        project / "pipelines" / "secret.py",
        credential_assignment("password", "temp-exception-value"),
    )
    _write(
        project / DATA_CHECK_DIR / "waivers.yaml",
        (
            "waivers:\n"
            "  - rule_id: DE-A001\n"
            "    owner: data-platform\n"
            f"    expiry: {_future_expiry()}\n"
            "    reason: exceção temporária documentada\n"
        ),
    )
    result = compare_project(project, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_OK
    assert any(f.rule_id == "DE-A001" and f.status == "waived" for f in result.findings)

    # Expirado → volta a falhar
    _write(
        project / DATA_CHECK_DIR / "waivers.yaml",
        (
            "waivers:\n"
            "  - rule_id: DE-A001\n"
            "    owner: data-platform\n"
            f"    expiry: {_past_expiry()}\n"
            "    reason: já venceu\n"
        ),
    )
    expired = compare_project(project, contract_path=CONTRACT_PATH)
    assert expired.exit_code == EXIT_BLOCKERS
    assert any(f.rule_id == "DE-A001" and f.status == "fail" for f in expired.findings)


def test_baseline_idempotent_and_no_raw_secrets(tmp_path: Path) -> None:
    from config.canonical_data_check.baseline import write_baseline

    project = _minimal_good_project(tmp_path / "idem")
    _write(
        project / "pipelines" / "leak.py",
        credential_assignment("password", "super-secret-never-baseline"),
    )
    first = write_baseline(project, contract_path=CONTRACT_PATH)
    payload1 = (project / DATA_CHECK_DIR / "baseline.json").read_text(encoding="utf-8")
    second = write_baseline(project, contract_path=CONTRACT_PATH)
    payload2 = (project / DATA_CHECK_DIR / "baseline.json").read_text(encoding="utf-8")

    assert first.exit_code == EXIT_OK
    assert second.exit_code == EXIT_OK
    # Determinístico: mesmo conteúdo sem timestamp volátil no body de findings
    body1 = json.loads(payload1)
    body2 = json.loads(payload2)
    assert body1["findings"] == body2["findings"]
    assert "super-secret-never-baseline" not in payload1
    assert "super-secret-never-baseline" not in payload2
    for item in body1["findings"]:
        assert "message" not in item or "super-secret" not in str(item.get("message", ""))


def test_compare_without_baseline_fails_new_blockers(tmp_path: Path) -> None:
    from config.canonical_data_check.baseline import compare_project

    project = _brownfield_with_known_debt(tmp_path / "no-base")
    # Sem baseline: blockers atuais devem falhar (não há dívida conhecida)
    result = compare_project(project, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_BLOCKERS
    assert any(f.rule_id == "DE-B002" and f.status == "fail" for f in result.findings)


def test_canonical_templates_document_schema() -> None:
    """AC: schema/template do baseline documentado no canônico (seed install)."""
    assert TEMPLATES_DIR.is_dir()
    assert (TEMPLATES_DIR / "project_profile.yaml").is_file()
    assert (TEMPLATES_DIR / "baseline.json").is_file()
    assert (TEMPLATES_DIR / "waivers.yaml").is_file()
    assert (TEMPLATES_DIR / "SCHEMA.md").is_file()

    schema_doc = (TEMPLATES_DIR / "SCHEMA.md").read_text(encoding="utf-8")
    assert "baseline.json" in schema_doc
    assert "`profiles`" in schema_doc
    assert "databricks-multi" in schema_doc
    assert "owner" in schema_doc
    assert "expiry" in schema_doc
    assert ".harness/data-check" in schema_doc

    seed_baseline = json.loads(
        (TEMPLATES_DIR / "baseline.json").read_text(encoding="utf-8")
    )
    assert seed_baseline["version"] == 1
    assert seed_baseline["findings"] == []

    seed_waivers = parse_waivers_document(
        (TEMPLATES_DIR / "waivers.yaml").read_text(encoding="utf-8")
    )
    assert seed_waivers == []


def test_cli_subprocess_baseline_compare(tmp_path: Path) -> None:
    project = _brownfield_with_known_debt(tmp_path / "subproc")
    base = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "baseline",
            str(project),
            "--contract",
            str(CONTRACT_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert base.returncode == EXIT_OK

    cmp_ok = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "compare",
            str(project),
            "--contract",
            str(CONTRACT_PATH),
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert cmp_ok.returncode == EXIT_OK
    payload = json.loads(cmp_ok.stdout)
    assert payload["exit_code"] == EXIT_OK


@pytest.mark.parametrize("cmd", ["baseline", "compare"])
def test_cli_help_baseline_compare(cmd: str) -> None:
    assert cli_main([cmd, "--help"]) == 0


def test_fingerprint_ignores_line_shift(tmp_path: Path) -> None:
    """Ressalva revisor: shift de linha não cria finding 'novo'."""
    from config.canonical_data_check.baseline import compare_project, write_baseline

    project = _brownfield_with_known_debt(tmp_path / "lineno")
    write_baseline(project, contract_path=CONTRACT_PATH)
    # Insere linha em branco antes do SELECT * → muda :lineno, mesma dívida
    legacy = project / "pipelines" / "legacy.sql"
    legacy.write_text("\nSELECT * FROM bronze.orders;\n", encoding="utf-8")
    result = compare_project(project, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_OK
    assert any(f.rule_id == "DE-B002" and f.status == "baseline" for f in result.findings)


def test_corrupt_baseline_returns_usage(tmp_path: Path) -> None:
    from config.canonical_data_check import EXIT_USAGE
    from config.canonical_data_check.baseline import compare_project

    project = _brownfield_with_known_debt(tmp_path / "corrupt")
    data_check = project / DATA_CHECK_DIR
    data_check.mkdir(parents=True, exist_ok=True)
    (data_check / "baseline.json").write_text("{not-json", encoding="utf-8")
    result = compare_project(project, contract_path=CONTRACT_PATH)
    assert result.exit_code == EXIT_USAGE
    assert any(f.rule_id == "DE-USAGE" for f in result.findings)
