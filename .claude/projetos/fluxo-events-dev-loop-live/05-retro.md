# Fluxo-events Dev Loop + backfill — Retrospectiva de Ship

Ship em: 2026-08-17  
Slug: `fluxo-events-dev-loop-live`  
Branch: `feat/fluxo-events-dev-loop-live`

## Métricas de entrega (via /scorecard)

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 (67–74) |
| Critérios de aceite atendidos | 100% (26/26) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado/ressalvas/bloqueado | 6 / 2 / 0 |
| Intervenções humanas | 0 |
| Taxa de autonomia | 100% (8/8) |
| Change-failure rate (neste ship) | sem dado (sem reopen/bug pós-done) |
| Lead time / gh | sem dado (Azure; fetch 403; sem `gh` neste ciclo) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 67 | contrato-dev-loop-map | 3/3 | verde (1) | aprovado | sim |
| 68 | helper-slug-from-prompt | 3/3 | verde (1) | aprovado | sim |
| 69 | render-dual-map-dev | 3/3 | verde (1) | aprovado | sim |
| 70 | wiring-ux-crafter-executor | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 71 | truncate-exit-complete | 3/3 | verde (1) | aprovado | sim |
| 72 | backfill-commits-58-65 | 3/3 | verde (1) | aprovado | sim |
| 73 | guardrail-naming-ptbr | 3/3 | verde (1) | aprovado | sim |
| 74 | docs-validar-dogfood | 4/4 | verde (1) | aprovado c/ ressalvas | sim |

## O que funcionou bem

- Extensão do kernel existente (mapa dual + helper) sem fork nem event_types novos.
- Test-first + suite `tests/fluxo_events/` (55 passed) manteve o gate previsível.
- Backfill one-shot 58–65 → `e4dfc69` e guardrail PT-BR fecharam dívidas do ship anterior.
- Evidence-gate hard revalidado no ship (67–74 verdes).

## O que melhorar

- Mirror `.cursor/projetos/dev-loop-*` pode falhar soft (FS/mount) — documentar no wiring.
- CLI `evidence_gate check --entregas` com quirk de resolução relativa a `metrics/` (pré-existente).
- Ship antes do commit deixa `commit: pending` até o acordo de commit (este fluxo).

## Armadilhas encontradas (para o próximo projeto)

- Orthografia **flujo** (x) vs **flujo** (j): só o guardrail mecânico no pacote evita regressão.
- Soft-block `git fetch` Azure 403: não fingir sync com remote.
- Working tree “suja” durante ship+commit na mesma sessão é esperado; não stash sem acordo.

## ADRs desta implementação

- [ADR-005](../../../docs/adr/005-kernel-fluxo-events.md): addendum Dev Loop live (`dev_loop_map`,
  slug sintético, truncate no `EXIT_COMPLETE`, guardrail naming).

## Harness — o que aprendemos

- Aviso UX no enter Dev Loop fecha o buraco do MVP SDD-only (task 66).
- `dev_loop_map` + prefixo de slug escala o painel sem segundo kernel.
- Drift automático (`check_context_drift`) veio limpo; sync manual de CLAUDE/CONTEXT ainda
  necessário para invariantes novos (`dev_loop_map`, aviso Dev Loop).
- Telemetria continua ortogonal a evidence-gate e agent-policies (§1.3).

## Leitura para stakeholders

Pacote 67–74 entrega telemetria live no Dev Loop, higiene de commits 58–65 e guardrail de
naming PT-BR, com aceite 100% e autonomia total nesta sessão. Risco residual: commit/push e
PR Azure ainda dependem de acordo + auth (fetch 403).
