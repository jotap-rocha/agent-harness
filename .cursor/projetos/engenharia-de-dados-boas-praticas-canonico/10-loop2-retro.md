# Boas práticas de Engenharia de Dados no canônico — Retrospectiva Loop 2

Ship em: 2026-08-07  
Slug: `engenharia-de-dados-boas-praticas-canonico`  
Escopo: Tasks **17–24** (Databricks SDP + DLT)  
Branch de ship: `chore/ship-de-loop2` (a partir de `master` @ merge PR 215002)  
Implementação mergeada: PR **215002** → `master` @ `137922c`  
Delivery records: commit `4fd90b6`

> Não substitui `05-retro.md` (Loop 1). Este arquivo fecha só o Loop 2.

## GIT_PREFLIGHT no ship (soft-blocks registrados)

| Check | Resultado |
|---|---|
| `git fetch` / `git pull --ff-only` | **Falha 403** (proxy Azure) — soft-block conhecido; `origin/master` local já em `137922c` (PR 215002) |
| HEAD no tronco | **Não** — ship em `chore/ship-de-loop2` (git-hygiene: sem editar tronco sem acordo) |
| Working tree | Limpa no início do ship |
| Tag `prod-*` | **N/A** (fora do MVP) |
| Push / commit do ship | **Pendentes de acordo humano** (parent) |

### §1.3 — limites reais

Nenhum gate impede de fato sem Edit policies / branch protection. Hooks locais e soft-blocks
são contornáveis.

## Métricas de entrega (via /scorecard)

Fonte: `metrics/entregas.jsonl` (issues **17–24**). Tracker remoto (`gh`/`az` issues): **não medido**
(fetch/auth Azure limitados neste ambiente).

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 |
| Critérios de aceite atendidos | 100% (34/34) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 1 / 7 / 0 |
| Intervenções humanas (por delivery record) | 0 |
| Taxa de autonomia (records) | 100% (8/8) |
| Change-failure rate | 0 conhecido |
| Lead time | mesmo dia (2026-08-07) |
| Commit tip dos records | `4fd90b6` |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 17 | yaml-perfis-pacote-d | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 18 | engine-registry-detect | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 19 | checks-databricks-cloud | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 20 | baseline-profiles-array | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 21 | example-databricks-sdp-min | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 22 | example-databricks-dlt-min | 3/3 | verde (1) | aprovado | sim |
| 23 | validar-autodetect-espelho | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 24 | freeze-stackmap-regressao | 4/4 | verde (1) | aprovado c/ ressalvas | sim |

### Leitura para stakeholders

Kernel Databricks entregue no canônico: norma com três perfis + pacote D, engine com
auto-detect, baseline `profiles[]`, dois examples greenfield e `/validar` condicional
(marker **ou** SDP/DLT). Aceite 100% e gate verde na 1ª tentativa. 7/8 revisões com
ressalvas (0 bloqueantes) — típico de extensão de enforcement. `pipeline_dados` e
Loop 1 yarn permaneceram intactos (freeze Task 24). Loop 3 (agents/skills/KBs DE)
**não** entrou neste ship.

## O que funcionou bem

- Ordem adversarial: YAML/perfis → registry/detect → checks D ∥ baseline → examples → `/validar` → freeze.
- Override de marker vence auto-detect; DAB isolado não dispara data-check (evita falso positivo).
- Espelho `.claude` ↔ `.cursor` nas tasks de commands/rules (`/validar`, pipeline).
- Regressão explícita do example `spark-yarn-airflow-min` + freeze do `stack_map`.
- Checks D só em filesystem (sem API live / secrets) — alinhado a SI c+d.

## O que melhorar

- Ressalvas concentradas em detect/engine/checks (Tasks 18–19, 24): documentar globs e
  sentinel do canônico mais cedo no harness plan para reduzir ida-e-volta na revisão.
- `check_context_drift.py` ainda **não** detecta artefatos canônicos novos (yaml/CLI/examples
  Databricks) — sync do ship de novo exigiu inventário manual (mesmo gap do Loop 1).
- Fetch Azure 403 continua impedindo dogfood completo de PR/`az` neste ambiente.
- Decisões do grill/PRD/harness Loop 2 não viraram ADR formal (mesmo padrão dos ships anteriores).

## Armadilhas encontradas (para o próximo projeto / Loop 3)

- Canônico com examples Databricks internos: `validate .` na raiz pode resolver
  `databricks-multi`; o helper de `/validar` usa sentinel para **não** ativar data-check no
  framework — gate DE do ship = validate explícito nos examples.
- Ambiguidade SDP+DLT → `databricks-multi` + união de checks; baseline grava `profiles[]`
  lexicográfico — não confundir com `profile` singular legado.
- Soft-block de fetch não bloqueia ship se `origin/master` local já reflete o merge; registrar
  aviso e SHA, não fingir sync de rede.

## ADRs desta implementação

- Nenhuma ADR nova em `docs/adr/` para o Loop 2. Decisões ficaram em
  `.claude/projetos/engenharia-de-dados-boas-praticas-canonico/{07-loop2-grill,08-loop2-prd,09-loop2-harness}.md`.
- Existente (contexto): [ADR-001](../../../docs/adr/001-sincronia-de-contexto-no-fechamento.md) — sync no fechamento.
- Loop 1: ver `05-retro.md`.

## Drift no sync-context (ship)

| Fonte | Resultado |
|---|---|
| `check_context_drift.py --warn/--json` | `has_drift: false` (notas: sem HANDOFF.md; env vars não rastreadas; commits desde último CLAUDE.md) |
| Inventário manual | Drift semântico: `CLAUDE.md` / `CONTEXT.md` ainda descreviam só Loop 1 |
| Correção | Atualizados para perfis Databricks, pacote D, examples sdp/dlt, `/validar` marker\|SDP/DLT, baseline `profiles[]`; **sem** inventar Loop 3 |
| `sync_agents_from_claude.py --apply` | Regenera `AGENTS.md` após o CLAUDE.md |

## Harness — o que aprendemos

- Estender norma + CLI + examples **antes** de agents/skills (Loop 3) continua sendo o caminho
  certo: conformidade verificável sem inflar o catálogo agentic.
- Auto-detect útil (SDP/DLT) vs DAB isolado é invariante de produto — candidato a prose fixa
  em `rules/pipeline` / checklist do revisor.
- Gap do detector de drift canônico permanece candidato a melhoria da skill `sync-context`.
- Fase 0 do plano pós-Loop 2: ship/retro **antes** de abrir Loop 3 — cumprido neste artefato.
