# Medallion SDD Gates

## Ideia

Evoluir o **harness canônico** com gates de processo (SDD + Dev Loop) para projetos de
engenharia de dados Medallion — **sem** implementar pipelines de produto neste fluxo.

Objetivo: quando alguém abrir `/novo-projeto` (tipo pipeline) ou `/dev` (evolução pontual),
o harness **obriga** perguntas sobre camadas, tabelas, colunas/amostra, `_source_system`,
JSON aninhado (Bronze fiel → Silver normaliza), contrato dual (ingestão + ODCS), Genie/NL
e semântica/ontologia.

Entregáveis:
- KB `patterns/medallion-sdd-gates.md`
- Gates em `harness-brainstorm` (4b), `harness-define` (2c), `prompt-crafter` (3b)
- Atualização `rules/pipeline.md`, command `/dev`
- pytest dual-tree + wiring

**Não inclui:** novos checks DE em `data-engineering.yaml`, examples com transformação real.

## SI Assessment

Nível: **a** — Não — apenas dados abertos, sintéticos ou públicos

Implicações:
- Harness mínimo de SI; KB usa placeholders sintéticos
- Patterns de CPF/telefone são inferência documentada, sem PII real

## Tipo de Projeto

**e** — Evolução do harness canônico (processo SDD/Dev Loop + KB pipeline)

Stack prevista:
- Agents workflow + dev; KB pipeline; rules; commands
- Espelho dual-tree `.claude/` ↔ `.cursor/`
- Referência cruzada com `silver-checklist-odcs.md`

## Medallion Gates (brainstorm)

| Item | Resposta |
|---|---|
| Camada-alvo | Harness (processo) — não pipeline produto |
| Entidades/tabelas | N/A — gates genéricos por entidade declarada pelo usuário |
| _source_system | Obrigatório na Bronze/Silver (lineage) |
| JSON aninhado | Bronze fiel; Silver normaliza; contrato dual |
| SDDs separados | Recomendado 3 SDDs por camada no projeto-filho |
| Genie / NL | Gate T8 + G1–G7 no define |
| Semântica / ontologia | Documentado no KB; perguntado se Genie=sim |

## Próximos passos

1. Implementar tasks 88–93 nesta branch
2. `/validar` + evidence-gate + revisor antes de ship
3. Grill/define opcional para PRD formal se escopo crescer
