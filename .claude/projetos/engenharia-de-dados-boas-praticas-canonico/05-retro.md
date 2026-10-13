# Boas práticas de Engenharia de Dados no canônico — Retrospectiva de Ship

Ship em: 2026-08-06  
Slug: `engenharia-de-dados-boas-praticas-canonico`  
Branch: `feat/de-boas-praticas-canonico` @ `195ec15` (alinhada a `origin/master` no fechamento)

## GIT_PREFLIGHT no ship (soft-blocks registrados)

| Check | Resultado |
|---|---|
| `git fetch` | **Falha 403** (proxy) — não tratado como sync confirmado; usuário validou alinhamento `master`/`feat`/`origin/master` via `rev-parse` + `0 0` |
| HEAD no tronco | **Não** — trabalho em `feat/de-boas-praticas-canonico` |
| Working tree | Limpa no início do ship |
| Tag `prod-*` | **N/A** (fora do MVP) |
| Push / PR do ship | **Pendentes de acordo humano** após commit de fechamento |

### §1.3 — limites reais

Nenhum gate impede de fato sem Edit policies / branch protection. Hooks locais e soft-blocks
são contornáveis.

## Métricas de entrega (via /scorecard)

Fonte: `metrics/entregas.jsonl` (issues **09–16**). Tracker remoto (`gh`/`az` issues): **não medido**
(fetch/auth Azure limitados neste ambiente).

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 |
| Critérios de aceite atendidos | 100% (37/37) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 4 / 4 / 0 |
| Intervenções humanas (por delivery record) | 0 |
| Taxa de autonomia (records) | 100% (8/8) |
| Change-failure rate | 0 conhecido |
| Lead time mediano | mesmo dia (2026-08-06) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 09 | yaml-contrato-loader | 4/4 | verde (1) | aprovado | sim |
| 10 | cli-validate-abc | 5/5 | verde (1) | aprovado | sim |
| 11 | example-spark-yarn-min | 5/5 | verde (1) | aprovado | sim |
| 12 | baseline-compare-waiver | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 13 | report-explain | 4/4 | verde (1) | aprovado | sim |
| 14 | relatorio-ro-sql-capacity | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 15 | install-pacote-minimo | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 16 | validar-rule-espelho | 5/5 | verde (1) | aprovado c/ ressalvas | sim |

### Leitura para stakeholders

Kernel de conformidade DE entregue no canônico: norma executável + CLI + example + baseline/waiver
+ install mínimo + `/validar` condicional, **sem** novos agents/skills/KBs DE. Aceite 100% e gate
verde na 1ª tentativa. Metade das revisões veio com ressalvas (seed-once, RO, prosa) — típico de
enforcement novo. O commit de metrics (`c253ab0`) ficou fora do 1º PR e exigiu 2º merge +
realinhamento de branches — fricção de processo, não de produto.

## O que funcionou bem

- Ordem adversarial respeitada: norma → validator → baseline/waiver → example → install → `/validar`.
- Espelho `.claude` ↔ `.cursor` mantido nas tasks de install/commands/rules.
- Seed-once (`seed: true` → KEEP) corrigiu o risco real de apagar baseline/waivers no re-install.
- Fixture `_secret_fixtures.credential_assignment` evitou falso positivo do pre-commit sem enfraquecer checks DE.
- Relatório RO do sql-capacity sem escrita no alvo (invariante SI preservada).

## O que melhorar

- Delivery records no **mesmo** PR do kernel (ou PR metrics imediatamente após) para não divergir tip da feat vs merge Azure.
- Cherry-pick local vs merge PR no Azure gerou SHAs diferentes para o mesmo conteúdo — documentar “fonte da verdade = origin/master pós-merge”.
- `check_context_drift.py` ainda **não** detecta artefatos canônicos novos (yaml/CLI/example) — sync do ship precisou de inventário manual de novo.
- Decisões do grill/PRD/harness DE não viraram ADR formal (mesmo padrão do ship git-hygiene).

## Armadilhas encontradas (para o próximo projeto)

- Após merge Azure, tip da feat ≠ tip da master (merge commit) — esperado; “mesmo ponto” = mesmo SHA só após reset da feat para `origin/master` (ou FF).
- Commit feito **depois** do PR aberto/mergeado não entra sozinho — precisa push + novo PR ou cherry-pick consciente.
- Literais de assignment de credencial em testes (ex.: campo password/api_key) disparam o pre-commit de segredos; montar a linha em runtime via helper.
- Hook `Stop` ≠ `/validar` condicional DE (de propósito no ship mínimo) — não prometer paridade total.

## ADRs desta implementação

- Nenhuma ADR nova em `docs/adr/` para o Loop 1. Decisões ficaram em
  `.claude/projetos/engenharia-de-dados-boas-praticas-canonico/{01-grill,02-prd,03-harness}.md`.
- Existente (contexto): [ADR-001](../../../docs/adr/001-sincronia-de-contexto-no-fechamento.md) — sync no fechamento.

## Harness — o que aprendemos

- Pacote mínimo verificável (`pipeline_dados`) prova conformidade **antes** de expandir catálogo agentic (Loops 2/3).
- `seed: true` no stack_map é invariante de runtime do filho — candidato a rule/checklist fixo do `install-harness` / revisor.
- Drift de contagens/artefatos do canônico continua buraco do `check_context_drift.py` — candidato a extensão do detector.
- Fetch 403 no proxy continua impedindo dogfood completo de PR via `az` neste ambiente.
