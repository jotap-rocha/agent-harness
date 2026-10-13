"""Testes de contrato da fonte normativa de Engenharia de Dados."""

from __future__ import annotations

from pathlib import Path

import pytest

from config.data_engineering import DataEngineeringContract

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "data-engineering.yaml"


def test_loads_root_contract_with_version_and_pilot_profile() -> None:
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    assert contract.version == 1
    assert contract.profile("spark-yarn-airflow").id == "spark-yarn-airflow"


def test_public_api_supports_load_and_from_mapping() -> None:
    loaded = DataEngineeringContract.load(CONTRACT_PATH)
    rebuilt = DataEngineeringContract.from_mapping(
        {
            "version": 1,
            "profiles": {
                "spark-yarn-airflow": {
                    "description": "Perfil piloto",
                    "packages": ["A", "B", "C"],
                }
            },
            "packages": {
                "A": {
                    "description": "Universal",
                    "applicability": "universal",
                    "severity": "blocker",
                    "rules": {
                        "DE-A001": {
                            "category": "security",
                            "severity": "blocker",
                            "applicability": "universal",
                            "title": "Secrets não versionados",
                            "explanation": "Credenciais devem vir de secret manager.",
                            "remediation": "Remova o secret e rotacione a credencial.",
                        }
                    },
                },
                "B": {
                    "description": "Spark/YARN",
                    "applicability": "profile",
                    "severity": "blocker",
                    "rules": {
                        "DE-B001": {
                            "category": "architecture",
                            "severity": "blocker",
                            "applicability": "spark-yarn-airflow",
                            "title": "Camadas declaradas",
                            "explanation": "O fluxo deve separar suas camadas.",
                            "remediation": "Declare as camadas do pipeline.",
                        }
                    },
                },
                "C": {
                    "description": "Airflow",
                    "applicability": "conditional",
                    "severity": "blocker",
                    "rules": {
                        "DE-C001": {
                            "category": "orchestration",
                            "severity": "blocker",
                            "applicability": "airflow-dag-present",
                            "title": "Tags de DAG",
                            "explanation": "DAGs precisam de tags.",
                            "remediation": "Adicione tags à DAG.",
                        }
                    },
                },
            },
        }
    )

    assert rebuilt.version == loaded.version
    assert rebuilt.package("A").rule("DE-A001").category == "security"


@pytest.mark.parametrize(
    "mapping,expected_message",
    [
        ({}, "version"),
        ({"version": 1}, "profiles"),
        ({"version": 1, "profiles": {}}, "profiles"),
        (
            {
                "version": 1,
                "profiles": {
                    "spark-yarn-airflow": {
                        "description": "Perfil piloto",
                        "packages": ["A", "B", "C"],
                    }
                },
            },
            "packages",
        ),
    ],
)
def test_rejects_missing_required_fields(
    mapping: dict[str, object],
    expected_message: str,
) -> None:
    with pytest.raises(ValueError, match=expected_message):
        DataEngineeringContract.from_mapping(mapping)


def test_rejects_invalid_yaml(tmp_path: Path) -> None:
    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("version: 1\n  profiles:\n", encoding="utf-8")

    with pytest.raises(ValueError):
        DataEngineeringContract.load(invalid_yaml)


def test_loaded_contract_contains_rule_ids_for_packages_a_b_c() -> None:
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    expected_ids = {
        "A": {"DE-A001", "DE-A002", "DE-A003", "DE-A004", "DE-A005"},
        "B": {"DE-B001", "DE-B002", "DE-B003"},
        "C": {"DE-C001", "DE-C002", "DE-C003"},
    }

    for package_id, rule_ids in expected_ids.items():
        assert {rule.id for rule in contract.package(package_id).rules} == rule_ids


def test_rejects_profile_referencing_unknown_package() -> None:
    mapping: dict[str, object] = {
        "version": 1,
        "profiles": {
            "spark-yarn-airflow": {
                "description": "Perfil piloto",
                "packages": ["UNKNOWN"],
            }
        },
        "packages": {
            "A": {
                "description": "Universal",
                "applicability": "universal",
                "severity": "blocker",
                "rules": {
                    "DE-A001": {
                        "category": "security",
                        "severity": "blocker",
                        "applicability": "universal",
                        "title": "Secrets não versionados",
                        "explanation": "Credenciais devem vir de secret manager.",
                        "remediation": "Remova o secret e rotacione a credencial.",
                    }
                },
            }
        },
    }

    with pytest.raises(ValueError, match="pacotes desconhecidos: UNKNOWN"):
        DataEngineeringContract.from_mapping(mapping)


def test_rules_expose_explain_metadata_and_classification() -> None:
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    for package in contract.packages:
        assert package.description
        assert package.applicability in {"universal", "profile", "conditional"}
        for rule in package.rules:
            assert rule.category
            assert rule.severity in {"blocker", "warning"}
            assert rule.applicability
            assert rule.title
            assert rule.explanation
            assert rule.remediation


# --- Loop 2 / Task 17: perfis Databricks + pacote D ---------------------------------


CLOUD_PROFILE_IDS = (
    "databricks-sdp-medallion",
    "databricks-dlt-legacy",
    "databricks-multi",
)

PACKAGE_D_RULE_IDS = {
    "DE-D001",
    "DE-D002",
    "DE-D003",
    "DE-D004",
    "DE-D005",
}


def test_loads_databricks_profiles_and_package_d() -> None:
    """AC1: três perfis Databricks + pacote D com regras DE-D* carregam."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    for profile_id in CLOUD_PROFILE_IDS:
        assert contract.profile(profile_id).id == profile_id

    package_d = contract.package("D")
    assert "databricks-cloud" in package_d.description
    assert package_d.applicability == "conditional"
    assert {rule.id for rule in package_d.rules} == PACKAGE_D_RULE_IDS


def test_cloud_profiles_enable_packages_a_and_d() -> None:
    """AC2: perfis cloud apontam A+D; multi documenta união semântica SDP+DLT."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    for profile_id in CLOUD_PROFILE_IDS:
        profile = contract.profile(profile_id)
        assert set(profile.package_ids) == {"A", "D"}

    multi = contract.profile("databricks-multi")
    description_lower = multi.description.lower()
    assert "união" in description_lower or "uniao" in description_lower
    assert "sdp" in description_lower
    assert "dlt" in description_lower


def test_package_d_rules_expose_conditional_sdp_dlt_applicability() -> None:
    """Metadata normativa: applicability condicional por sinal SDP/DLT/DAB/cloud."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)
    package_d = contract.package("D")

    by_id = {rule.id: rule for rule in package_d.rules}
    assert by_id["DE-D001"].applicability == "databricks-dab-present"
    assert by_id["DE-D002"].applicability == "sdp-signal-present"
    assert by_id["DE-D003"].applicability == "dlt-signal-present"
    assert by_id["DE-D004"].applicability == "databricks-cloud"
    assert by_id["DE-D005"].applicability == "databricks-cloud"

    for rule in package_d.rules:
        assert rule.severity == "blocker"
        assert rule.category
        assert rule.title
        assert rule.explanation
        assert rule.remediation


def test_loop1_spark_yarn_and_packages_abc_still_load() -> None:
    """AC3: regressão Loop 1 — spark-yarn-airflow e A/B/C intactos."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    spark = contract.profile("spark-yarn-airflow")
    assert spark.package_ids == ("A", "B", "C")

    expected_ids = {
        "A": {"DE-A001", "DE-A002", "DE-A003", "DE-A004", "DE-A005"},
        "B": {"DE-B001", "DE-B002", "DE-B003"},
        "C": {"DE-C001", "DE-C002", "DE-C003"},
    }
    for package_id, rule_ids in expected_ids.items():
        assert {rule.id for rule in contract.package(package_id).rules} == rule_ids


def _minimal_valid_rule() -> dict[str, str]:
    return {
        "category": "databricks-layout",
        "severity": "blocker",
        "applicability": "databricks-dab-present",
        "title": "Regra mínima",
        "explanation": "Explicação mínima para teste negativo.",
        "remediation": "Corrija o artefato no repositório.",
    }


def _minimal_package_a() -> dict[str, object]:
    return {
        "description": "Universal",
        "applicability": "universal",
        "severity": "blocker",
        "rules": {
            "DE-A001": {
                "category": "security",
                "severity": "blocker",
                "applicability": "universal",
                "title": "Secrets",
                "explanation": "Sem secrets versionados.",
                "remediation": "Use secret manager.",
            }
        },
    }


@pytest.mark.parametrize(
    "mutate,expected_message",
    [
        (
            lambda packages: packages["D"].pop("description"),
            r"packages\.D\.description",
        ),
        (
            lambda packages: packages["D"].update({"rules": {}}),
            r"packages\.D\.rules",
        ),
        (
            lambda packages: packages["D"].update({"applicability": "cloud-only"}),
            r"packages\.D\.applicability",
        ),
        (
            lambda packages: packages["D"]["rules"]["DE-D001"].pop("title"),
            r"packages\.D\.rules\.DE-D001\.title",
        ),
        (
            lambda packages: packages["D"].update({"severity": "critical"}),
            r"packages\.D\.severity",
        ),
    ],
)
def test_rejects_malformed_package_d(
    mutate: object,
    expected_message: str,
) -> None:
    """AC4: loader rejeita pacote D malformado."""
    mapping: dict[str, object] = {
        "version": 1,
        "profiles": {
            "databricks-sdp-medallion": {
                "description": "Perfil SDP",
                "packages": ["A", "D"],
            }
        },
        "packages": {
            "A": _minimal_package_a(),
            "D": {
                "description": "Pacote databricks-cloud",
                "applicability": "conditional",
                "severity": "blocker",
                "rules": {"DE-D001": _minimal_valid_rule()},
            },
        },
    }
    packages = mapping["packages"]
    assert isinstance(packages, dict)
    mutate(packages)  # type: ignore[operator]

    with pytest.raises(ValueError, match=expected_message):
        DataEngineeringContract.from_mapping(mapping)


@pytest.mark.parametrize(
    "mutate,expected_message",
    [
        (
            lambda profiles: profiles["databricks-sdp-medallion"].pop("description"),
            r"profiles\.databricks-sdp-medallion\.description",
        ),
        (
            lambda profiles: profiles["databricks-sdp-medallion"].update(
                {"packages": []}
            ),
            r"profiles\.databricks-sdp-medallion\.packages",
        ),
        (
            lambda profiles: profiles["databricks-sdp-medallion"].update(
                {"packages": ["A", "Z"]}
            ),
            r"pacotes desconhecidos: Z",
        ),
    ],
)
def test_rejects_malformed_databricks_profile(
    mutate: object,
    expected_message: str,
) -> None:
    """AC4: loader rejeita perfil Databricks malformado."""
    mapping: dict[str, object] = {
        "version": 1,
        "profiles": {
            "databricks-sdp-medallion": {
                "description": "Perfil SDP",
                "packages": ["A", "D"],
            }
        },
        "packages": {
            "A": _minimal_package_a(),
            "D": {
                "description": "Pacote databricks-cloud",
                "applicability": "conditional",
                "severity": "blocker",
                "rules": {"DE-D001": _minimal_valid_rule()},
            },
        },
    }
    profiles = mapping["profiles"]
    assert isinstance(profiles, dict)
    mutate(profiles)  # type: ignore[operator]

    with pytest.raises(ValueError, match=expected_message):
        DataEngineeringContract.from_mapping(mapping)


# --- Loop keyvault / Task 33: pacote E -------------------------------------------------


PACKAGE_E_RULE_IDS = {
    "DE-E001",
    "DE-E002",
    "DE-E003",
}


def test_loads_package_e_keyvault_cloud() -> None:
    """AC: pacote E keyvault-cloud com regras DE-E* carregáveis."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    package_e = contract.package("E")
    assert "keyvault-cloud" in package_e.description
    assert package_e.applicability == "conditional"
    assert {rule.id for rule in package_e.rules} == PACKAGE_E_RULE_IDS


def test_package_e_rules_expose_keyvault_applicability_and_remediation() -> None:
    contract = DataEngineeringContract.load(CONTRACT_PATH)
    package_e = contract.package("E")
    by_id = {rule.id: rule for rule in package_e.rules}

    assert by_id["DE-E001"].applicability == "keyvault-cloud"
    assert by_id["DE-E002"].applicability == "keyvault-cloud"
    assert by_id["DE-E003"].applicability == "keyvault-cloud"
    for rule in package_e.rules:
        assert rule.severity == "blocker"
        assert rule.category
        assert rule.title
        assert rule.explanation
        assert rule.remediation


def test_loop2_profiles_do_not_list_package_e_by_default() -> None:
    """E é ortogonal ao perfil DE — injectado pelo engine quando vault aplica."""
    contract = DataEngineeringContract.load(CONTRACT_PATH)

    assert "E" not in contract.profile("spark-yarn-airflow").package_ids
    for profile_id in CLOUD_PROFILE_IDS:
        assert "E" not in contract.profile(profile_id).package_ids


def _minimal_valid_rule_e() -> dict[str, str]:
    return {
        "category": "secret-facade",
        "severity": "blocker",
        "applicability": "keyvault-cloud",
        "title": "Regra mínima E",
        "explanation": "Explicação mínima para teste negativo.",
        "remediation": "Corrija o wiring de vault no repositório.",
    }


@pytest.mark.parametrize(
    "mutate,expected_message",
    [
        (
            lambda packages: packages["E"].pop("description"),
            r"packages\.E\.description",
        ),
        (
            lambda packages: packages["E"].update({"rules": {}}),
            r"packages\.E\.rules",
        ),
        (
            lambda packages: packages["E"].update({"applicability": "vault-only"}),
            r"packages\.E\.applicability",
        ),
        (
            lambda packages: packages["E"]["rules"]["DE-E001"].pop("title"),
            r"packages\.E\.rules\.DE-E001\.title",
        ),
    ],
)
def test_rejects_malformed_package_e(
    mutate: object,
    expected_message: str,
) -> None:
    mapping: dict[str, object] = {
        "version": 1,
        "profiles": {
            "spark-yarn-airflow": {
                "description": "Perfil piloto",
                "packages": ["A"],
            }
        },
        "packages": {
            "A": _minimal_package_a(),
            "E": {
                "description": "Pacote keyvault-cloud",
                "applicability": "conditional",
                "severity": "blocker",
                "rules": {"DE-E001": _minimal_valid_rule_e()},
            },
        },
    }
    packages = mapping["packages"]
    assert isinstance(packages, dict)
    mutate(packages)  # type: ignore[operator]

    with pytest.raises(ValueError, match=expected_message):
        DataEngineeringContract.from_mapping(mapping)
