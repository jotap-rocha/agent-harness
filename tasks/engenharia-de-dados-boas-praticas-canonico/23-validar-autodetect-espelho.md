# Validar autodetect + espelho

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/18-engine-registry-detect.md, tasks/engenharia-de-dados-boas-praticas-canonico/21-example-databricks-sdp-min.md

## What to build

Estender `/validar` (e espelho `.cursor`) para invocar data-check quando existir marker
**ou** auto-detect Databricks no tree. Atualizar helpers (`de_marker` / detect) e testes
condicionais. Ajustar `rules/pipeline` se necessário para citar perfis `databricks-*` /
pacote D — com espelho `.mdc`.

## Acceptance criteria

- [x] Sem marker e sem sinais Databricks → não invoca data-check — tested by: teste condicional (AC7)
- [x] Com auto-detect Databricks (sem marker) → invoca data-check — tested by: teste com fixture tree (AC7)
- [x] Com marker → invoca (comportamento Loop 1 preservado) — tested by: teste
- [x] Commands `/validar` `.claude` ↔ `.cursor` idênticos — tested by: diff/assert espelho (AC9)
- [x] Se `rules/pipeline` mudar, corpo espelhado `.mdc` — tested by: teste corpo espelhado

## Notes

- Hook Stop permanece sem data-check obrigatório (paridade não exigida).
- Blocked-by 21 garante example real; 22 também serve como fixture se 21 atrasar — preferir 21.
- Trigger útil = marker **ou** SDP/DLT (`DatabricksSignals.useful_pipeline`). **DAB isolado**
  não escolhe perfil cloud e **não** ativa `/validar` sem marker.
- Helper Python é fonte única (`should_run_data_check` / `data_check_validate_argv`); docs
  `/validar` + README commands + `rules/pipeline` espelhados — sem heurística duplicada em shell.
- Override de perfil via marker continua no engine (`resolve_effective_profile`).
- GIT_PREFLIGHT: fetch Azure soft-block conhecido/autorizado; working tree 17–22 preservada;
  sem commit/push/stash/reset/clean. Task 24 **não** implementada.
- `pytest` na raiz do canônico colide `test_smoke.py` entre examples, efeito das Tasks
  21–22 — gate desta task usa `tests/`; correção de regressão fica no freeze da Task 24.

### Evidências (Task 23)

| Etapa | Resultado |
|---|---|
| RED (test-first) | 8 falhas (SDP/DLT/multi/examples + docs espelho) antes da implementação |
| GREEN focado | `test_validar_condicional.py` → 14 passed |
| Gate DE | `pytest tests/data_engineering/` → 128 passed |
| Suite tests/ | `pytest tests/` → 173 passed |
| Lint focado | `ruff check` → OK (`de_marker` + teste) |
| Tipos focado | `mypy` → Success (2 arquivos) |
| Examples validate | SDP/DLT/spark-yarn → exit 0 |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; colisão de coleta raiz encaminhada à Task 24 |

### Sugestão de melhoria (SOLID)

Extrair um port `DataCheckGatePolicy` (interface) com implementação `MarkerOrUsefulDatabricksGate`
facilitaria testar policies alternativas (ex.: DAB+marker-only) sem acoplar `/validar` ao
módulo `de_marker` — fora do escopo desta task.
