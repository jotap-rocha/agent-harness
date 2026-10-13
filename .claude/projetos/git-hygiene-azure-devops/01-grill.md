# Git Hygiene Azure DevOps no Harness — Grill & Requisitos

Slug: `git-hygiene-azure-devops`  
Data: 2026-08-06  
Fonte: `sketch/portal-git/plan.md` + brainstorm + codebase-explorer + sessão /grill-me  
SI: nível **b** · Tipo: **e** (evolução do framework / Agent Harness Canônico)

## Declaração obrigatória (plano §1.3)

Nesta etapa, **nenhum gate impede de fato** uma ação errada (sem `Edit policies`).
Objetivo: tornar o caminho certo mais fácil e o errado **visível** — sem falsa
sensação de segurança. Esta declaração deve constar no cheatsheet e no material
entregue ao time.

## Contexto (da sessão /grill-me)

### Problema

Os gates do harness cobrem qualidade de código (`/validar`, `revisor-codigo`, DoD),
mas **não cobrem higiene de controle de versão**. Não há padrão propagável para
branch isolada, título de PR, template de Pull Request, hooks locais nem adapter
SCM. Agentes e humanos podem trabalhar direto no tronco; clones limpos não
recebem hooks; agents `harness-*` **não propagam** via `stack_map.json`.

O problema real não é “falta de portal Git” — é **ausência de convenção
operacional no framework**, num ambiente sem permissão de branch policies no
Azure DevOps. Sem convenção, o caminho errado continua tão fácil quanto o certo.

### Usuários

| Persona | Pain point |
|---|---|
| Mantenedor do canônico | Evoluir o framework sem dogfood de Git hygiene; lacuna de propagação `harness-*` |
| Agente do harness (Cursor/Claude) | Sem preflight Git; edita no tronco; sem comando único para branch/PR |
| Dev em projeto-filho (time em formação CI/CD) | Carga cognitiva alta; precisa do caminho certo automatizado, não de mais docs |
| Operador `/install-harness` | Precisa optar conscientemente por hooks no Install Plan; clone limpo sem bootstrap fica sem gates |

### Objetivos (MoSCoW)

**MUST (MVP = Fase 1 Convenção + dogfood no canônico):**
- Rule transversal `git-hygiene` agnóstica de SCM + espelho `.cursor/rules/git-hygiene.mdc`
- Fonte única `git-hygiene.yaml` (regex branch + título PR)
- Comando `/nova-branch` (fetch → sync tronco → acordo → cria `tipo/escopo`)
- Comando `/git-ajuda` + cheatsheet `docs/git-hygiene-cheatsheet.md` (mesma fonte)
- Pasta `.githooks/` + bootstrap `core.hooksPath` no `/install-harness` **após confirmação** no Install Plan
- `pre-commit`: heurística leve de segredos **bloqueante**; `commit-msg` aviso; `pre-push` no tronco = aviso
- Template `.azuredevops/pull_request_template.md`
- Adapter SCM por remote (`azure` \| `github`); ambíguo → pergunta
- Soft-block `GIT_PREFLIGHT` em todos `harness-*` + Dev Loop; `revisor-codigo` só avisa no tronco
- PR híbrido: `az repos pr create` se autenticado (tentar squash); senão prepara título/corpo para UI
- Commit/push só com acordo explícito; working tree suja → soft-block (stash/commit/descartar)
- Sync tronco: `git pull --ff-only`; divergência → soft-block humano
- Correção `stack_map.json` para propagar `harness-*` + novos artefatos git-hygiene
- Espelhamento `.claude` ↔ `.cursor` na mesma sessão; dogfood no próprio canônico
- Declaração §1.3 visível no cheatsheet

**SHOULD:**
- Mensagens de erro didáticas (o que fazer + exemplo colável + por quê)
- Sugestão leve de Conventional Commits (não bloqueante) nos commits locais
- Título de PR sugerido ao final de `/nova-branch` e no `harness-ship`
- Fixtures/testes de regex (branch e título válidos/inválidos)

**COULD (depois do MVP):**
- Plugar `gitleaks` no lugar da heurística
- Prefixo `Merged PR NNN:` vs editar mensagem no squash (documentar decisão)
- `pre-push` bloqueante após N semanas de aviso
- Tag `prod-*`, pipeline de detecção, métricas, `repo_profile`, Edit policies

### Out of Scope (MVP)

- Tag `prod-*` (Fase 2)
- Pipeline de detecção / `metrics/git-hygiene.jsonl` (Fase 2)
- Baseline + pedido de `Edit policies` (Fase 0 — paralelo, fora deste merge)
- `repo_profile` / `/validar` multi-perfil (Fase 4)
- Portal UI, rename forçado `master→main`, deploy automático
- Duas branches de longa duração; force-push no tronco
- Severidade gradual do `pre-push` como entrega deste MVP (fica aviso)

### Restrições

- Sem `Edit policies` / Project Administrator no Azure DevOps → nenhum gate server-side
- Azure Repos sem hook server-side → validação local contornável (`--no-verify`, clone sem bootstrap)
- Framework canônico: **somente artefatos** (rules, commands, hooks, wiring, install) — sem código de produto
- Invariante: espelho `.claude/` ↔ `.cursor/` na mesma sessão
- Secrets/PAT: só via env ou secret manager; nunca logs, nunca hardcoded
- SI nível **b**: métricas futuras agregadas por repositório, nunca por pessoa
- Path canônico documentado em CLAUDE.md pode divergir deste clone v2 — dogfood neste workspace

### SLA / performance (inferido)

- `GIT_PREFLIGHT` (`git fetch` + checagens locais): expectativa de concluir em segundos em rede típica; se `fetch` falhar → soft-block com mensagem clara (não travar silenciosamente)
- Sem SLA de disponibilidade de produto (não há runtime HTTP)

## Decisões fechadas do grill (não reabrir sem necessidade)

| # | Tema | Decisão |
|---|---|---|
| 1 | Escopo | Fase 1 (Convenção) + preflight Git nas atividades de harness/Dev Loop |
| 2 | Severidade preflight | Soft-block: oferece `/nova-branch`/sync e **só segue** com branch ok |
| 3 | Quem cria a branch | Agente conduz com **acordo explícito**; nome alinhado à intenção |
| 4 | Nome da branch | Infere do contexto; mostra proposta; usuário confirma ou ajusta |
| 5 | Adapter SCM | Detecta pelo remote; se ambíguo, pergunta |
| 6 | Abertura de PR | Híbrido: `az` se autenticado; senão prepara UI |
| 7 | Hooks no install | Automático **após confirmação** no Install Plan |
| 8 | Onde vale o preflight | Todos `harness-*` + Dev Loop; `revisor-codigo` só avisa |
| 9 | Tag `prod-*` | Fora do MVP (Fase 2) |
| 10 | Working tree suja | Soft-block: stash / commit / descartar — nunca destrutivo sem acordo |
| 11 | Commit e push | Só com acordo explícito |
| 12 | Sync do tronco | `git pull --ff-only`; divergência → humano |
| 13 | Mensagem de commit local | Livre + sugestão leve; formalidade no **título do PR** |
| 14 | Segredos | Heurística leve bloqueante agora; caminho para `gitleaks` depois |
| 15 | Dogfood | Canônico recebe e usa os mesmos artefatos |
| 16 | Cheatsheet | `docs/git-hygiene-cheatsheet.md` + `/git-ajuda` |
| 17 | Merge type | Tentar squash via `az`; senão checklist + cheatsheet |
| 18 | Nome do tronco | Default branch do remote (`origin/HEAD`); fallback `master` |
| 19 | SI / tipo | Nível b; tipo e (evolução framework) |
| 20 | Gates reais | Sem Edit policies: nenhum gate impede de fato |

## Contrato operacional

### Branch
```
{tipo}/{escopo-kebab}
tipos: feat | fix | chore
escopo: até 40 caracteres, kebab-case, sem acento
Proibidos: tmp, teste, nome de pessoa, data solta, nova-branch
```

### Título do PR (ponto de controle)
```
{tipo}({escopo}): {resumo ≤ 72 chars}
```

### Preflight (obrigatório antes de editar)
1. `git fetch`
2. Detectar tronco (default remote / fallback `master`)
3. Se HEAD no tronco ou local atrás → soft-block → `/nova-branch` com acordo
4. Se working tree suja → soft-block (stash/commit/descartar)
5. Prosseguir só com branch de trabalho ok e sync ok

### Entradas cobertas
- `harness-brainstorm`, `harness-define`, `harness-design`, `harness-build`,
  `harness-iterate`, `harness-ship`
- Dev Loop (`prompt-crafter` / `dev-loop-executor` / `/dev`)
- `revisor-codigo`: ressalva não-bloqueante se diff no tronco

### Propagação
- Incluir agents `harness-*` e artefatos git-hygiene no `stack_map.json`
- Espelhar `.claude` ↔ `.cursor` na mesma sessão
- Template PR Azure versionado (funciona sem permissão ADO)

## Especificações implícitas detectadas

1. **Falha de dependência externa:** Se `git fetch` / rede falhar → soft-block com mensagem didática (não prosseguir como se estivesse sync). Se `az` falhar ou não autenticado → fallback: preparar título/corpo/checklist para abertura manual na UI. Se `gh` no adapter github: mesma lógica híbrida.
2. **Concorrência:** Working tree suja (outro agente/humano) → soft-block; nunca stash/commit/descartar sem acordo. Duas sessões no mesmo clone: responsabilidade humana; o preflight torna o conflito visível.
3. **Idempotência:** `/nova-branch` com nome já existente → soft-block / oferta de switch (não sobrescrever). Bootstrap de hooks: reexecutável com segurança (`core.hooksPath` idempotente). Reabrir fluxo de PR: se PR já existe para a branch, informar URL em vez de duplicar (inferido — confirmar na implementação se `az` expõe isso de forma estável).
4. **Autenticação/Autorização:** Sem multi-tenant. Auth SCM = credenciais locais do usuário (`az login` / `gh auth`). Agente nunca embute PAT. Quem confirma Install Plan decide se hooks são instalados.
5. **Dados sensíveis:** Cobertos pelo SI Assessment nível b + `pre-commit` de segredos. PAT/tokens só via env. Sem novos campos PII; sem `[AVISO_LGPD]`.
6. **Abuso e limites:** Escopo de branch ≤ 40 chars; título PR ≤ 72 chars no resumo. N/A rate-limit de produto (sem API própria).
7. **Auditoria:** N/A trilha formal além do histórico Git + template de PR no MVP. Métricas por pessoa proibidas (SI).
8. **Estados de erro visíveis:** Mensagens didáticas obrigatórias (o que fazer + exemplo + por quê). Soft-block sempre explica a saída. Sem retry automático destrutivo.
9. **Ciclo de vida dos dados:** N/A — sem store de PII; artefatos de harness versionados no repo.
10. **Dependência de terceiros mudando:** Adapter `scm` isola `az` vs `gh`. Regex centralizada em `git-hygiene.yaml` para não divergir. Mudança de UI/CLI Azure → fallback UI continua válido.

## Critérios de sucesso mensuráveis (MVP Fase 1)

Critérios **testáveis** alinhados ao plan.md §14 (Fase 1) e ao grill — nenhum afirma que um gate server-side impede:

| # | Critério de aceite | Evidência |
|---|---|---|
| A1 | Existe `git-hygiene.yaml` com regex de branch e título; rule `git-hygiene` (+ `.mdc`) consome essa fonte | Arquivos no canônico; teste unitário das regex |
| A2 | `/nova-branch` cria `feat\|fix\|chore/<escopo>` a partir do tronco sincronizado (`--ff-only`) e recusa/ soft-block se tronco desatualizado ou divergente | Demo / script com exit code ≠ 0 / soft didático |
| A3 | Nome de branch inválido (ex.: `tmp`, acento, >40 chars) é rejeitado pela validação | Fixture de casos inválidos |
| A4 | Template `.azuredevops/pull_request_template.md` versionado no canônico e propagável via install | Arquivo presente + entrada no `stack_map.json` |
| A5 | Clone limpo + bootstrap (`core.hooksPath=.githooks`) deixa hooks ativos e verificáveis | `git config core.hooksPath` == `.githooks` |
| A6 | Commit com padrão de segredo sintético é **bloqueado** pelo `pre-commit` (heurística) | Teste de hook com fixture |
| A7 | `pre-push` no tronco emite **aviso** (não bloqueia neste MVP) | Teste / demo |
| A8 | Soft-block `GIT_PREFLIGHT` documentado/wireado em todos `harness-*` + Dev Loop; `revisor-codigo` só avisa no tronco | Diff nos agents + checklist de wiring |
| A9 | Adapter SCM: remote Azure → `azure`; GitHub → `github`; ambíguo → pergunta | Teste de detecção por URL de remote |
| A10 | Fluxo de PR: com `az` autenticado tenta create + squash; sem auth prepara payload para UI | Demo dos dois caminhos |
| A11 | `stack_map.json` inclui agents `harness-*` e artefatos git-hygiene | Diff do mapa + dry-run do install |
| A12 | Artefatos espelhados `.claude` ↔ `.cursor` | Verificação de paridade na sessão de implementação |
| A13 | Cheatsheet + `/git-ajuda` existem; cheatsheet inclui declaração §1.3 | Arquivos + comando |
| A14 | Dogfood: canônico usa os mesmos artefatos (hooks bootstrapados no workspace de desenvolvimento) | `core.hooksPath` no canônico após setup |
| A15 | Commit/push/stash/descartar nunca ocorrem sem acordo explícito do usuário | Wiring nos agents + rule |

Metas de adoção do plan.md §13 (90 dias) são **fora do MVP** (dependem de Fase 0/2); não são critérios de aceite desta entrega.

## Decisões inferidas (avanço sem travar)

| Tema | Inferência | Confirmação humana? |
|---|---|---|
| Adversarial judge | **Não** rodar agora — seguir para harness-design | Opcional depois |
| Idempotência de PR duplicado | Informar PR existente em vez de criar outro | Validar na implementação `az` |
| SLA de preflight | Soft expectation; falha de rede = soft-block | Não bloqueia |
| Personas | Quatro personas acima | Ajuste fino ok no PRD |

## Abertos (não bloqueiam PRD / design)

1. Aceitar prefixo `Merged PR NNN:` vs editar mensagem no squash (plano §5.3)
2. `pre-push` no tronco: só aviso agora vs bloqueante após N semanas
3. Fase 0 (baseline + pedido Edit policies) em paralelo, fora deste MVP
4. Fase 2 (detecção, métricas, tag `prod-*`)

## Próximo passo

Rode `harness-design` para gerar o PRD e montar o harness / tasks da Fase 1.
