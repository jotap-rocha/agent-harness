# Template PR Azure

**Status:** done  
**Blocked by:** none

## What to build

Versionar o template de Pull Request do Azure Repos no canônico, com checklist
mínimo (branch no padrão, título convencional, sem segredo, gate local verde).
O arquivo deve ser propagável depois via install (entrada no stack_map fica na
task 08); nesta task basta existir e estar pronto para dogfood.

## Acceptance criteria

- [x] Existe `.azuredevops/pull_request_template.md` no canônico — tested by: no test — arquivo presente
- [x] Template contém seções “O que muda”, “Como testei” e checklist alinhado ao contrato (branch, título, segredos, gate) — tested by: no test — checklist de conteúdo
- [x] Nenhuma credencial/PAT de exemplo real no template — tested by: no test — revisão SI (nível b)

## Notes

- Critério A4.
- Funciona sem permissão `Edit policies` — apenas arquivo versionado.
- Texto do checklist consistente com o contrato (feat|fix|chore).
- **No test:** artefato de documentação/template — verificação por presença + checklist de conteúdo.
- Revisor: **aprovado** (0 bloqueantes, 0 ressalvas materiais).
