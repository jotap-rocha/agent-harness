# Baseline profiles array

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/18-engine-registry-detect.md

## What to build

Estender baseline/compare para gravar e ler **`profiles[]`** além do `profile` singular
legado (compat Loop 1). Ratchet e waivers (owner + expiry) permanecem. Atualizar SCHEMA e
templates seed se necessário (sem forçar AUTO_UPDATE de seed no filho).

## Acceptance criteria

- [x] `write_baseline` persiste `profiles[]` quando multi/cloud — tested by: teste baseline (AC6)
- [x] `compare` lê baseline legado só com `profile` singular sem quebrar — tested by: teste compat
- [x] Ratchet: finding novo falha; baselineado não — tested by: regressão + caso cloud
- [x] SCHEMA.md documenta `profiles[]` — no test — docs; checklist revisão

## Notes

- Preferir campo adicional a bump breaking sem necessidade.
- Seed-once: não apagar baseline de filhos em re-install.
- `profile` singular permanece no payload com o perfil efetivo. `profiles[]` só é
  adicionado para cloud; em `databricks-multi`, lista DLT/SDP em ordem lexicográfica.
- O template `baseline.json` de `spark-yarn-airflow` permanece singular de propósito,
  preservando compatibilidade e sem alterar a política `seed: true` / `KEEP`.
- GIT_PREFLIGHT: fetch Azure é soft-block conhecido e a execução sem novo fetch foi
  autorizada explicitamente. Working tree das Tasks 17–19 preservada; sem
  commit/push/stash/reset/clean.

### Evidências (Task 20)

| Etapa | Resultado |
|---|---|
| RED (test-first) | baseline cloud/multi/ratchet: 3 falhas antes da implementação; documentação: 1 falha antes do SCHEMA |
| GREEN focado | baseline + engine detect + pacote D → 45 passed; após ressalvas, baseline → 19 passed |
| Gate DE | `pytest tests/data_engineering/` → 109 passed |
| Lint focado | `ruff check` → OK nos arquivos Python da Task 20 |
| Tipos focado | `mypy --explicit-package-bases` → Success nos 2 arquivos Python |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; alteração fora de escopo no SCHEMA do example Loop 1 revertida |
