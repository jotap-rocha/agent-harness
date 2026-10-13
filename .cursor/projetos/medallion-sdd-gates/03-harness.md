# Medallion SDD Gates — Decisões de Harness

Slug: `medallion-sdd-gates`  
Branch: `feat/medallion-sdd-gates`  
Data: 2026-08-24  
PRD: `02-prd.md`  
Judge: **(b)** pulado — sem `02b-judge.md`  
Tipo: **e** — evolução canônico (processo SDD/Dev Loop)

> Este ship **evolui o canônico**. Não cria `.claude/` de produto-filho.  
> `/harness-architect` adaptado: plano KB + agents workflow/dev existentes.  
> Implementação tasks 88–93 **concluída**; falta ship formal (evidence-gate, revisor).

## Invariantes (sempre valem)

- Entrega = **processo + documentação** KB; sem pipeline executável
- **Sem** novo rule_id em `data-engineering.yaml`
- Gates = perguntas agente; **não** enforcement CLI mecânico
- Dual-tree `.claude/` ↔ `.cursor/` na mesma sessão
- `_source_system` lineage Bronze + Silver (propagado)
- Bronze JSON fiel; Silver normaliza; contrato dual documentado
- SI **a** — amostras sintéticas nos gates
- Commit/push só com acordo explícito

## Naming fechado (architect — sem entrevista)

| Item | Escolha | Motivo |
|---|---|---|
| KB gates | `patterns/medallion-sdd-gates.md` | Fonte única checklist |
| KB Genie | `patterns/genie-readiness.md` | Gate T8=sim |
| KB Gold | `concepts/gold-analytic.md` | Antes de Diamond |
| Brainstorm | passo **4b** Gate Medallion | Tipo b/c/e pipeline |
| Define | passo **2c** validação | Antes 01-grill |
| Dev Loop | passo **3b** prompt-crafter | Detecção pipeline |
| Hard-stop | T1 tabelas + T2 colunas/amostra + T3 `_source_system` | Grill MUST |
| SDD recomendado | 3 branches por camada | Grill decisão |
| Agent officer | **nenhum** | Estender workflow/dev only |
| Example JSON | **nenhum** neste ship | COULD backlog |

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Checklist entrada SDD | `medallion-sdd-gates.md` | processo | brainstorm, define |
| Dev Loop pipeline | `prompt-crafter.md` 3b | processo | /dev craft |
| Lineage `_source_system` | `medallion.md`, `data-lineage.md`, `quick-reference.md` | conhecimento | engenheiro DE |
| Gold analítico | `gold-analytic.md` | conceito | architect, define |
| Genie/NL | `genie-readiness.md` | governança | define (T8=sim) |
| Silver pós-gate | `silver-checklist-odcs.md` | implementação | build filho |
| Rule filho template | `rules/pipeline.md` | convenção | install pipeline_dados |
| Command /dev | `commands/dev.md` | UX | usuário Dev Loop |
| Guardrail CI | `test_medallion_sdd_gates.py` | validação | `/validar` |

## O que foi gerado / atualizado

### Agentes criados
- **Nenhum** agent novo

### Agents estendidos (MUST — done)
- `.claude/agents/workflow/harness-brainstorm.md` — 4b
- `.claude/agents/workflow/harness-define.md` — 2c + template grill
- `.claude/agents/dev/prompt-crafter.md` — 3b
- Espelho `.cursor/agents/` correspondente

### KBs (MUST — done)
- **Novo:** `patterns/medallion-sdd-gates.md`
- **Novo:** `patterns/genie-readiness.md`
- **Novo:** `concepts/gold-analytic.md`
- **Editado:** `concepts/medallion.md`, `data-lineage.md`, `quick-reference.md`
- **Editado:** `pipeline/index.md`, `kb/_index.yaml`

### Rules (MUST — done)
- **Editado:** `rules/pipeline.md` — `_source_system`, gates, contrato dual

### Commands (MUST — done)
- **Editado:** `commands/dev.md` — Gate Medallion

### Skills
- **Sem** alteração obrigatória em `de-conformidade` (ponte existente DE-B003 + silver-checklist)

### Examples / kernel DE
- **Não** alterar `data-engineering.yaml`
- **Não** criar example neste ship

## Tasks implementadas

| Task | Escopo | Status |
|---|---|---|
| 88 | KB medallion-sdd-gates | done |
| 89 | harness-brainstorm 4b | done |
| 90 | harness-define 2c | done |
| 91 | prompt-crafter 3b + dev.md | done |
| 92 | rules/pipeline + index | done |
| 93 | pytest wiring | done |

## Ortogonalidade

| Artefato | Relação |
|---|---|
| `data-engineering.yaml` | **Inalterado** |
| `silver-checklist-odcs.md` | Complementar — Silver pós-gates |
| `agent-policies` | Ortogonal |
| `evidence-gate` | Manifestos tasks 88–93 no ship |
| `fluxo-events` | Opcional emit design phase |

## Decisões contestáveis (ADR opcional)

1. **Gates process-only vs DE check** — processo vence; honesty §1.3
2. **Contrato dual vs Silver-only** — dual documentado (ingestão + ODCS)
3. **3 SDDs por camada** — recomendação, não enforcement
4. **Genie checklist separado** — `genie-readiness.md` vs inflar gates KB

## Pendências ship (DoD)

- [ ] `/validar` global verde
- [ ] evidence-gate collect/check tasks 88–93
- [ ] `revisor-codigo` aprovado
- [ ] `metrics/entregas.jsonl` linhas por task
- [ ] `05-retro.md` + `/sync-context` no harness-ship

## Próximo passo

1. **Evidence-gate** — manifestos em `.claude/projetos/medallion-sdd-gates/evidencias/`
2. **`/validar`** — suite completa
3. **`revisor-codigo`** — diff branch vs master
4. **`harness-ship`** — retro + sync-context
