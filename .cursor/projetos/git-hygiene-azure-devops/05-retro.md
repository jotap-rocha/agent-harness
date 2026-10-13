# Git Hygiene Azure DevOps — Retrospectiva de Ship

Ship em: 2026-08-06

## GIT_PREFLIGHT no ship (soft-blocks registrados)

| Check | Resultado |
|---|---|
| `git fetch` | **Falha 403** (proxy) — não tratado como sync confirmado |
| HEAD no tronco | **`master`** — exceção **explícita do usuário** (recusou `/nova-branch`); não reaberta |
| Working tree | Untracked de artefatos do projeto + `sketch/` — versionados no commit de fechamento |
| Tag `prod-*` | **N/A nesta fase** (fora do MVP / grill+PRD) — não criada |
| Push / PR | **Pendentes de acordo humano** — payload preparado abaixo; sem push |

### §1.3 — limites reais

Nenhum gate impede de fato sem Edit policies / branch protection. Hooks locais e soft-blocks
são contornáveis (`--no-verify`, clone sem bootstrap). Critérios A1–A15 não afirmam bloqueio
server-side.

## Métricas de entrega (via /scorecard)

Fonte: `metrics/entregas.jsonl` (8 records). Tracker remoto (`gh`/`az` issues): **não medido**
(`az` ausente; SCM Azure DevOps).

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 |
| Critérios de aceite atendidos | 100% (38/38) |
| Tentativas medianas até gate verde | 1 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 1 / 7 / 0 |
| Intervenções humanas (por delivery record) | 0 |
| Taxa de autonomia (records) | 100% (8/8) |
| Change-failure rate | 0 conhecido (sem tracker de reopen/bug) |
| Lead time mediano | mesmo dia (2026-08-06) |

### Por issue

| # | Título | Aceite | Gate (tent.) | Revisor | Autônoma |
|---|---|---|---|---|---|
| 01 | contrato-regex-testes | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 02 | cheatsheet-rule-ajuda | 4/4 | verde (1) | aprovado c/ ressalvas | sim |
| 03 | template-pr-azure | 3/3 | verde (1) | aprovado | sim |
| 04 | githooks-bootstrap | 6/6 | verde (1) | aprovado c/ ressalvas | sim |
| 05 | comando-nova-branch | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 06 | adapter-pr-hibrido | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 07 | wiring-git-preflight | 5/5 | verde (1) | aprovado c/ ressalvas | sim |
| 08 | stack-map-install | 6/6 | verde (1) | aprovado c/ ressalvas | sim |

### Leitura para stakeholders

Entrega da Camada Convenção fechou com aceite 100% e gate verde na 1ª tentativa em todas as
tasks. Quase todas as revisões vieram com ressalvas (não bloqueantes) — típico de framework
evolutivo com avisos de tronco/espelho. A autonomia por record é alta, mas o **trabalho no
tronco foi intervenção humana de processo** (exceção explícita); o revisor sinalizou isso sem
bloquear. PR/push e sync remoto ficaram fora do ship por política de acordo + fetch 403.

## O que funcionou bem

- Fatias tracer-bullet 01→08 com delivery records consistentes e gate verde na 1ª tentativa.
- Contrato único (`git-hygiene.yaml`) + testes/fixtures evitaram regex duplicada na prose.
- Espelho `.claude` ↔ `.cursor` mantido nas tasks; install-harness recebeu stack_map + hooks.
- Declaração §1.3 no cheatsheet evita falsa sensação de segurança.

## O que melhorar

- Alta taxa de “aprovado com ressalvas” (7/8) — muitas ressalvas repetem tronco/espelho/§1.3;
  candidatas a checklist fixo do revisor para não poluir cada task.
- Decisões contestáveis do `03-harness.md` não viraram ADR formal (ficaram no grill/PRD).
- `check_context_drift.py` não detecta drift de **contagens de artefatos do canônico**
  (rules/commands) — sync do ship precisou de inventário manual.
- Fetch Azure via proxy 403 neste ambiente — dogfood de PR híbrido com `az` não exercitado.

## Armadilhas encontradas (para o próximo projeto)

- Soft-block de tronco vs. exceção humana: documentar a exceção cedo (STATUS/retro) para o
  revisor não reabrir a cada task.
- Script `sync_agents_from_claude.py` remapeia paths; células que já citam `.cursor/` no
  `CLAUDE.md` duplicam path no `AGENTS.md` — evitar path dual na mesma célula.
- `az` CLI ausente → fluxo híbrido cai no payload UI; preparar título/corpo no ship sempre.

## ADRs desta implementação

- [ADR-001](../../../docs/adr/001-sincronia-de-contexto-no-fechamento.md): sync de contexto no
  fechamento (pré-existente; reforçado neste ship).
- **ADRs não criados** para decisões do MVP git-hygiene (rule agnóstica + adapter; soft-block
  preflight; heurística de segredos vs gitleaks; `pre-push` só aviso; prefixo `Merged PR`
  aberto) — documentadas em `01-grill.md` / `02-prd.md` / `03-harness.md`. Candidato a ADR
  consolidado numa evolução futura se forem contestadas de novo.

## Harness — o que aprendemos

- Wiring `GIT_PREFLIGHT` nos `harness-*` e Dev Loop captura o caminho feliz; não impede
  exceção humana no tronco (comportamento desejado do soft-block).
- Faltou no harness: detector de drift para **inventário canônico** (qtd rules/commands/agents)
  além de stack/docker/env.
- Quase-violação: editar no tronco — revisor avisou; humano autorizou; candidato a deny **só**
  se Edit policies existirem (Fase futura), não nesta Camada Convenção.
- Drift sync: CLAUDE.md rules 11→12, commands 20→22; CONTEXT.md preenchido com glossário
  git-hygiene; AGENTS.md regenerado.

## Payload PR (pendente — sem push)

- **SCM:** Azure DevOps (`origin` = `dev.azure.com/.../agent-harness-canonico-v2`)
- **CLI `az`:** não instalada / não autenticada neste ambiente
- **Título sugerido:** `feat(git-hygiene): padroniza fluxo Git Azure DevOps no canônico`
- **Target:** `master` (trabalho já está em `master` — PR clássico de feature branch **não se
  aplica** até haver branch isolada; alternativa: documentar entrega local e sync remoto
  quando houver acordo de push do `master`, ou criar branch a posteriori só para PR)
- **Corpo:** usar `.azuredevops/pull_request_template.md` + resumo das tasks 01–08
- **Tag `prod-*`:** N/A

## Próximo passo humano

1. Revisar commit de fechamento local (artefatos do projeto + sync + retro).
2. Decidir se quer **push** de `master` (ahead do remote) e/ou abrir PR a partir de branch
   isolada criada agora.
3. Opcional: ADR consolidado das decisões git-hygiene; Fase 2 (portal / Edit policies / `prod-*`).
