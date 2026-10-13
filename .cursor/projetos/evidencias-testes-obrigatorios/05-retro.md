# Evidências e Testes Obrigatórios — Retrospectiva de Ship

Ship em: 2026-08-13

## GIT_PREFLIGHT no ship (soft-blocks registrados)

| Check | Resultado |
|---|---|
| Branch | **`feat/evidencias-testes-obrigatorios`** (trabalho ainda na feature — **não** mergeado na `master`) |
| `git fetch` | **Falha 403** (proxy Azure) — soft-block didático; não tratado como sync remoto |
| HEAD no tronco | Não — feature isolada OK |
| Working tree | **Suja** (build completo não commitado: kernel, tests, tasks, docs, wiring) — soft-block; stash/commit **somente com acordo** |
| Tag `prod-*` | **N/A** — não criada |
| Commit / push de ship | **Pendentes de acordo humano** — retro/STATUS gravados sobre árvore suja |

### §1.3 — limites reais

Evidence-gate (manifesto forjável) ≠ Edit policies / branch protection. Sem controle server-side,
nenhum gate impede de fato. Ortogonal a `agent-policies` (Bash deny ≠ aceite).

## Evidence-gate revalidação (dogfood no ship)

Root: `.claude/projetos/evidencias-testes-obrigatorios/evidencias`

| Task | `check` | Nota |
|---|---|---|
| 49–52 | **fail** (manifesto ausente) | Gap honesto: entregas **sem** `evidencias_ref`; wiring DoD/build só a partir da 53 |
| 53 | ok (exit 0) | `evidencias_ref` presente |
| 54 | ok (exit 0) | `evidencias_ref` presente |
| 55 | ok (exit 0) | `evidencias_ref` presente |
| 56 | ok (exit 0) | `evidencias_ref` presente |

**Decisão de ship:** encerramento documental com gap explícito em 49–52 (não inventar logs).
Suite global: **40** testes coletados em `tests/evidence_gate/`.

## Métricas de entrega (via /scorecard)

Fonte: `metrics/entregas.jsonl` (issues 49–56). Tracker remoto (`gh`/`az` issues): **não medido**
(SCM Azure DevOps; fetch 403 neste ambiente). Commits: `pending-no-commit` em todos os records.

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 (49–56) |
| Critérios de aceite atendidos | 100% (33/33) |
| Tentativas medianas até gate verde | 1.5 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 3 / 5 / 0 |
| Intervenções humanas (por delivery record) | 0 |
| Taxa de autonomia (records) | 100% (8/8) |
| `evidencias_ref` nos records | 4/8 (53–56; gap 49–52) |
| Change-failure rate | 0 conhecido (sem tracker de reopen; bloqueantes sanados antes do veredito final) |
| Lead time mediano | mesmo dia (2026-08-13) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | `evidencias_ref` | Autônoma |
|---|---|---|---|---|---|---|
| 49 | contrato-yaml-loader | 4/4 | verde (2) | aprovado c/ ressalvas | **não** | sim |
| 50 | collect-run-logs | 4/4 | verde (2) | aprovado c/ ressalvas | **não** | sim |
| 51 | check-manifest-ref | 4/4 | verde (2) | aprovado c/ ressalvas | **não** | sim |
| 52 | audit-append-only | 4/4 | verde (1) | aprovado | **não** | sim |
| 53 | wiring-build-ship | 4/4 | verde (2) | aprovado c/ ressalvas | sim | sim |
| 54 | install-foundation-seed | 4/4 | verde (1) | aprovado | sim | sim |
| 55 | dod-agents-totasks | 4/4 | verde (1) | aprovado | sim | sim |
| 56 | docs-adr-sync | 5/5 | verde (1) | aprovado c/ ressalvas | sim | sim |

### Leitura para stakeholders

Kernel evidence-gate (`collect|check` + manifesto + audit append-only + foundation + DoD) fechou
com aceite 100% e 40 pytest verdes, ainda **só na branch feature** (não mergeado). Ressalvas
concentradas no início do kernel e no wiring; bloqueantes corrigidos. Gap dogfood 49–52 é
esperado (gate ainda não existia para auto-provar) — candidata a backfill opcional, não a
reabrir o aceite das fatias.

## O que funcionou bem

- Contrato YAML único (`evidence-gate.yaml`) + engine `config/evidence_gate/` (`collect|check`,
  cap 2 MiB, LWW manifesto, audit append-only) antes do wiring build/ship.
- Install foundation + seed `.harness/evidence-gate/` KEEP; command `/evidencias`; ADR-004 +
  cheatsheet + sync CLAUDE/CONTEXT/AGENTS.
- DoD / harness-build / harness-ship / to-tasks / revisor amarrados a `evidencias_ref` sem
  confundir com `/validar` nem com agent-policies.
- SI nível **a**; sem Stop dual (decisão consciente — gate hard no build/ship, não no Stop).

## O que melhorar

- Backfill opcional de manifesto/`evidencias_ref` para 49–52 (ou waiver explícito no critério)
  para o scorecard e o ship revalidate ficarem 8/8.
- Índice de `tasks/README.md` ficou “not started” enquanto a seção 49–56 já estava **done** —
  corrigido no ship; evitar drift de dashboard.
- Judge adversarial **(b) pulado** no define e no PRD — segunda opinião formal ausente; se o
  próximo kernel for contestável, rodar judge pelo menos no PRD.
- Ressalvas recorrentes (5/8) — capturar padrões de review cedo (fixtures/wiring) para baixar
  tentativas medianas abaixo de 1.5.

## Armadilhas encontradas (para o próximo projeto)

- Ship com árvore **suja** + fetch 403: documentar soft-blocks; não stash/commit sem acordo;
  retro/STATUS podem ir sobre o estado do build.
- Feature ainda **não** na master (diferente do ship de policies): PR/híbrido SCM só após acordo
  de commit+push.
- Dogfood do evidence-gate só cobre fatias pós-wiring — declarar gap cedo no STATUS/retro para
  não fingir `check` verde em 49–52.

## ADRs desta implementação

- [ADR-004](../../../docs/adr/004-kernel-evidence-gate.md): kernel evidence-gate (YAML +
  collect/check + manifesto/logs/audit + foundation + DoD wiring; ortogonal a `/validar` e
  agent-policies; §1.3 honesty — manifesto forjável).

## Harness — o que aprendemos

- Capturou certo: espelho `.claude`↔`.cursor`, DoD com evidence-gate hard, scorecard via
  `entregas.jsonl`, ADR + cheatsheet.
- Faltou: enforcement mecânico de `evidencias_ref` **desde a primeira task** do fluxo (hoje o
  wiring nasce na fatia 53 — chicken-and-egg do próprio kernel).
- Quase-violação: fechar ship com `check` ≠ 0 em 49–52 — mitigado por gap honesto + instrução
  explícita de não inventar logs.
- Drift sync no ship: `check_context_drift.py --warn` → **nenhum drift**; `AGENTS.md` em sync
  com `CLAUDE.md`. Correção pontual só no índice de `tasks/README.md`.
