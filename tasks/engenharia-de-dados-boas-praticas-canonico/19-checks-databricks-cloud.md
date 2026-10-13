# Checks Databricks cloud (pacote D)

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/18-engine-registry-detect.md

## What to build

Implementar checks executáveis do pacote **D** `databricks-cloud` alinhados ao YAML:
DAB/job config, layout SDP, DLT + quarentena, schema rescue policy, Unity Catalog
grants/linhagem **em filesystem** (sem API live). Regras condicionais por sinal SDP/DLT.
Universal A continua sempre rodando junto nos perfis cloud.

## Acceptance criteria

- [x] Validate em fixture SDP acusa/ausenta findings D esperados — tested by: pytest checks D (AC10)
- [x] Validate em fixture DLT exige quarentena para qualquer tree com sinal DLT — tested by: pytest
- [x] Schema rescue + UC FS + DAB signals cobertos como blockers quando ausentes no greenfield mínimo — tested by: casos negativos
- [x] Findings sem payload sensível (path + rule_id) — tested by: assert em message/report
- [x] `explain` funciona para IDs DE-D* — tested by: CLI/API explain

## Notes

- Pacote bloqueante “completo do grill” — priorizar sinais estáticos.
- Não alterar pacotes B/C.
- Implementação em `config/canonical_data_check/checks/package_d.py` reutiliza
  `detect_databricks_signals` (Task 18); skip condicional espelha applicability do YAML.
- D001 exige valor não vazio em `owner`, `run_as`, `run_identity` ou service principal;
  `owner:`/`run_as:` vazios não satisfazem identidade auditável.
- D003 aplica sempre que há sinal DLT, sem depender de expectations. A busca de
  quarentena fica restrita a fontes DLT e arquivos versionados sob `policies/` ou
  policies de qualidade nomeadas em `config/`, sem inspecionar datasets/PII.
- Fixture `databricks-multi` prova D002 (SDP medallion) e D003 (DLT quarantine)
  no mesmo validate.
- GIT_PREFLIGHT: `git fetch` Azure indisponível (soft-block conhecido); execução sem
  fetch remoto autorizada explicitamente pelo parent neste turno. Working tree das
  Tasks 17–18 preservada; sem commit/push/stash/reset/clean.

### Evidências (Task 19)

| Etapa | Resultado |
|---|---|
| RED (test-first) | `test_package_d_checks.py` escrito antes da lógica D001–D005 |
| GREEN focado | `pytest test_package_d_checks.py` → 14 passed |
| Regressão focada | package D + registry/detect + explain → 31 passed |
| Gate DE | `pytest tests/data_engineering/` → 104 passed |
| Lint focado | `ruff check` → OK em `package_d.py`, `de_marker.py` e testes |
| Tipos focado | `mypy package_d.py de_marker.py` → Success |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; 5 correções proporcionais aplicadas e testadas |
