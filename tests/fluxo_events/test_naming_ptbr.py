"""Task 73 — guardrail orthografia PT-BR: fluxo (x), nunca flujo (j) em paths do pacote."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# "flujo" com j (espanhol) — construído para o próprio arquivo não falhar o scan de paths
_SPANISH = "flu" + "j" + "o"
_PTBR = "flu" + chr(0x78) + "o"  # fluxo

PACKAGE_SCAN_ROOTS: tuple[Path, ...] = (
    REPO_ROOT / f"{_PTBR}-events.yaml",
    REPO_ROOT / "config" / f"{_PTBR}_events",
    REPO_ROOT / "tests" / f"{_PTBR}_events",
    REPO_ROOT / ".claude" / "commands" / f"{_PTBR}-live.md",
    REPO_ROOT / ".cursor" / "commands" / f"{_PTBR}-live.md",
    REPO_ROOT / "config" / f"{_PTBR}_events" / "templates" / _PTBR,
    REPO_ROOT / "docs" / f"{_PTBR}-events-cheatsheet.md",
)


def scan_spanish_flujo_in_paths(roots: tuple[Path, ...] | list[Path]) -> list[str]:
    """Retorna paths versionados cujo nome relativo contém a substring espanhola (j).

    Escopo = pacote fluxo-events (roots explícitos), **não** o repositório inteiro.
    """
    hits: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file():
            candidates = [root]
        else:
            candidates = [p for p in root.rglob("*") if p.is_file() or p.is_dir()]
            candidates.append(root)
        for path in candidates:
            try:
                rel = str(path.relative_to(REPO_ROOT))
            except ValueError:
                rel = str(path)
            # Checa cada componente do path (não conteúdo de arquivo)
            parts = Path(rel).parts
            if any(_SPANISH in part for part in parts):
                hits.append(rel)
    return sorted(set(hits))


def test_no_spanish_flujo_in_package_paths() -> None:
    hits = scan_spanish_flujo_in_paths(PACKAGE_SCAN_ROOTS)
    assert hits == [], f"encontrado {_SPANISH!r} em paths do pacote: {hits}"


def test_scan_detects_spanish_flujo(tmp_path: Path) -> None:
    bad = tmp_path / f"config_{_SPANISH}_events" / "x.py"
    bad.parent.mkdir(parents=True)
    bad.write_text("# ok\n", encoding="utf-8")
    hits = scan_spanish_flujo_in_paths([tmp_path / f"config_{_SPANISH}_events"])
    assert hits, "fixture negativa deveria detectar path com j"


def test_scan_roots_are_scoped() -> None:
    """Documenta escopo: não varre repo inteiro — só roots do pacote."""
    assert PACKAGE_SCAN_ROOTS
    assert all(
        _PTBR in str(p) or p.name.endswith(f"{_PTBR}-events.yaml")
        or f"{_PTBR}-events" in str(p)
        or f"{_PTBR}_events" in str(p)
        or f"{_PTBR}-live" in str(p)
        for p in PACKAGE_SCAN_ROOTS
    )
    # Explicitamente não inclui REPO_ROOT sozinho
    assert REPO_ROOT not in PACKAGE_SCAN_ROOTS
