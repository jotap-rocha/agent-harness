# Fluxo — Grafo Causal Real — Retrospectiva de Ship

Ship em: 2026-08-18  
Slug: `fluxo-grafo-causal`  
Branch: `feat/fluxo-grafo-causal`

## Métricas de entrega (via /scorecard)

| Métrica | Valor |
|---|---|
| Tasks entregues | 7 (75–81) |
| Critérios de aceite atendidos | 100% (25/25) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado/ressalvas/bloqueado | 7 / 0 / 0 |
| Intervenções humanas | 0 |
| Taxa de autonomia | 100% (7/7) |
| Change-failure rate (neste ship) | sem dado |
| Lead time / gh | sem dado (Azure; fetch 403) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 75 | emit-causal-ids | 5/5 | verde (1) | aprovado | sim |
| 76 | stack-parent-gitignore | 4/4 | verde (1) | aprovado | sim |
| 77 | cli-run-parent-flags | 1/1 | verde (1) | aprovado | sim |
| 78 | render-causal-svg | 5/5 | verde (1) | aprovado | sim |
| 79 | wiring-sdd-dev-causal | 3/3 | verde (1) | aprovado | sim |
| 80 | docs-adr-cheatsheet | 2/2* | verde (1) | aprovado | sim |
| 81 | validar-dogfood-causal | 3/3* | verde (1) | aprovado | sim |

\*Evidence-gate coletou critérios com teste; ADR addendum / dogfood visual com waiver docs onde aplicável.

## O que funcionou bem

- Schema aditivo (`version: 1`) sem quebrar eventos legados.
- Dois SVGs no mesmo `live.html` deixam claro previsto vs executado.
- Stack fail-soft + parent explícito cobrem wiring CLI e agents sem mutex.
- Suite `tests/fluxo_events/` chegou a 79 passed com ruff/mypy verdes.

## O que melhorar

- `.cursor/projetos/` RO neste host — espelho de evidencias/STATUS às vezes incompleto.
- `stack.json` em FS read-only gera warning soft (comportamento correto; UX barulhenta no dogfood).
- Ship antes do commit deixa `commit: pending` até o acordo de commit (este fluxo).

## Armadilhas encontradas

- `install-harness` só mudou mode bits (100644→100755) — fora do ship; não incluir no commit.
- Telemetria residual em `visao-grafica-fluxo-agentes/fluxo/` — não misturar neste PR.
- Sem `event_id` nos emits antigos o grafo causal fica órfão/parcial até o wiring novo rodar.

## ADRs desta implementação

- [ADR-005](../../../docs/adr/005-kernel-fluxo-events.md): addendum grafo causal
  (`event_id`/`run_id`/`parent_event_id`, stack, dois SVGs).

## Harness — o que aprendemos

- Identidade de evento é pré-requisito do SVG causal; mapa canônico sozinho não basta.
- Parent explícito + stack local escala sem fork do kernel.
- Drift automático limpo; sync manual de CLAUDE/CONTEXT ainda necessário para invariantes novos.

## Leitura para stakeholders

Pacote 75–81 entrega telemetria causal no painel live (IDs + stack + dois SVGs) com aceite
100% e autonomia total nesta sessão. Próximo risco: push/PR Azure (auth 403 local).
