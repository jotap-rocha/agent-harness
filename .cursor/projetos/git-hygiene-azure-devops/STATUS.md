# Git Hygiene Azure DevOps no Harness
Slug: git-hygiene-azure-devops
Iniciado em: 2026-08-06

## SI Assessment: Nível b

Metadados de acesso e repositórios; sem PII direto. PAT/secrets via env; métricas
agregadas por repo.

## Tipo: e — Evolução do framework / Agent Harness Canônico

## Fase atual: CONCLUÍDO — Projeto arquivado

## Checklist
- [x] 0. Ideia + SI assessment (2026-08-06)
- [x] 1. Grill concluído (2026-08-06) — ver `01-grill.md`
- [x] 2. PRD gerado (2026-08-06) — ver `02-prd.md`
- [x] 3. Plano de implementação no canônico (2026-08-06) — ver `03-harness.md`
- [x] 4. Tasks criadas (2026-08-06) — ver `tasks/` (01–08, A1–A15)
- [x] 5. Implementação concluída (2026-08-06) — tasks 01–08 done
- [x] 6. Ship / retrospectiva (2026-08-06) — ver `05-retro.md`

## Resultado final

Camada Convenção (Fase 1) entregue no canônico: contrato `git-hygiene.yaml`, rule, cheatsheet
(§1.3), hooks, `/nova-branch`, `/git-ajuda`, adapter PR híbrido, wiring `GIT_PREFLIGHT`,
template Azure e propagação via `install-harness`. Aceite 38/38; tag `prod-*` N/A; push/PR
pendentes de acordo humano.

## Artefatos
- `00-ideia.md` / `00b-codebase.md` / `01-grill.md` / `02-prd.md` / `03-harness.md` / `05-retro.md`
- Tasks: `tasks/01` … `tasks/08` + `tasks/README.md` (todas done)
- Contrato: `git-hygiene.yaml` + `config/git_hygiene/` + `tests/git_hygiene/`
- Cheatsheet / commands / rule / hooks / template / adapter / wiring / stack_map
- Contexto sincronizado: `CLAUDE.md` · `CONTEXT.md` · `AGENTS.md`

## Próximo passo
Push/PR sob acordo humano. Novo projeto: `harness-brainstorm` ou `/novo-projeto`.
