# Example — keyvault-azure-min

Greenfield mínimo com `secret_store: azure` + facade Azure Key Vault (pacote **E**).
Placeholders only — **sem live API**.

Instancia `config/templates/cloud-secrets/` (não forka lógica). Fora do `stack_map`.

## Validar

Na raiz do canônico:

```bash
python -m config.canonical_data_check validate examples/keyvault-azure-min
```

Esperado: exit `0` (A+B; C skip sem DAG; E PASS).

## Layout

| Path | Papel |
|---|---|
| `src/key_azure.py` | Facade Azure (de scaffold) |
| `config/secrets_map.yaml` | Map só URIs/placeholders |
| `src/consumer_stub.py` | Consumidor sem SDK vault |
| `.harness/data-check/project_profile.yaml` | `secret_store: azure` |
| `pipelines/` · `contracts/` · `config/layers.yaml` | mínimo A+B |
