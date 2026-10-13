# Catálogo core families

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/41-contrato-yaml-loader.md

## What to build

Popular o catálogo core no `agent-policies.yaml`: `shell`, `docker`, `git`,
`sql-cli`, `databricks-cli`, `terraform`, `k8s` — com patterns e severity
(deny-hard vs ask) conforme decisão 12. Famílias extras podem existir no YAML
desligadas / opt-in.

## Acceptance criteria

- [x] Sete famílias core presentes e carregáveis — tested by: pytest contrato/lista core
- [x] Severity deny-hard cobre irreversível infra/dados (ex.: rm -rf, down -v, DROP, terraform destroy, kubectl delete amplo) — tested by: pytest match amostras
- [x] Severity ask cobre git force/reset e deletes Databricks “recuperáveis com dor” — tested by: pytest match amostras
- [x] `check` do contrato passa com catálogo completo core — tested by: CLI/pytest check

## Notes

Catálogo “completo” versionado; extras opt-in via profile (task 47). Não exigir
todas as cloud CLIs no core.
