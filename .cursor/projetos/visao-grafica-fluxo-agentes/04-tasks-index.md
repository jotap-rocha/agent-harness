# Tasks index — Visão Gráfica do Fluxo de Agentes

Slug: `visao-grafica-fluxo-agentes`  
Branch: `feat/visao-grafica-fluxo-agentes`  
Pasta de tasks: `tasks/visao-grafica-fluxo-agentes/`  
Fontes: `02-prd.md`, `03-harness.md`  
Aprovado (granularidade): 2026-08-13 · Ship: 2026-08-13

## Objetivo

Kernel `fluxo-events` (contrato + emit/render/truncate + live.html SDD 0–4) + wiring
agents + install foundation + docs; dogfood no próprio projeto.

## Tasks (58–65)

| # | File | Status | Blocked by | AC PRD |
|---|---|---|---|---|
| 58 | `tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md` | done | none | AC1, AC15 |
| 59 | `tasks/visao-grafica-fluxo-agentes/59-cli-emit-jsonl.md` | done | 58 | AC2, AC5, AC7, AC10 |
| 60 | `tasks/visao-grafica-fluxo-agentes/60-render-live-html.md` | done | 58 | AC3, AC4, AC5, AC17 |
| 61 | `tasks/visao-grafica-fluxo-agentes/61-rotate-truncate-ship.md` | done | 59, 60 | AC6, AC8 |
| 62 | `tasks/visao-grafica-fluxo-agentes/62-wiring-sdd-emit.md` | done | 59–61 | AC11, AC14, AC16 |
| 63 | `tasks/visao-grafica-fluxo-agentes/63-install-foundation-seed.md` | done | 58–61 | AC9 |
| 64 | `tasks/visao-grafica-fluxo-agentes/64-docs-adr-fluxo-live.md` | done | 58 | AC13, AC18 |
| 65 | `tasks/visao-grafica-fluxo-agentes/65-validar-dogfood-slug.md` | done | 62, 63, 64 | AC11, AC12 |
| 66 | `tasks/visao-grafica-fluxo-agentes/66-aviso-ux-painel-live.md` | done | none | UX aviso SDD |

## Próximo passo

Tasks **58–66 done**. Ver `05-retro.md` / STATUS. Task 66 = aviso UX (chore/tasks-por-slug).
