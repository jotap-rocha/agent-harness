# KBs oci-vault e azure-keyvault

**Status:** done  
**Blocked by:** none

## What to build

Criar KBs JIT `oci-vault` e `azure-keyvault` (index + quick-reference + concepts/patterns
mínimos) com paridade conceitual. Lift de padrões do sql-capacity (não product keys).
Espelhar em `.cursor/kb/`.

## Acceptance criteria

- [x] KB `oci-vault` com index + quick-reference + concepts/patterns mínimos — no test — filesystem
- [x] KB `azure-keyvault` com paridade conceitual mínima — no test — filesystem + review paridade
- [x] Espelho `.cursor/kb/` completo para ambos — no test — checklist simétrica
- [x] Sem OCID/credencial real; placeholders apenas — tested by: grep heurístico SI

## Notes

Paralelo com 33/36. Agent `key-oci-expert` fora de escopo.
Testes SI/espelho: `test_cloud_secrets_catalog.py`.
Commit pendente de acordo explícito.
