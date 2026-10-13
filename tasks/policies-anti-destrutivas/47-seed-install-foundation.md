# Seed + install foundation

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/45-generate-dual-artifacts.md, tasks/policies-anti-destrutivas/46-hooks-dual-runtime.md

## What to build

Seed `.harness/policies/project_profile.yaml` (`families[]`, `seed: true` KEEP) e
wiring do `/install-harness` na foundation: sempre-on engine + core + hooks dual;
filho deixa de nascer com `deny: []`. Extras via profile opt-in.

## Acceptance criteria

- [x] Template seed em `config/agent_policies/templates/policies/` com KEEP — tested by: pytest seed marker / install KEEP
- [x] Install foundation gera `permissions.deny` ≠ `[]` no filho — tested by: pytest fixture install
- [x] Install gera `.cursor/hooks.json` (ou equivalente) no filho — tested by: pytest fixture install
- [x] Re-install preserva `families[]` do profile (KEEP) — tested by: pytest re-install
- [x] stack_map / generate documentados como always-on foundation — no test — docs assert em teste de freeze/stack se existir padrão

## Notes

Corrige gap histórico do install (`deny: []`). Não misturar com categoria vault/DE.

## Notes (fechamento)
Bloqueantes revisor sanados: seed block-style `families:`; profile wired no guard/install.

