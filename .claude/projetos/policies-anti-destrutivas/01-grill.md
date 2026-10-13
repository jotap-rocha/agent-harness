# Policies Anti-Destrutivas — Grill & Requisitos

Slug: `policies-anti-destrutivas`  
Branch: `feat/policies-anti-destrutivas`  
Grill fechado em: 2026-08-12  
Define enriquecido em: 2026-08-12  
Fontes: `00-ideia.md`, `00b-codebase.md`, decisões do `/grill-me`, `harness-define`

## Checklist de completude (qualquer tipo)

| Dimensão | Status |
|---|---|
| Problema real (não sintoma) | OK — gap de gate dual-runtime + install `deny: []` |
| Usuários / personas | OK — maintainer, agente/dev filho, revisor/SI |
| Critérios de sucesso mensuráveis | OK — ver seção abaixo |
| Out of scope | OK — Edit policies server-side, live API, agent dedicado, etc. |
| Restrições técnicas | OK — framework, SI d, paridade política, §1.3 |
| SLA / performance | OK — ver seção SLA (hook local; ask ≠ bloqueio de Dev Loop) |

## Contexto (da sessão /grill-me)

### Problema

O canônico tem deny parcial só no dogfood Claude (`.claude/settings.json`), sem
`PreToolUse`, sem espelho Cursor, e o `/install-harness` gera filhos com
`"deny": []`. Ops destrutivas (Linux, docker, git, SQL CLI, Databricks, terraform,
k8s, etc.) dependem de soft policy (`seguranca`) e de `DE-A002` (código versionado),
não de gate de sessão dual-runtime. §1.3 continua válido: sem Edit policies
server-side, nenhum gate impede de fato.

### Usuários

| Persona | Pain |
|---|---|
| Maintainer do canônico | Precisa de contrato versionado + dogfood Claude↔Cursor sem drift |
| Agente / dev em projeto-filho | Precisa de freio mecânico no Bash sem travar o Dev Loop em ops cinzentas |
| Revisor / SI | Precisa de deny-hard auditável, bypass explícito e honestidade §1.3 |

### Objetivos (MoSCoW)

**MUST:**
- Contrato `agent-policies.yaml` (raiz) + `config/agent_policies/` (loader, matcher, generate)
- Paridade Claude ↔ Cursor: mesmo catálogo → `permissions.deny` + PreToolUse **e**
  `.cursor/hooks.json` / `beforeShellExecution` (inclui `"permission": "ask"`)
- Modo híbrido: severity `deny` vs `ask` no YAML
- Catálogo completo (schema + famílias amplas); core sempre-on no install; extras opt-in
- Install foundation sempre-on: engine + core families + hooks dual
- Seed `.harness/policies/project_profile.yaml` (`families[]`, KEEP no re-install)
- Bypass: `HARNESS_ALLOW_DESTRUCTIVE=1` (ou equivalente) + log; ADR se prod/DDL
- Fail closed em deny-hard; fail open em ask / famílias opt-in
- Testes: matcher + guard (stdin JSON) + fixture install → settings/hooks
- Cross-link docs com `DE-A002` / `seguranca` / §1.3 — sem unificar kernels
- Espelho de artefatos de projeto (hooks/scripts) conforme invariante do canônico

**SHOULD:**
- Canônico dogfooda core + extras no próprio profile
- Limpar paths de máquina em `allow`/`additionalDirectories` do settings dogfood neste ship
- Cheatsheet / rule curta de agent-policies (ou ponte em `seguranca`)
- CLI `python -m config.agent_policies generate|check` (nome exato no PRD)

**COULD:**
- Famílias futuras no YAML desligadas por default (cloud CLIs extras)
- Prompt-hook Cursor além de command-hook
- Métricas de bloqueio em `metrics/`

### Out of Scope

- Edit policies / branch protection server-side / portal UI
- Live API cloud no CI do canônico para “provar” destroy
- Agent dedicado “policy officer” no canônico
- Remover rule `seguranca` (soft policy permanece)
- Unificar ou deprecar `DE-A002`
- E2E obrigatório Claude Code / Cursor IDE no CI (só dogfood manual)

### Restrições

- Evolução de **framework** (não produto)
- SI **d**: freio real em ops destrutivas; bypass consciente
- Paridade de **política** Claude↔Cursor (mesmo catálogo/severity); UI pode diferir
- Fetch Azure pode falhar 403 — soft-block didático; branch `feat/policies-anti-destrutivas`
- Sem commit/push neste passo define (só com acordo explícito)

## SLA / expectativa de performance (hook)

Inferido do domínio + decisão 7 (fail closed/open) — confirmação implícita no define:

| Expectativa | Alvo |
|---|---|
| Latência do guard (match local YAML + regex) | Ordem de **ms** por invocação; sem I/O de rede |
| Cold start (1ª carga do YAML) | Aceitável no início da sessão; preferir cache in-process se o runtime reusar o processo |
| Severity `ask` | **Não** é timeout do Dev Loop — é pausa para confirmação humana do runtime; o pipeline de tasks segue após allow/deny do usuário |
| Hook quebrado / YAML inválido | deny-hard → **fail closed** (bloquear); ask / famílias opt-in → **fail open** (não travar Dev Loop) |
| Bypass `HARNESS_ALLOW_DESTRUCTIVE=1` | Short-circuit imediato + log; sem retry loop |

## Decisões numeradas (grill — fechadas)

1. Perímetro MVP: deny + PreToolUse Claude **e** espelho Cursor no mesmo ship (**c**)
2. Fonte de verdade: YAML canônico + script único; **paridade Cursor obrigatória** (**a**)
3. Modo: híbrido deny-hard / ask (**c**)
4. Catálogo: **completo** (shell, docker, git, sql-cli, databricks, terraform, k8s, cloud CLIs…) (**d**)
5. Ativação: catálogo completo versionado; famílias **opt-in** via profile; core no default (**b**)
6. Install: **sempre-on** na foundation (engine + core + hooks); extras via marker (**b**)
7. Falha do hook: fail **closed** em deny-hard; fail **open** em ask/opt-in (**c**)
8. Bypass humano: env `HARNESS_ALLOW_DESTRUCTIVE=1` + log; ADR se prod/DDL (**b**)
9. `DE-A002`: **ortogonal** — só cross-link (**a**)
10. Core families: `shell` + `docker` + `git` + `sql-cli` + `databricks-cli` + `terraform` + `k8s` (**c**)
11. Testes: matcher + guard script + fixture install (**c**); E2E IDE = dogfood
12. Severity default: deny-hard p/ irreversível infra/dados; ask p/ git force/reset e deletes Databricks “recuperáveis com dor” (**a**)
13. Layout: `agent-policies.yaml` + `config/agent_policies/` + hooks `.claude/` e `.cursor/` (**a**)
14. Marker filho: `.harness/policies/project_profile.yaml` (**a**)
15. Fora do ship: Edit policies server-side / portal / live API / agent dedicado / remover `seguranca` (**a**)

### Inferidos (confirmados — não reabrir)

| # | Inferência | Status |
|---|---|---|
| I1 | Cursor `beforeShellExecution` pode retornar `permission: ask\|deny\|allow` | Confirmado (create-hook) |
| I2 | Install hoje gera `deny: []` — este ship corrige via generate a partir do YAML | Confirmado (00b) |
| I3 | `mirror_to_cursor` ignora `settings.json` — hooks Cursor são artefato próprio | Confirmado (00b) |
| I4 | Githooks permanecem camada de secrets, não anti-shell | Confirmado |

## Amarras a artefatos (previsto)

| Artefato | Onde (canônico) | Nota |
|---|---|---|
| Contrato | `agent-policies.yaml` | Famílias, patterns, severity |
| Engine | `config/agent_policies/` | load, match, generate deny/hooks |
| Hook Claude | `.claude/settings.json` PreToolUse + opcional `.claude/hooks/` | Chama entrypoint compartilhado |
| Hook Cursor | `.cursor/hooks.json` + `.cursor/hooks/` | `beforeShellExecution` |
| Seed | `config/.../templates/policies/` → `.harness/policies/` | `seed: true` KEEP |
| Install | `stack_map` foundation + `install_harness.py` generate | Sempre-on core |
| Rule / docs | ponte `seguranca` + §1.3 / CONTEXT | Honestidade de limites |
| Testes | `tests/agent_policies/` | matcher, guard, install fixture |
| DE-A002 | inalterado | Cross-link only |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- Provedor: N/A
- N/A: **sem key vault** — este projeto é policies anti-destrutivas de runtime (deny/ask/hooks), não wiring de cofre OCI/Azure

## Pipeline (meta — tipo e, não b/c)

N/A como produto de dados. Em meta-nível framework (análogo ao grill de keyvault):

| # | Pergunta (meta) | Resposta |
|---|---|---|
| 1 | Fontes | Catálogo = `agent-policies.yaml`; profile = `.harness/policies/project_profile.yaml` |
| 2 | Schema | Contrato tipado no loader; mudanças versionadas no canônico |
| 3 | Volume | N/A — match por invocação de shell, não batch |
| 4 | Sensibilidade | SI **d** (ops destrutivas); sem PII de domínio neste escopo |
| 5 | SLA | Ver seção SLA (latência local do hook) |
| 6 | Consumidores | Runtimes Claude/Cursor + `/install-harness` filhos |
| 7 | Owner | Maintainer do canônico / SI do projeto-filho |
| 8 | Ambiente | Dual IDE local; sem Edit policies server-side |
| 9 | Qualidade | deny-hard = bloqueante; ask = confirmação; fail closed/open conforme decisão 7 |
| 10 | Portabilidade | Profile `families[]` + seed KEEP; core always-on no install |

## Especificações implícitas detectadas

1. **Falha de dependência (hook/YAML/runtime):** já decidido — fail **closed** em deny-hard; fail **open** em ask / famílias opt-in (decisão 7). Sem rede no hot path.
2. **Concorrência (dois agents):** avaliação **por invocação**, independente; sem mutex cross-agent no MVP. Dois agents com a mesma env de bypass podem ambos passar; risco residual de destruir o mesmo alvo é do operador, fora do escopo do gate.
3. **Idempotência:** reexecutar o mesmo comando = nova avaliação; seguro e determinístico dado o mesmo YAML/profile/env. Bypass não “consome” token.
4. **Autenticação/autorização:** modelo = runtime do IDE + bypass explícito via `HARNESS_ALLOW_DESTRUCTIVE`; **sem** multi-tenant / RBAC de produto neste ship.
5. **Dados sensíveis não declarados:** N/A — sem novos campos PII de domínio (SI d). Log do bypass/deny **não** registra secrets; comando matched pode ser truncado/redacted se parecer credencial (heurística leve, não vault).
6. **Abuso e limites:** N/A — hook local por sessão, não API multi-usuário. Sem rate limit de produto; catálogo/patterns limitados pelo tamanho do YAML versionado.
7. **Auditoria do bypass:** `HARNESS_ALLOW_DESTRUCTIVE=1` **deve** emitir trilha (stderr ou log estruturado do guard): timestamp, family/pattern matched, decisão (`bypass`), runtime adapter — **sem** secret. Sem SIEM/central no MVP; ADR permanece obrigatório se a ação for prod/DDL (decisão 8 + rule `seguranca`).
8. **Estados de erro visíveis:**
   - **deny-hard:** runtime bloqueia + mensagem com family/pattern (agente/usuário vê deny, não allow silencioso)
   - **ask:** Cursor/`beforeShellExecution` → `permission: ask`; Claude PreToolUse equivalente de confirmação conforme adapter
   - **fail closed/open:** mensagem clara de “policy engine unavailable” + decisão aplicada
   - Sem retry automático de ops destrutivas
9. **Ciclo de vida dos dados:** N/A — sem store de PII; profile seed KEEP no re-install; logs de hook são efêmeros de sessão (sem retenção obrigatória neste ship).
10. **Dependência de terceiros mudando:** contrato de stdin/stdout dos hooks Claude/Cursor pode mudar — mitigações: adapters finos + testes de fixture JSON; docs §1.3 honestos se o runtime deixar de honrar deny/ask.

## Critérios de sucesso mensuráveis

- `agent-policies.yaml` valida no loader; core families cobertas com severity
- Canônico: comando deny-hard simulado → exit/deny nos dois adapters (fixture)
- Canônico: comando ask → `ask` (não allow silencioso) nos dois adapters
- `HARNESS_ALLOW_DESTRUCTIVE=1` permite deny-hard e deixa trilha em log (sem secret)
- Install de filho (fixture): `deny` ≠ `[]`; `.cursor/hooks.json` presente; profile seed KEEP
- `/validar` (ou suite pytest) verde com testes novos; DE-A002 regressão intacta
- Docs §1.3 / SI mencionam bypass e limites (não prometem Edit policies)
- Zero path de máquina obrigatório no template gerado para filhos
- Guard local: match sem rede; ask não tratado como falha de Dev Loop

## Soft-blocks registrados

- `git fetch` Azure → HTTP 403 — trabalho na branch local `feat/policies-anti-destrutivas` (não fingir sync novo)
- Working tree: artefatos untracked sob `projetos/policies-anti-destrutivas/` (esperado)
- `origin/HEAD` ausente neste clone — tronco inferido via histórico (`a226042`); branch de trabalho ok
- Adversarial judge: **(b)** pulado (2026-08-12) — sem `01b-judge.md`

## Próximo passo

Requisitos estruturados neste arquivo. Judge pulado.

Dizer **`harness-design`** para gerar o PRD (`02-prd.md`) e montar o harness.