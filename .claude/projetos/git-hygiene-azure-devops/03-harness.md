# Git Hygiene Azure DevOps — Plano de implementação no canônico

Slug: `git-hygiene-azure-devops`  
Data: 2026-08-06  
Tipo: **e** — evolução do framework (não app-filho)

> **Adaptação do passo harness-architect:** este projeto **não** monta `.claude/` de
> produto. Em vez de `/harness-architect` de app, este documento é o plano de artefatos
> a criar/alterar no **próprio canônico**, propagáveis via `/install-harness`.
>
> Adversarial judge sobre o PRD: **pulado** (usuário, opção b, 2026-08-06).

## O que NÃO foi feito

- Não foi gerado harness de app-filho.
- Não foram criados agents/skills/KBs de domínio de produto.
- Não há `settings.json` de app novo.

## O que será gerado no canônico (Fase 1)

### Rules

| Artefato | Propósito |
|---|---|
| `.claude/rules/git-hygiene.md` (+ `.cursor/rules/git-hygiene.mdc`) | Invariantes agnósticos de SCM: branch isolada, título convencional, sem segredo no diff, acordo explícito em commit/push/stash |
| (existente) `seguranca` | Mantém PAT/secrets via env; SI nível b |

### Commands

| Artefato | Propósito |
|---|---|
| `/nova-branch` | fetch → sync tronco `--ff-only` → acordo → cria `tipo/escopo` → sugere título PR |
| `/git-ajuda` | Atalho para o contrato + cheatsheet |

### Hooks e bootstrap

| Artefato | Propósito |
|---|---|
| `.githooks/pre-commit` | Heurística de segredos — bloqueante |
| `.githooks/commit-msg` | Aviso Conventional Commits |
| `.githooks/pre-push` | Aviso em push no tronco |
| Bootstrap no install | `core.hooksPath=.githooks` após confirmação no Install Plan |

### Config / templates / docs

| Artefato | Propósito |
|---|---|
| `git-hygiene.yaml` | Fonte única de regex (branch + título) |
| `.azuredevops/pull_request_template.md` | Template versionado (sem permissão ADO) |
| `docs/git-hygiene-cheatsheet.md` | Contrato de 1 página + declaração §1.3 |
| Fixtures/testes de regex | Validação A1/A3 |

### Wiring (agents / Dev Loop)

| Alvo | Mudança |
|---|---|
| `harness-brainstorm` … `harness-ship` | Soft-block `GIT_PREFLIGHT` |
| `harness-ship` | Título PR sugerido; checklist squash (tag `prod-*` = Fase 2) |
| `dev-loop-executor` / `prompt-crafter` / `/dev` | Preflight + seção Git |
| `revisor-codigo` | Aviso não-bloqueante se diff no tronco |

### Propagação (`install-harness`)

| Alvo | Mudança |
|---|---|
| `stack_map.json` | Incluir agents `harness-*` (lacuna atual) + artefatos git-hygiene |
| SKILL / scripts install | Passo confirmável de hooks + cópia dos artefatos |
| Template CLAUDE.md filho | Campo `scm: azure \| github` |

### Skills / KBs

- **Nenhuma skill nova de produto** neste MVP.
- Opcional futuro: skill auxiliar de validação regex — só se `/to-tasks` justificar; não bloqueia A1–A15.

## Decisões contestáveis (ver ADR na implementação se necessário)

- Rule agnóstica + adapter `scm` (não cravar Azure).
- Soft-block no preflight dos agents.
- Heurística de segredos agora → `gitleaks` depois.
- `pre-push` aviso no MVP.
- Prefixo `Merged PR NNN:` aberto (plano §5.3).

## Declaração §1.3 (obrigatória no cheatsheet)

Nenhum gate impede de fato sem `Edit policies`. Caminho certo fácil; errado visível.

## Critérios de aceite

A1–A15 em `.claude/projetos/git-hygiene-azure-devops/02-prd.md` (e `01-grill.md`).

## Ordem de implementação

Ver seção homônima no `02-prd.md` (yaml → cheatsheet → rule → template → hooks → nova-branch → adapter → wiring → stack_map → paridade).

## Próximo passo

1. Rodar **`/to-tasks`** (offline) fatiando A1–A15 na ordem do PRD — ou `/to-issues` se houver tracker.
2. Depois dizer **`harness-build`** para implementar no canônico (com espelho `.claude` ↔ `.cursor`).
3. Dogfood: bootstrap hooks neste workspace antes de propagar.
