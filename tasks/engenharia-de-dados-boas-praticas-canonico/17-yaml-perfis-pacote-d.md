# YAML perfis Databricks + pacote D

**Status:** done  
**Blocked by:** none

## What to build

Estender `data-engineering.yaml` com os perfis `databricks-sdp-medallion`,
`databricks-dlt-legacy` e `databricks-multi`, e o pacote **D** `databricks-cloud` (IDs,
categorias, severidades, applicability condicional SDP/DLT). Loader/contrato continua
carregando o YAML; perfil `spark-yarn-airflow` e pacotes A/B/C permanecem intactos.

## Acceptance criteria

- [x] YAML declara os três perfis Databricks + pacote D com regras DE-D* — tested by: pytest contrato/loader (AC1)
- [x] Perfis apontam packages corretos (A+D; multi = união semântica documentada) — tested by: asserts no contrato carregado
- [x] Regressão: perfil `spark-yarn-airflow` e pacotes A/B/C ainda carregam — tested by: testes Loop 1 existentes verdes
- [x] Loader rejeita perfil/pacote D malformado — tested by: casos negativos unitários

## Notes

- Fonte: `08-loop2-prd.md`, `09-loop2-harness.md`, grill #14–15.
- Sem implementar checks executáveis ainda (só norma + load).
- Sem agents/skills/KBs novas; `pipeline_dados` inalterado.
- Loader/contrato: **sem mudança de schema** — o contrato tipado já aceita perfis/pacotes aditivos com o mesmo shape de A/B/C.
- Blocos folded usam `>` (não `>-`): subset do `MinimalYaml` em `config/git_hygiene/yaml_loader.py`.

### Evidências (Task 17)

| Etapa | Resultado |
|---|---|
| RED (test-first) | `test_loads_databricks_profiles_and_package_d` e `test_package_d_rules_*` falharam com KeyError (perfil/pacote ausentes) antes do YAML |
| GREEN | `pytest tests/data_engineering/test_contract.py` → 22 passed; `pytest tests/data_engineering/` → 77 passed |
| Lint | `ruff check` OK nos arquivos tocados; `mypy` OK em `config/data_engineering` + `test_contract.py` |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; dashboard e helper de teste corrigidos após revisão |

### Pacote D (IDs normativos)

| ID | Applicability | Área |
|---|---|---|
| DE-D001 | `databricks-dab-present` | DAB / layout / run identity |
| DE-D002 | `sdp-signal-present` | SDP medallion |
| DE-D003 | `dlt-signal-present` | DLT quarentena |
| DE-D004 | `databricks-cloud` | Schema rescue policy |
| DE-D005 | `databricks-cloud` | UC grants/linhagem em FS |

SI secrets/destrutivo permanece no pacote A (perfis cloud sempre incluem A).
