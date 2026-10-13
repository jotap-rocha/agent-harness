# Contrato YAML + loader

**Status:** done  
**Blocked by:** none

## What to build

Criar o contrato versionado `agent-policies.yaml` (mínimo válido) e o pacote
`config/agent_policies/` com loader tipado. YAML inválido ou schema quebrado falha
de forma explícita (CLI/`check`). Base para matcher, generate e hooks.

## Acceptance criteria

- [x] Contrato na raiz carrega com famílias/patterns/severity tipados — tested by: pytest loader contrato
- [x] YAML inválido ou campo obrigatório ausente falha sem silently empty — tested by: pytest casos negativos
- [x] CLI `python -m config.agent_policies check` exit ≠ 0 em contrato inválido — tested by: pytest subprocess/CLI
- [x] Pacote importável alinhado ao padrão git_hygiene/data_engineering — tested by: import + smoke pytest

## Notes

Slug: `policies-anti-destrutivas`. Branch: `feat/policies-anti-destrutivas`.
Naming: `python -m config.agent_policies generate|check` (03-harness).
Catálogo completo pode chegar fino nas tasks 44+; aqui o schema e um mínimo dogfood.
