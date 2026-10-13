# Install categoria vault

**Status:** done  
**Blocked by:** tasks/keyvault-oci-azure-choice/36-skill-cloud-secrets.md, tasks/keyvault-oci-azure-choice/37-kbs-oci-azure-vault.md

## What to build

Estender `stack_map.json` com **categoria nova** condicionada a flag “usa vault” /
`secret_store` (não acoplar sempre a `pipeline_dados`). Quando a condição for verdadeira,
propagar skill `cloud-secrets` + KBs `oci-vault` + `azure-keyvault`. Examples continuam
fora do install.

## Acceptance criteria

- [x] Categoria nova no `stack_map` com condition vault (não always / não só pipeline_dados) — tested by: pytest/parse stack_map ou dry-run install
- [x] Com flag vault: skill + duas KBs entram no plan — tested by: teste install/stack_map positivo
- [x] Sem flag vault: skill/KBs vault **não** entram — tested by: teste negativo
- [x] Examples keyvault-* **não** listados no stack_map — tested by: assert ausência
- [x] Espelho skill install-harness (`.claude`↔`.cursor`) se tocado — no test — checklist

## Notes

Seed `.harness/data-check` permanece KEEP; SCHEMA já documenta `secret_store` via task 33.
Categoria `cloud_secrets`: keywords `secret_store|keyvault|azure-keyvault|oci-vault`;
marker injeta `secret_store` em `detect_stack_signals`.
Testes: `tests/data_engineering/test_install_cloud_secrets.py`.
Commit pendente de acordo explícito.
