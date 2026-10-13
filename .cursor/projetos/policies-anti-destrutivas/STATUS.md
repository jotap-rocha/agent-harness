# Policies Anti-Destrutivas
Slug: policies-anti-destrutivas
Iniciado em: 2026-08-12

## SI Assessment: Nível d

## Tipo: e — Evolução do harness canônico (Edit policies + hooks)

## Fase atual: CONCLUÍDO — Projeto arquivado

## Checklist
- [x] 0. Ideia + SI assessment (2026-08-12)
- [x] 0b. Codebase-explorer → `00b-codebase.md` (2026-08-12)
- [x] 1. Grill concluído → `01-grill.md` (2026-08-12; define enriquecido 2026-08-12)
- [x] 2. PRD gerado → `02-prd.md` (2026-08-12)
- [x] 3. Harness montado → `03-harness.md` (2026-08-12)
- [x] 4. Tasks criadas → `tasks/41–48` (2026-08-12)
- [x] 5. Implementação concluída (2026-08-13)
- [x] 6. Ship / retrospectiva (2026-08-13)

## Resultado final

Kernel `agent-policies` dual Claude↔Cursor entregue e mergeado na master (PR 215670,
`8bec96f`): contrato YAML, match/generate/guard, hooks, install foundation (`deny ≠ []`),
bypass `HARNESS_ALLOW_DESTRUCTIVE`, ADR-003 e cheatsheet. Tasks 41–48 done; aceite 100%
(36/36); 47 testes `agent_policies`.

## Git
- Código: mergeado em `master` via PR 215670 (merge `8bec96f`; tip feat `9892c49`)
- Branch de trabalho histórica: `feat/policies-anti-destrutivas` (base `a226042`)
- Ship: artefatos `05-retro.md` + STATUS no tronco **somente** por pedido explícito pós-merge
- Nota: `git fetch` pode falhar 403/proxy — não fingir sync remoto novo
- Commit/push dos artefatos de ship: **pendente de acordo explícito**

## Decisões-chave (grill)
- YAML `agent-policies.yaml` + paridade Claude↔Cursor
- Híbrido deny/ask; catálogo completo; core+terraform+k8s always-on; extras opt-in
- Bypass `HARNESS_ALLOW_DESTRUCTIVE`; DE-A002 ortogonal; sem Edit policies server-side
- Vault: N/A — sem key vault (runtime policies)
- Define: SLA hook local + especificações implícitas (lentes 1–10) registradas
- Adversarial judge: **(b)** pulado no define e no PRD (2026-08-12)

## Tasks
- 41 contrato-yaml-loader → 48 docs-adr-dogfood-sync — **todas done** (ver `tasks/README.md`)

## Artefatos de ship
- Retrospectiva: `05-retro.md`
- ADR: `docs/adr/003-kernel-agent-policies-dual-runtime.md`
- Métricas: `metrics/entregas.jsonl` (issues 41–48)
