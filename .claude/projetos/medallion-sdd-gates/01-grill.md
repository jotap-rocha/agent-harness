# Medallion SDD Gates — Grill & Requisitos

## Contexto (brainstorm 2026-08-24)

### Problema

Projetos de pipeline Medallion no harness não tinham gates de processo que obrigassem
perguntas sobre camadas, entidades, `_source_system`, JSON aninhado, contratos dual e
consumo NL (Genie) **antes** de implementar código.

### Objetivos (MoSCoW)

**MUST:**
- KB `medallion-sdd-gates.md` com checklist T/B/S/G
- Gates em SDD (`harness-brainstorm` 4b, `harness-define` 2c)
- Gate Dev Loop (`prompt-crafter` 3b)
- Hard-stop: tabelas + colunas/amostra + `_source_system`
- pytest dual-tree verde

**SHOULD:**
- Atualizar `medallion.md`, `data-lineage.md`, quick-reference com `_source_system`
- KB Gold analítico + Genie readiness (ship complementar)

**COULD:**
- Example JSON aninhado (stub) — fora deste ship

**WON'T:**
- Novos rule_ids em `data-engineering.yaml`
- Pipeline de produto ou transformações reais
- Enforcement mecânico de gates (só processo agente)

### Out of Scope

- Código PySpark/DLT executável
- Checks DE novos (DE-B004 etc.)
- Camada Diamond (multidimensional) — só referência no KB

### Restrições

- Dual-tree `.claude/` ↔ `.cursor/` na mesma sessão
- SI nível **a** — dados sintéticos nos exemplos
- Branch isolada: `feat/medallion-sdd-gates`

## Medallion Gates — validação

- Checklist transversal T1–T8: **preenchido** (gates genéricos no KB)
- Camada-alvo deste SDD: **harness (processo)**
- _source_system: **obrigatório Bronze/Silver** (documentado)
- Contrato dual: ingestão Bronze + ODCS Silver
- JSON aninhado: Bronze fiel → Silver normaliza
- Genie/NL: gate T8 + G1–G7 no define
- Semântica/ontologia: documentado se Genie=sim

### Bronze (escopo documentação)

- B1 JSON fiel na Bronze — **sim** (KB + rules)
- B2 Contrato ingestão — **documentado**
- B3 Schema rescue — referência existente DE-D004
- B4 _source_system — **sim**

### Silver (escopo documentação)

- S1–S8 referenciados via `silver-checklist-odcs.md` + gates KB
- Normalização JSON, trim, sentinels, inferência CPF/CEP — checklist no KB gates

### Gold (escopo documentação)

- G1–G7 gates Genie/semântica/ontologia no KB
- Gold analítico antes de Diamond — conceito no KB gates

## Critérios de sucesso mensuráveis

- `pytest tests/data_engineering/test_medallion_sdd_gates.py` verde
- Agents referenciam `medallion-sdd-gates.md` sem duplicar lista completa
- `tasks/README.md` lista slug `medallion-sdd-gates` (88–93)

## Próximo passo

- Complementar KB (`medallion.md`, `data-lineage`, gold/genie) se ainda pendente
- `harness-design` opcional para PRD formal
- Ship: `/validar` + evidence-gate + revisor
