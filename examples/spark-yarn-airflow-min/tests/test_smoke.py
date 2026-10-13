"""Smoke do example — não executa Spark; só prova layout testável."""


def test_synthetic_contract_version_declared() -> None:
    from pathlib import Path

    contract = Path(__file__).resolve().parents[1] / "contracts" / "orders.v1.yaml"
    text = contract.read_text(encoding="utf-8")
    assert "version: 1" in text
    assert "order_id" in text
