# Kernel pacote E + marker

**Status:** done  
**Blocked by:** none

## What to build

Adicionar o pacote **E** `keyvault-cloud` (`DE-E*`) à norma e ao kernel: regras de wiring
(facade / map só IDs-URIs / sem SDK nos consumidores), marker `secret_store:
oci|azure|multi`, auto-detect conservador e resolução **multi** (união). Validate
executa E quando aplicável; `DE-A001` permanece independente. Sem live API.

## Acceptance criteria

- [x] `data-engineering.yaml` declara pacote E com regras `DE-E*` carregáveis — tested by: pytest contrato loader (packages.E)
- [x] `check_package_e` registrado no registry e roda no validate quando aplicável — tested by: pytest registry + validate em fixture
- [x] Marker `secret_store` parse + override sobre auto-detect — tested by: pytest `de_marker`
- [x] Auto-detect OCI-only / Azure-only / ambos→multi / nenhum — tested by: pytest fixtures detect
- [x] Checks E: facade presente; map só IDs/URIs; consumidores sem SDK vault — tested by: pytest package_e positivos/negativos
- [x] `DE-A001` ainda falha literais com E presente — tested by: pytest regressão package_a / A001

## Notes

Slug do projeto: `keyvault-oci-azure-choice`. Branch: `feat/oci-vault-harness`.
IDs: DE-E001–E003. Remediations no YAML para `de-conformidade`.
E é ortogonal ao perfil DE (não listado em `profiles.*.packages`); engine injeta
quando `resolve_effective_secret_store` ≠ None.
Gate: ruff+mypy+pytest DE verdes (188 passed). Commit pendente de acordo explícito.
Revisor: self-check harness-build (subagent sem spawn de revisor-codigo) — sem
bloqueantes SI aparentes; findings E sem ecoar secret.
