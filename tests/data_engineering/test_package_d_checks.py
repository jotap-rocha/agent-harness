"""Testes da Task 19 — checks executáveis do pacote D (Databricks cloud)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from config.canonical_data_check import EXIT_BLOCKERS, EXIT_OK, validate_project
from config.canonical_data_check.checks.package_d import check_package_d
from config.canonical_data_check.cli import main as cli_main
from config.canonical_data_check.de_marker import (
    DATABRICKS_MULTI_PROFILE,
    DATABRICKS_SDP_PROFILE,
    is_dab_manifest,
)
from config.canonical_data_check.scanner import iter_text_files

from tests.data_engineering._secret_fixtures import credential_assignment

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"
PSEUDO_SECRET = "sp-cloud-secret-must-not-leak"


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _force_cloud_profile(root: Path, profile: str = DATABRICKS_SDP_PROFILE) -> None:
    _write(
        root / ".harness" / "data-check" / "project_profile.yaml",
        f"profile: {profile}\n",
    )


def _layout_a_minimum(root: Path) -> None:
    """Satisfaz pacote A (Universal) sem depender de B/C."""
    _write(
        root / "config" / "pipeline.yaml",
        "owner: data-platform\nrun_id_field: run_id\nlogging: structured\n",
    )
    _write(
        root / "pipelines" / "transform.py",
        (
            "import logging\n"
            "run_id = context['run_id']\n"
            "logging.getLogger(__name__).info('start', extra={'run_id': run_id})\n"
        ),
    )
    _write(root / "tests" / "test_smoke.py", "def test_ok() -> None:\n    assert True\n")
    _write(root / "OWNER", "data-platform\n")


def _dab_with_identity(root: Path) -> None:
    _write(
        root / "databricks.yml",
        (
            "bundle:\n"
            "  name: orders\n"
            "run_as:\n"
            "  service_principal_name: sp-orders-runner\n"
            "owner: data-platform\n"
        ),
    )


def _sdp_pipeline(root: Path) -> None:
    _write(
        root / "pipelines" / "orders_sdp.py",
        (
            "from pyspark import pipelines as dp\n\n"
            "@dp.materialized_view()\n"
            "def bronze_orders():\n"
            "    return None\n"
        ),
    )


def _sdp_medallion(root: Path) -> None:
    _write(
        root / "config" / "layers.yaml",
        "layers:\n  - bronze\n  - silver\n  - gold\n",
    )


def _dlt_pipeline(root: Path, *, with_quarantine: bool) -> None:
    quarantine = (
        "quarantine_table = 'ops.quarantine_orders'\n"
        if with_quarantine
        else ""
    )
    _write(
        root / "pipelines" / "orders_dlt.py",
        (
            "import dlt\n\n"
            f"{quarantine}"
            "@dlt.expect_or_drop('id_not_null', 'id IS NOT NULL')\n"
            "@dlt.table\n"
            "def orders():\n"
            "    return None\n"
        ),
    )


def _schema_rescue_policy(root: Path) -> None:
    _write(
        root / "config" / "schema-rescue-policy.yaml",
        (
            "schema_rescue:\n"
            "  on_drift: quarantine\n"
            "  alternatives:\n"
            "    - fail\n"
            "    - quarantine\n"
        ),
    )


def _uc_fs_artifacts(root: Path) -> None:
    _write(
        root / "uc" / "grants.yaml",
        "grants:\n  - principal: data-readers\n    privilege: SELECT\n",
    )
    _write(
        root / "uc" / "lineage.md",
        "# Unity Catalog lineage\n\nSource → bronze → silver\n",
    )


def _good_sdp_project(root: Path) -> Path:
    _layout_a_minimum(root)
    _force_cloud_profile(root)
    _dab_with_identity(root)
    _sdp_pipeline(root)
    _sdp_medallion(root)
    _schema_rescue_policy(root)
    _uc_fs_artifacts(root)
    return root


def _failed_ids(result) -> set[str]:
    return {f.rule_id for f in result.findings if f.status == "fail"}


def _skipped_ids(result) -> set[str]:
    return {f.rule_id for f in result.findings if f.status == "skip"}


def test_sdp_fixture_passes_expected_d_rules(tmp_path: Path) -> None:
    project = _good_sdp_project(tmp_path / "sdp-good")
    result = validate_project(project, contract_path=CONTRACT_PATH)

    assert "DE-D003" in _skipped_ids(result)
    assert not ({"DE-D001", "DE-D002", "DE-D004", "DE-D005"} & _failed_ids(result))
    assert result.exit_code == EXIT_OK
    assert result.profile == DATABRICKS_SDP_PROFILE


def test_sdp_fixture_reports_missing_medallion_schema_rescue_and_uc(
    tmp_path: Path,
) -> None:
    project = tmp_path / "sdp-bad"
    _layout_a_minimum(project)
    _force_cloud_profile(project)
    _dab_with_identity(project)
    _sdp_pipeline(project)
    # sem medallion, schema rescue e UC

    result = validate_project(project, contract_path=CONTRACT_PATH)
    failed = _failed_ids(result)

    assert result.exit_code == EXIT_BLOCKERS
    assert "DE-D002" in failed
    assert "DE-D004" in failed
    assert "DE-D005" in failed
    assert "DE-D003" in _skipped_ids(result)


def test_dlt_fixture_requires_quarantine_when_expectations_present(
    tmp_path: Path,
) -> None:
    project = tmp_path / "dlt-bad"
    _layout_a_minimum(project)
    _force_cloud_profile(project, profile="databricks-dlt-legacy")
    _dab_with_identity(project)
    _dlt_pipeline(project, with_quarantine=False)
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D003" in _failed_ids(result)
    assert result.exit_code == EXIT_BLOCKERS


def test_dlt_fixture_passes_with_quarantine_and_expectations(tmp_path: Path) -> None:
    project = tmp_path / "dlt-good"
    _layout_a_minimum(project)
    _force_cloud_profile(project, profile="databricks-dlt-legacy")
    _dab_with_identity(project)
    _dlt_pipeline(project, with_quarantine=True)
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D003" not in _failed_ids(result)
    assert "DE-D002" in _skipped_ids(result)
    assert result.exit_code == EXIT_OK


def test_dab_without_run_identity_is_blocker(tmp_path: Path) -> None:
    project = tmp_path / "dab-no-identity"
    _layout_a_minimum(project)
    _force_cloud_profile(project)
    _write(project / "databricks.yml", "bundle:\n  name: orders\n")
    _sdp_pipeline(project)
    _sdp_medallion(project)
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D001" in _failed_ids(result)
    assert result.exit_code == EXIT_BLOCKERS


def test_dab_with_empty_owner_and_run_as_is_blocker(tmp_path: Path) -> None:
    project = tmp_path / "dab-empty-identity"
    _layout_a_minimum(project)
    _force_cloud_profile(project)
    _write(
        project / "databricks.yml",
        "bundle:\n  name: orders\nowner:\nrun_as:\n",
    )
    _sdp_pipeline(project)
    _sdp_medallion(project)
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D001" in _failed_ids(result)
    assert result.exit_code == EXIT_BLOCKERS


def test_public_dab_manifest_helper_matches_detector_contract() -> None:
    assert is_dab_manifest("databricks.yml")
    assert is_dab_manifest("bundle-orders.yaml")
    assert not is_dab_manifest("pipeline.yaml")


def test_dlt_quarantine_policy_can_live_outside_dlt_corpus(tmp_path: Path) -> None:
    project = tmp_path / "dlt-policy"
    _layout_a_minimum(project)
    _force_cloud_profile(project, profile="databricks-dlt-legacy")
    _dab_with_identity(project)
    _dlt_pipeline(project, with_quarantine=False)
    _write(
        project / "config" / "policies" / "quality.yaml",
        "quality:\n  invalid_records: quarantine_orders\n",
    )
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D003" not in _failed_ids(result)
    assert result.exit_code == EXIT_OK


def test_dlt_signal_requires_quarantine_without_expectations(tmp_path: Path) -> None:
    project = tmp_path / "dlt-no-expectations"
    _layout_a_minimum(project)
    _force_cloud_profile(project, profile="databricks-dlt-legacy")
    _dab_with_identity(project)
    _write(
        project / "pipelines" / "orders_dlt.py",
        "import dlt\n\n@dlt.table\ndef orders():\n    return None\n",
    )
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D003" in _failed_ids(result)
    assert result.exit_code == EXIT_BLOCKERS


def test_multi_profile_exercises_sdp_and_dlt_rules_together(tmp_path: Path) -> None:
    project = tmp_path / "multi"
    _layout_a_minimum(project)
    _force_cloud_profile(project, profile=DATABRICKS_MULTI_PROFILE)
    _dab_with_identity(project)
    _sdp_pipeline(project)
    _write(
        project / "pipelines" / "orders_dlt.py",
        "import dlt\n\n@dlt.table\ndef orders():\n    return None\n",
    )
    _schema_rescue_policy(project)
    _uc_fs_artifacts(project)

    result = validate_project(project, contract_path=CONTRACT_PATH)
    failed = _failed_ids(result)
    assert {"DE-D002", "DE-D003"} <= failed
    assert result.profile == DATABRICKS_MULTI_PROFILE
    assert result.exit_code == EXIT_BLOCKERS


def test_cloud_without_dab_skips_d001_but_blocks_schema_rescue_and_uc(
    tmp_path: Path,
) -> None:
    project = tmp_path / "cloud-no-dab"
    _layout_a_minimum(project)
    _force_cloud_profile(project)
    _sdp_pipeline(project)
    _sdp_medallion(project)
    # sem DAB, schema rescue e UC

    result = validate_project(project, contract_path=CONTRACT_PATH)
    assert "DE-D001" in _skipped_ids(result)
    failed = _failed_ids(result)
    assert "DE-D004" in failed
    assert "DE-D005" in failed
    assert result.exit_code == EXIT_BLOCKERS


def test_d_findings_expose_only_path_and_safe_message(tmp_path: Path) -> None:
    project = tmp_path / "safe-finding"
    _layout_a_minimum(project)
    _force_cloud_profile(project)
    _write(
        project / "databricks.yml",
        (
            "bundle:\n  name: orders\n"
            + credential_assignment("client_secret", PSEUDO_SECRET)
        ),
    )
    _sdp_pipeline(project)

    files = iter_text_files(project)
    findings = check_package_d(project, files)
    serialized = " ".join(f"{f.rule_id}|{f.path}|{f.message}" for f in findings)

    assert findings
    assert all(f.rule_id.startswith("DE-D") for f in findings)
    assert all(f.path for f in findings)
    assert PSEUDO_SECRET not in serialized
    assert "super-secret" not in serialized.lower()


def test_explain_works_for_package_d_rule_ids() -> None:
    for rule_id in ("DE-D001", "DE-D002", "DE-D003", "DE-D004", "DE-D005"):
        code = cli_main(["explain", rule_id, "--contract", str(CONTRACT_PATH)])
        assert code == EXIT_OK

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "config.canonical_data_check",
            "explain",
            "DE-D004",
            "--contract",
            str(CONTRACT_PATH),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert proc.returncode == EXIT_OK
    assert "DE-D004 — Schema rescue policy deve estar documentada" in proc.stdout
    assert "Aplicabilidade: databricks-cloud" in proc.stdout
    assert "Remediação:" in proc.stdout


def test_package_d_check_is_deterministic(tmp_path: Path) -> None:
    project = _good_sdp_project(tmp_path / "det")
    files = iter_text_files(project)
    first = check_package_d(project, files)
    second = check_package_d(project, files)
    assert first == second
