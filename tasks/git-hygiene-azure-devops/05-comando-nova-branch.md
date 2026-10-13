# Comando /nova-branch

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/01-contrato-regex-testes.md, tasks/git-hygiene-azure-devops/02-cheatsheet-rule-ajuda.md

## What to build

Comando `/nova-branch` que consolida: fetch → detectar tronco (default do
remote, fallback `master`) → sync `--ff-only` → checar working tree → propor
`tipo/escopo` alinhado à intenção (inferido do contexto quando houver) →
aguardar acordo explícito → criar branch → imprimir título de PR sugerido.
Soft-block didático em tronco desatualizado, divergência, nome inválido,
branch já existente ou working tree suja (stash/commit/descartar só com acordo).

## Acceptance criteria

- [x] Comando existe em `.claude/commands/nova-branch.md` + espelho `.cursor/` — tested by: no test — arquivos espelhados
- [x] Fluxo documentado inclui fetch, sync `--ff-only`, acordo antes de criar, e soft-block se tronco atrás/divergente — tested by: no test — checklist do command (demo manual valida A2)
- [x] Validação de nome consome `git-hygiene.yaml` (rejeita inválidos da task 01) — tested by: referência explícita no command + reuso das fixtures A3
- [x] Ao final, sugere título de PR no padrão `tipo(escopo): resumo` — tested by: no test — checklist do command
- [x] Working tree suja e branch já existente têm soft-block com opções (nunca destrutivo sem acordo) — tested by: no test — checklist do command

## Notes

- Critérios A2, A3 (uso), parte de A15 no fluxo de branch.
- Agente conduz o fluxo, mas sempre com “de acordo” do usuário antes de `git switch -c`.
- Não implementa abertura de PR (task 06).
- **No test:** artefato de command (docs) — verificação por espelho + checklist/smoke do fluxo; validação de nome reusa fixtures A3 via `GitHygieneContract` + `branches_invalid.txt` (sem lógica Python nova).
- WT checada **antes** do sync/switch (correção do revisor).
- Revisor: 1ª **bloqueado** (Notes sem No test); após fix → fechar com ressalvas menores (README catálogo → sync-context/task 08).
