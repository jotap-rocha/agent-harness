# Boas práticas de Engenharia de Dados no canônico

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Branch: `feat/de-boas-praticas-canonico`  
Iniciado em: 2026-08-06  
Sketch adversarial: [`sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`](../../../sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md)

> Nota: o slug excede o guideline típico de 30 caracteres (len=42). Mantido por escolha explícita do usuário.

## Ideia

Evoluir o Agent Harness Canônico para que **sempre que um novo pipeline de dados** seja criado (e também em brownfield), o projeto herde boas práticas fim a fim — da camada raw até gold no medalhão — com governança, qualidade de dados, limpeza, higienização, tratamento de nulos, tipagem, nomes de colunas, metadados, data lineage, alertas, etc.

A evolução não deve ser só um catálogo de prompts/KBs. Deve seguir a visão adversarial do sketch: evidências → decisões arquiteturais → modelo normativo → **validadores executáveis** → CI / baseline / exceções → scaffolds → skills / commands / agents → piloto brownfield.

Fontes de evidência já consolidadas no sketch:

- `data-agentic-ai-for-pipelines` → norma / organização agentic / on-prem
- `databricks-varonis-dataflow-prd` → implementação de referência fim a fim
- `dtbks-auditoria` → gaps reais doc×código (casos de teste do canônico)
- `ai-dev-kit-main-databricks` → modernização SDP / DABs / system tables

Problema central a resolver:

```text
prática documentada → implementação parcial → sem enforcement automático
```

Risco a evitar: harness que **explica** boas práticas sem **provar** que os projetos as seguem.

## SI Assessment

Nível: **c + d**

- **c)** PII — o canônico em si pode não processar PII, mas os projetos-filhos de pipeline frequentemente lidam com CPF, email, dados financeiros, etc. O harness deve assumir PII e configurar templates/rules (`[AVISO_LGPD]`, `rules/pii.md` quando aplicável).
- **d)** Produção com risco de escrita/deleção — pipelines podem escrever em catálogos/tabelas de produção; deny list + ADR obrigatório antes de DDL/DML destrutivo em prod.

Implicações:

- Declarar no template de CLAUDE.md dos projetos-filhos o aviso LGPD quando o perfil DE indicar PII.
- Instrui criar `rules/pii.md` específico do domínio quando houver PII.
- Deny list / gates para operações destrutivas em produção; ADR antes de escrita destrutiva.
- Secrets nunca em código; checks executáveis (não só prosa).
- PII nunca em logs/query strings sem masking — alinhar checks futuros a `seguranca` + mandatos SEC.

## Tipo de Projeto

**e) Outro** — evolução do harness canônico / **framework de conformidade de Engenharia de Dados**.

Não é um pipeline de domínio único. É a camada de framework que os projetos-filhos consomem via `/install-harness`.

Alvos dos projetos-filhos (perfis):

- **b)** Pipeline LOCAL (PySpark + Airflow, on-premises)
- **c)** Pipeline CLOUD (Databricks + Unity Catalog / SDP / DAB)

Stack prevista (canônico):

- Rules + modelo normativo versionado (IDs, categorias universal/condicional/recomendada/informativa)
- Validadores executáveis (`canonical-data-check` ou equivalente)
- CI / baseline brownfield / política de waiver
- Scaffolds de referência (DAB+SDP e/ou Spark+Airflow)
- Skills, commands e agents DE (evoluir os 10 agents já existentes; não duplicar)
- Espelho `.claude/` ↔ `.cursor/` + propagação controlada via `install-harness` / `stack_map`

## Codebase já mapeado

Ver [`00b-codebase.md`](00b-codebase.md).

Resumo: o canônico já tem 10 agents DE, 7 commands DE, ~11 KBs e a rule `pipeline.md`, mas é sobretudo documentação. Falta o kernel de conformidade (norma → checks → CI/exceções → scaffolds). `install-harness` hoje só propaga `kb/pipeline` + `rules/pipeline` por keywords.

## Próximos passos

0. Repo já mapeado — ver `00b-codebase.md` antes do grill.
1. Rode `/grill-me` para aprofundar a ideia (ordem do sketch, perfil mínimo, o que é mandato vs recomendação, MVP do validator, piloto brownfield).
2. Ao terminar, use `harness-define` para estruturar os requisitos (incluindo perguntas específicas de pipeline / perfis b+c).
3. Depois: `harness-design` → PRD + decisões → implementação na ordem adversarial (kernel antes de novos agents).
