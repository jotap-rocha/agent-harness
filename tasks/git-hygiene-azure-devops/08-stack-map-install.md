# stack_map + install-harness

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/02-cheatsheet-rule-ajuda.md, tasks/git-hygiene-azure-devops/03-template-pr-azure.md, tasks/git-hygiene-azure-devops/04-githooks-bootstrap.md, tasks/git-hygiene-azure-devops/05-comando-nova-branch.md, tasks/git-hygiene-azure-devops/06-adapter-pr-hibrido.md, tasks/git-hygiene-azure-devops/07-wiring-git-preflight.md

## What to build

Corrigir a propagação: incluir agents `harness-*` e os artefatos git-hygiene
(rule, commands, yaml, hooks, template Azure, cheatsheet) no `stack_map.json`.
Estender `/install-harness` para, no Install Plan, pedir confirmação explícita
antes de bootstrap de `core.hooksPath=.githooks`. Verificar paridade
`.claude` ↔ `.cursor` dos artefatos desta evolução e dry-run/checklist de que o
mapa cobre o necessário. Documentar `scm` no template CLAUDE.md filho quando
aplicável.

## Acceptance criteria

- [x] `stack_map.json` (`.claude` + `.cursor`) lista agents `harness-*` que antes faltavam — tested by: grep/diff do mapa + dry-run/checklist do install (A11)
- [x] Artefatos git-hygiene (rule, commands, hooks, template, yaml/cheatsheet conforme mapa) entram no plano de install — tested by: entradas no `stack_map` / plano gerado
- [x] Install Plan inclui passo confirmável de bootstrap de hooks (idempotente) — tested by: no test — checklist SKILL/script (A5 via install)
- [x] Paridade `.claude` ↔ `.cursor` dos artefatos tocados nesta Fase 1 verificada — tested by: script ou checklist de paridade (A12)
- [x] Dogfood: evidência de `core.hooksPath=.githooks` no canônico permanece válida após a propagação documentada — tested by: `git config core.hooksPath` (A14)
- [x] Template/docs mínimos mencionam adapter `scm: azure | github` — tested by: no test — grep em template CLAUDE/HARNESS-GUIDE

## Notes

- Critérios A11, A12, fechamento A14/A5 via install.
- Não copiar YAML de pipeline por filho neste MVP.
- Categoria nova `git_hygiene` (always) no `stack_map.json`.
- Passo 3.5 no SKILL + `_maybe_bootstrap_githooks` no CLI interativo.
- **No test (parcial):** bootstrap confirmável e docs scm — checklist; dry-run do plan cobre A11.
- Gate: 45 pytest + py_compile install_harness.py; paridade OK; hooksPath=.githooks.
- Revisor: **aprovado com ressalvas** (0 bloqueantes). Ressalvas: prosa SKILL always-cats; returncode bootstrap; sync CLAUDE no ship.
