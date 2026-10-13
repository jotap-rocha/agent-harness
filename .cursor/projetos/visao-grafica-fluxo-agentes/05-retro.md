# Visão gráfica do fluxo de agentes — Retrospectiva de Ship

Ship em: 2026-08-13

## Métricas de entrega (via /scorecard — derivado de `metrics/entregas.jsonl`)

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 (58–65) |
| Critérios de aceite atendidos | 100% (33/33) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado/ressalvas/bloqueado | 4/4/0 |
| Intervenções humanas | 0 (nas linhas de entrega) |
| Taxa de autonomia | 100% (8/8 sem intervenção humana registrada) |
| Evidence-gate revalidado no ship | 8/8 ok |
| Suite `tests/fluxo_events/` | 26 passed |
| Commit SHA | pending (acordo pós-ship) |

Gaps de scorecard: `git fetch` 403 (sem sync remoto); `gh`/Azure PR não medidos; `commit: "pending"` em todas as entregas 58–65.

## O que funcionou bem

- Fatias verticais 58→65 com evidence-gate hard e `evidencias_ref` desde o início.
- Kernel ortogonal (`fluxo-events` ≠ evidence-gate ≠ agent-policies ≠ `/validar`) manteve o DoD intacto.
- Fail-soft de telemetria: emit/render/truncate não bloquearam o fluxo SDD.
- Dogfood no próprio slug (live + truncate no ship) validou o caminho feliz.
- Wiring enter/exit nos agents/skills SDD sem criar “fluxo officer”.

## O que melhorar

- Naming: build chegou a renomear **fluxo→flujo** (ES); parent corrigiu para **fluxo** (PT-BR, `chr(0x78)`), consolidou pastas e ajustou testes — custo de atrito evitável com check mecânico de orthografia no gate.
- 4/8 tasks com “aprovado com ressalvas” (58, 61, 62, 64) — ressalvas tipicamente de honestidade §1.3 / wiring; vale checklist pré-revisor.
- Working tree grande acumulada até o ship (pedido explícito de commit único) — OK para este fluxo, mas dificulta bisect.

## Armadilhas encontradas (para o próximo projeto)

- Homófonos / cognatos ES↔PT (`flujo` vs `fluxo`) em paths e seeds quebram install e testes silenciosamente.
- Residual ainda presente: `.claude/projetos/visao-grafica-flujo-agentes/` (slug com **j**) contendo `fluxo/events.jsonl` + `live.html` de emit errado — **não apagado neste ship** (operação destrutiva sem acordo).
- `git fetch` 403 via proxy: GIT_PREFLIGHT soft — não tratar working tree como sync com remoto.
- `assert events_path` (função) falhou mypy `truthy-function` — smoke de import deve usar `callable(...)`.

## ADRs desta implementação

- [ADR-0005](../../../docs/adr/005-kernel-fluxo-events.md): kernel `flujo-events` telemetria live SDD (fail-soft, foundation, sem SSE, truncate N=100 no ship).

## Harness — o que aprendemos

- Capturou certo: foundation always-on + seed KEEP; cheatsheet + `/fluxo-live`; dual-tree `.claude`/`.cursor`.
- Faltou no harness: guardrail de naming PT-BR para artefatos novos (candidato a check em `/validar` ou teste de contrato `chr(0x78)` genérico para slugs/paths).
- Drift sync: CLAUDE/AGENTS/CONTEXT não citavam fluxo-events antes do ship — contagem de commands 23→24; invariante + tabela “onde fica” adicionados.
- Telemetria live é complementar: STATUS/scorecard/evidence-gate continuam a fonte de fechamento.

---

## Pós-ship — task 66 (2026-08-17)

Fatia UX na branch `chore/tasks-por-slug`: aviso ao usuário no enter SDD (brainstorm/build) +
reforço `/fluxo-live`. Evidence-gate 4/4; suite fluxo_events 30 passed. Detalhe e métricas da
chore em [`.claude/projetos/chore-tasks-por-slug/05-retro.md`](../chore-tasks-por-slug/05-retro.md).
