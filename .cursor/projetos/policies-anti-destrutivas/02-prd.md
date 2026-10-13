# PRD — Policies Anti-Destrutivas (deny + hooks dual-runtime)

Slug: `policies-anti-destrutivas`  
Repo: Agent Harness Canônico (framework — **não** produto)  
Branch: `feat/policies-anti-destrutivas`  
Data: 2026-08-12  
Tipo: **e** — evolução do harness canônico  
SI: **d** (ops destrutivas / escrita-deleção em produção)  
Fontes: `00-ideia.md`, `00b-codebase.md`, `01-grill.md` (15 decisões + define enriquecido)

> Decisões do grill estão **fechadas** — este PRD as materializa; não reabre a matriz.

---

## Problem Statement

O canônico dogfooda um `permissions.deny` parcial só no runtime Claude
(`.claude/settings.json`), sem `PreToolUse`, sem espelho Cursor versionado, e o
`/install-harness` gera projetos-filho com `"deny": []`. Ops destrutivas (Linux,
docker volumes, git force/reset hard, SQL CLI, Databricks CLI, terraform, k8s, etc.)
dependem de soft policy (`rules/seguranca`) e de `DE-A002` (código versionado DE) —
camadas ortogonais que **não** freiam Bash de sessão nos dois IDEs.

O sintoma é “filho nasce sem deny” e “Cursor não tem o mesmo freio”. O problema real é a
ausência de um **contrato de framework**: catálogo versionado de famílias/patterns com
severity → engine única (load/match/generate) → hooks dual Claude↔Cursor → install
foundation sempre-on com core families → seed de profile no filho → testes de matcher,
guard e fixture de install. Sem isso, o freio mecânico permanece dogfood-only e
assimétrico.

§1.3 continua válido: sem Edit policies / branch protection server-side, nenhum gate
impede de fato; bypass humano e clone sem hooks existem. O ship precisa ser **honesto**
sobre esses limites enquanto entrega o melhor freio local possível.

---

## Solution

Evoluir o canônico com um **kernel de agent-policies** (runtime anti-destrutivo),
paralelo ao kernel DE (não unificado):

1. **Contrato** `agent-policies.yaml` na raiz — famílias, patterns, severity (`deny` |
   `ask`).
2. **Engine** `config/agent_policies/` — load tipado, matcher, generate de
   `permissions.deny` + payloads de hooks.
3. **Paridade Claude ↔ Cursor** no mesmo ship: Claude `permissions.deny` + PreToolUse;
   Cursor `.cursor/hooks.json` + `beforeShellExecution` (inclui `"permission": "ask"`).
4. **Modo híbrido:** deny-hard para irreversível infra/dados; ask para git force/reset e
   deletes Databricks “recuperáveis com dor”.
5. **Catálogo completo** versionado; **core** always-on no install; **extras** opt-in via
   profile.
6. **Install foundation** sempre-on: engine + core families + hooks dual; seed
   `.harness/policies/project_profile.yaml` (`families[]`, KEEP no re-install).
7. **Bypass** `HARNESS_ALLOW_DESTRUCTIVE=1` + trilha de log; ADR se prod/DDL (rule
   `seguranca` permanece).
8. **Fail closed** em deny-hard; **fail open** em ask / famílias opt-in.
9. **`DE-A002` ortogonal** — só cross-link em docs; não unificar kernels.
10. **Testes:** matcher + guard (stdin JSON) + fixture install → settings/hooks; E2E IDE =
    dogfood manual.

---

## Goals (MoSCoW)

### MUST

- Contrato `agent-policies.yaml` + engine `config/agent_policies/` (load, match, generate)
- Paridade política Claude ↔ Cursor (mesmo catálogo/severity → deny + PreToolUse **e**
  hooks Cursor / `beforeShellExecution`)
- Modo híbrido deny-hard / ask no YAML
- Catálogo completo; core always-on no install; extras opt-in via profile
- Install foundation: engine + core + hooks dual (corrige `deny: []` nos filhos)
- Seed `.harness/policies/project_profile.yaml` (`families[]`, KEEP)
- Bypass `HARNESS_ALLOW_DESTRUCTIVE=1` + log; ADR se prod/DDL
- Fail closed em deny-hard; fail open em ask / opt-in
- Testes: matcher + guard + fixture install
- Cross-link docs com `DE-A002` / `seguranca` / §1.3 — sem unificar kernels
- Espelho de artefatos de projeto (hooks/scripts) conforme invariante do canônico

### SHOULD

- Canônico dogfooda core + extras no próprio profile
- Limpar paths de máquina em `allow` / `additionalDirectories` do settings dogfood
- Cheatsheet / rule curta de agent-policies (ou ponte em `seguranca`)
- CLI `python -m config.agent_policies generate|check`

### COULD

- Famílias futuras no YAML desligadas por default (cloud CLIs extras)
- Prompt-hook Cursor além de command-hook
- Métricas de bloqueio em `metrics/`

### WON'T (neste ship)

- Edit policies / branch protection server-side / portal UI
- Live API cloud no CI do canônico para “provar” destroy
- Agent dedicado “policy officer” no canônico
- Remover rule `seguranca` (soft policy permanece)
- Unificar ou deprecar `DE-A002`
- E2E obrigatório Claude Code / Cursor IDE no CI (só dogfood manual)

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want a versioned `agent-policies.yaml` contract at the repo root with families, patterns, and severity, so that deny/ask policy is auditable like `git-hygiene.yaml` / `data-engineering.yaml`.
2. As a mantenedor do canônico, I want a typed loader under `config/agent_policies/`, so that invalid YAML fails fast in CI instead of silently shipping empty deny.
3. As a mantenedor do canônico, I want a shared matcher that evaluates a shell command against the active families, so that both Claude and Cursor adapters share one decision engine.
4. As a mantenedor do canônico, I want a generate path that materializes Claude `permissions.deny` and Cursor hook config from the same catalog, so that drift between runtimes is impossible by construction.
5. As a mantenedor do canônico, I want PreToolUse on Claude wired to the shared guard entrypoint, so that deny is not only declarative permissions but also an explicit hook gate.
6. As a mantenedor do canônico, I want `.cursor/hooks.json` + hook scripts with `beforeShellExecution` returning `permission: ask|deny|allow`, so that Cursor has policy parity even without project `settings.json` mirror.
7. As a mantenedor do canônico, I want hybrid severity in the contract (deny-hard vs ask), so that irreversible infra/data ops block while recoverable-with-pain ops pause for human confirm.
8. As a mantenedor do canônico, I want a complete catalog (shell, docker, git, sql-cli, databricks-cli, terraform, k8s, cloud CLIs, …) versioned in YAML, so that coverage is explicit and extensible without code forks.
9. As a mantenedor do canônico, I want core families always-on (`shell`, `docker`, `git`, `sql-cli`, `databricks-cli`, `terraform`, `k8s`) and extras opt-in via profile, so that install stays safe by default without forcing every cloud CLI.
10. As a mantenedor do canônico, I want default severity deny-hard for irreversible infra/data and ask for git force/reset and Databricks deletes that are painful but recoverable, so that product judgment matches SI d without freezing the Dev Loop.
11. As a mantenedor do canônico, I want `/install-harness` foundation to always ship engine + core families + dual hooks, so that children no longer start with `deny: []`.
12. As a mantenedor do canônico, I want seed `.harness/policies/project_profile.yaml` with `families[]` and `seed: true` KEEP on re-install, so that child opt-ins survive harness updates.
13. As a mantenedor do canônico, I want fail-closed behavior when the deny-hard path cannot evaluate (broken hook / invalid YAML), so that SI d does not silently allow destruction.
14. As a mantenedor do canônico, I want fail-open behavior for ask / opt-in families when the engine is unavailable, so that the Dev Loop is not bricked by optional policy surfaces.
15. As a mantenedor do canônico, I want `HARNESS_ALLOW_DESTRUCTIVE=1` to short-circuit deny-hard with an audit trail (no secrets), so that maintainers can consciously bypass without `--no-verify`-style secrecy.
16. As a mantenedor do canônico, I want `DE-A002` left unchanged with only documentation cross-links, so that static DE destructive checks stay orthogonal to session Bash gates.
17. As a mantenedor do canônico, I want pytest for matcher, guard stdin/stdout fixtures, and install generate fixtures, so that regressions fail harness CI without IDE E2E.
18. As a mantenedor do canônico, I want docs and SI bridges to state §1.3 honesty (no Edit policies promise), so that the framework never claims server-side impossibility of destruction.
19. As a mantenedor do canônico, I want generated child templates free of machine-specific absolute paths in allow/additionalDirectories, so that install artifacts are portable.
20. As CI do canônico, I want `/validar` (ruff + mypy + pytest) green with the new `tests/agent_policies/` suite and DE-A002 regression intact, so that this ship does not weaken existing gates.

### Agente / desenvolvedor em projeto-filho

21. As an agente em projeto-filho, I want core destructive Bash patterns denied by default after install, so that accidental `rm -rf` / volume wipe / dropdb are mechanically blocked.
22. As an agente em projeto-filho, I want ask prompts for git force/reset and painful-but-recoverable Databricks deletes, so that I can proceed after human confirmation without treating ask as a Dev Loop failure.
23. As an agente em projeto-filho, I want the same policy catalog whether I run under Claude Code or Cursor, so that switching IDE does not change what is forbidden.
24. As an agente em projeto-filho, I want opt-in extras via `.harness/policies/project_profile.yaml`, so that my stack can enable additional cloud CLI families without forking the engine.
25. As an agente em projeto-filho, I want clear deny messages naming family/pattern (never silent allow), so that I know what to change or escalate.
26. As an agente em projeto-filho, I want bypass only via explicit env + log trail, so that destructive work is conscious and reviewable, not accidental.
27. As an engenheiro no filho, I want soft policy `seguranca` to remain (ask human + ADR for prod DDL), so that mechanical deny and human SI process reinforce each other.
28. As an engenheiro no filho, I want re-install to KEEP my `families[]` profile, so that harness upgrades do not wipe local opt-ins.

### Segurança / SI (nível d)

29. As a responsável por SI, I want deny-hard fail-closed for irreversible ops, so that a broken guard does not open a destruction window.
30. As a responsável por SI, I want bypass audit trails without secrets or PII in logs, so that LGPD/SI logging rules hold for command redaction heuristics.
31. As a responsável por SI, I want ADR still required for prod/DDL destructive actions even with bypass, so that mechanical allow does not replace governance.
32. As a responsável por SI, I want §1.3 documented next to agent-policies (bypass, `--no-verify`, clone without hooks, no Edit policies), so that auditors are not misled by “we have deny lists”.
33. As a responsável por SI, I want githooks to remain secrets-focused (not anti-shell), so that layers stay clear and responsibilities do not blur.
34. As a revisor, I want install fixtures proving child `deny` is non-empty and Cursor hooks exist, so that the historic `deny: []` gap cannot regress silently.

### Install / propagação

35. As an operador de `/install-harness`, I want foundation always-on for agent-policies (not a niche category), so that every child gets the core freio.
36. As an operador de `/install-harness`, I want generate (not hand-copy of dogfood machine paths) for settings/hooks, so that children get portable policy artifacts.
37. As an operador de `/install-harness`, I want Cursor hooks as first-class install artifacts (not relying on `settings.json` mirror), so that Cursor parity survives the existing mirror early-return for settings.
38. As an operador de `/install-harness`, I want optional CLI `python -m config.agent_policies generate|check` (SHOULD), so that I can regenerate/verify policy outputs offline.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `agent-policies.yaml` carrega no loader tipado; core families presentes com severity | pytest contrato / loader |
| AC2 | Matcher: comando deny-hard → deny; ask → ask (não allow silencioso) | pytest matcher |
| AC3 | Guard Claude adapter (stdin JSON fixture) → deny/ask/allow coerente | pytest guard |
| AC4 | Guard Cursor adapter (`beforeShellExecution` payload) → `permission` coerente | pytest guard |
| AC5 | `HARNESS_ALLOW_DESTRUCTIVE=1` permite deny-hard e emite trilha (sem secret) | pytest bypass + log assert |
| AC6 | Fail closed: YAML inválido / engine down em path deny-hard → bloqueia | pytest |
| AC7 | Fail open: engine down em ask/opt-in → não bloqueia Dev Loop | pytest |
| AC8 | Install fixture: filho com `deny` ≠ `[]`; `.cursor/hooks.json` presente | pytest install generate |
| AC9 | Seed `.harness/policies/project_profile.yaml` com `families[]`; KEEP no re-install | teste seed / install |
| AC10 | Core families always-on; extras só com profile opt-in | pytest generate matrix |
| AC11 | `DE-A002` regressão intacta; sem unificação de kernels | pytest DE existente |
| AC12 | Docs §1.3 / SI / cross-link `seguranca` + `DE-A002` sem prometer Edit policies | review + grep honestidade |
| AC13 | Template gerado sem path de máquina obrigatório | fixture install assert |
| AC14 | Espelho hooks/scripts Claude↔Cursor (artefatos de projeto) na mesma sessão | checklist simétrica |
| AC15 | `/validar` verde no canônico após implementação | ruff + mypy + pytest |

---

## Functional Requirements

### FR1 — Contrato `agent-policies.yaml`

- Fonte única de famílias, patterns (Bash/CLI), severity (`deny` | `ask`).
- Core families (decisão 10): `shell`, `docker`, `git`, `sql-cli`, `databricks-cli`,
  `terraform`, `k8s`.
- Catálogo completo versionado; famílias extras existem no YAML mas só ativam via profile.
- Severity default (decisão 12): deny-hard para irreversível infra/dados; ask para git
  force/reset e deletes Databricks recuperáveis com dor.

### FR2 — Engine `config/agent_policies/`

- Load tipado (padrão dos loaders `git_hygiene` / `data_engineering`).
- Matcher determinístico por invocação (sem rede; latência ms).
- Generate: materializa `permissions.deny` Claude + config/scripts de hooks Cursor/Claude.
- CLI SHOULD: `python -m config.agent_policies generate|check`.

### FR3 — Dual runtime (paridade política)

- Claude: `permissions.deny` + PreToolUse chamando entrypoint compartilhado.
- Cursor: `.cursor/hooks.json` + scripts com `beforeShellExecution` retornando
  `permission: ask|deny|allow`.
- Mesmo catálogo/severity; UI pode diferir; política não.
- Adapters finos isolam contrato stdin/stdout de cada runtime.

### FR4 — Install foundation + seed

- Foundation sempre-on: engine + core + hooks dual (corrige `deny: []`).
- Seed template → `.harness/policies/project_profile.yaml` (`families[]`, `seed: true`,
  KEEP).
- Extras via marker/profile; não exigir categoria opcional para o core.
- Generate portável: sem paths de máquina no template de filho.

### FR5 — Bypass e falha

- `HARNESS_ALLOW_DESTRUCTIVE=1` (ou equivalente documentado): short-circuit + log
  (timestamp, family/pattern, decisão `bypass`, adapter) — sem secret.
- Prod/DDL: ADR + rule `seguranca` mesmo com bypass.
- Fail closed em deny-hard; fail open em ask / opt-in (decisão 7).
- Sem retry automático de ops destrutivas.

### FR6 — Ortogonalidade DE-A002

- Não alterar `DE-A002` / `package_a` destructive checks.
- Docs: cross-link “runtime Bash gate” vs “código versionado DE”.
- Soft policy `seguranca` permanece; githooks permanecem secrets-only.

### FR7 — Documentação e honesty §1.3

- Ponte em `seguranca` e/ou cheatsheet curta de agent-policies.
- Declarar: deny/hooks ≠ Edit policies; bypass env; `--no-verify`; clone sem hooks.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | SI **d**: freio real em ops destrutivas; bypass só consciente + auditável |
| NFR-SI2 | Logs de deny/bypass sem secrets; comando matched truncado/redacted se parecer credencial |
| NFR-SI3 | Sem novos campos PII de domínio (nível d, não c); sem `[AVISO_LGPD]` obrigatório neste ship |
| NFR-SI4 | ADR obrigatório para escrita/DDL destrutivo em produção (rule `seguranca`) |
| NFR-SI5 | Honesty §1.3: não prometer bloqueio server-side / Edit policies |
| NFR-Q1 | Match local sem I/O de rede; latência ordem de ms |
| NFR-Q2 | Ask ≠ falha/timeout do Dev Loop — pausa de confirmação do runtime |
| NFR-Q3 | Avaliação por invocação; sem mutex cross-agent no MVP |
| NFR-Q4 | Espelho de hooks/scripts Claude↔Cursor na mesma sessão de promoção |
| NFR-Q5 | Soft-block git: fetch Azure 403 → trabalho na branch local; sem inventar sync |

---

## Architecture — artefatos canônicos

```text
┌─ agent-policies.yaml ──► famílias / patterns / severity
│
├─ config/agent_policies/ ──► load · match · generate · (CLI)
│
├─ Claude: settings permissions.deny + PreToolUse → guard
├─ Cursor: hooks.json + beforeShellExecution → guard
│         (mesmo matcher; adapters finos)
│
├─ install-harness foundation ──► engine + core + hooks dual
├─ seed .harness/policies/project_profile.yaml ──► families[] KEEP
│
├─ bypass HARNESS_ALLOW_DESTRUCTIVE + log
├─ docs: seguranca · §1.3 · cross-link DE-A002
└─ tests/agent_policies/ ──► matcher · guard · install fixture
```

### Amarras a módulos lógicos (evitar paths frágeis demais)

| Artefato | Módulo / superfície |
|---|---|
| Contrato | `agent-policies.yaml` (raiz) |
| Engine | `config/agent_policies/` |
| Hook Claude | settings PreToolUse + hooks sob `.claude/` |
| Hook Cursor | `.cursor/hooks.json` + hooks sob `.cursor/` |
| Seed | templates policies → `.harness/policies/` |
| Install | foundation / `stack_map` + generate em `install_harness` |
| Rule / docs | ponte `seguranca` + §1.3 / CONTEXT |
| Testes | `tests/agent_policies/` |
| DE-A002 | inalterado — cross-link only |
| Projeto | `.claude/projetos/policies-anti-destrutivas/` (+ espelho `.cursor/projetos/`) |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | Perímetro dual Claude+Cursor no mesmo ship | FR3 / AC3–AC4 |
| 2 | YAML canônico + script único; paridade Cursor | FR1–FR2 / AC1 |
| 3 | Híbrido deny-hard / ask | FR1 severity / AC2 |
| 4 | Catálogo completo | FR1 |
| 5 | Core default; extras opt-in via profile | FR4 / AC10 |
| 6 | Install foundation sempre-on | FR4 / AC8 |
| 7 | Fail closed deny-hard; fail open ask/opt-in | FR5 / AC6–AC7 |
| 8 | Bypass env + log; ADR se prod/DDL | FR5 / AC5 |
| 9 | DE-A002 ortogonal (cross-link) | FR6 / AC11 |
| 10 | Core families shell+docker+git+sql-cli+databricks-cli+terraform+k8s | FR1 / AC1 |
| 11 | Testes matcher + guard + fixture install | Testing Decisions / AC2–AC8 |
| 12 | Severity default deny vs ask | FR1 |
| 13 | Layout yaml + config/agent_policies + hooks dual | Architecture |
| 14 | Marker `.harness/policies/project_profile.yaml` | FR4 / AC9 |
| 15 | Fora: Edit policies / portal / live API / agent / remover seguranca | Out of Scope |
| I1 | Cursor `permission: ask\|deny\|allow` | FR3 |
| I2 | Install corrige `deny: []` via generate | FR4 / AC8 |
| I3 | Hooks Cursor são artefato próprio (não mirror settings) | FR3 / FR4 |
| I4 | Githooks = secrets, não anti-shell | FR6 / SI |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (decisão deny/ask/allow, payloads de hook,
conteúdo gerado no install, trilha de bypass), não detalhes privados de regex salvo o
contrato documentado no YAML.

Alinhado à **decisão 11**: matcher + guard script + fixture install; E2E IDE = dogfood
manual (fora do CI obrigatório).

| Área | O que testar | Prior art |
|---|---|---|
| Contrato YAML | load tipado; core families + severity | `tests/git_hygiene/`, `tests/data_engineering/` contrato |
| Matcher | comandos representativos → deny / ask / allow | unit puro, sem IDE |
| Guard | stdin JSON → stdout/exit/`permission` por adapter | fixtures JSON versionadas |
| Bypass | env set → allow + log sem secret | pytest env monkeypatch |
| Fail closed/open | YAML quebrado / engine stub | pytest matrix severity |
| Install generate | `deny` ≠ `[]`; hooks Cursor presentes; sem path de máquina | testes install / stack_map (estilo DE vault) |
| Seed KEEP | re-install não apaga `families[]` | seed `true` pattern (data-check) |
| DE-A002 regressão | destructive code check intacto | `tests/data_engineering/` |
| SI honesty | docs não prometem Edit policies | review checklist |

### Plano de validação (DoD gate)

```bash
# Código (sempre)
uv run ruff check --fix . && uv run mypy . && uv run pytest -q

# Suite nova (quando existir)
uv run pytest -q tests/agent_policies/

# CLI SHOULD (quando existir)
python -m config.agent_policies check
python -m config.agent_policies generate --dry-run   # ou equivalente documentado
```

Critério: gate **verde** no canônico; fixtures de install PASS; sem E2E IDE obrigatório no CI;
DE-A002 regressão verde.

---

## Out of Scope

Materializa a **decisão 15** + lista do grill:

- Edit policies / branch protection server-side / portal UI
- Live API cloud no CI do canônico para “provar” destroy
- Agent dedicado “policy officer” no canônico
- Remover rule `seguranca` (soft policy permanece)
- Unificar ou deprecar `DE-A002`
- E2E obrigatório Claude Code / Cursor IDE no CI (só dogfood manual)
- Transformar githooks em anti-shell (permanecem secrets)
- Multi-tenant / RBAC de produto / SIEM central de bypass
- Tag `prod-*` / Fase 2 git hygiene
- Key vault / pacote E (N/A — projeto ortogonal)

---

## Risks

| Risco | Mitigação |
|---|---|
| Drift Claude↔Cursor | generate único a partir do YAML; testes dual-adapter |
| Falso negativo (pattern incompleto) | catálogo completo versionado; dogfood core+extras no canônico (SHOULD) |
| Falso positivo (bloqueia Dev Loop) | severity ask + fail open em opt-in; bypass explícito |
| Runtime deixa de honrar deny/ask | adapters + fixtures; docs §1.3 honestos |
| Install volta a emitir `deny: []` | AC8 fixture bloqueante |
| Paths de máquina no dogfood vazam p/ filhos | generate portável; limpeza SHOULD no settings canônico |
| Confusão com DE-A002 | FR6 cross-link; kernels separados |
| Fetch Azure 403 atrasa sync | soft-block didático; branch local `feat/policies-anti-destrutivas` |
| Promessa excessiva de “impede de fato” | AC12 + NFR-SI5 §1.3 |

---

## SI Considerations

- **Nível d:** freio real contra ops de escrita/deleção destrutivas (local, DB CLI, cloud
  CLIs no catálogo). Não é Assessment c (PII) — sem `rules/pii.md` / `[AVISO_LGPD]`
  obrigatório neste ship, salvo descoberta futura.
- Deny-hard + fail closed no path crítico; bypass só via env explícita com trilha.
- ADR + confirmação humana (`seguranca`) para DDL/escrita em produção — bypass não
  substitui governança.
- Logs: sem secret; redaction leve de comando se parecer credencial.
- **Honesty §1.3 (CONTEXT / git-hygiene):** sem Edit policies / branch protection, nenhum
  gate impede de fato; `--no-verify` e clone sem hooks contornam; este ship entrega o
  melhor freio **local** dual-runtime, não bloqueio server-side.
- Githooks continuam camada de secrets — não confundir com agent-policies.
- Revisor-codigo: SI bloqueante se o ship prometer Edit policies ou remover honesty §1.3.

---

## Further Notes

- **Adversarial judge (grill/define):** pulado (b) — sem `01b-judge.md`.
- **Adversarial judge (PRD):** pendente — checkpoint obrigatório antes do
  `/harness-architect`.
- SLA do hook: match local ms; ask = pausa humana, não timeout de task; cold start YAML
  aceitável; preferir cache in-process se o runtime reusar o processo.
- Concorrência: dois agents na mesma env de bypass podem ambos passar — risco residual do
  operador, fora do escopo do gate.
- Naming exato da CLI (`generate|check`) e paths de templates podem fechar na task de
  implementação desde que FR1–FR7 e ACs sejam preservados.

---

## Próximo passo (após aceite do PRD + judge)

1. Checkpoint adversarial judge (a/b) — se (a), gerar `02b-judge.md` e opcionalmente
   ajustar o PRD
2. `/harness-architect` — montar/atualizar artefatos de harness desta evolução
3. Registrar `03-harness.md` → `/to-tasks` → `harness-build`
