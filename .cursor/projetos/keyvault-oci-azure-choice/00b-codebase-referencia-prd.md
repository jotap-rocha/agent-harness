# 00b — Codebase referência PRD (OCI Key Vault)

Fonte: `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd`  
Data: 2026-08-11 · somente leitura

## Executive Summary

Pipeline PySpark (capacidade SQL) resolve secrets via OCI Vault:
- Facade: `src/utils/key_oci.py` (`return_secret`, `resolve_credential_value`, `_get_secrets_client`)
- Mapping: `.config` INI com OCIDs `ocid1.vaultsecret…` por ambiente (`ANL`/`PRD`)
- Auth: `~/.oci/config` profile DEFAULT → fallback Resource Principal
- SDK: `oci==2.159.0`
- KB local: `.claude/kb/key-oci/` (+ espelhos)
- Agent local: `.claude/agents/domain/key-oci-expert.md` (product-bound)
- MCP: Node `ociBridge.js` → Python `resolve_oci_mcp.py`

Azure Key Vault **não** é usado no código de produto deste PRD.

## Reutilizável no canônico vs product-bound

| Levar (framework) | Não levar (produto) |
|---|---|
| Auth dual + decode Base64 + híbrido OCID/literal | Chaves `SQL_SERVER_*` / `ORACLE_*` |
| Padrão `.config` só OCID (placeholders) | Seções ANL/PRD e OCIDs reais |
| Estrutura KB concepts/patterns/troubleshooting | `config-keys.md` de capacity |
| Snippet bridge Node→Python | MCP tools DatabaseCapacity |
| “Nunca logar secret” | Agent amarrado a sql-capacity-prd |

## Dívidas SI no PRD (aviso)
- Ficheiro `.config` com OCIDs pode estar versionado — examples no canônico devem usar `.config.example` sem OCID real.
- Drift possível entre espelhos Claude/Cursor do agent expert.

## Lift acordado (B4=c)
Padrões + scaffold facade Python genérica + example mínimo no canônico (sem live API).
