#!/usr/bin/env python3
"""CLI standalone para instalar/atualizar o Agent Harness Canônico num projeto alvo.

Uso:
    python3 install_harness.py <destino> [--canonical PATH] [--dry-run] [--yes] [--json]
                                [--force-category NOME ...]

Roda sozinha, sem depender do Claude Code — Python 3 stdlib apenas, sem dependências.
Nunca sobrescreve um arquivo existente sem confirmação explícita do usuário.

Fluxo:
  1. detect_mode()          -> NOVO | SEM_HARNESS | ATUALIZACAO
  2. collect_keywords()     -> vocabulário de keywords derivado do stack_map.json (não hardcoded)
  3. detect_stack_signals() -> parse de pyproject.toml/package.json/lockfiles + fallback textual
  4. build_plan()           -> classifica cada artefato do stack_map.json (--force-category
                                inclui categoria mesmo sem stack detectada)
  5. resolve_conflicts      -> interativo (input()) ou via --decisions-file (--json)
  6. apply_plan()           -> copia/gera/scaffold, espelha .cursor/, grava manifest
"""
from __future__ import annotations

import argparse
import difflib
import filecmp
import json
import os
import re
import shutil
import sys
import tomllib
from datetime import date
from pathlib import Path

# Default = raiz deste clone (…/.claude/skills/install-harness/scripts → 4 níveis acima).
# Override: --canonical PATH ou env HARNESS_CANONICAL (launcher bash).
DEFAULT_CANONICAL = str(Path(__file__).resolve().parents[4])
MANIFEST_REL = ".claude/harness-manifest.json"
KEYWORD_FILES = ["pyproject.toml", "package.json"]  # fallback: scan bruto se o parse estruturado falhar

# Detecção de nuvem (categorias cloud_*): campo `cloud:` do CLAUDE.md, blocos `provider` em *.tf
# e prefixos de dependência. Injeta keywords sintéticas `cloud_<provider>` + `cloud_any`.
CLOUD_PROVIDERS = ("azure", "aws", "gcp")
# `cloud: aws`, `cloud: aws, gcp`, `cloud: multi`, `cloud: none`; tolera bullet/negrito/crase.
# Linha de template com `|` (ex.: `azure | aws | gcp | multi`) não é declaração.
CLOUD_FIELD_RE = re.compile(
    r"^[ \t>*\-]*\**cloud:\**[ \t]*`?([A-Za-z, ]+?)`?[ \t]*(?:#.*)?$", re.MULTILINE
)
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
TF_PROVIDER_RE = re.compile(r'provider\s+"(azurerm|azuread|aws|google|google-beta)"')
TF_SOURCE_RE = re.compile(r'source\s*=\s*"hashicorp/(azurerm|azuread|aws|google|google-beta)"')
TF_COMMENT_RE = re.compile(r"(?m)(?:#|//).*$")
TF_PROVIDER_TO_CLOUD = {"azurerm": "azure", "azuread": "azure", "aws": "aws",
                        "google": "gcp", "google-beta": "gcp"}
TF_SKIP_DIRS = {".git", ".terraform", "node_modules", ".venv", "venv", "__pycache__"}
TF_MAX_DEPTH = 4
# Só dependências DECLARADAS (pyproject/package.json/requirements) — lockfiles trazem transitivas
# (ex.: dbt-snowflake -> boto3, mssql -> @azure/identity) e dariam falso positivo.
CLOUD_DEP_PREFIXES = {
    "azure": ("azure-", "@azure/"),
    "aws": ("boto3", "botocore", "aioboto3", "awswrangler", "aws-cdk", "aws-lambda-powertools",
            "aws-sdk", "@aws-sdk/", "@aws-cdk/"),
    "gcp": ("google-cloud-", "@google-cloud/"),
}

# Hook de aviso de drift de contexto: avisa, nunca bloqueia (exit 0 sempre). Sai silencioso se a
# skill sync-context não foi instalada, e usa stamp file para avisar no máximo a cada 4h.
CONTEXT_DRIFT_HOOK_COMMAND = (
    'S=.claude/skills/sync-context/scripts/check_context_drift.py; [ -f "$S" ] || exit 0; '
    "STAMP=.claude/.context-drift-stamp; "
    '[ -n "$(find $STAMP -mmin -240 2>/dev/null)" ] && exit 0; '
    "touch $STAMP; python3 $S --warn; exit 0"
)
CONTEXT_DRIFT_PERMISSION = "Bash(python3 .claude/skills/sync-context/scripts/*)"

# Assinatura do CLAUDE.md do canônico — nunca deve ser o título do projeto-filho.
CANONICAL_AGENT_GUIDE_TITLE = "Agent Harness Canônico — guia do agente"
PLACEHOLDER_MARKERS = (
    "(preencher com /grill-me)",
    "(preencher com /grill-with-docs)",
    "Stub gerado pelo install-harness",
    "Gerado pelo install-harness",
    "Iniciado pelo install-harness",
)


def anti_canonical_banner(project_name: str) -> str:
    """Banner obrigatório no topo dos stubs de contexto do filho."""
    return (
        f"> **Este repositório é o projeto `{project_name}`, "
        "não o Agent Harness Canônico.**\n"
        "> Não copie o guia do repositório canônico do harness. "
        "Refine com `/grill-me`, `/grill-with-docs` ou `harness-architect`.\n"
    )


def looks_like_canonical_context(text: str) -> bool:
    """True se o texto ainda carrega título/assinatura do canônico (H1 ou corpo)."""
    if not text:
        return False
    for line in text.splitlines()[:40]:
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        # Só headings — o banner pode citar o nome do canônico em prosa.
        if CANONICAL_AGENT_GUIDE_TITLE in stripped:
            return True
        if stripped.startswith("# Agent Harness Canônico"):
            return True
    head = text[:1500]
    return "Este repositório é o **framework** do Agent Harness Method" in head


def needs_context_rebind(text: str) -> bool:
    """True se o arquivo ainda é placeholder de install ou assinatura canônica."""
    if looks_like_canonical_context(text):
        return True
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


# --------------------------------------------------------------------------- detecção

def read_manifest(target: Path) -> dict | None:
    manifest_path = target / MANIFEST_REL
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def detect_mode(target: Path, manifest: dict | None) -> str:
    claude_dir = target / ".claude"
    if not claude_dir.exists() or not any(claude_dir.iterdir()):
        return "NOVO"
    if manifest is None:
        return "SEM_HARNESS"
    return "ATUALIZACAO"


def collect_keywords(stack_map: dict) -> set[str]:
    """Deriva o vocabulário de keywords do stack_map.json — nunca hardcoded em duplicata.
    Adicionar uma categoria keyword_in_files nova no stack_map já basta; nada a tocar aqui."""
    keywords: set[str] = set()
    for category in stack_map["categories"]:
        condition = category["condition"]
        if condition["type"] == "keyword_in_files":
            keywords.update(condition["keywords"])
    return keywords


def _dep_name(raw: str) -> str:
    """'fastapi[standard]>=0.100,<1.0' -> 'fastapi'. 'requests ; python_version<"3.9"' -> 'requests'."""
    return re.split(r"[<>=!\[\];~\s(]", raw.strip(), maxsplit=1)[0].strip().lower()


def _names_from_pyproject(path: Path) -> set[str]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError, UnicodeDecodeError):
        return set()
    names: set[str] = set()
    project = data.get("project", {})
    for dep in project.get("dependencies", []) or []:
        names.add(_dep_name(dep))
    for group in (project.get("optional-dependencies") or {}).values():
        for dep in group or []:
            names.add(_dep_name(dep))
    poetry = data.get("tool", {}).get("poetry", {})
    for key in ("dependencies", "dev-dependencies"):
        for pkg_name in (poetry.get(key) or {}):
            if pkg_name.lower() != "python":
                names.add(pkg_name.lower())
    for group in (poetry.get("group") or {}).values():
        for pkg_name in (group.get("dependencies") or {}):
            names.add(pkg_name.lower())
    uv_dev = data.get("tool", {}).get("uv", {}).get("dev-dependencies", []) or []
    for dep in uv_dev:
        names.add(_dep_name(dep))
    return names


def _names_from_package_json(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return set()
    names: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        names.update(pkg.lower() for pkg in (data.get(key) or {}))
    return names


def _names_from_toml_lockfile(path: Path) -> set[str]:
    """uv.lock / poetry.lock — ambos TOML com [[package]] name = '...'."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError, UnicodeDecodeError):
        return set()
    return {pkg["name"].lower() for pkg in data.get("package", []) or [] if pkg.get("name")}


def _names_from_package_lock_json(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return set()
    names: set[str] = set()
    for key in (data.get("packages") or {}):
        # chaves tipo "node_modules/pkg" ou "node_modules/@scope/pkg"
        leaf = key.rsplit("node_modules/", 1)[-1]
        if leaf:
            names.add(leaf.lower())
    names.update(pkg.lower() for pkg in (data.get("dependencies") or {}))
    return names


def _names_from_requirements_txt(path: Path) -> set[str]:
    names: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return names
    for line in lines:
        line = line.strip()
        if not line or line.startswith(("#", "-")):
            continue
        names.add(_dep_name(line))
    return names


def detect_stack_signals(target: Path, keywords: set[str]) -> dict:
    """Sinais de stack do projeto-alvo. Parse estruturado (TOML/JSON) das listas de
    dependência declaradas + lockfiles (sinal mais forte que o declarado) primeiro;
    scan de texto bruto como rede de segurança para formato não-padrão/malformado."""
    signals = {
        "pyproject": (target / "pyproject.toml").exists(),
        "package_json": (target / "package.json").exists(),
        "docker_compose": (target / "docker-compose.yml").exists(),
        "keywords": set(),
    }

    dep_names: set[str] = set()
    if signals["pyproject"]:
        dep_names |= _names_from_pyproject(target / "pyproject.toml")
    if signals["package_json"]:
        dep_names |= _names_from_package_json(target / "package.json")
    if (target / "requirements.txt").exists():
        dep_names |= _names_from_requirements_txt(target / "requirements.txt")
    declared_deps = set(dep_names)  # antes dos lockfiles (detecção de nuvem usa só estas)
    if (target / "uv.lock").exists():
        dep_names |= _names_from_toml_lockfile(target / "uv.lock")
    if (target / "poetry.lock").exists():
        dep_names |= _names_from_toml_lockfile(target / "poetry.lock")
    if (target / "package-lock.json").exists():
        dep_names |= _names_from_package_lock_json(target / "package-lock.json")

    for kw in keywords:
        if any(kw == name or kw in name for name in dep_names):
            signals["keywords"].add(kw)

    # rede de segurança: scan de texto bruto (pega o que o parse estruturado não cobre —
    # formato não-padrão, dependência mencionada em comentário/script, etc.)
    for fname in KEYWORD_FILES:
        fpath = target / fname
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        for kw in keywords:
            if kw in text:
                signals["keywords"].add(kw)

    # Flag vault / secret_store: marker DE injeta keyword para categoria cloud_secrets
    # (ortogonal a pipeline_dados — não acoplar sempre).
    marker = target / ".harness" / "data-check" / "project_profile.yaml"
    if marker.is_file() and "secret_store" in keywords:
        try:
            marker_text = marker.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            marker_text = ""
        if "secret_store" in marker_text.lower():
            signals["keywords"].add("secret_store")

    clouds = detect_clouds(target, declared_deps)
    signals["clouds"] = sorted(clouds)  # lista: signals vai para json.dumps em --json
    signals["keywords"].update(f"cloud_{c}" for c in clouds)
    if clouds:
        signals["keywords"].add("cloud_any")

    return signals


def _declared_clouds(claude_md: Path) -> set[str] | None:
    """Lê `cloud:` do CLAUDE.md fora de blocos de código. None = sem declaração válida."""
    try:
        text = FENCED_BLOCK_RE.sub("", claude_md.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return None
    for match in CLOUD_FIELD_RE.finditer(text):
        tokens = {t.strip().lower() for t in match.group(1).split(",") if t.strip()}
        if not tokens:
            continue
        if tokens == {"none"}:
            return set()
        if "multi" in tokens:
            return set(CLOUD_PROVIDERS)
        if tokens <= set(CLOUD_PROVIDERS):
            return tokens
    return None


def _terraform_clouds(target: Path) -> set[str]:
    """Nuvens por `provider "x"` / `source = "hashicorp/x"` em *.tf (recursivo, com limite)."""
    clouds: set[str] = set()
    root_depth = len(target.parts)
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in TF_SKIP_DIRS]
        if len(Path(dirpath).parts) - root_depth >= TF_MAX_DEPTH:
            dirnames[:] = []
        for name in filenames:
            if not name.endswith(".tf"):
                continue
            try:
                text = (Path(dirpath) / name).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            text = TF_COMMENT_RE.sub("", text)
            found = TF_PROVIDER_RE.findall(text) + TF_SOURCE_RE.findall(text)
            clouds.update(TF_PROVIDER_TO_CLOUD[p] for p in found)
    return clouds


def detect_clouds(target: Path, declared_deps: set[str]) -> set[str]:
    """Nuvens do projeto-alvo. O campo `cloud:` do CLAUDE.md é declaração explícita e vence
    (`cloud: none` suprime a inferência); sem ele, infere por *.tf e por deps declaradas."""
    claude_md = target / "CLAUDE.md"
    if claude_md.is_file():
        declared = _declared_clouds(claude_md)
        if declared is not None:
            return declared

    clouds = _terraform_clouds(target)
    for cloud, prefixes in CLOUD_DEP_PREFIXES.items():
        if any(name.startswith(prefixes) for name in declared_deps):
            clouds.add(cloud)
    return clouds


def condition_matches(condition: dict, signals: dict) -> bool:
    ctype = condition["type"]
    if ctype == "always":
        return True
    if ctype == "file_exists":
        return any((Path(f) == Path("pyproject.toml") and signals["pyproject"])
                   or (Path(f) == Path("package.json") and signals["package_json"])
                   or (Path(f) == Path("docker-compose.yml") and signals["docker_compose"])
                   for f in condition["files"])
    if ctype == "keyword_in_files":
        return any(kw in signals["keywords"] for kw in condition["keywords"])
    raise ValueError(f"condição desconhecida: {ctype}")


def load_stack_map(canonical: Path) -> dict:
    map_path = canonical / ".claude/skills/install-harness/scripts/stack_map.json"
    return json.loads(map_path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- plano

def paths_differ(a: Path, b: Path) -> bool:
    """True se a (existente) e b (canônico) têm conteúdo diferente. Compara árvore para dirs."""
    if a.is_dir() or b.is_dir():
        if not a.is_dir() or not b.is_dir():
            return True
        cmp = filecmp.dircmp(a, b)
        if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
            return True
        for sub in cmp.common_dirs:
            if paths_differ(a / sub, b / sub):
                return True
        return False
    try:
        return a.read_bytes() != b.read_bytes()
    except OSError:
        return True


def resolve_canonical_src(canonical: Path, item_or_artefact: dict) -> Path | None:
    """Resolve o path de origem no canônico.

    Artefatos `copy` podem declarar `from` quando o path de destino no
    projeto-filho difere do path no canônico (ex.: seed `.harness/data-check/` a partir
    de `config/canonical_data_check/templates/data-check`).
    """
    kind = item_or_artefact["kind"]
    if kind == "generate":
        return None
    src_rel = item_or_artefact.get("from") or item_or_artefact["path"]
    return canonical / src_rel


def build_plan(target: Path, canonical: Path, stack_map: dict, manifest: dict | None,
               signals: dict, force_categories: frozenset[str] = frozenset(),
               force_all: bool = False) -> list[dict]:
    artefacts = (manifest or {}).get("artefacts", {})
    plan: list[dict] = []

    for category in stack_map["categories"]:
        detected = condition_matches(category["condition"], signals)
        forced = not detected and (force_all or category["name"] in force_categories)
        matched = detected or forced
        for artefact in category["artifacts"]:
            rel = artefact["path"]
            kind = artefact["kind"]
            dest = target / rel
            src = resolve_canonical_src(canonical, artefact)
            item = {
                "path": rel,
                "kind": kind,
                "category": category["name"],
                "exists": dest.exists(),
            }
            if artefact.get("from"):
                item["from"] = artefact["from"]
            if artefact.get("seed"):
                item["seed"] = True
            if forced:
                item["forced"] = True

            if not matched:
                item["action"] = "SKIP_STACK"
                plan.append(item)
                continue

            tracked = artefacts.get(rel)

            if not dest.exists():
                item["action"] = "SCAFFOLD" if kind == "scaffold" else ("COPY" if kind == "copy" else "GENERATE")
                plan.append(item)
                continue

            if kind == "scaffold":
                item["action"] = "KEEP"
                item["note"] = "pasta já existe — nunca sobrescrita"
                plan.append(item)
                continue

            # Seed runtime (ex.: .harness/data-check): após o 1º install o filho é dono —
            # nunca AUTO_UPDATE (apagaria baseline/waivers).
            if artefact.get("seed"):
                item["action"] = "KEEP"
                item["note"] = "seed runtime — estado do filho preservado"
                plan.append(item)
                continue

            if tracked is None:
                item["action"] = "CONFLICT"
                plan.append(item)
                continue

            if tracked.get("customized"):
                item["action"] = "KEEP"
                item["note"] = "manifest: customized=true"
                plan.append(item)
                continue

            # customized:false — candidato a auto-update, só se conteúdo realmente mudou
            if kind == "copy" and src is not None and paths_differ(dest, src):
                item["action"] = "AUTO_UPDATE"
            else:
                item["action"] = "UP_TO_DATE"
            plan.append(item)

    return plan


# --------------------------------------------------------------------------- conflitos

def render_diff(dest: Path, src: Path) -> str:
    if dest.is_dir() or src.is_dir():
        if not dest.is_dir() or not src.is_dir():
            return "(um dos lados é arquivo, outro é diretório)"
        cmp = filecmp.dircmp(dest, src)
        lines = []
        if cmp.left_only:
            lines.append(f"  só no destino: {sorted(cmp.left_only)}")
        if cmp.right_only:
            lines.append(f"  só no canônico: {sorted(cmp.right_only)}")
        if cmp.diff_files:
            lines.append(f"  arquivos diferentes: {sorted(cmp.diff_files)}")
        return "\n".join(lines) or "(diretórios equivalentes)"
    try:
        dest_lines = dest.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
        src_lines = src.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
    except OSError as exc:
        return f"(não foi possível ler para diff: {exc})"
    diff = difflib.unified_diff(dest_lines, src_lines, fromfile="destino (atual)", tofile="canônico (novo)")
    return "".join(diff) or "(sem diferenças de texto)"


def resolve_conflicts_interactive(plan: list[dict], target: Path, canonical: Path) -> None:
    keep_all = False
    overwrite_all = False
    for item in plan:
        if item["action"] != "CONFLICT":
            continue
        if keep_all:
            item["resolution"] = "keep"
            continue
        if overwrite_all:
            item["resolution"] = "overwrite"
            continue

        dest = target / item["path"]
        src = resolve_canonical_src(canonical, item)
        while True:
            print(f"\n{item['path']} já existe e não está rastreado no manifest (ou difere do canônico).")
            choice = input(
                "[k]eep  [o]verwrite  [d]iff  [m]erge manual (salva canônico como .harness-incoming)  "
                "[K]eep all restantes  [O]verwrite all restantes  [q] cancelar > "
            ).strip()
            if choice == "k":
                item["resolution"] = "keep"
                break
            if choice == "o":
                item["resolution"] = "overwrite"
                break
            if choice == "m":
                item["resolution"] = "merge"
                break
            if choice == "d":
                if src is None:
                    print("(artefato generate — sem fonte canônica para diff)")
                else:
                    print(render_diff(dest, src))
                continue
            if choice == "K":
                item["resolution"] = "keep"
                keep_all = True
                break
            if choice == "O":
                item["resolution"] = "overwrite"
                overwrite_all = True
                break
            if choice == "q":
                print("Instalação cancelada.")
                sys.exit(1)
            print("Opção inválida.")


def resolve_conflicts_from_decisions(plan: list[dict], decisions: dict) -> None:
    for item in plan:
        if item["action"] != "CONFLICT":
            continue
        resolution = decisions.get(item["path"])
        if resolution not in ("keep", "overwrite", "merge"):
            raise ValueError(f"decisão ausente/inválida para conflito: {item['path']!r} -> {resolution!r}")
        item["resolution"] = resolution


# --------------------------------------------------------------------------- geração de stubs

def _load_agent_policies_artifacts(
    canonical: Path | None,
    target: Path | None = None,
) -> tuple[list[str], dict]:
    """Deny Claude + fragmento PreToolUse a partir de agent-policies.yaml (foundation)."""
    if canonical is None:
        return [], {}
    contract = canonical / "agent-policies.yaml"
    if not contract.is_file():
        raise FileNotFoundError(
            f"agent-policies.yaml ausente em {canonical} — foundation exige o contrato"
        )
    root = str(canonical.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    from config.agent_policies.generate import (  # noqa: PLC0415
        build_claude_pretooluse_hooks,
        generate_artifacts,
    )

    profile = None
    if target is not None:
        candidate = target / ".harness" / "policies" / "project_profile.yaml"
        if candidate.is_file():
            profile = candidate
    result = generate_artifacts(contract_path=contract, profile_path=profile)
    deny = list(result.claude_deny)
    if not deny:
        raise ValueError("generate agent-policies produziu deny vazio — não instalar deny: []")
    return deny, build_claude_pretooluse_hooks()


def _load_cursor_hooks(canonical: Path | None, target: Path | None = None) -> dict:
    if canonical is None:
        raise ValueError("canonical obrigatório para gerar .cursor/hooks.json")
    root = str(canonical.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    from config.agent_policies.generate import generate_artifacts  # noqa: PLC0415

    profile = None
    if target is not None:
        candidate = target / ".harness" / "policies" / "project_profile.yaml"
        if candidate.is_file():
            profile = candidate
    result = generate_artifacts(
        contract_path=canonical / "agent-policies.yaml",
        profile_path=profile,
    )
    return result.cursor_hooks


def generate_content(
    rel_path: str,
    project_name: str,
    stack_summary: str,
    canonical: Path | None = None,
    target: Path | None = None,
) -> str:
    today = date.today().isoformat()
    banner = anti_canonical_banner(project_name)
    if rel_path == "CLAUDE.md":
        return (
            f"{banner}\n"
            f"# {project_name}\n\n"
            f"> Gerado pelo install-harness em {today}. Stack detectada: {stack_summary or '(nenhuma detectada)'}.\n"
            "> Refine com `/grill-me` para registrar invariantes e decisões reais do projeto.\n\n"
            "## Stack\n\n"
            f"{stack_summary or '(preencher)'}\n\n"
            "## Invariantes\n\n"
            "(preencher com /grill-me)\n"
        )
    if rel_path == "AGENTS.md":
        return (
            f"{banner}\n"
            f"# {project_name} — espelho portátil (Cursor/Windsurf/Codex)\n\n"
            f"> Gerado pelo install-harness em {today}. Sem referências a `.claude/`.\n\n"
            "## Stack\n\n"
            f"{stack_summary or '(preencher)'}\n\n"
            "## Comandos\n\n(preencher)\n\n## Invariantes\n\n(preencher)\n"
        )
    if rel_path == "CONTEXT.md":
        return (
            f"{banner}\n"
            f"# Glossário de domínio — {project_name}\n\n"
            "> Iniciado pelo install-harness. Refinar com /grill-with-docs junto ao especialista de domínio.\n"
            "> Cada termo deve ter: definição precisa + sinônimos usados pelo time + o que NÃO é.\n\n"
            "---\n\n## Domínio\n\n(preencher com /grill-with-docs)\n\n"
            "## Termos do domínio\n\n| Termo | Definição | Sinônimos | O que NÃO é |\n|---|---|---|---|\n\n"
            "## Acrônimos e siglas\n\n| Sigla | Significado |\n|---|---|\n(nenhum informado)\n\n"
            "## Regras de negócio implícitas\n\n(preencher com /grill-with-docs)\n"
        )
    if rel_path == "README.md":
        return (
            f"{banner}\n"
            f"# {project_name}\n\n"
            "> Stub gerado pelo install-harness. "
            "Para um README completo a partir dos artefatos do projeto, use `/make-readme`.\n\n"
            "## Visão geral\n\n"
            "(preencher)\n"
        )
    if rel_path == "HANDOFF.md":
        return (
            f"# Handoff — {project_name}\n\n"
            f"> Gerado pelo install-harness em {today}. Atualize a cada handoff de sessão.\n\n"
            "## Estado atual\n\n(preencher)\n\n## Próximos passos\n\n(preencher)\n"
        )
    if rel_path == ".claude/settings.json":
        deny, pretool = _load_agent_policies_artifacts(canonical, target)
        hooks = build_hooks(stack_summary)
        for key, value in pretool.items():
            hooks.setdefault(key, [])
            if isinstance(value, list):
                hooks[key] = list(value) + list(hooks.get(key) or [])
        settings = {
            "env": {},
            "permissions": {"allow": [CONTEXT_DRIFT_PERMISSION], "deny": deny},
            "hooks": hooks,
        }
        return json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
    if rel_path == ".cursor/hooks.json":
        return (
            json.dumps(_load_cursor_hooks(canonical, target), indent=2, ensure_ascii=False)
            + "\n"
        )
    raise ValueError(f"sem template de geração para: {rel_path}")

def build_gate_hooks(stack_summary: str) -> dict:
    """Hooks de lint/type/test conforme a stack detectada. Vazio se nada foi detectado."""
    stack = stack_summary.lower()
    if "python" in stack or "fastapi" in stack:
        return {
            "PostToolUse": [{"matcher": "Edit|Write", "hooks": [
                {"type": "command", "command": "uv run ruff format . 2>/dev/null; uv run ruff check --fix . 2>/dev/null; true"}
            ]}],
            "Stop": [{"hooks": [
                {"type": "command", "command": "uv run ruff check . && uv run mypy . && uv run pytest -q || exit 2"}
            ]}],
        }
    if "react" in stack or "frontend" in stack:
        return {
            "PostToolUse": [{"matcher": "Edit|Write", "hooks": [
                {"type": "command", "command": "npx eslint --fix . 2>/dev/null; true"}
            ]}],
            "Stop": [{"hooks": [
                {"type": "command", "command": "npx eslint . && npx vitest run || exit 2"}
            ]}],
        }
    return {}


def build_hooks(stack_summary: str) -> dict:
    """Gate por stack + aviso de drift de contexto (sempre, mesmo sem stack detectada)."""
    hooks = build_gate_hooks(stack_summary)
    hooks.setdefault("Stop", []).append(
        {"hooks": [{"type": "command", "command": CONTEXT_DRIFT_HOOK_COMMAND}]}
    )
    return hooks


# --------------------------------------------------------------------------- aplicação

def mirror_to_cursor(target: Path, canonical: Path, rel_path: str) -> None:
    p = Path(rel_path)
    parts = p.parts
    if rel_path in ("CLAUDE.md", "AGENTS.md", "CONTEXT.md", "README.md", "HANDOFF.md", "docs/manuais/harness-guide.md"):
        return
    if rel_path == ".claude/settings.json":
        return
    if len(parts) < 2 or parts[0] != ".claude":
        return
    cursor_rel = Path(".cursor", *parts[1:])
    src_installed = target / rel_path

    if parts[1] == "rules" and p.suffix == ".md":
        mdc_path = target / ".cursor/rules" / (p.stem + ".mdc")
        mdc_path.parent.mkdir(parents=True, exist_ok=True)
        mdc_path.write_text(convert_rule_to_mdc(src_installed), encoding="utf-8")
        return

    if parts[1] in ("agents", "skills", "kb", "commands", "design", "projetos", "sdd", "dev"):
        cursor_dest = target / cursor_rel
        cursor_dest.parent.mkdir(parents=True, exist_ok=True)
        if src_installed.is_dir():
            if cursor_dest.exists():
                shutil.rmtree(cursor_dest)
            shutil.copytree(src_installed, cursor_dest)
        else:
            shutil.copy2(src_installed, cursor_dest)


def convert_rule_to_mdc(rule_path: Path) -> str:
    text = rule_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    description = rule_path.stem.replace("-", " ")
    globs: list[str] = []
    body_start = 0

    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            header = lines[1:end]
            in_paths = False
            for hline in header:
                stripped = hline.strip()
                if stripped.startswith("#"):
                    description = stripped.lstrip("#").strip()
                elif stripped == "paths:":
                    in_paths = True
                elif in_paths and stripped.startswith("-"):
                    globs.append(stripped.lstrip("-").strip().strip('"'))
                elif stripped and not stripped.startswith("-"):
                    in_paths = False
            body_start = end + 1

    body = "\n".join(lines[body_start:]).lstrip("\n")
    always_apply = "false" if globs else "true"
    globs_json = json.dumps(globs, ensure_ascii=False)
    return f"---\ndescription: {description}\nglobs: {globs_json}\nalwaysApply: {always_apply}\n---\n\n\n{body}\n"


def apply_plan(plan: list[dict], target: Path, canonical: Path, project_name: str, stack_summary: str,
               mode: str, manifest: dict | None) -> dict:
    artefacts = dict((manifest or {}).get("artefacts", {}))
    counts = {"copied": 0, "generated": 0, "scaffolded": 0, "auto_updated": 0,
              "kept": 0, "overwritten": 0, "merged_manual": 0, "skipped_stack": 0}

    for item in plan:
        rel = item["path"]
        dest = target / rel
        src = resolve_canonical_src(canonical, item)
        action = item.get("resolution") or item["action"]

        if action == "SKIP_STACK":
            counts["skipped_stack"] += 1
            continue

        if action == "UP_TO_DATE":
            continue

        if action == "KEEP":
            # Seed runtime: normaliza manifest legado (customized:false) e brownfield
            # sem entrada — o filho já é dono; re-installs futuros continuam protegidos.
            if item.get("seed"):
                artefacts[rel] = {
                    "source": "canonical",
                    "customized": True,
                    "seed": True,
                }
            counts["kept"] += 1
            continue

        if action == "SCAFFOLD":
            dest.mkdir(parents=True, exist_ok=True)
            if rel in (".claude/design", ".claude/sdd"):
                for sub in ("features", "archive", "reports"):
                    (dest / sub).mkdir(exist_ok=True)
            if rel in (".claude/projetos", ".claude/guias"):
                readme_src = canonical / rel / "README.md"
                if readme_src.exists():
                    shutil.copy2(readme_src, dest / "README.md")
            artefacts[rel] = {"source": "generated", "customized": True}
            mirror_to_cursor(target, canonical, rel)
            counts["scaffolded"] += 1
            continue

        if action == "COPY":
            if src is None or not src.exists():
                raise FileNotFoundError(
                    f"fonte canônica ausente para copy de {rel!r} "
                    f"(from={item.get('from')!r})"
                )
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                # docs/rascunhos = planos internos do canônico; não propagar aos filhos.
                ignore = shutil.ignore_patterns("rascunhos") if rel == "docs" else None
                shutil.copytree(src, dest, ignore=ignore)
            else:
                shutil.copy2(src, dest)
            # Seed runtime: o filho passa a ser dono (baseline/waivers) — nunca auto-update.
            artefacts[rel] = {
                "source": "canonical",
                "customized": bool(item.get("seed")),
            }
            if item.get("seed"):
                artefacts[rel]["seed"] = True
            mirror_to_cursor(target, canonical, rel)
            counts["copied"] += 1
            continue

        if action == "GENERATE":
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(
                generate_content(rel, project_name, stack_summary, canonical, target),
                encoding="utf-8",
            )
            artefacts[rel] = {"source": "generated", "customized": True}
            counts["generated"] += 1
            continue

        if action == "AUTO_UPDATE":
            if src is None or not src.exists():
                raise FileNotFoundError(
                    f"fonte canônica ausente para auto-update de {rel!r} "
                    f"(from={item.get('from')!r})"
                )
            if src.is_dir():
                shutil.rmtree(dest)
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)
            artefacts[rel] = {"source": "canonical", "customized": False}
            mirror_to_cursor(target, canonical, rel)
            counts["auto_updated"] += 1
            continue

        if action == "overwrite":
            if item["kind"] == "generate":
                dest.write_text(
                    generate_content(rel, project_name, stack_summary, canonical, target),
                    encoding="utf-8",
                )
            else:
                if src is None or not src.exists():
                    raise FileNotFoundError(
                        f"fonte canônica ausente para overwrite de {rel!r} "
                        f"(from={item.get('from')!r})"
                    )
                if src.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
            artefacts[rel] = {"source": "canonical" if item["kind"] == "copy" else "generated", "customized": False}
            mirror_to_cursor(target, canonical, rel)
            counts["overwritten"] += 1
            continue

        if action == "keep":
            artefacts[rel] = {"source": artefacts.get(rel, {}).get("source", "unknown"), "customized": True}
            counts["kept"] += 1
            continue

        if action == "merge":
            incoming = Path(str(dest) + ".harness-incoming")
            if incoming.exists():
                shutil.rmtree(incoming) if incoming.is_dir() else incoming.unlink()
            if item["kind"] == "generate":
                incoming.write_text(
                    generate_content(rel, project_name, stack_summary, canonical, target),
                    encoding="utf-8",
                )
            else:
                if src is None or not src.exists():
                    raise FileNotFoundError(
                        f"fonte canônica ausente para merge de {rel!r} "
                        f"(from={item.get('from')!r})"
                    )
                if src.is_dir():
                    shutil.copytree(src, incoming)
                else:
                    shutil.copy2(src, incoming)
            artefacts[rel] = {"source": artefacts.get(rel, {}).get("source", "unknown"), "customized": True}
            counts["merged_manual"] += 1
            continue

    write_manifest(target, canonical, mode, artefacts)
    return counts


def write_manifest(target: Path, canonical: Path, mode: str, artefacts: dict) -> None:
    manifest_path = target / MANIFEST_REL
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "canonical_path": str(canonical),
        "installed_at": date.today().isoformat(),
        "mode": mode,
        "artefacts": artefacts,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- apresentação

BUCKET_LABELS = {
    "COPY": "COPIAR do canônico",
    "GENERATE": "GERAR (projeto-específico)",
    "SCAFFOLD": "SCAFFOLD (pastas)",
    "AUTO_UPDATE": "ATUALIZAR (canônico evoluiu, customized=false)",
    "SKIP_STACK": "PULAR (stack não detectada)",
    "KEEP": "NÃO TOCAR (já existe ou customizado)",
    "UP_TO_DATE": "NÃO TOCAR (já atualizado)",
    "CONFLICT": "CONFLITOS — precisa decidir",
}


def print_plan_human(plan: list[dict], mode: str, signals: dict) -> None:
    print(f"\n# Install Plan\n\n## Modo: {mode}")
    kw = ", ".join(sorted(signals["keywords"])) or "(nenhuma)"
    print(f"## Stack detectada: keywords={kw} pyproject={signals['pyproject']} package.json={signals['package_json']}\n")
    for bucket, label in BUCKET_LABELS.items():
        items = [i for i in plan if i["action"] == bucket]
        if not items:
            continue
        print(f"## {label}")
        for i in items:
            note = f" ← {i['note']}" if i.get("note") else ""
            forced = " [forçado — sem stack detectada]" if i.get("forced") else ""
            print(f"- {i['path']}{note}{forced}")
        print()
    skipped_categories = sorted({i["category"] for i in plan if i["action"] == "SKIP_STACK"})
    if skipped_categories:
        print(f"Categorias puladas por falta de stack detectada: {', '.join(skipped_categories)}")
        print("Para incluir mesmo assim: --force-category NOME (repetível)\n")


def plan_to_json(plan: list[dict], mode: str, signals: dict) -> dict:
    return {
        "mode": mode,
        "stack_signals": {**{k: v for k, v in signals.items() if k != "keywords"}, "keywords": sorted(signals["keywords"])},
        "items": plan,
    }


def summarize(counts: dict) -> str:
    parts = [f"{v} {k}" for k, v in counts.items() if v]
    return ", ".join(parts) if parts else "nada a fazer"


def _githooks_bootstrap_cmd(target: Path) -> list[str] | None:
    """Comando de bootstrap dos githooks conforme o SO; None → fallback `git config`.

    Windows: `.ps1` via PowerShell (o `bash` do PATH costuma ser o stub do WSL, sem distro).
    POSIX: `.sh` via bash.
    """
    scripts = target / "scripts"
    if os.name == "nt":
        ps1 = scripts / "bootstrap-githooks.ps1"
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if ps1.is_file() and shell:
            return [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1), str(target)]
        return None
    sh = scripts / "bootstrap-githooks.sh"
    bash = shutil.which("bash")
    if sh.is_file() and bash:
        return [bash, str(sh), str(target)]
    return None


def _maybe_bootstrap_githooks(target: Path, *, interactive: bool) -> None:
    """Pede confirmação explícita antes de `git config core.hooksPath=.githooks`.

    Idempotente. Nunca roda no modo --json sem TTY (a skill Claude pergunta no Passo 3.5).
    """
    import subprocess

    hooks_dir = target / ".githooks"
    if not hooks_dir.is_dir():
        return
    if not (target / ".git").exists():
        print("[git-hygiene] destino sem .git — pule bootstrap de hooks.")
        return
    if not interactive:
        print(
            "[git-hygiene] hooks copiados. Bootstrap de core.hooksPath NÃO aplicado "
            "automaticamente neste modo — rode scripts/bootstrap-githooks.sh (POSIX) ou "
            "scripts\bootstrap-githooks.ps1 (Windows) após acordo."
        )
        return
    ans = input(
        "\n[git-hygiene] Configurar core.hooksPath=.githooks neste repo? "
        "(idempotente; contornável com --no-verify) [s/N] "
    ).strip().lower()
    if ans != "s":
        print("[git-hygiene] hooks NÃO bootstrapados — acordo negado ou pulado.")
        return
    cmd = _githooks_bootstrap_cmd(target)
    if cmd:
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            print(
                f"[git-hygiene] ERRO: bootstrap-githooks saiu com código {result.returncode}. "
                "Verifique permissões e se o destino é um repo git.",
                file=sys.stderr,
            )
    else:
        result = subprocess.run(
            ["git", "config", "core.hooksPath", ".githooks"],
            cwd=str(target),
            check=False,
        )
        if result.returncode != 0:
            print(
                f"[git-hygiene] ERRO: git config core.hooksPath falhou (código {result.returncode}).",
                file=sys.stderr,
            )
        else:
            print(f"[git-hygiene] core.hooksPath=.githooks em {target}")


# --------------------------------------------------------------------------- main

def main() -> None:
    # Consoles Windows (cp1252) quebram em caracteres fora do codec; nunca derrubar o instalador por isso.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("destino", nargs="?", help="pasta alvo onde instalar/atualizar o harness")
    parser.add_argument("--canonical", default=DEFAULT_CANONICAL, help="path do canônico (default: %(default)s)")
    parser.add_argument("--dry-run", action="store_true", help="só mostra o plano, não escreve nada")
    parser.add_argument("--yes", action="store_true", help="modo não-interativo: mantém tudo que já existe (nunca sobrescreve)")
    parser.add_argument("--json", action="store_true", help="imprime o plano em JSON; usa --decisions-file para aplicar")
    parser.add_argument("--decisions-file", help="JSON {path: keep|overwrite|merge} para resolver conflitos sem prompt")
    parser.add_argument("--force-category", action="append", default=[], metavar="NOME",
                         help="inclui a categoria mesmo sem stack detectada (repetível, ex.: "
                              "--force-category langgraph --force-category rag_vetorial)")
    parser.add_argument("--force-all", action="store_true",
                         help="inclui TODAS as categorias mesmo sem stack detectada (sobrepõe --force-category)")
    args = parser.parse_args()

    canonical = Path(args.canonical).resolve()
    if not (canonical / ".claude/agents").exists():
        print(f"CANÔNICO NÃO ENCONTRADO em {canonical}", file=sys.stderr)
        sys.exit(1)

    destino = args.destino
    if destino is None:
        if args.json:
            print("--json requer <destino> explícito", file=sys.stderr)
            sys.exit(1)
        destino = input(f"Em qual pasta devo instalar/atualizar o harness? (Enter para {Path.cwd()}) ").strip() or str(Path.cwd())

    target = Path(destino).resolve()
    if not target.exists():
        if args.yes or args.json or input(f"{target} não existe. Criar? [S/n] ").strip().lower() != "n":
            target.mkdir(parents=True)
        else:
            print("Cancelado.")
            sys.exit(1)

    manifest = read_manifest(target)
    mode = detect_mode(target, manifest)
    stack_map = load_stack_map(canonical)
    keywords = collect_keywords(stack_map)
    signals = detect_stack_signals(target, keywords)
    force_categories = frozenset(args.force_category)
    plan = build_plan(target, canonical, stack_map, manifest, signals, force_categories, args.force_all)

    if args.json:
        print(json.dumps(plan_to_json(plan, mode, signals), indent=2, ensure_ascii=False))
        if args.dry_run or not args.decisions_file:
            return
        decisions = json.loads(Path(args.decisions_file).read_text(encoding="utf-8"))
        resolve_conflicts_from_decisions(plan, decisions)
        project_name = target.name
        stack_summary = ", ".join(sorted(signals["keywords"])) or "(genérica)"
        counts = apply_plan(plan, target, canonical, project_name, stack_summary, mode, manifest)
        print(json.dumps({"applied": counts}, indent=2, ensure_ascii=False))
        return

    print_plan_human(plan, mode, signals)
    if args.dry_run:
        return

    if args.yes:
        for item in plan:
            if item["action"] == "CONFLICT":
                item["resolution"] = "keep"
    else:
        resolve_conflicts_interactive(plan, target, canonical)
        n_actionable = sum(1 for i in plan if i["action"] not in ("SKIP_STACK", "KEEP", "UP_TO_DATE"))
        if n_actionable == 0:
            print("Nada a fazer — harness já está atualizado.")
            return
        confirm = input(f"\n{n_actionable} artefatos serão tocados. Confirma? [s/N] ").strip().lower()
        if confirm != "s":
            print("Cancelado — nada foi escrito.")
            return

    project_name = target.name
    stack_summary = ", ".join(sorted(signals["keywords"])) or "(genérica)"
    counts = apply_plan(plan, target, canonical, project_name, stack_summary, mode, manifest)
    print(f"\nFeito: {summarize(counts)}.")
    _maybe_bootstrap_githooks(target, interactive=not args.yes and not args.json)
    print("\nPróximos passos:")
    print("  0. CONTEXT_REBIND — confirmar que CLAUDE/AGENTS/CONTEXT/README falam do filho")
    print("     (não do canônico). Soft-block até /grill-with-docs, /grill-me ou harness-architect.")
    print("  1. /grill-with-docs — preencher CONTEXT.md com terminologia real do domínio")
    print("  2. /grill-me — refinar CLAUDE.md (inclua scm: azure | github e, se usar nuvem, cloud:)")
    print("  3. Revisar hooks em .claude/settings.json")
    print("  4. Bootstrap de githooks — só após acordo (Passo 3.5 / pergunta acima)")
    print("  5. /validar — confirmar gate verde antes da primeira sessão de build")
    print("  6. Espelhar edições de contexto .claude <-> .cursor quando dual-tree")
    if (target / ".githooks").is_dir():
        cur = ""
        try:
            import subprocess as _sp

            cur = _sp.check_output(
                ["git", "config", "--get", "core.hooksPath"],
                cwd=str(target),
                text=True,
            ).strip()
        except Exception:
            cur = "(unset)"
        if cur != ".githooks":
            print(
                "  → hooks ainda inativos: scripts/bootstrap-githooks.sh ou .ps1 no Windows (após acordo)"
            )


if __name__ == "__main__":
    main()
