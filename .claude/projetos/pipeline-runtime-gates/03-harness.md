# Harness Design — Pipeline Runtime + AI-DEV-KIT Gates

Slug: `pipeline-runtime-gates`  
Branch: `feat/pipeline-runtime-gates`  
Data: 2026-08-24

## Artefatos tocados

| Camada | Path | Mudança |
|---|---|---|
| KB | `.claude/kb/databricks/patterns/ai-dev-kit-gate.md` | **novo** — gate humano |
| Agent | `harness-brainstorm.md` | passos **4a**, **4a-bis** + template 00-ideia |
| Agent | `harness-define.md` | passo **2a** validação |
| KB | `medallion-sdd-gates.md` | pré-requisito 4a/4a-bis |
| Rule | `rules/pipeline.md` | cross-link gates |
| KB index | `databricks/index.md`, `_index.yaml` | roteamento ai-dev-kit-gate |
| Testes | `tests/data_engineering/test_pipeline_runtime_gates.py` | **novo** |

## Wiring SDD

| Fase | Agent | Passo | Gatilho |
|---|---|---|---|
| Brainstorm | harness-brainstorm | **4a** | tipo b/c/e pipeline |
| Brainstorm | harness-brainstorm | **4a-bis** | runtime = Databricks |
| Brainstorm | harness-brainstorm | 4b | após 4a (e 4a-bis se aplicável) |
| Define | harness-define | **2a** | valida 00-ideia antes de grill |
| Define | harness-define | 2c | Medallion (inalterado) |

## Invariantes

- Resposta humana obrigatória — **não** inferir runtime do código
- Databricks sem AI-DEV-KIT confirmado → **sem** `00-ideia.md`
- §1.3: gate não verifica instalação mecanicamente

## Tasks

| # | Título | Status |
|---|---|---|
| 94 | kb-ai-dev-kit-gate | done |
| 95 | gates-brainstorm-4a | done |
| 96 | gates-define-2a | done |
| 97 | rules-index-crossrefs | done |
| 98 | pytest-ship | done |

## Ship checklist

- [ ] `/validar` verde
- [ ] evidence-gate 94–98
- [ ] revisor-codigo aprovado
- [ ] `metrics/entregas.jsonl`
- [ ] sync-context
