# Githooks + bootstrap dogfood

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/01-contrato-regex-testes.md

## What to build

Entregar pasta versionada `.githooks/` com `pre-commit` (heurística leve de
segredos, bloqueante), `commit-msg` (aviso Conventional Commits, não bloqueante)
e `pre-push` (aviso se push no tronco, não bloqueante no MVP). Incluir helper de
bootstrap que configura `core.hooksPath=.githooks` de forma idempotente e
aplicar dogfood no workspace canônico após confirmação explícita do mantenedor
nesta sessão de implementação (não silencioso).

## Acceptance criteria

- [x] `.githooks/pre-commit`, `commit-msg` e `pre-push` existem e são executáveis — tested by: no test — permissões + presença
- [x] Commit com segredo sintético (ex.: prefixo AKIA, bloco PEM de chave privada, assignment password) é bloqueado (exit ≠ 0) com mensagem didática — tested by: teste de hook com fixture
- [x] `pre-push` com push simulado/alvo no tronco emite aviso e exit 0 — tested by: teste/demo de hook
- [x] `commit-msg` fora do Conventional Commits emite aviso e não bloqueia — tested by: teste/demo de hook
- [x] Após bootstrap acordado, `git config core.hooksPath` no canônico é `.githooks` — tested by: comando `git config core.hooksPath` (A5/A14)
- [x] Mensagens de erro ensinam o que fazer (exemplo colável + por quê) — tested by: no test — revisão das strings

## Notes

- Critérios A5–A7, A14 (bootstrap local).
- Caminho para plugar `gitleaks` documentado em `.githooks/README.md`, sem implementar.
- Integração no Install Plan (confirmação) fica na task 08; aqui é dogfood local.
- Nunca logar o segredo detectado em claro além do necessário para localizar o arquivo/linha.
- Dogfood acordado na sessão (“seguir com todas as tasks”) → `./scripts/bootstrap-githooks.sh` → `core.hooksPath=.githooks`.
- Gate: `PYTHONPATH=. python3 -m pytest tests/githooks/` — 9 passed (1 tentativa pós-correção revisor).
- Revisor: 1ª passagem **bloqueado** (grep PEM, labels auto-bloqueio, literal AKIA nos testes, hooksPath unset). 2ª passagem **aprovado com ressalvas** (0 bloqueantes). Ressalvas: assert quiet pre-push feature; vazamento stderr só AWS.
