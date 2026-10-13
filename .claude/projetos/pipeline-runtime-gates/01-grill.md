# Pipeline Runtime + AI-DEV-KIT Gates — Grill & Requisitos

## Contexto

Decisão de produto (sessão 2026-08-24): o canônico não tinha gate único que **forçasse** o
analista a declarar Spark local vs Databricks no início do SDD. Auto-detect DE só roda com
código existente. Projetos Databricks exigem **AI-DEV-KIT** instalado no repo — segundo gate
humano; resposta "não sei" encerra brainstorm e manda falar com administrador.

### Problema

- Brainstorm passo 4 misturava tipo de projeto com runtime, sem hard-stop dedicado.
- Databricks sem AI-DEV-KIT gerava SDD inválido para a organização.
- Analista sem conhecimento do kit não deveria prosseguir inventando.

### Objetivos (MoSCoW)

**MUST:**
- Gate 4a runtime humano (Spark local | Databricks)
- Gate 4a-bis AI-DEV-KIT se Databricks (sim | não | não sei → stop)
- KB `ai-dev-kit-gate.md` como fonte única
- Validação `harness-define` 2a
- pytest dual-tree

**SHOULD:**
- Cross-link `medallion-sdd-gates.md` e `rules/pipeline.md`

**COULD (fora deste SDD):**
- Check mecânico opcional de artefatos AI-DEV-KIT no filesystem

### Out of Scope

- Novos rule_ids DE
- Instalação automatizada do AI-DEV-KIT
- Alteração do `de_marker.py`

### Restrições

- Gate humano only (§1.3 honesty)
- Espelho `.claude/` ↔ `.cursor/` na mesma sessão

## Critérios de sucesso

- Brainstorm não cria artefatos SDD se Databricks + kit não confirmado
- Testes `test_pipeline_runtime_gates.py` verdes
- `/validar` verde no ship

## Próximo passo

PRD em `02-prd.md` · implementação tasks 94–98.
