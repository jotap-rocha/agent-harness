# Policies Anti-Destrutivas — Retrospectiva de Ship

Ship em: 2026-08-13

## GIT_PREFLIGHT no ship (soft-blocks registrados)

| Check | Resultado |
|---|---|
| `git fetch` | **Falha 403** (proxy) — soft-block didático; não tratado como sync remoto novo |
| HEAD no tronco | **`master`** pós-merge PR 215670 (`8bec96f`) — exceção **explícita do usuário** para documentação de encerramento (código já na linha principal) |
| Working tree | Limpa; `HEAD == origin/master` (`8bec96f`) no momento do ship |
| Tag `prod-*` | **N/A** — não criada |
| Commit / push de ship | **Pendentes de acordo humano novo** — só artefatos de retro/STATUS escritos |

### §1.3 — limites reais

Deny/hooks locais ≠ Edit policies / branch protection. Bypass `HARNESS_ALLOW_DESTRUCTIVE=1`,
`--no-verify` e clone sem hooks existem. Nenhum gate impede de fato sem controle server-side.

## Métricas de entrega (via /scorecard)

Fonte: `metrics/entregas.jsonl` (issues 41–48). Tracker remoto (`gh`/`az` issues): **não medido**
(SCM Azure DevOps; `gh` não é a fonte deste repo). Gate local: **47 testes** coletados em
`tests/agent_policies`.

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 (41–48) |
| Critérios de aceite atendidos | 100% (36/36) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 6 / 2 / 0 |
| Intervenções humanas (por delivery record) | 0 |
| Taxa de autonomia (records) | 100% (8/8) |
| Change-failure rate | 0 conhecido (sem tracker de reopen/bug; task 47 teve bloqueantes sanados antes do merge) |
| Lead time mediano | mesmo dia (2026-08-13) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 41 | contrato-yaml-loader | 4/4 | verde (2) | aprovado | sim |
| 42 | matcher-deny-ask | 4/4 | verde (1) | aprovado | sim |
| 43 | bypass-fail-modes | 4/4 | verde (1) | aprovado | sim |
| 44 | catalog-core-families | 4/4 | verde (1) | aprovado | sim |
| 45 | generate-dual-artifacts | 4/4 | verde (1) | aprovado | sim |
| 46 | hooks-dual-runtime | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 47 | seed-install-foundation | 5/5 | verde (2) | aprovado (bloqueantes sanados) | sim |
| 48 | docs-adr-dogfood-sync | 6/6 | verde (1) | aprovado c/ ressalvas | sim |

### Leitura para stakeholders

Kernel agent-policies dual Claude↔Cursor fechou com aceite 100%, autonomia por record 100% e
merge na master via PR 215670. Ressalvas concentradas em UX ask (Claude vs Cursor) e KEEP
estático do deny no re-install — não bloqueantes. Judge adversarial pulado (b) no define e no
PRD; não atrapalhou a entrega, mas removeu uma segunda opinião formal no plano.

## O que funcionou bem

- Fatias 41→48 com contrato YAML único + engine compartilhada (match/generate/guard) antes dos
  adapters — paridade Claude↔Cursor sem drift manual de política.
- Bypass explícito `HARNESS_ALLOW_DESTRUCTIVE=1` + fail closed/open documentados; `DE-A002`
  mantido ortogonal (código versionado ≠ freio de sessão).
- Install foundation always-on com `deny ≠ []` + seed `.harness/policies` KEEP corrige gap
  histórico do filho nascer sem freio.
- 47 testes `agent_policies` como gate concreto; ADR-003 + cheatsheet + ponte SI fechando docs.

## O que melhorar

- Ask: UX Claude vs Cursor ainda assimétrica (ressalva task 46) — candidata a checklist fixo /
  dogfood IDE, não só fixtures stdin.
- Re-install: deny estático KEEP (ressalva task 48) — documentar expectativa vs regenerate
  explícito para quem espera “sempre o YAML atual” no filho.
- Task 47 exigiu 2ª tentativa no gate e sanar bloqueantes do revisor (seed `families:` /
  profile no guard) — wiring install+seed merece fixture mais cedo no tracer-bullet.
- Judge pulado (b) no define e PRD — se o plano for contestável de novo, rodar judge pelo menos
  no PRD.

## Armadilhas encontradas (para o próximo projeto)

- Soft-block de tronco vs ship pós-merge: documentar exceção cedo (STATUS/retro) quando o
  trabalho já está em `master` e o ship é só encerramento documental.
- Fetch Azure 403 neste ambiente continua: não fingir sync remoto; PR já existia (215670).
- Não unificar kernels DE-A002 e agent-policies — cross-link só; tentação de “um freio só”
  gera falso negativo de escopo.

## ADRs desta implementação

- [ADR-003](../../../docs/adr/003-kernel-agent-policies-dual-runtime.md): kernel agent-policies
  dual-runtime (YAML + match/generate/guard + hooks Claude/Cursor; bypass; fail modes;
  ortogonal a DE-A002; §1.3 honesty).

## Harness — o que aprendemos

- Capturou certo: espelho `.claude`↔`.cursor`, install foundation always-on, rule SI ponte curta,
  scorecard via `entregas.jsonl`.
- Faltou como skill/hook: asserção automática de paridade UX ask entre runtimes (hoje só
  contratos de I/O).
- Quase-violação: falsa sensação de Edit policies — §1.3 e cheatsheet mitiga; bypass env é
  consciente, não substitui ADR/DDL produção.
- Drift sync no ship: `check_context_drift.py --warn` → **nenhum drift**; `AGENTS.md` já em
  sync com `CLAUDE.md`; agent-policies já declarado em CLAUDE/CONTEXT do build — residual
  trivial (HANDOFF.md ausente opcional; env vars não rastreadas no canônico).
