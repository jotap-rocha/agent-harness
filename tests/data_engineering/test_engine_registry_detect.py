"""Testes da Task 18 — registry, auto-detect e resolução de perfil."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.canonical_data_check import engine
from config.canonical_data_check.constants import DEFAULT_PROFILE
from config.canonical_data_check.de_marker import (
    DATABRICKS_DLT_PROFILE,
    DATABRICKS_MULTI_PROFILE,
    DATABRICKS_SDP_PROFILE,
    DatabricksSignals,
    detect_databricks_signals,
    resolve_effective_profile,
)
from config.canonical_data_check.findings import Finding
from config.canonical_data_check.scanner import TextFile

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"


def _write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.parametrize(
    ("relative_path", "content", "expected"),
    [
        (
            "databricks.yml",
            "bundle:\n  name: orders\n",
            DatabricksSignals(dab=True),
        ),
        (
            "resources/bundle-orders.yaml",
            "resources:\n  jobs: {}\n",
            DatabricksSignals(dab=True),
        ),
        (
            "pipelines/orders_dlt.py",
            "import dlt\n\n@dlt.table\ndef orders():\n    return None\n",
            DatabricksSignals(dlt=True),
        ),
        (
            "src/orders_sdp.py",
            (
                "from pyspark import pipelines as dp\n\n"
                "@dp.materialized_view()\n"
                "def orders():\n"
                "    return None\n"
            ),
            DatabricksSignals(sdp=True),
        ),
    ],
)
def test_detect_databricks_signals_from_documented_tree_heuristics(
    tmp_path: Path,
    relative_path: str,
    content: str,
    expected: DatabricksSignals,
) -> None:
    project = tmp_path / "project"
    _write(project / relative_path, content)

    assert detect_databricks_signals(project) == expected


def test_sdp_decorator_is_detected_without_matching_similar_alias(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    _write(
        project / "src/orders.py",
        "@dp.table\ndef orders():\n    return None\n",
    )
    assert detect_databricks_signals(project).sdp is True

    _write(
        project / "src/orders.py",
        "@dpx.table\ndef orders():\n    return None\n",
    )
    assert detect_databricks_signals(project).sdp is False


def test_marker_override_wins_over_detected_sdp(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _write(
        project / ".harness/data-check/project_profile.yaml",
        f"profile: {DATABRICKS_DLT_PROFILE}\n",
    )
    _write(
        project / "src/orders_sdp.py",
        "from pyspark import pipelines as dp\n@dp.table\ndef orders(): pass\n",
    )

    assert (
        resolve_effective_profile(project, valid_profiles=_contract_profiles())
        == DATABRICKS_DLT_PROFILE
    )


def test_invalid_marker_does_not_override_detected_sdp(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _write(
        project / ".harness/data-check/project_profile.yaml",
        "profile: databricks-unknown\n",
    )
    _write(
        project / "src/orders.py",
        "from pyspark import pipelines as dp\n@dp.table\ndef orders(): pass\n",
    )

    assert (
        resolve_effective_profile(project, valid_profiles=_contract_profiles())
        == DATABRICKS_SDP_PROFILE
    )


def test_sdp_and_dlt_resolve_to_multi_profile(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _write(
        project / "src/orders.py",
        (
            "import dlt\n"
            "from pyspark import pipelines as dp\n"
            "@dlt.table\n"
            "def legacy_orders(): pass\n"
            "@dp.table\n"
            "def streaming_orders(): pass\n"
        ),
    )

    assert (
        resolve_effective_profile(project, valid_profiles=_contract_profiles())
        == DATABRICKS_MULTI_PROFILE
    )


def test_no_marker_or_cloud_signal_preserves_loop_one_default(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _write(project / "pipelines/orders.py", "import logging\nrun_id = 'local'\n")

    assert (
        detect_databricks_signals(project)
        == DatabricksSignals()
    )
    assert (
        resolve_effective_profile(project, valid_profiles=_contract_profiles())
        == DEFAULT_PROFILE
    )


def test_dab_only_does_not_choose_sdp_or_dlt_profile(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _write(project / "databricks.yml", "bundle:\n  name: orders\n")

    assert detect_databricks_signals(project) == DatabricksSignals(dab=True)
    assert (
        resolve_effective_profile(project, valid_profiles=_contract_profiles())
        == DEFAULT_PROFILE
    )


def test_engine_dispatches_package_d_for_cloud_profile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    _write(
        project / ".harness/data-check/project_profile.yaml",
        f"profile: {DATABRICKS_SDP_PROFILE}\n",
    )

    def stub_package_d(
        project_root: Path,
        files: tuple[TextFile, ...],
    ) -> tuple[Finding, ...]:
        del project_root, files
        return (
            Finding(
                rule_id="DE-D-STUB",
                severity="warning",
                status="pass",
                path=".",
                message="package D dispatched",
            ),
        )

    monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, "D", stub_package_d)

    result = engine.validate_project(project, contract_path=CONTRACT_PATH)

    assert result.profile == DATABRICKS_SDP_PROFILE
    assert any(finding.rule_id == "DE-D-STUB" for finding in result.findings)


def test_engine_reuses_single_filesystem_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    _write(project / "pipelines/orders.py", "import logging\nrun_id = 'local'\n")
    original_iter_text_files = engine.iter_text_files
    calls = 0

    def counting_iter_text_files(project_root: Path) -> tuple[TextFile, ...]:
        nonlocal calls
        calls += 1
        return original_iter_text_files(project_root)

    monkeypatch.setattr(engine, "iter_text_files", counting_iter_text_files)

    engine.validate_project(project, contract_path=CONTRACT_PATH)

    assert calls == 1


def test_engine_uses_multi_profile_and_dispatches_d_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    _write(
        project / "src/orders.py",
        (
            "import dlt\n"
            "from pyspark import pipelines as dp\n"
            "@dlt.table\n"
            "def legacy_orders(): pass\n"
            "@dp.table\n"
            "def streaming_orders(): pass\n"
        ),
    )
    calls = 0

    def stub_package_d(
        project_root: Path,
        files: tuple[TextFile, ...],
    ) -> tuple[Finding, ...]:
        nonlocal calls
        del project_root, files
        calls += 1
        return ()

    monkeypatch.setitem(engine.PACKAGE_CHECK_REGISTRY, "D", stub_package_d)

    result = engine.validate_project(project, contract_path=CONTRACT_PATH)

    assert result.profile == DATABRICKS_MULTI_PROFILE
    assert calls == 1


def _contract_profiles() -> frozenset[str]:
    from config.data_engineering import DataEngineeringContract

    contract = DataEngineeringContract.load(CONTRACT_PATH)
    return frozenset(profile.id for profile in contract.profiles)
