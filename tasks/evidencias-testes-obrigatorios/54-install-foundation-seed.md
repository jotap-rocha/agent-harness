# Install foundation seed

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/51-check-manifest-ref.md

## What to build

Propagar evidence-gate na foundation do `/install-harness`: contrato/CLI/seed
`.harness/evidence-gate/` (KEEP), para filhos não nascerem sem o freio. Fixture de
install prova presença.

## Acceptance criteria

- [x] stack_map foundation inclui artefatos evidence-gate — tested by: pytest freeze/stack ou install fixture
- [x] Seed template KEEP no re-install — tested by: pytest install KEEP
- [x] Filho fixture tem CLI/módulo check importável ou script path — tested by: pytest install
- [x] Espelho scripts install `.claude`↔`.cursor` — tested by: parity assert se padrão existir

## Notes

Always-on (grill decisão 6). Não misturar com agent-policies/vault.

Revisor: aprovado. Gate tentativas_ate_verde=1.
