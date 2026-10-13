# Wiring GIT_PREFLIGHT nos agents

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/02-cheatsheet-rule-ajuda.md, tasks/git-hygiene-azure-devops/05-comando-nova-branch.md

## What to build

Wirear soft-block `GIT_PREFLIGHT` em todos os agents `harness-*` e no Dev Loop
(`prompt-crafter`, `dev-loop-executor`, `/dev`): fetch, tronco, sync, working
tree, branch isolada — só seguir após acordo e branch ok (oferecer
`/nova-branch`). `revisor-codigo` apenas avisa (não bloqueia) se o diff foi
produzido no tronco. Garantir na prosa dos agents que commit/push/stash/descartar
exigem acordo explícito.

## Acceptance criteria

- [x] `harness-brainstorm`, `define`, `design`, `build`, `iterate`, `ship` documentam `GIT_PREFLIGHT` soft-block antes de editar — tested by: no test — checklist de diff nos 6 agents (A8)
- [x] `dev-loop-executor` / `prompt-crafter` / `/dev` incluem preflight (step 0 ou seção `## Git`) — tested by: no test — checklist de diff (A8)
- [x] `revisor-codigo` sinaliza ressalva não-bloqueante se HEAD/diff no tronco — tested by: no test — checklist de diff (A8)
- [x] Agents de build/ship/dev-loop exigem acordo explícito para commit e push — tested by: no test — checklist de conteúdo (A15)
- [x] Espelho `.claude` ↔ `.cursor` dos agents/commands alterados na mesma sessão — tested by: no test — paridade de paths

## Notes

- Critérios A8, A15.
- Não criar tag `prod-*` (fora do MVP).
- `harness-ship` sugere título de PR convencional + fluxo híbrido (task 06) — alinhado, sem lógica conflitante.
- **No test:** wiring de prosa em agents/commands — verificação por checklist de presença `GIT_PREFLIGHT` + paridade de espelho (script na sessão).
