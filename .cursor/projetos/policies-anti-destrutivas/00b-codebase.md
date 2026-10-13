# Policies Anti-Destrutivas — mapeamento de codebase (00b)

Fonte: codebase-explorer em 2026-08-12 · branch `feat/policies-anti-destrutivas` @ a226042  
Escopo: gates anti-destrutivos existentes no canônico (settings, hooks, SI, DE, githooks, install).

## Executive Summary

- **Runtime Claude (dogfood):** `.claude/settings.json` tem `permissions.deny` com 11 padrões Bash (`rm -rf`, `docker compose down -v/--volumes`, `docker volume rm/prune`, `dropdb`, `mysqladmin drop`, `databricks … delete`, `git push --force`, `git reset --hard`). Não há tier `ask`. Não há equivalente `.cursor/settings.json`.
- **Hooks Claude:** só `PostToolUse` (ruff) e `Stop` (ruff+mypy+pytest + drift). **Não há `PreToolUse`** no settings canônico — o template do `harness-architect` documenta PreToolUse, mas não está instalado.
- **Rule SI:** `.claude/rules/seguranca.md` ↔ `.cursor/rules/seguranca.mdc` (corpo idêntico; Cursor `alwaysApply: true`) — “pare e pergunte” + prod somente-leitura (soft, via prompt).
- **Kernel DE:** `DE-A002` em `data-engineering.yaml` + `package_a.py` (DROP/TRUNCATE/DELETE FROM sem marcador de gate → blocker). Escopo = código versionado DE, não Bash de sessão.
- **Githooks:** `.githooks/` = segredos (bloqueante) + avisos commit/push — **não** barram `rm -rf`/DDL. Honesty §1.3: sem Edit policies, nenhum gate impede de fato.
- **Lacuna de propagação:** `install_harness.py` gera filhos com `"deny": []` e **não espelha** `settings.json` para `.cursor/`. Os denies dogfood do canônico **não** vão automaticamente aos filhos.
- **Testes:** há cobertura de `DE-A002`; **nenhum** teste de `permissions.deny` / PreToolUse em `tests/`.

## Deep Dive

### Entry points / superfície

| Entry | Path | Papel |
|---|---|---|
| Install CLI | `./install-harness` → `install_harness.py` | Propaga foundation + settings gerados |
| DE CLI | `python -m config.canonical_data_check` | validate/baseline/compare/report/explain |
| Settings runtime | `.claude/settings.json` | permissions + hooks Claude Code |
| Norma DE | `data-engineering.yaml` | Inclui destrutivo (`DE-A002`) |
| Contrato git | `git-hygiene.yaml` + `.githooks/` | hygiene local, não anti-shell |

### Settings & permissions

Arquivo único: `.claude/settings.json` (**não** existe `.cursor/settings.json`).

Deny atual (11 padrões Bash). Allow amplo inclui `Bash(docker compose:*)` — deny só cobre variantes com volumes; `docker compose down` sem `-v` não está na deny list. Tier `ask` ausente no canônico.

Install (filho) gera:

```text
permissions: { allow: [...], deny: [] }
```

→ deny vazio; dogfood do canônico não é copiado.

### Hooks

| Onde | O que existe |
|---|---|
| `.claude/settings.json` → `hooks` | PostToolUse (Edit\|Write → ruff) + Stop (gate + check_context_drift) |
| `.claude/hooks/` / `.cursor/hooks/` | **não existe** |
| `.cursor/hooks.json` | **não existe** |
| Template architect | Exemplifica PreToolUse + SessionStart + ask/deny |
| Install `build_hooks()` | Só PostToolUse/Stop por stack — sem PreToolUse anti-destrutivo |

### Rules SI

- `.claude/rules/seguranca.md` / `.cursor/rules/seguranca.mdc` — corpos alinhados
- Propagação: `stack_map.json` categoria `code_quality` (copy + mirror `.mdc`)
- Enforcement = orientação ao agente + revisor SI — **não** deny mecânico no Cursor

### DE destructive (`DE-A002`)

- Norma: production-safety, blocker, universal — DELETE/DROP/TRUNCATE exigem gate + ADR
- Check: regex em `package_a.py`; passa com marcadores `DESTRUCTIVE_GATE` / `destructive-gate` / `APPROVED_DESTRUCTIVE` / `docs/adr/`
- Escopo: projetos DE via `/validar` — não intercepta Bash do agente

### Githooks vs Edit policies (§1.3)

| Camada | Artefato | Bloqueia shell/DB destrutivo? |
|---|---|---|
| Agent runtime (Claude) | `settings.json` deny | Parcialmente (lista), só Claude Code |
| Soft policy | rules `seguranca` / `git-hygiene` | Soft-block / “pergunte” |
| Git local | `.githooks/pre-commit` | Só segredos no staged diff |
| Git local | commit-msg / pre-push | Avisos, não bloqueiam |
| Server / Edit policies | Fora do MVP | Explicitamente não implementado |

Honesty: `CONTEXT.md`, `git-hygiene`, cheatsheet §1.3 — `--no-verify` e clone sem hooks contornam.

### Install propagation

| Artefato | Comportamento |
|---|---|
| `.claude/settings.json` | `kind: generate` → allow mínimo + **deny []** + hooks de stack |
| `seguranca.md` | copy + mirror `.mdc` |
| `.githooks/` | copy (git_hygiene); hooksPath só após confirmação |
| Deny dogfood canônico | **Não** está no gerador |
| Mirror settings → Cursor | `mirror_to_cursor` **retorna cedo** para settings.json |

### Espelho `.claude/` ↔ `.cursor/`

Invariante CLAUDE.md espelha agents/skills/rules/kb/commands/guias — **settings/hooks fora** dessa lista.

| Item | Claude | Cursor | Gap |
|---|---|---|---|
| settings.json | existe | ausente | deny/hooks não aplicam no Cursor por arquivo de projeto |
| Pre/Post/Stop | no settings Claude | sem equivalente versionado | — |
| seguranca / git-hygiene | .md | .mdc | alinhado |

### Convenções de teste

- DE: `tests/data_engineering/test_validate_cli.py` — DE-A002
- Settings deny / PreToolUse: **nenhum** teste
- Cobertura anti-destrutivo runtime = baixa (só DE-A002 no código)

### Dívidas observadas (para o grill)

1. Install propaga SI em prose + deny vazio — filhos nascem sem deny dogfood
2. Sem PreToolUse guard — depende do runtime honorar `permissions.deny`
3. Cursor sem settings/hooks versionados para o mesmo perímetro
4. Allow `docker compose:*` + deny parcial de volumes — superfície incompleta
5. Settings canônico pode conter paths de máquina em allow/additionalDirectories (dogfood)
6. §1.3 permanece válido: githooks e soft-blocks ≠ Edit policies
