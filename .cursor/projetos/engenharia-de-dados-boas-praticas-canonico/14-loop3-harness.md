# Boas práticas DE no canônico — Decisões de Harness (Loop 3)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Branch: `feat/de-agents-skills-loop3` @ `fa0ab0c`  
Fontes: `13-loop3-prd.md`, `12-loop3-grill.md`, `00d-codebase-loop3.md`, `09-loop2-harness.md`  
Modo: **evolução do framework canônico** — amarra catálogo agentic ao kernel; NÃO greenfield de app  
Judge PRD: **pulado** (decisões fechadas)

> **Estado deste artefato:** Harness Plan **aprovado** (2026-08-07). Tasks `25`–`32`
> criadas no mesmo passo de planejamento. **Não implementar** até `harness-build`.

---

# Harness Plan — Agents / Skills / KBs / Install (Loop 3 / Ship 3)

## Inferências confirmadas (sem lacunas bloqueantes)

| Cluster | Inferido |
|---|---|
| Escopo | 10 agents + 7 commands + pontes KB + KB databricks + skill `de-conformidade` + install completo |
| Propagação | `pipeline_dados` copia **todos** agents/commands DE |
| Kernel | A–D consumido, não reescrito |
| SI | c+d; sem live API; seed KEEP |
| Espelho | `.claude` ↔ `.cursor` |
| Tasks | 25–32 |

---

## Invariantes (sempre valem no Loop 3)

1. **Kernel é fonte da norma** — agents/KBs/skill apontam; não duplicam YAML.
2. **Amarras explícitas** — seção Kernel DE em cada agent (tabela do grill).
3. **Propagar completo** — 10 + 7 em `pipeline_dados` (fim do pacote “só mínimo”).
4. **Uma skill DE** — só `de-conformidade`.
5. **Espelho** obrigatório em artefatos agentic.
6. **Seed KEEP** — não regressar `seed: true`.
7. **Sem live API** no CI / skill / agents.
8. **Git hygiene** — branch `feat/de-agents-skills-loop3`; commit/push só com acordo.

---

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Amarrar 10 agents | `.claude/agents/data-engineering/*.md` (+ espelho) | Execução / estado | agentes, install |
| Amarrar 7 commands | `.claude/commands/data-engineering/*.md` (+ espelho) | Execução | humanos/agentes |
| Pontes KB (10) | `kb/{domínio}/index.md` (ou quick-ref) — âncora DE-* | Estado | agents JIT |
| KB databricks | `kb/databricks/**` + `_index.yaml` | Estado | lakehouse/platform/DQ |
| Skill conformidade | `skills/de-conformidade/SKILL.md` (+ refs) | Ferramentas | agents, humanos |
| Install completo | `stack_map.json` + `install-harness/SKILL.md` | Ferramentas | `/install-harness` |
| Reescrever freeze/install | `tests/data_engineering/test_freeze_*`, `test_install_*` | Validação | CI |
| Regressão examples | pytest validate 3 examples + fixture cópia | Validação | CI |
| Freeze DoD Loop 3 | novo baseline inventário + gate | Validação | ship |
| Sync contexto no ship | `CLAUDE.md` / `CONTEXT.md` / `AGENTS.md` (no ship, não agora) | Estado | agentes |

### Pilares

| Pilar | Cobertura Loop 3 |
|---|---|
| **Estado/memória** | KBs + pontes + amarras nos agents |
| **Ferramentas** | skill `de-conformidade` + install expandido |
| **Execução** | commands → agents → gate |
| **Validação** | freeze novo + regressão examples + fixture install |

---

## Amarras agent → pacote (contrato de implementação)

| Agent | Seção Kernel deve citar |
|---|---|
| todos | DE-A\*; `/validar` / CLI; baseline/waiver vs corrigir |
| `spark-engineer` | A + B |
| `pipeline-architect` | A + B + C |
| `data-quality-analyst` | A + DE-D003 + DE-D004 |
| `lakehouse-architect` | A + D |
| `data-platform-engineer` | A + D |
| `schema-designer` | A + DE-D004 |
| `dbt-specialist`, `sql-optimizer`, `streaming-engineer`, `data-contracts-engineer` | A (+ D se cloud/multi) |

---

## O que NÃO entra agora

| Item | Por quê |
|---|---|
| Reabrir checks D / perfis YAML | Loop 2 fechado |
| Live UC API | SI + CI |
| Segunda skill DE | Decisão 4 = uma skill |
| Remover pacote seed / KEEP | Invariante |
| Implementação das tasks | Planejamento only |

---

## Ordem de implementação (tasks)

| # | Task | Depende |
|---|---|---|
| 25 | `amarrar-agents-de-kernel` | none |
| 26 | `amarrar-commands-de` | 25 |
| 27 | `kbs-de-ponte-ids` | 25 |
| 28 | `kb-databricks` | 27 (recomendado) |
| 29 | `skill-de-conformidade` | 25 |
| 30 | `install-pipeline-dados-completo` | 25, 26, 28, 29 |
| 31 | `regressao-examples-install` | 30 |
| 32 | `freeze-loop3-dod` | 31 |

```text
25 → 26
25 → 27 → 28
25 → 29
(26 ∧ 28 ∧ 29) → 30 → 31 → 32
```

---

## O que foi “gerado” neste passo

Só o **plan** + tasks locais. Nenhuma edição ainda em agents/skills/kb/stack_map de produto.

### Planejado (pós `harness-build`)

- Evoluir 10 agents + 7 commands  
- Pontes em 10 KBs + domínio `databricks`  
- Skill `de-conformidade`  
- Expandir `pipeline_dados` + reescrever testes freeze/install  
- Freeze DoD Loop 3  

---

## Decisões contestáveis (ADRs futuros — não criar agora)

| Tema | Sugestão |
|---|---|
| Keywords Databricks no detector `pipeline_dados` | Manter keywords atuais; artefatos explícitos bastam no MVP Loop 3 |
| Skill no stack_map vs só doc | Incluir path da skill no stack_map (AC6) |
| Granularidade concepts KB databricks | 1 concept por DE-D00n vs agrupado — fechar na task 28 |

---

## Aprovação

**Status:** Harness Plan **aprovado** (decisões 1–4 fechadas pelo mantenedor, 2026-08-07).

## Próximo passo

1. ~~`/to-tasks`.~~ **Feito** — `tasks/25`–`32` + `tasks/README.md`.  
2. Dizer `harness-build` ou `implement task 25` para começar.  
3. **Não** implementar neste passo de planejamento.
