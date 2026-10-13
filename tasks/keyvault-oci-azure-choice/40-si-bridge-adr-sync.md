# SI bridge ADR sync docs

**Status:** done  
**Blocked by:** tasks/keyvault-oci-azure-choice/33-kernel-pacote-e-marker.md, tasks/keyvault-oci-azure-choice/34-validar-dispara-e.md, tasks/keyvault-oci-azure-choice/35-scaffold-examples-min.md, tasks/keyvault-oci-azure-choice/36-skill-cloud-secrets.md, tasks/keyvault-oci-azure-choice/37-kbs-oci-azure-vault.md, tasks/keyvault-oci-azure-choice/38-grill-pergunta-vault.md, tasks/keyvault-oci-azure-choice/39-install-categoria-vault.md

## What to build

Fechar o ship: ponte curta em `rules/seguranca` (nunca logar secret / placeholders),
ADR do pacote E + dual-cloud, remediações `DE-E*` na skill `de-conformidade`, atualizar
contagens/`CLAUDE.md`/`AGENTS.md`, espelho final `.claude`↔`.cursor`, e DoD do projeto
(STATUS + freeze mínimo se necessário).

## Acceptance criteria

- [x] Ponte SI em `seguranca` (+ `.mdc`) — no test — diff rule; review SI
- [x] ADR registrado em `docs/adr/` cobrindo pacote E + skill dual + install vault — no test — arquivo ADR + índice
- [x] `de-conformidade` mapeia `DE-E*` → remediação — tested by: pytest `test_task40_si_bridge_adr_sync` + review skill/YAML
- [x] `CLAUDE.md` / `AGENTS.md` refletem skills/KBs/pacote E — no test — sync-context / review tabela
- [x] Espelho completo dos artefatos deste ship — no test — checklist simétrica
- [x] STATUS do projeto: item 5 pronto para ship (ou freeze DoD se o fluxo pedir) — no test — STATUS.md

## Notes

Não reabrir decisões do grill. Gate `/validar` verde no canônico antes de marcar done.
Commit só com acordo explícito do usuário.
ADR: `docs/adr/002-pacote-e-keyvault-cloud-dual-install.md`.
Self-review harness-build: sem bloqueantes SI; delivery record só após commit.
