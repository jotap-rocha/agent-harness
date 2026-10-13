# Example — databricks-dlt-min

Greenfield mínimo do perfil `databricks-dlt-legacy` (pacotes A + D).
Stubs **estáticos** — sem Databricks SDK, sem API live, sem PII/secrets.
Fora do install automático do harness.

O perfil é resolvido por **auto-detect** (sinais DAB + DLT); este example
**não** declara `project_profile.yaml` com override, para não mascarar a detecção.

## Validar

Na raiz do canônico:

```bash
python -m config.canonical_data_check validate examples/databricks-dlt-min
```

Esperado: exit `0` (pacotes A + D aplicáveis; D002 skip — sem sinal SDP).

## Layout

| Path | Papel |
|---|---|
| `databricks.yml` | DAB com `owner` / `run_as` auditáveis (DE-D001) |
| `config/pipeline.yaml` | owner, `run_id`, logging (pacote A) |
| `config/quarantine-policy.yaml` | destino/política de quarentena (DE-D003) |
| `config/schema-rescue-policy.yaml` | fail vs quarantine (DE-D004) |
| `pipelines/orders_dlt.py` | stub DLT (`import dlt` / `@dlt.`) + expectations |
| `uc/grants.yaml` | grants Unity Catalog em FS (DE-D005) |
| `uc/lineage.md` | linhagem UC em FS (DE-D005) |
| `tests/` | smoke test |
| `OWNER` | ownership declarado |
