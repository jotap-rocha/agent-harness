# Pipeline Runtime + AI-DEV-KIT Gates

## Ideia

Evoluir o **harness canônico** com gates de processo no SDD (`/novo-projeto`) que **obrigam**
resposta humana explícita sobre o runtime de execução do pipeline **antes** de continuar o
brainstorm:

1. **Gate 4a — Runtime:** Spark LOCAL vs Databricks CLOUD (hard-stop; não inferir do código).
2. **Gate 4a-bis — AI-DEV-KIT:** se Databricks, confirmar instalação do AI-DEV-KIT no repositório.
   Respostas **Não** ou **Não sei** → encerrar brainstorm e orientar administrador.

Contexto: o auto-detect DE (`de_marker.py`) infere perfil **depois** que código existe; o SDD
precisa de decisão humana **no início**. Projetos Databricks dependem do pacote organizacional
AI-DEV-KIT (SDP, DABs, agents alinhados ao workspace) — complementa `/install-harness`.

Entregáveis:
- KB `kb/databricks/patterns/ai-dev-kit-gate.md`
- `harness-brainstorm` passos 4a e 4a-bis + template `00-ideia.md`
- `harness-define` passo 2a (validação)
- Cross-links em `rules/pipeline.md`, `medallion-sdd-gates.md`, `kb/databricks/index.md`
- pytest `test_pipeline_runtime_gates.py` + espelho dual-tree

**Não inclui:** check mecânico de instalação do AI-DEV-KIT (gate humano §1.3).

## SI Assessment

Nível: **a** — Não — apenas dados abertos, sintéticos ou públicos

Implicações:
- Harness mínimo de SI; KB sem PII
- Gate humano — sem validação live de workspace Databricks

## Tipo de Projeto

**e** — Evolução do harness canônico (processo SDD + KB Databricks)

Stack prevista:
- Agents workflow (`harness-brainstorm`, `harness-define`)
- KB `databricks/patterns/ai-dev-kit-gate.md`
- Rules pipeline; espelho `.claude/` ↔ `.cursor/`

## Runtime Pipeline (gate 4a)

| Campo | Valor |
|---|---|
| Runtime | N/A — evolução do canônico (gates genéricos spark-local \| databricks) |
| Declaração | humana (2026-08-24 — decisão de produto no brainstorm do projeto-filho) |
| Notas | Gate aplica-se a tipos b/c/e pipeline no `/novo-projeto` |

## AI-DEV-KIT (gate 4a-bis — só Databricks)

| Campo | Valor |
|---|---|
| Instalado | N/A — escopo canônico (define regra para projeto-filho) |
| Declaração | humana (2026-08-24) |
| Status gate | aprovado — SDD canônico aberto |

## Medallion Gates (brainstorm)

| Item | Resposta |
|---|---|
| Camada-alvo | Harness (processo) — gates 4a/4a-bis precedem Medallion 4b |
| Entidades/tabelas | N/A |
| _source_system | Inalterado — gate Medallion existente |
| SDDs separados | N/A |
| Genie / NL | Inalterado — gate Medallion existente |

## Próximos passos

1. Tasks 94–98 nesta branch
2. `/validar` + evidence-gate + revisor antes de ship
3. PR → master (acordo explícito para push)
