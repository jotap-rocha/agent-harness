# Cheatsheet + rule + /git-ajuda

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/01-contrato-regex-testes.md

## What to build

Publicar o contrato de uma página para o time (cheatsheet com declaração §1.3),
o comando `/git-ajuda` que devolve o mesmo conteúdo, e a rule transversal
`git-hygiene` (agnóstica de SCM) espelhada em `.cursor/rules/*.mdc`. A rule
declara invariantes (branch isolada, título convencional, sem segredo no diff,
commit/push/stash/descartar só com acordo) e aponta para `git-hygiene.yaml` —
sem cravar Azure DevOps.

## Acceptance criteria

- [x] `docs/git-hygiene-cheatsheet.md` existe e inclui a declaração §1.3 (nenhum gate impede de fato sem Edit policies) — tested by: no test — verificação de arquivo + grep pela declaração
- [x] Comando `/git-ajuda` existe em `.claude/commands/` e espelho `.cursor/`, apontando para o cheatsheet — tested by: no test — arquivos espelhados presentes
- [x] Rule `.claude/rules/git-hygiene.md` + `.cursor/rules/git-hygiene.mdc` com `alwaysApply` (ou equivalente) e referência à fonte YAML — tested by: no test — paridade de arquivos + frontmatter
- [x] Rule exige acordo explícito para commit, push, stash e descartar — tested by: no test — checklist de conteúdo da rule (A15 na camada de invariante)

## Notes

- Critérios A13, A1 (parte rule), A15 (invariantes).
- Mensagens do cheatsheet usam os mesmos tipos/padrões da task 01 (`feat|fix|chore`).
- Espelho `.claude` ↔ `.cursor` nesta mesma sessão.
- **No test:** critérios são artefatos docs/commands/rules — verificação por presença + grep; justificado nos próprios critérios.
- Gate: N/A de pytest (sem lógica Python). Checklist de conteúdo ok.
- Revisor: **aprovado com ressalvas** (0 bloqueantes). Ressalvas: forward-ref a `/nova-branch` (task 05); contagens CLAUDE/AGENTS ficam para sync-context.
