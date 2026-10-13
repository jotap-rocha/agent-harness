# Pull Request — Azure DevOps

## Título (copiar)

```
feat(medallion-sdd-gates): gates SDD/Dev Loop para pipelines Medallion
```

## Branch

- **Source:** `feat/medallion-sdd-gates`
- **Target:** `master`

## Push (manual — você)

```bash
git push -u origin feat/medallion-sdd-gates
```

## Abrir PR na UI

Após o push, abra (ou cole no navegador):

https://dev.azure.com/icatu/Infraestrutura/_git/agent-harness-canonico-v2/pullrequestcreate?sourceRef=feat/medallion-sdd-gates&targetRef=master

---

## Descrição (corpo do PR — colar abaixo)

## O que muda

Evolução do harness canônico com **gates de processo** para projetos pipeline Medallion:
perguntas obrigatórias (tabelas, colunas/amostra, `_source_system`, JSON fiel, Genie/NL)
no SDD (`harness-brainstorm` 4b, `harness-define` 2c) e Dev Loop (`prompt-crafter` 3b).

**Sem** pipeline executável nem novos rule_ids DE — só processo + KB.

## Entregáveis principais

- KB `patterns/medallion-sdd-gates.md` (+ `gold-analytic.md`, `genie-readiness.md`)
- Atualização `medallion.md`, `data-lineage.md`, `rules/pipeline.md`, `commands/dev.md`
- Tasks **88–93** · pytest `test_medallion_sdd_gates.py` (26 testes)
- PRD/design/retro em `.claude/projetos/medallion-sdd-gates/`

## Como testei

- [x] `ruff check .` — verde
- [x] `mypy config` — verde
- [x] `pytest` — **494 passed** (global)
- [x] `pytest tests/data_engineering/test_medallion_sdd_gates.py` — **26 passed**
- [x] evidence-gate tasks 88–93 — verde
- [x] `data-engineering.yaml` — sem diff
- [x] sync-context — sem drift
- [x] revisor-codigo — **aprovado com ressalvas** (0 bloqueantes)

## Checklist

- [x] Branch `feat/medallion-sdd-gates`
- [x] Título `feat(medallion-sdd-gates): ...`
- [x] Sem segredo no diff
- [x] Gate local verde
- [ ] Squash merge (conforme política do repo)

## Commits (5)

1. `dfc8cfb` — feat: gates SDD/Dev Loop + KB + agents + tasks 88–93
2. `cc4ac2f` — docs: KB complementar (_source_system, gold, genie) + grill
3. `77f7182` — docs: PRD + 03-harness
4. `93ea151` — chore: ship (evidence-gate, retro, STATUS)
5. `99fcffe` — metrics: entregas 88–93

## Notas

- Ressalvas revisor: pytest dual-tree parcial; define 2c lista T1–T8 inline (não bloqueante).
- Example JSON aninhado ficou backlog COULD.
- Filhos pipeline: usar KB gates antes de implementar bronze/silver/gold.
