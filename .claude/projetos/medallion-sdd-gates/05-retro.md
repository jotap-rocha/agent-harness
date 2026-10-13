# Medallion SDD Gates — Retrospectiva de Ship

Ship em: 2026-08-24  
Slug: `medallion-sdd-gates`  
Branch: `feat/medallion-sdd-gates`

## Métricas de entrega

| Métrica | Valor |
|---|---|
| Tasks entregues | 6 (88–93) |
| Critérios de aceite atendidos | 100% (18/18) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor | aprovado com ressalvas (0 bloqueantes) |
| Intervenções humanas (mid-task) | 0 |
| Taxa de autonomia | 100% (6/6) |
| `/validar` global | 494 passed |
| evidence-gate 88–93 | verde |

### Por issue

| # | Título | Aceite | Gate | Revisor |
|---|---|---|---|---|
| 88 | kb-pattern-medallion-gates | 3/3 | verde (1) | aprovado c/ ressalvas |
| 89 | gates-harness-brainstorm | 2/2 | verde (1) | aprovado c/ ressalvas |
| 90 | gates-harness-define | 2/2 | verde (1) | aprovado c/ ressalvas |
| 91 | gates-prompt-crafter | 2/2 | verde (1) | aprovado c/ ressalvas |
| 92 | rules-pipeline-index | 2/2 | verde (1) | aprovado c/ ressalvas |
| 93 | pytest-wiring | 3/3 | verde (1) | aprovado c/ ressalvas |

## O que funcionou bem

- KB único `medallion-sdd-gates.md` evita duplicação nos agents (brainstorm 4b, define 2c, crafter 3b).
- GIT_PREFLIGHT respeitado — branch criada antes dos artefatos SDD.
- Complemento `gold-analytic` + `genie-readiness` + `_source_system` em lineage/medallion.
- 26 testes dedicados + suite global verde; kernel DE intacto.
- Sync-context: drift limpo — evolução KB não exige mudança em CLAUDE.md (framework).

## O que melhorar

- pytest dual-tree poderia cobrir `gold-analytic`, `genie-readiness`, `rules/pipeline.mdc` (ressalva revisor).
- `harness-define` 2c ainda lista T1–T8 inline — candidato a só referenciar KB (consistência com brainstorm).
- Example JSON aninhado (stub) ficou backlog COULD.

## Armadilhas

- evidence-gate critério `kernel` separado exige `test_paths` ou waiver — consolidar no comando `gate` (task 93).
- `tasks/README.md` status "in progress" desatualizado até ship — corrigido no fechamento.

## ADRs

- Nenhum ADR novo — gates process-only alinhado ao PRD; sem enforcement DE mecânico.

## Harness — aprendizado

- Gates Medallion pertencem ao **processo SDD/Dev Loop**, não ao kernel DE.
- Projeto-filho pipeline: usar 3 SDDs por camada quando escopo multi-camada.
- Próximo passo operacional: PR `feat/medallion-sdd-gates` → master (push com acordo humano).

## Leitura stakeholders

Pacote 88–93 entrega checklist de entrada para pipelines Medallion (tabelas, amostra, `_source_system`, JSON fiel, Genie/NL) integrado ao fluxo `/novo-projeto` e `/dev`, sem pipeline executável no canônico.
