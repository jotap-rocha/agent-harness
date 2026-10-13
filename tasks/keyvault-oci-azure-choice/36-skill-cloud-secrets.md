# Skill cloud-secrets dual

**Status:** done  
**Blocked by:** none

## What to build

Criar a skill dual `cloud-secrets` (OCI + Azure) com playbook de wiring, auth, SI e
ponte JIT para as KBs. Espelhar em `.cursor/skills/cloud-secrets/`. Sem agent dedicado.

## Acceptance criteria

- [x] Skill em `.claude/skills/cloud-secrets/` com `description:` clara — no test — filesystem + review description
- [x] Espelho idêntico em `.cursor/skills/cloud-secrets/` — no test — checklist simétrica
- [x] Playbook cobre facade + map IDs/URIs + auth dual (OCI e Azure) + nunca logar secret — no test — review conteúdo vs PRD FR2
- [x] Skill aponta para KBs `oci-vault` e `azure-keyvault` (mesmo que KBs venham em task paralela) — no test — links/paths no SKILL.md

## Notes

Pode avançar em paralelo com task 33. Não criar agent.
Cobertura leve: `tests/data_engineering/test_cloud_secrets_catalog.py`.
Commit pendente de acordo explícito.
