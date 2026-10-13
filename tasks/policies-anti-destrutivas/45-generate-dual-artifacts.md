# Generate dual artifacts

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/42-matcher-deny-ask.md, tasks/policies-anti-destrutivas/44-catalog-core-families.md

## What to build

`python -m config.agent_policies generate` materializa, a partir do mesmo catálogo
+ famílias ativas: (1) lista `permissions.deny` Claude e (2) stubs/config de hooks
Cursor — sem drift manual entre runtimes.

## Acceptance criteria

- [x] Generate produz deny Claude não vazio para core — tested by: pytest generate snapshot/assert
- [x] Generate produz artefato Cursor (hooks.json ou fragmento) coerente com o mesmo catálogo — tested by: pytest generate
- [x] Alterar severity/pattern no YAML muda ambos os lados no regenerate — tested by: pytest dual output
- [x] Template filho sem paths absolutos de máquina obrigatórios — tested by: pytest generate fixture filho

## Notes

Paridade de política Claude↔Cursor. Wiring real dos hooks = task 46.
