# Example — databricks-sdp-min

Greenfield mínimo do perfil `databricks-sdp-medallion` (pacotes A + D).
Stubs **estáticos** — sem Databricks SDK, sem API live, sem PII/secrets.
Fora do install automático do harness.

O perfil é resolvido por **auto-detect** (sinais DAB + SDP); este example
**não** declara `project_profile.yaml` com override, para não mascarar a detecção.

## Validar

Na raiz do canônico:

```bash
python -m config.canonical_data_check validate examples/databricks-sdp-min
```

Esperado: exit `0` (pacotes A + D aplicáveis; D003 skip — sem sinal DLT).

## Layout

| Path | Papel |
|---|---|
| `databricks.yml` | DAB com `owner` / `run_as` auditáveis (DE-D001) |
| `config/pipeline.yaml` | owner, `run_id`, logging (pacote A) |
| `config/layers.yaml` | medallion bronze/silver/gold (DE-D002) |
| `config/schema-rescue-policy.yaml` | fail vs quarantine (DE-D004) |
| `pipelines/orders_sdp.py` | stub SDP (`pyspark.pipelines` / `@dp.`) |
| `uc/grants.yaml` | grants Unity Catalog em FS (DE-D005) |
| `uc/lineage.md` | linhagem UC em FS (DE-D005) |
| `tests/` | smoke test |
| `OWNER` | ownership declarado |
