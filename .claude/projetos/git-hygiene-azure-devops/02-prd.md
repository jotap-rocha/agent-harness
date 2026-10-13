# PRD — Git Hygiene Azure DevOps no Harness (Fase 1 · Convenção)

Slug: `git-hygiene-azure-devops`  
Data: 2026-08-06  
Tipo: **e** — evolução do framework / Agent Harness Canônico  
SI: nível **b**  
Fonte: `01-grill.md` · `00-ideia.md` · `00b-codebase.md` · `sketch/portal-git/plan.md`  
Adversarial judge: **pulado** (usuário optou por b nesta sessão — não reperguntar)

> **Natureza:** este PRD especifica artefatos de framework propagáveis via `/install-harness`.
> Não há produto, runtime HTTP nem `.claude/` de app-filho a montar. O alvo é o próprio
> canônico (`agent-harness-canonico-v2`) + dogfood + correção de propagação.

---

## Declaração obrigatória (plano §1.3)

Nesta etapa, **nenhum gate impede de fato** uma ação errada (sem `Edit policies` no Azure
DevOps). Todos os gates locais são contornáveis (`--no-verify`, clone sem bootstrap).

Objetivo: tornar o caminho certo mais fácil que o errado e tornar o errado **visível** —
sem falsa sensação de segurança.

Esta declaração **deve** constar no cheatsheet (`docs/git-hygiene-cheatsheet.md`) e em
qualquer material entregue ao time. Critérios de aceite **não** afirmam bloqueio
server-side.

---

## Problem Statement

Os gates do harness cobrem qualidade de código (`/validar`, `revisor-codigo`, DoD), mas
**não cobrem higiene de controle de versão**. Não existe padrão propagável para branch
isolada, título de Pull Request, template de PR, hooks locais nem adapter SCM.

Consequências:
- Agentes e humanos podem editar direto no tronco.
- Clones limpos não recebem hooks.
- Agents `harness-*` **não propagam** via `stack_map.json` (lacuna crítica).
- Sem `Edit policies`, o Azure DevOps não trava push no tronco — e sem convenção no
  framework, o caminho errado continua tão fácil quanto o certo.

O problema real não é “falta de portal Git”. É **ausência de convenção operacional no
framework**, num ambiente sem permissão de branch policies.

---

## Solution

Entregar a **Fase 1 — Convenção** da estratégia Convenção → Detecção → Policy:

1. **Fonte única** `git-hygiene.yaml` (regex de branch e título de PR).
2. **Rule transversal** `git-hygiene` (agnóstica de SCM) + espelho `.cursor/rules/*.mdc`.
3. **Comandos** `/nova-branch` e `/git-ajuda` + cheatsheet com §1.3.
4. **Hooks versionados** em `.githooks/` com bootstrap `core.hooksPath` no install
   (após confirmação no Install Plan).
5. **Template** `.azuredevops/pull_request_template.md`.
6. **Adapter SCM** `azure | github` (detecta pelo remote; ambíguo → pergunta).
7. **Wiring** `GIT_PREFLIGHT` (soft-block) em todos `harness-*` + Dev Loop;
   `revisor-codigo` só avisa no tronco.
8. **Correção** `stack_map.json` para propagar `harness-*` + artefatos git-hygiene.
9. **Dogfood** no próprio canônico.

Por quê esta abordagem: automatizar o caminho certo vale mais que mais documentação;
centralizar regex evita divergência; adapter SCM evita cravar Azure numa rule always-on;
sem inventar produto/portal — só artefatos de harness.

---

## User Stories

1. As a mantenedor do canônico, I want a rule `git-hygiene` + `git-hygiene.yaml` versionados e espelhados, so that a convenção única propaga via `/install-harness` sem divergir.
2. As a mantenedor do canônico, I want agents `harness-*` no `stack_map.json`, so that wiring de preflight e ship chegue aos projetos-filho.
3. As an agente do harness, I want `GIT_PREFLIGHT` soft-block antes de editar, so that eu não continue no tronco sem acordo explícito.
4. As an agente do harness, I want `/nova-branch` (fetch → sync `--ff-only` → acordo → `tipo/escopo`), so that a branch certa nasça de um comando único.
5. As a developer em projeto-filho, I want mensagens de erro didáticas nos hooks (o que fazer + exemplo + por quê), so that eu aprenda pelo uso sem carga cognitiva alta.
6. As a developer, I want `pre-commit` bloqueando padrões de segredo sintéticos, so that vazamento óbvio não entre no histórico.
7. As a developer, I want `pre-push` no tronco em modo aviso (não bloqueante neste MVP), so that o desvio fique visível sem desativar o gate.
8. As a developer, I want template `.azuredevops/pull_request_template.md`, so that o PR abra já com checklist (funciona sem permissão ADO).
9. As an operador de `/install-harness`, I want bootstrap de hooks só após confirmação no Install Plan, so that a instalação de hooks seja consciente e idempotente.
10. As an agente, I want adapter SCM pelo remote (`az` vs `gh`), so that abertura de PR funcione em Azure ou GitHub sem rule falsa.
11. As an agente, I want fluxo híbrido de PR (`az` autenticado tenta create + squash; senão prepara UI), so that falta de auth não trave a entrega.
12. As a developer, I want commit/push/stash/descartar só com acordo explícito, so that o agente nunca destrua working tree sem consentimento.
13. As a developer, I want `/git-ajuda` + cheatsheet com §1.3, so that eu saiba o contrato e os limites reais dos gates.
14. As a revisor (`revisor-codigo`), I want aviso não-bloqueante se o diff foi produzido no tronco, so that a higiene entre na revisão sem travar merge indevido.
15. As a mantenedor, I want fixtures/testes das regex (válidos/inválidos), so that a fonte única não seja o componente menos testado.
16. As a mantenedor, I want dogfood no canônico (mesmos artefatos + hooks bootstrapados), so that o framework prove o fluxo antes de propagar.
17. As an agente em Dev Loop, I want o mesmo `GIT_PREFLIGHT` do harness workflow, so that tarefa pontual não escape da convenção.
18. As a developer, I want título de PR sugerido ao final de `/nova-branch` e no `harness-ship`, so that a formalidade concentre-se no ponto que sobrevive ao squash.

---

## Implementation Decisions

### Escopo e natureza

- **MVP = Fase 1 Convenção** + dogfood + correção `stack_map.json`.
- **Tipo e:** somente artefatos de framework (rules, commands, hooks, wiring, install, docs).
- **Não** montar harness-architect de app-filho; **não** inventar código de produto.
- Estratégia completa (Detecção / Policy) documentada no plano, **fora** deste PRD.

### Contrato operacional (fonte: grill)

**Branch:** `{tipo}/{escopo-kebab}` — tipos `feat|fix|chore`; escopo ≤ 40 chars, kebab, sem acento; proibidos: `tmp`, `teste`, nome de pessoa, data solta, `nova-branch`.

**Título PR (ponto de controle):** `{tipo}({escopo}): {resumo ≤ 72 chars}`.

**Tronco:** default branch do remote (`origin/HEAD`); fallback `master`.

**Sync:** `git pull --ff-only`; divergência → soft-block humano.

**Merge:** tentar squash via `az`; senão checklist + cheatsheet.

**Commits locais:** mensagem livre + sugestão leve Conventional Commits (não bloqueante).

### Soft-block `GIT_PREFLIGHT` (antes de editar)

1. `git fetch` (falha de rede → soft-block didático, não prosseguir como sync).
2. Detectar tronco.
3. HEAD no tronco ou local atrás → soft-block → oferecer `/nova-branch`.
4. Working tree suja → soft-block (stash/commit/descartar — nunca sem acordo).
5. Prosseguir só com branch de trabalho ok e sync ok.

Entradas: todos `harness-*` + Dev Loop (`prompt-crafter` / `dev-loop-executor` / `/dev`).  
`revisor-codigo`: ressalva não-bloqueante se diff no tronco.

### Adapter SCM e PR

- Detectar pelo URL do remote; ambíguo → pergunta.
- Azure: `az repos pr create` se autenticado (tentar squash); senão payload para UI.
- GitHub: lógica híbrida equivalente com `gh`.
- PAT/tokens: somente env / secret manager; nunca hardcoded, nunca logs, nunca query string.
- Idempotência de PR: se já existe PR da branch, informar URL (validar na impl. `az`).

### Hooks

| Hook | Comportamento MVP |
|---|---|
| `pre-commit` | Heurística leve de segredos — **bloqueante** |
| `commit-msg` | Aviso Conventional Commits |
| `pre-push` | Aviso se push no tronco (não bloqueia neste MVP) |

Bootstrap: `git config core.hooksPath .githooks` via install **após confirmação** no Install Plan; idempotente.

### Decisões contestáveis (candidatas a ADR na implementação)

1. Rule agnóstica + adapter `scm` (não cravar Azure na rule always-on).
2. Soft-block (não hard-stop silencioso) no preflight dos agents.
3. Heurística de segredos agora; caminho para `gitleaks` depois.
4. `pre-push` aviso agora; bloqueante após N semanas = fase posterior.
5. Prefixo `Merged PR NNN:` vs editar squash — aberto (§5.3 do plano); documentar antes de changelog automatizado.

### Abertos (não bloqueiam)

- Aceitar `Merged PR NNN:` vs customize merge message.
- Data de corte para `pre-push` bloqueante.
- Fase 0 (baseline + pedido Edit policies) em paralelo, fora deste merge.
- Fase 2 (detecção, métricas, tag `prod-*`).

---

## Mapa de artefatos (criar / alterar no canônico)

Espelhamento obrigatório `.claude/` ↔ `.cursor/` na mesma sessão (rules `.md` → `.mdc`).

### Criar

| Artefato | Path(s) | Aceite |
|---|---|---|
| Fonte única YAML | `git-hygiene.yaml` (raiz do canônico) | A1 |
| Rule | `.claude/rules/git-hygiene.md` + `.cursor/rules/git-hygiene.mdc` | A1, A12 |
| Command nova-branch | `.claude/commands/nova-branch.md` + espelho `.cursor/` | A2, A3 |
| Command git-ajuda | `.claude/commands/git-ajuda.md` + espelho | A13 |
| Cheatsheet (§1.3) | `docs/git-hygiene-cheatsheet.md` | A13 |
| Hooks | `.githooks/pre-commit`, `commit-msg`, `pre-push` (+ README se útil) | A5–A7 |
| Bootstrap hooks | script/helper referenciado pelo install-harness | A5, A14 |
| Template PR Azure | `.azuredevops/pull_request_template.md` | A4 |
| Fixtures regex | testes/fixtures de branch e título (local do canônico) | A1, A3 (SHOULD) |

### Alterar (wiring)

| Artefato | Mudança | Aceite |
|---|---|---|
| `stack_map.json` (`.claude` + `.cursor`) | Incluir agents `harness-*` + artefatos git-hygiene + template Azure + hooks | A11 |
| `install-harness` SKILL + scripts | Passo Install Plan: confirmar hooks; bootstrap `core.hooksPath` | A5, A11 |
| `harness-brainstorm` … `harness-ship` | Soft-block `GIT_PREFLIGHT`; ship sugere título PR | A8, A15 |
| `dev-loop-executor` / `prompt-crafter` / `/dev` | Step 0 preflight; seção `## Git` no prompt | A8 |
| `revisor-codigo` | Aviso não-bloqueante se diff no tronco | A8 |
| CLAUDE.md / HARNESS-GUIDE (mínimo) | Documentar adapter `scm`, commands novos, §1.3 se couber | A13 |
| Templates CLAUDE.md filho (harness-architect refs) | Campo `scm: azure \| github` quando aplicável | A9 |

### Não criar neste MVP

- Portal UI, pipeline de detecção, `metrics/git-hygiene.jsonl`, tag `prod-*` no ship, `repo_profile`, Edit policies, rename `master→main`.

---

## Ordem de implementação recomendada

1. **Contrato:** `git-hygiene.yaml` + fixtures/testes de regex (A1, A3).
2. **Cheatsheet + `/git-ajuda`** com §1.3 (A13) — entregar cedo (plano: antes dos scripts pesados).
3. **Rule** `git-hygiene` + espelho `.mdc` (A1, A12).
4. **Template** `.azuredevops/pull_request_template.md` (A4).
5. **`.githooks/`** + heurística segredos + avisos; bootstrap local dogfood (A5–A7, A14).
6. **`/nova-branch`** (A2, A3, sync ff-only, título sugerido).
7. **Adapter SCM** + fluxo híbrido de PR (A9, A10).
8. **Wiring** `GIT_PREFLIGHT` em harness-* + Dev Loop + revisor (A8, A15).
9. **`stack_map.json` + install-harness** (confirmação hooks + cópia artefatos) (A11).
10. **Paridade** `.claude` ↔ `.cursor` + dry-run install (A12).
11. **DoD:** evidências A1–A15; delivery record se aplicável ao fluxo de evolução do canônico.

---

## Testing Decisions

- Testar **comportamento externo** (exit codes, mensagens, `git config`, regex), não detalhes internos de implementação.
- **Regex:** fixtures válidas/inválidas para branch e título (A1, A3).
- **Hooks:** fixture com segredo sintético → pre-commit exit ≠ 0 (A6); pre-push no tronco → aviso, exit 0 (A7).
- **`/nova-branch`:** demo/script — tronco desatualizado ou divergente → soft-block; nome inválido rejeitado (A2, A3).
- **Adapter:** URLs de remote Azure vs GitHub vs ambíguo (A9).
- **Install:** dry-run / checklist de `stack_map` inclui harness-* e git-hygiene (A11).
- **Paridade:** verificação de espelho na sessão (A12).
- **Dogfood:** `core.hooksPath=.githooks` no workspace canônico após bootstrap (A14).
- Não exigir CI Azure neste MVP (Fase 2).

---

## Out of Scope (MVP)

- Tag `prod-*` (Fase 2)
- Pipeline de detecção / `metrics/git-hygiene.jsonl` (Fase 2)
- Baseline + pedido `Edit policies` (Fase 0 — paralelo, fora deste merge)
- `repo_profile` / `/validar` multi-perfil (Fase 4)
- Portal UI, rename forçado `master→main`, deploy automático
- Duas branches de longa duração; force-push no tronco
- `pre-push` bloqueante (fica aviso neste MVP)
- Código de produto / app-filho / harness-architect de produto

---

## SI Considerations (nível b)

- Dados: metadados de repositório/acesso — **não** PII direto.
- **Não** exige `[AVISO_LGPD]` nem `rules/pii.md`.
- PAT / tokens Azure DevOps: **somente** env ou secret manager; nunca hardcoded; nunca em logs; nunca em URL query strings.
- `pre-commit` de segredos: bloqueante desde o dia 1 (custo de falha irreversível → rotação).
- Métricas futuras (Fase 2): **agregadas por repositório**, nunca por pessoa.
- Relatórios e outputs do agente: sem vazar tokens ou conteúdo sensível de diffs com secrets.
- Impacto LGPD deste MVP: mínimo — sem novos campos pessoais; conformidade via rules/seguranca existentes + invariantes acima.

---

## Further Notes

- Path canônico documentado em CLAUDE.md (`<raiz-do-canonico>`) pode divergir deste clone v2 — dogfood neste workspace.
- Metas de adoção do plan.md §13 (90 dias) **fora** do MVP.
- Próximo passo operacional: `/to-tasks` para fatiar A1–A15; depois `harness-build` na ordem acima.
- Judge adversarial: usuário já optou por **não** rodar nesta sessão.
