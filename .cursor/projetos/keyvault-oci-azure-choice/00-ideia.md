# Key Vault OCI vs Azure — escolha e artefatos no canônico

Slug: `keyvault-oci-azure-choice`  
Branch: `feat/oci-vault-harness`  
Iniciado em: 2026-08-11

## Ideia

Evolução do harness canônico sobre o uso de key vault na nuvem:

- Quando for fazer uso de key vault, **perguntar** se vamos usar **Oracle OCI Vault** ou **Azure Key Vault**.
- Se for selecionado **Oracle OCI**, tomar como exemplo o modelo do projeto
  `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd`
  (facade `key_oci.py`, `.config` com OCIDs, auth `~/.oci/config` → Resource Principal,
  KB/agent locais `key-oci` / `key-oci-expert`).

## SI Assessment

Nível: **a + b**

- **a)** Artefatos do canônico em si são documentação/framework (sem dataset de produto).
- **b)** O domínio trata **secrets/credenciais** (connection strings, tokens, OCIDs de vault)
  tipicamente sem PII no conteúdo do secret.

Implicações:
- Nunca logar/expor valor de secret (output LLM, findings, URLs).
- Secrets só via env / secret manager; nunca hardcoded no repo.
- OCIDs em examples/templates: usar placeholders, nunca OCIDs reais de produção.
- PII (**c**) e write em produção (**d**) **fora** deste SI — se aparecerem no grill futuro, reabrir Assessment.

## Tipo de Projeto

**b + c + d** — a evolução do harness deve servir:

- **b)** Pipeline de dados LOCAL (PySpark + Airflow / on-prem)
- **c)** Pipeline de dados CLOUD (Databricks + Unity Catalog / Azure)
- **d)** Análise / Dashboard / Relatório (sem pipeline persistente)

Ou seja: não é um produto pipeline único; é **evolução do framework** consumida por projetos
tipo b/c/d. Stack prevista: artefatos canônicos (KB, skill, example, checks) + wiring em
`grill-me` / `harness-define`; enforcement via `canonical-data-check`.

## Decisões de escopo (Bloco B — fechadas no brainstorm)

| ID | Escolha | Significado |
|---|---|---|
| B1 | **a** | Pergunta OCI vs Azure só em `/grill-me` / `harness-define` |
| B2 | **c** | MVP: KB + skill OCI **e** paridade Azure (skill/KB Azure alinhada) |
| B3 | **a** | **Sem** agent dedicado no canônico (só skill + KB) |
| B4 | **c** | Reuso do PRD: padrões + scaffold facade + **example mínimo** no canônico |
| B5 | **a** | Novo domínio KB `oci-vault` (+ Azure) com **ponte** nos KBs existentes |
| B6 | **b** | Estender `canonical-data-check` / rules com sinais OCI (e espelho Azure) |

## Decisão agent vs skill (validada)

No **canônico**: **KB + skill** (OCI e Azure em paridade) — **sem** agent `key-oci-expert`.

Motivos:
- Agents do canônico devem ser genéricos; o expert do PRD é product-bound.
- Processo multi-step cabe em skill; conceitos estáveis cabem em KB JIT.
- Agent especializado permanece **opcional no projeto-filho**, fora deste MVP.

## Artefatos previstos (alto nível)

- KB `.claude/kb/oci-vault/` (+ espelho) e paridade Azure Key Vault
- Skill(s) de integração/troubleshooting OCI e Azure
- Example greenfield estático no canônico (sem live API / sem OCID real)
- Pergunta vault no grill/define
- Extensão de checks (além de `DE-A001` regex) para sinais de wiring vault
- Pontes curtas em KBs/rules SI existentes
- Espelho `.claude` ↔ `.cursor` obrigatório

## Fora do MVP (explícito)

- Agent dedicado no canônico
- Live calls OCI/Azure Vault no CI do canônico
- Propagar agent `key-oci-expert` via install (pode ser Loop futuro)
- Pergunta vault em install-harness / commands DE (B1 = só grill/define)

## Próximos passos

0. Repo mapeado — ver `00b-codebase-canonico.md` e `00b-codebase-referencia-prd.md` antes do grill
1. Rode `/grill-me` para aprofundar (matriz OCI vs Azure, checks, example layout, nomes de skill)
2. Ao terminar, use `harness-define` para estruturar os requisitos
3. Depois: `harness-design` → PRD + harness-architect
