# Silver Checklist ODCS — Decisões de Harness

Slug: `silver-checklist-odcs`  
Branch: `feat/silver-checklist-odcs` (criar no build)  
Data: 2026-08-19  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Tipo: **e** — evolução canônico (KB pipeline DE)

> Este ship **evolui o canônico**. Não cria `.claude/` de produto-filho.  
> `/harness-architect` adaptado: plano de extensão KB + agents existentes.  
> Implementação via `/to-tasks` → `harness-build`.

## Invariantes (sempre valem)

- Entrega = documentação prescritiva KB; **sem** novo rule_id DE
- DE-B003 (contrato versionado) permanece gate mecânico; checklist = guia de implementação
- Bronze: tipagem `.cast()`; Silver: dedup/limpeza/validação — **sem** inferSchema no Silver
- SI **a** — só dados sintéticos nos exemplos do KB
- Dual-tree `.claude/` ↔ `.cursor/` na mesma sessão de promoção
- `/validar` verde; evidence-gate por task no build
- Filho recebe KB via categoria `pipeline_dados` no install (sem categoria nova)
- Commit/push só com acordo explícito

## Naming fechado (architect — sem entrevista)

| Item | Escolha | Motivo |
|---|---|---|
| KB pattern | `.claude/kb/pipeline/patterns/silver-checklist-odcs.md` | Grill #1 |
| Espelho | `.cursor/kb/pipeline/patterns/silver-checklist-odcs.md` | Dual-tree |
| Prefixo regras orders | `SLV-ORD-NNN` | Domínio + sequência |
| Prefixo template | `SLV-CORE-NNN` / `SLV-OPT-NNN` | Core vs opcional |
| Severidades | `fail` \| `quarantine` \| `log` | Grill #6 |
| ingestion_mode | `batch` \| `cdc` | Grill #9 |
| Lineage contrato | `_contract_id`, `_contract_version` | Grill #7 |
| Lineage medallion | `_processed_at`, `_pipeline_version`, `_run_id` | `data-lineage.md` |
| Cross-link concepts | § "Integração Silver" em `data-contracts.md` | PRD FR7 |
| de-conformidade | `references/silver-checklist-odcs.md` ou parágrafo em rule-ids | PRD FR9 |
| Agent officer | **nenhum** | Estender refs JIT apenas |
| Example | **nenhum** neste ship | Grill #5 |
| ADR | opcional SHOULD se decisão contestável (doc-only vs DE check) | Ver ADRs abaixo |

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Checklist prescritivo | `patterns/silver-checklist-odcs.md` | conhecimento | engenheiro DE, agents |
| Ponte ODCS → Silver | `concepts/data-contracts.md` (link) | conhecimento | contracts-engineer |
| Índice pipeline | `pipeline/index.md` | navegação | JIT agents |
| Remediação DE-B003 | `de-conformidade/references/` | operação | skill de-conformidade |
| Expectations/quarantine | `data-quality-analyst.md` JIT | execução | agent |
| Contrato → regras | `data-contracts-engineer.md` JIT | governança | agent |
| Guardrail espelho | pytest dual-tree / kb smoke | validação | CI |
| Index YAML | `kb/_index.yaml` pipeline patterns | descoberta | install / @-mention |

## O que o architect NÃO gera agora (fica para build)

### Agentes criados
- **Nenhum** agent novo

### Agents a estender (MUST)
- `.claude/agents/data-engineering/data-quality-analyst.md` — JIT link pattern
- `.claude/agents/data-engineering/data-contracts-engineer.md` — JIT link pattern
- Espelho `.cursor/agents/data-engineering/`

### KBs (MUST)
- **Novo:** `.claude/kb/pipeline/patterns/silver-checklist-odcs.md`
- **Editar:** `concepts/data-contracts.md` (cross-link)
- **Editar:** `pipeline/index.md` (tabela Padrões)
- **Editar (opcional):** `kb/_index.yaml` se patterns indexados

### Skills (MUST leve)
- **Editar:** `de-conformidade/references/` — ponte DE-B003 → checklist Silver

### Rules
- **Sem** rule nova obrigatória
- `rules/pipeline.md` — link opcional SHOULD (já tem tabela medallion)

### Commands
- **Nenhum** command novo

### Examples / kernel DE
- **Não** alterar `data-engineering.yaml`
- **Não** criar example neste ship

## Tasks sugeridas (`/to-tasks`)

| Task | Escopo | AC |
|---|---|---|
| 82-kb-pattern | Criar `silver-checklist-odcs.md` completo | AC1–AC6, AC13–AC14 |
| 83-crosslinks | data-contracts + index + de-conformidade | AC7–AC9 |
| 84-agents-jit | 2 agents DE + espelho | AC10 |
| 85-index-yaml | `_index.yaml` se necessário | SHOULD |
| 86-pytest-kb | smoke dual-tree / seções obrigatórias | AC1–AC2, AC11 |
| 87-validar-dogfood | `/validar` + espelho | AC11–AC12 |
| 88-ship-sync | STATUS, retro, `/sync-context` | DoD fluxo |

Numeração **82+** — confirmar próximo NN livre em `tasks/README.md` no to-tasks.

## Ortogonalidade

| Artefato | Relação |
|---|---|
| `data-engineering.yaml` | **Inalterado** — DE-B003 exige contrato; checklist guia Silver |
| `medallion.md` | Complementar — fronteira Bronze/Silver referenciada, não reescrita |
| `data-quality.md` | Complementar — snippets DLT/PySpark alinhados |
| `quarantine.md` | Complementar — severidade quarantine |
| evidence-gate | Tasks do ship têm manifesto próprio |
| agent-policies | Ortogonal |

## Decisões contestáveis (ADR opcional)

1. **Doc-only vs DE check** — checklist não vira rule_id (grill #3); ADR curto se maintainer quiser ratificar
2. **Pattern separado vs merge em data-contracts** — pattern vence (grill #1)
3. **10 core + opcionais** vs número fixo 15 — flexível com N/A (grill #11)
4. **Dual snippets** PySpark+DLT — custo de manutenção aceito por dual perfil DE

## Soft-blocks

- `git fetch` Azure 403 — trabalho local; branch feat no build
- Sem commit/push neste passo design
- Judge PRD: **(b)** pulado

## Próximo passo

1. **`/to-tasks`** — fatiar PRD (tasks 82–88 sugeridas)
2. **`/nova-branch`** → `feat/silver-checklist-odcs`
3. **`harness-build`** — implementar com `/validar` + `revisor-codigo` + evidence-gate
4. **`harness-ship`** — sync-context + retro
