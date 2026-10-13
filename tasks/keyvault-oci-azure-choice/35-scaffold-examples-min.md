# Scaffold + examples min

**Status:** done  
**Blocked by:** tasks/keyvault-oci-azure-choice/33-kernel-pacote-e-marker.md

## What to build

Criar scaffold canônico de facade em `config/templates/cloud-secrets/` e instanciar dois
examples greenfield com placeholders: `examples/keyvault-oci-min/` e
`examples/keyvault-azure-min/`. Ambos passam validate estático (pacote E) sem live API e
ficam **fora** do `stack_map`.

## Acceptance criteria

- [x] Template scaffold existe e examples instanciam (não forkam lógica divergente) — tested by: diff/assert estrutura template↔examples ou teste de presença de stubs
- [x] `validate examples/keyvault-oci-min` PASS estático (placeholders) — tested by: pytest ou CLI validate no example
- [x] `validate examples/keyvault-azure-min` PASS estático (placeholders) — tested by: pytest ou CLI validate no example
- [x] Examples **não** aparecem no `stack_map.json` — tested by: grep/assert no teste install/stack_map
- [x] Zero OCID/secret real nos artefatos novos — tested by: grep heurístico / fixture SI; no secret em findings

## Notes

README dos examples: “sem live API”. Marker `secret_store` adequado em cada example.
Testes: `tests/data_engineering/test_example_keyvault_min.py`.
Commit pendente de acordo explícito.
