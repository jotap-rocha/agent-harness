# Fluxo — Grafo Causal Real

## Ideia

Loop de implementação do **grafo causal real** do fluxo-events:

- Hoje o `live.html` tem fluxograma SVG do mapa **canônico previsto** (fases/agentes do contrato).
- Falta o grafo **causal de execução**: quem chamou quem de fato.
- Evolução do schema: adicionar `run_id` e `parent_event_id` aos eventos (metadados only).
- Compatível com eventos antigos (campos opcionais).
- Fail-soft; orthografia **fluxo** (x), nunca **flujo** (j).
- NÃO fork do kernel; estender `fluxo-events.yaml` + `config/fluxo_events/` + render SVG.
- Ortogonal a evidence-gate e agent-policies.
- Canvas/SSE continuam WON'T salvo se o usuário mudar no grill.

## SI Assessment

Nível: **a** — Não — apenas dados abertos, sintéticos ou públicos / metadados de processo

Implicações:
- Harness mínimo de SI (rules/seguranca.md já cobrem)
- Telemetria: só metadados (`run_id`, `parent_event_id`, agent, phase, timestamps) — sem PII, sem prompts, sem secrets
- Sem `[AVISO_LGPD]` / `rules/pii.md` neste escopo

## Tipo de Projeto

**e** — Outro: evolução do **harness canônico** (kernel fluxo-events)

Stack prevista:
- Contrato `fluxo-events.yaml` (schema de eventos + campos opcionais novos)
- Engine `config/fluxo_events/` (emit / load / render SVG)
- Painel `projetos/{slug}/fluxo/live.html` (mapa canônico + grafo causal de execução)
- Testes em `tests/fluxo_events/`; cheatsheet e ADR existentes como base

## Próximos passos

1. Rode `/grill-me` para aprofundar a ideia (schema `run_id`/`parent_event_id`, UX do SVG causal, compatibilidade com eventos antigos, escopo Canvas/SSE)
2. Ao terminar, use `harness-define` para estruturar os requisitos
3. Depois: `harness-design` → PRD + harness-architect
