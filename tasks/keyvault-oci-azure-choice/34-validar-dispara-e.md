# Validar dispara E

**Status:** done  
**Blocked by:** tasks/keyvault-oci-azure-choice/33-kernel-pacote-e-marker.md

## What to build

Estender o helper do `/validar` para disparar data-check (incluindo pacote E) quando
houver marker `secret_store` **ou** auto-detect de vault, além das regras já existentes
(marker DE / SDP/DLT). Sem sinal de vault → não forçar E. DAB isolado sem vault continua
sem ativar E.

## Acceptance criteria

- [x] Com `secret_store` no marker, `data_check_validate_argv` / `should_run` inclui validate — tested by: pytest helper argv
- [x] Com auto-detect vault (sem marker), validate é disparado — tested by: pytest fixture auto-detect
- [x] Sem marker DE, sem SDP/DLT e sem vault → argv None / não força E — tested by: pytest negativo
- [x] Documentação do command `/validar` menciona aplicabilidade E — no test — docs only; espelho `.claude`↔`.cursor`

## Notes

Não alterar comportamento A–D existente além da condição de disparo E.
Gate: ruff+mypy+pytest verdes. Commit pendente de acordo explícito.
Revisor: self-check harness-build — sem bloqueantes.
