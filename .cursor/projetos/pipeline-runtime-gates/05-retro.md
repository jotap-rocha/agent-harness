# Pipeline Runtime + AI-DEV-KIT Gates — Retrospectiva de Ship

Ship em: 2026-08-24  
Slug: `pipeline-runtime-gates`  
Branch: `feat/pipeline-runtime-gates`

## Métricas de entrega

| Métrica | Valor |
|---|---|
| Tasks entregues | 5 (94–98) |
| Critérios de aceite atendidos | 100% (18/18) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor | aprovado com ressalvas (0 bloqueantes) |
| Intervenções humanas (mid-task) | 0 |
| Taxa de autonomia | 100% (5/5) |
| pytest global | 512 passed |
| pytest dedicado | 18 passed |
| evidence-gate 94–98 | verde |

### Por issue

| # | Título | Aceite | Gate | Revisor |
|---|---|---|---|---|
| 94 | kb-ai-dev-kit-gate | 3/3 | verde (1) | aprovado c/ ressalvas |
| 95 | gates-brainstorm-4a | 4/4 | verde (1) | aprovado c/ ressalvas |
| 96 | gates-define-2a | 3/3 | verde (1) | aprovado c/ ressalvas |
| 97 | rules-index-crossrefs | 3/3 | verde (1) | aprovado c/ ressalvas |
| 98 | pytest-ship | 5/5 | verde (1) | aprovado c/ ressalvas |

## O que funcionou bem

- KB único `ai-dev-kit-gate.md` evita duplicação nos agents (4a-bis, define 2a).
- Hard-stop humano alinhado ao pedido de produto (Spark local vs Databricks + kit).
- Complementa Medallion 4b sem conflito de numeração.
- 18 testes dedicados + suite global verde.

## O que melhorar

- pytest dual-tree byte-a-byte para `rules/pipeline.mdc` e todos os KBs (ressalva revisor).
- Documentar paths concretos do AI-DEV-KIT quando administrador definir layout de instalação.
- Check mecânico opcional de divergência humano vs filesystem (backlog COULD).

## Armadilhas

- Não incluir no commit artefatos de fluxo de outros SDDs (`visao-grafica-fluxo-agentes/fluxo/`).
- `mypy .` na raiz falha por duplicate module em examples (pré-existente).

## ADRs

- Nenhum ADR novo — gates process-only; sem enforcement DE mecânico.

## Harness — aprendizado

- Runtime Databricks exige confirmação humana de AI-DEV-KIT **antes** de criar `00-ideia.md`.
- Resposta "não sei" encerra brainstorm — contato com administrador.

## Leitura stakeholders

Pacote 94–98 entrega gates SDD que obrigam declaração humana de runtime (Spark local vs Databricks)
e confirmação de AI-DEV-KIT instalado para projetos cloud, integrado ao fluxo `/novo-projeto`.
