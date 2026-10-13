# Boas práticas de Engenharia de Dados no canônico

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Iniciado em: 2026-08-06  
Branch atual: `feat/de-agents-skills-loop3` (base ship Loop 2 `fa0ab0c`)

## SI Assessment: Nível c + d *(confirmado Loops 2–3)*

- c) PII em projetos-filhos de pipeline
- d) Risco de escrita/deleção em produção

## Tipo: e — evolução do harness / framework de conformidade DE

## Fase atual: CONCLUÍDO — Loops 1–3 shipados (catálogo agentic DE)

## Checklist

### Loop 1 (Ship 1) — arquivado
- [x] 0–6. Kernel `spark-yarn-airflow` + ship (`05-retro.md`) (2026-08-06)

### Loop 2 (Databricks) — arquivado
- [x] 0–6. Kernel Databricks + ship (`10-loop2-retro.md`) (2026-08-07)

### Loop 3 (Agents / skills / KBs DE)
- [x] 0. Ideia (`11-loop3-ideia.md`) + branch `feat/de-agents-skills-loop3` (2026-08-07)
- [x] 0b. Codebase map (`00d-codebase-loop3.md`) (2026-08-07)
- [x] 1. Grill (`12-loop3-grill.md`) (2026-08-07)
- [x] 2. PRD (`13-loop3-prd.md`) (2026-08-07) — **aprovado** (decisões do plano)
- [x] 3. Harness Plan (`14-loop3-harness.md`) (2026-08-07) — **aprovado**
- [x] 4. Tasks `25`–`32` + `tasks/README.md` (2026-08-07)
- [x] 5.1–5.8 Tasks 25–32 implementação + gates (2026-08-07)
- [x] 5. Implementação Loop 3 concluída (25–32) (2026-08-07)
- [x] 6. Ship / retrospectiva Loop 3 (`15-loop3-retro.md`) (2026-08-07)

## Acordos registrados (Loop 3)

| Decisão | Escolha |
|---|---|
| Entrada | Ship Loop 2 antes de abrir Loop 3 |
| Escopo MVP | Agents + skills + KBs + propagar install |
| Propagação | Todos os 10 agents + 7 commands DE em `pipeline_dados` |
| Artefatos novos | Evoluir existentes + skill `de-conformidade` + KB `databricks` |
| SI | permanece c + d |
| Slug | mesmo `engenharia-de-dados-boas-praticas-canonico` |

## Soft-blocks / avisos

- `git fetch` → autenticação Azure DevOps indisponível (403); builds usaram refs locais.
- sql-capacity: manter RO salvo acordo explícito + ADR.
- Lanes PASS/FAIL/WAIVED no `revisor-codigo` ficaram **fora** do MVP Loop 3.
