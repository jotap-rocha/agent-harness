# 00b — Codebase Canônico (foco secrets/vault/SI)

Projeto: **keyvault-oci-azure-choice**  
Fonte: `<raiz-do-clone>`  
Data: 2026-08-11 · somente leitura no mapa

## Executive Summary

Framework Agent Harness: agents/skills/KBs/rules + kernel DE via `/install-harness`.
Secrets hoje = política genérica (“env / secret manager”) + `DE-A001` (regex literais) +
pre-commit — **sem** KB/skill/example OCI Vault ou Azure Key Vault, **sem** pergunta
OCI vs Azure no grill.

### Entry points SI/secrets
- `.claude/rules/seguranca.md` (espelho `.mdc`)
- `data-engineering.yaml` → `DE-A001` · `config/canonical_data_check/checks/package_a.py`
- `.githooks/pre-commit`
- `harness-brainstorm.md` SI Assessment; `harness-define.md` lente PII/segredo

### Convenções
1. Espelho `.claude` ↔ `.cursor` obrigatório; rules `.md` → `.mdc`
2. Examples DE fora do `stack_map`
3. Ausentes: `app_security`, `ponto-unico-vault`, `oci-vault`, skill vault dual-cloud
4. `cloud-platforms` = Snowflake/Databricks/BigQuery — não Key Vault

## Gaps para este projeto
| Gap | Impacto |
|---|---|
| Pergunta OCI vs Azure no grill/define | Decisão some do `/novo-projeto` |
| KB oci-vault + paridade Azure | Sem JIT de SDK/IAM |
| Skill dual-cloud | Sem playbook wiring |
| Example greenfield | Sem dogfood |
| Checks além de regex | Não valida “wiring via vault” |
| stack_map vault | Install não propaga artefatos vault |

## Deep Dive (curto)
- install: `code_quality` copia `seguranca`; `pipeline_dados` traz `DE-A001`; sem categoria vault
- grill Q8 = on-prem vs Databricks — não vault cloud
- harness-architect interview-bank: sem cluster vault
- revisor-codigo: SI bloqueante se secret vazado

## Sugestões de evolução (não implementadas aqui)
1. Pergunta vault no grill/define (acordo B1)
2. KB + skill OCI e Azure (B2) sem agent (B3)
3. Example estático + scaffold (B4)
4. Extender data-check/rules com sinais OCI/Azure (B6)
