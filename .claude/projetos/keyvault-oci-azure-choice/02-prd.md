# PRD — Key Vault OCI vs Azure (escolha + artefatos no canônico)

Slug: `keyvault-oci-azure-choice`  
Repo: Agent Harness Canônico (framework — **não** produto ETL de domínio)  
Branch: `feat/oci-vault-harness`  
Data: 2026-08-11  
Tipo: **b + c + d** (consumidores) — entrega = **evolução do harness**  
SI: **a + b**  
Fontes: `00-ideia.md`, `00b-codebase-canonico.md`, `00b-codebase-referencia-prd.md`,
`01-grill.md` (14 decisões + I1–I3)  
Referência de lift (padrões, não product keys):
`/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd`

> Decisões do grill estão **fechadas** — este PRD as materializa; não reabre a matriz.

---

## Problem Statement

Projetos-filho (tipos b/c/d) que precisam de key vault na nuvem **não encontram no
canônico** um caminho genérico e auditável para escolher e wiring OCI Vault vs Azure Key
Vault. Hoje o harness só cobre secrets de forma genérica (`rules/seguranca` + `DE-A001`
regex de literais + pre-commit): não há pergunta formal OCI vs Azure no grill/define, nem
KB/skill dual-cloud, nem example greenfield, nem checks de *wiring* (facade / map /
ponto único).

O sintoma é “cada projeto inventa o seu vault”. O problema real é a ausência de um
**contrato de framework**: decisão explícita no `/novo-projeto` → artefatos JIT (skill +
KBs) → scaffold + examples dogfood → enforcement estático (pacote E) no `/validar` →
install condicional. Sem isso, o padrão já provado no PRD sql-capacity (`key_oci.py` +
map de OCIDs + auth dual) permanece **product-bound** e sem paridade Azure.

Mantenedores do canônico e engenheiros/agentes em filhos precisam de artefatos
reutilizáveis, SI-safe (nunca logar secret; placeholders), sem agent dedicado no canônico
e sem live API no CI do harness.

---

## Solution

Evoluir o canônico com um **pacote dual-cloud de secrets** (OCI + Azure), amarrado ao
kernel DE e ao fluxo grill/define:

1. **Pergunta obrigatória** OCI vs Azure em `/grill-me` / `harness-define`, com default por
   stack + confirmação humana (sem default quando ambíguo).
2. **Skill** `cloud-secrets` (dual) + **KBs** `oci-vault` e `azure-keyvault` (paridade;
   **sem** agent no canônico).
3. **Pacote E** `keyvault-cloud` (`DE-E*`) no `data-engineering.yaml` + check FS em
   `config/canonical_data_check/checks/` — facade + map só IDs/URIs + ponto único (sem SDK
   nos consumidores); **adicional** a `DE-A001` (I3).
4. **Applicability:** marker `secret_store: oci|azure|multi` **OU** auto-detect; OCI+Azure
   no tree → união **multi**; `/validar` dispara E quando aplicável (I2).
5. **Examples** `examples/*-oci-min/` e `examples/*-azure-min/` (placeholders; fora do
   `stack_map` — I1); scaffold template canônico que os examples instanciam.
6. **Install condicional:** propaga skill + KBs quando a stack pede secrets.
7. Espelho obrigatório `.claude/` ↔ `.cursor/` em toda promoção.

Lift do PRD sql-capacity: padrões (auth dual OCI config → Resource Principal, facade
Python, map só IDs, “nunca logar secret”) — **não** product keys, agent `key-oci-expert`,
nem OCIDs reais.

---

## Goals (MoSCoW)

### MUST

- Pergunta OCI vs Azure obrigatória no grill/define + default por stack + confirmação
- Skill `cloud-secrets` + KBs `oci-vault` e `azure-keyvault` (espelho Claude/Cursor)
- Pacote E `keyvault-cloud` (`DE-E*`); facade + map IDs/URIs + ponto único
- Marker `secret_store` OR auto-detect; `/validar` dispara E; `DE-A001` permanece
- Examples `*-oci-min` e `*-azure-min` (placeholders; fora `stack_map`)
- Install condicional skill + KBs quando stack pede secrets
- Zero secret/OCID real no repo; findings sem valor de secret

### SHOULD

- Default: host Databricks/Azure → Azure; sinal OCI → OCI; senão sem default
- Scaffold template canônico; examples instanciam
- União **multi** quando OCI+Azure no tree
- Pontes curtas em `rules/seguranca` e KBs cloud existentes (se fizer sentido)

### COULD

- Menção documental “outro cofre” (fora de implementação)
- Agent `key-oci-expert` só no projeto-filho (fora do MVP canônico)

### WON'T (neste ship)

- Agent dedicado no canônico / propagar `key-oci-expert` via install
- Live calls OCI/Azure Vault no CI do canônico
- AWS Secrets Manager, HashiCorp, etc.
- Pergunta vault em `install-harness` / commands DE (permanece só grill/define — B1)
- Remover/substituir `DE-A001`

---

## User Stories

### Mantenedor do canônico / CI

1. As a mantenedor do canônico, I want a mandatory OCI vs Azure question in grill/define with stack-based default + human confirmation, so that vault choice is explicit in `/novo-projeto`.
2. As a mantenedor do canônico, I want skill `cloud-secrets` dual-cloud versioned under `.claude/skills/` and mirrored to `.cursor/`, so that agents get a playbook without a dedicated agent.
3. As a mantenedor do canônico, I want KBs `oci-vault` and `azure-keyvault` with concepts/patterns/troubleshooting, so that JIT guidance matches both clouds.
4. As a mantenedor do canônico, I want package E `keyvault-cloud` with stable `DE-E*` IDs in `data-engineering.yaml`, so that wiring rules are normative like A–D.
5. As a mantenedor do canônico, I want `check_package_e` registered in `PACKAGE_CHECK_REGISTRY`, so that validate executes E when applicable.
6. As a mantenedor do canônico, I want marker field `secret_store: oci|azure|multi` in `project_profile.yaml`, so that children can override auto-detect.
7. As a mantenedor do canônico, I want auto-detect of OCI/Azure vault wiring signals, so that unmarked trees still get E when vault patterns exist.
8. As a mantenedor do canônico, I want OCI+Azure signals to resolve `multi` (union), so that both check surfaces apply.
9. As a mantenedor do canônico, I want `/validar` to invoke data-check package E when marker OR auto-detect applies, so that the gate covers vault wiring (I2).
10. As a mantenedor do canônico, I want `DE-A001` to remain unchanged and independent, so that literal-secret detection is not replaced by E (I3).
11. As a mantenedor do canônico, I want examples `*-oci-min` and `*-azure-min` outside `stack_map`, so that dogfood stays opt-in like other DE examples (I1).
12. As a mantenedor do canônico, I want a canonical facade scaffold template that examples instantiate, so that greenfield wiring is copy-paste-safe with placeholders.
13. As a mantenedor do canônico, I want pytest covering DE-E* contract + CLI behavior on examples, so that regressions fail harness CI.
14. As a mantenedor do canônico, I want install-harness to copy skill+KBs only when stack needs secrets, so that non-secret projects stay lean.
15. As a mantenedor do canônico, I want findings and reports never to include secret values, so that SI a+b holds in CI output.
16. As CI do canônico, I want validate on vault examples without live OCI/Azure API, so that gates stay offline and reproducible.

### Engenheiro DE / agente em projeto-filho

17. As an engenheiro DE, I want the grill to propose Azure when host is Databricks/Azure and OCI when OCI signals exist, so that defaults match my stack.
18. As an engenheiro DE, I want confirmation even when a default is proposed, so that I never inherit a silent wrong vault.
19. As an engenheiro DE, I want no default when stack is ambiguous, so that I am forced to choose.
20. As an engenheiro DE, I want consumers to call only the facade (no vault SDK imports), so that the single integration point is enforceable.
21. As an engenheiro DE, I want the secret map to store only OCIDs/URIs (placeholders in examples), so that values never land in git.
22. As an engenheiro DE, I want skill `cloud-secrets` to document auth dual (OCI config → Resource Principal; Azure equivalent), so that local and cloud runtimes both work.
23. As an engenheiro DE, I want `de-conformidade` / explain to remediate `DE-E*` rule_ids, so that red `/validar` is actionable.
24. As an engenheiro DE, I want optional local agent `key-oci-expert` to remain a child concern, so that the canonical stays generic.

### Segurança / SI (a+b)

25. As a responsável por SI, I want zero real secrets/OCIDs in canonical examples/templates, so that the framework cannot leak production credentials.
26. As a responsável por SI, I want “never log secret” bridges in `rules/seguranca` and KBs, so that LLM/output paths stay safe.
27. As a responsável por SI, I want revisor-codigo SI checks to flag vault literal leaks as blockers, so that merges cannot ship secrets.
28. As a responsável por SI, I want other vault vendors explicitly out of scope (doc mention only), so that scope creep does not dilute enforcement.

### Aceite testável (DoD deste ship)

| # | Critério | Evidência |
|---|---|---|
| AC1 | Pergunta OCI vs Azure obrigatória no grill/define com default por stack + confirmação; sem default se ambíguo | diff em agents workflow + checklist; teste/fixture de prompt se existir |
| AC2 | Skill `cloud-secrets` existe em `.claude/skills/cloud-secrets/` e espelho `.cursor/` | filesystem + description clara |
| AC3 | KBs `oci-vault` e `azure-keyvault` com index + quick-reference + concepts/patterns mínimos | filesystem espelhado |
| AC4 | `data-engineering.yaml` declara pacote **E** `keyvault-cloud` com regras `DE-E*` | contrato YAML + teste loader |
| AC5 | `check_package_e` no registry; validate executa E quando aplicável | pytest registry + validate |
| AC6 | Marker `secret_store: oci\|azure\|multi` reconhecido em `project_profile.yaml` | teste de_marker / schema |
| AC7 | Auto-detect OCI/Azure; ambos → `multi` | pytest detect |
| AC8 | `/validar` dispara E com marker **ou** auto-detect; sem sinal → não força E | teste `data_check_validate_argv` / should_run |
| AC9 | Checks E: presença de facade; map só IDs/URIs; sem SDK vault nos consumidores | pytest em fixtures positivas/negativas |
| AC10 | `DE-A001` permanece e continua a falhar literais independentemente de E | pytest regressão A001 |
| AC11 | Examples `examples/<nome>-oci-min/` e `examples/<nome>-azure-min/` passam validate estático (placeholders; sem live); **fora** `stack_map` | pytest + grep stack_map |
| AC12 | Scaffold template canônico; examples instanciam (não duplicam lógica divergente) | diff template ↔ examples |
| AC13 | Install propaga skill+KBs **somente** se stack pede secrets | teste stack_map / dry-run install |
| AC14 | Nenhum agent vault no canônico; nenhum secret/OCID real nos artefatos novos | revisão SI + grep heurístico |
| AC15 | Espelho `.claude` ↔ `.cursor` completo neste ship | checklist simétrica |
| AC16 | `python -m config.canonical_data_check validate` nos examples E + `/validar` verde no canônico após implementação | gate local |

---

## Functional Requirements

### FR1 — Pergunta e default (grill/define)

- Obrigatória quando o projeto declara uso de key vault / secrets cloud.
- Default:
  - host Databricks / Azure → **Azure**
  - sinal OCI (paths/config/OCID pattern) → **OCI**
  - senão → **sem default** (forçar escolha)
- Sempre pedir **confirmação** humana mesmo com default.
- Escopo de wiring: **somente** `grill-me` / `harness-define` (não install-harness, não commands DE).

### FR2 — Skill `cloud-secrets`

- Dual OCI + Azure no mesmo skill (playbooks: wiring, auth, troubleshooting, SI).
- Orienta facade + map + ponto único; aponta para KBs JIT.
- Não cria agent canônico.

### FR3 — KBs

- `oci-vault`: lift de padrões do sql-capacity (auth dual, facade, map OCID, decode, nunca logar).
- `azure-keyvault`: paridade conceitual (URI/secret name, DefaultAzureCredential ou equivalente documentado, map só URIs).
- Pontes curtas desde SI / cloud-platforms quando útil — sem copiar domínio inteiro sem necessidade (JIT).

### FR4 — Pacote E (`keyvault-cloud`)

Regras mínimas esperadas (IDs finais no YAML; nomes ilustrativos):

| Rule ID (alvo) | Intenção | Severidade |
|---|---|---|
| `DE-E001` | Facade / ponto único de resolução de secret presente quando vault aplicável | blocker |
| `DE-E002` | Map/config de secrets contém só IDs/URIs (não valores) | blocker |
| `DE-E003` | Consumidores não importam SDK OCI/Azure Vault diretamente | blocker |

- Applicability: marker `secret_store` **OR** auto-detect.
- `multi` = união dos checks/sinais OCI+Azure.
- Sem API live; só filesystem / AST / regex conservadores.
- Remediations em `data-engineering.yaml` + skill `de-conformidade`.

### FR5 — Marker e auto-detect

- Extender `.harness/data-check/project_profile.yaml`:

```yaml
profile: spark-yarn-airflow   # ou databricks-*
secret_store: oci             # oci | azure | multi
```

- Marker override vence auto-detect para `secret_store` (mesmo espírito do perfil DE).
- Auto-detect: sinais de facade/map/SDK/config OCI vs Azure Key Vault (heurística conservadora, espelhando estilo SDP/DLT em `de_marker.py`).

### FR6 — Examples + scaffold

- Nomes alvo (fechados no grill como sufixo): `examples/<slug>-oci-min/` e
  `examples/<slug>-azure-min/` — slug concreto a fechar na implementação
  (ex.: `keyvault-oci-min` / `keyvault-azure-min` ou prefixo alinhado a DE existing).
- Conteúdo: facade stub, `.config.example` / map com **placeholders**, tests smoke, marker
  `secret_store`, README “sem live API”.
- Template scaffold em path canônico (ex.:
  `config/canonical_data_check/templates/keyvault-facade/` ou sob
  `config/templates/cloud-secrets/`) — examples **instanciam**, não forkam.

### FR7 — Install condicional

- Estender `stack_map.json` / categoria adequada: quando stack indica secrets/vault,
  copiar skill `cloud-secrets` + KBs `oci-vault` + `azure-keyvault`.
- Examples **não** entram no `stack_map` (I1).
- Seed `.harness/data-check` permanece KEEP; schema documenta `secret_store`.

### FR8 — Gate `/validar`

- Helper `data_check_validate_argv` / `should_run_data_check` passa a considerar
  aplicabilidade E (marker `secret_store` OR auto-detect vault), além das regras atuais
  (marker DE / SDP/DLT).
- DAB isolado continua sem ativar cloud D sem marker; E só se vault aplicável.

---

## Non-Functional Requirements (SI + qualidade)

| ID | Requisito |
|---|---|
| NFR-SI1 | Nunca logar/expor valor de secret (LLM, findings, URLs, baseline message) |
| NFR-SI2 | Placeholders apenas em examples/templates; proibido OCID/URI real de produção |
| NFR-SI3 | Secrets só via env / secret manager / vault runtime — nunca hardcoded |
| NFR-SI4 | SI c (PII) e d (write prod) **fora** deste Assessment — reabrir se surgir |
| NFR-Q1 | Checks E offline, determinísticos, &lt; ~60s nos examples |
| NFR-Q2 | Espelho `.claude` ↔ `.cursor` na mesma sessão de cada promoção |
| NFR-Q3 | Agents/skills genéricos — sem acoplamento a sql-capacity product keys |
| NFR-Q4 | Soft-block git: fetch Azure 403 → trabalho na branch local; sem inventar sync |

---

## Architecture — artefatos canônicos

```text
┌─ grill / harness-define ──► pergunta OCI|Azure (+ default/confirm)
│
├─ skill cloud-secrets ──► playbook dual
├─ kb oci-vault / azure-keyvault ──► JIT concepts/patterns
│
├─ data-engineering.yaml ──► packages.E (DE-E*)
├─ checks/package_e.py ──► registry "E"
├─ de_marker.py ──► secret_store + auto-detect + multi
│
├─ templates/scaffold facade ──► examples/*-oci-min | *-azure-min
│
├─ install-harness stack_map ──► condicional skill+KBs
└─ /validar ──► A(+…) + E se aplicável; DE-A001 sempre no pacote A
```

### Amarras a paths concretos (canônico)

| Artefato | Path |
|---|---|
| Skill | `.claude/skills/cloud-secrets/` (+ `.cursor/skills/cloud-secrets/`) |
| KB OCI | `.claude/kb/oci-vault/` (+ espelho) |
| KB Azure | `.claude/kb/azure-keyvault/` (+ espelho) |
| Norma | `data-engineering.yaml` → `packages.E` |
| Check E | `config/canonical_data_check/checks/package_e.py` |
| Registry | `config/canonical_data_check/checks/__init__.py` |
| Marker / detect | `config/canonical_data_check/de_marker.py` (+ SCHEMA em `templates/data-check/`) |
| Scaffold | `config/canonical_data_check/templates/` (subpath facade/keyvault a criar) |
| Examples | `examples/<nome>-oci-min/`, `examples/<nome>-azure-min/` |
| Install | `.claude/skills/install-harness/scripts/stack_map.json` (+ espelho skill) |
| Grill wiring | `.claude/agents/workflow/harness-define.md`, skill `grill-me` / agents define |
| SI bridge | `.claude/rules/seguranca.md` → `.cursor/rules/seguranca.mdc` |
| Testes | `tests/data_engineering/` (contrato E, detect, package_e, examples, `/validar`) |
| Projeto | `.claude/projetos/keyvault-oci-azure-choice/` (+ `.cursor/projetos/...`) |

### Decisões de implementação (grill → PRD)

| # | Decisão | Materialização |
|---|---|---|
| 1 | Pergunta + default + confirm | FR1 / agents workflow |
| 2 | Skill dual + KBs | FR2–FR3 |
| 3 | Examples oci-min / azure-min | FR6 |
| 4 | Facade + map IDs + ponto único | FR4 DE-E* |
| 5 | Marker OR auto-detect | FR5 |
| 6 | Pacote E | FR4 |
| 7 | multi = união | FR5 |
| 8 | Install condicional | FR7 |
| 9 | Defaults por stack | FR1 |
| 10 | Scaffold + examples | FR6 |
| 11 | Nome skill `cloud-secrets` | path skill |
| 12 | `secret_store` enum | marker YAML |
| 13 | Outros cofres fora | Out of Scope |
| 14 | Sem agent canônico | AC14 |
| I1 | Examples fora stack_map | FR7 / AC11 |
| I2 | `/validar` dispara E | FR8 / AC8 |
| I3 | DE-A001 permanece | AC10 |

---

## Testing Decisions

**Boa prática:** testar comportamento externo (validate PASS/FAIL, argv do `/validar`,
conteúdo de marker, ausência de SDK nos consumidores), não detalhes privados de regex
salvo contrato documentado.

| Área | O que testar | Prior art |
|---|---|---|
| Contrato YAML | `packages.E` + `DE-E*` carregam | `tests/data_engineering/` contrato A–D |
| Marker | `secret_store` parse + override | `de_marker` tests Loop 2 |
| Auto-detect / multi | fixtures OCI-only, Azure-only, both, none | Databricks signals tests |
| Package E | positive examples PASS; negativos FAIL com rule_id | `package_d` / `package_a` tests |
| `/validar` helper | argv presente/ausente | testes should_run_data_check |
| DE-A001 regressão | literal ainda falha com E presente | package_a |
| Install | stack com/sem secrets | testes install stack_map |
| SI | grep/fixture garante placeholder; finding sem message secret | baseline sanitization |

### Plano de validação (DoD gate)

```bash
# Código (sempre)
uv run ruff check --fix . && uv run mypy . && uv run pytest -q

# DE + E (quando aplicável / nos examples)
python -m config.canonical_data_check validate examples/<nome>-oci-min
python -m config.canonical_data_check validate examples/<nome>-azure-min

# /validar (helper único)
python - <<'PY'
from config.canonical_data_check.de_marker import data_check_validate_argv
import subprocess, sys
argv = data_check_validate_argv(".")
sys.exit(0 if argv is None else subprocess.call(argv))
PY
```

Critério: gate **verde** no canônico + examples E PASS estático; sem live vault.

---

## Out of Scope

- Agent dedicado no canônico (`key-oci-expert` ou similar)
- Propagar agent product-bound via `install-harness`
- Live calls OCI Vault / Azure Key Vault no CI do canônico
- Outros cofres (AWS Secrets Manager, HashiCorp Vault, etc.) — só menção “outro”
- Pergunta vault em install-harness ou commands DE
- Alterar/remover `DE-A001`
- PII masking LGPD (SI c) e DDL/write em produção (SI d)
- MCP bridge Node→Python do sql-capacity como artefato canônico obrigatório (pode ser nota COULD na KB OCI)
- Tag `prod-*` / Fase 2 git hygiene

---

## Risks

| Risco | Mitigação |
|---|---|
| Falso positivo auto-detect (ex.: menção “vault” em docs) | Heurísticas conservadoras; marker override; testes de fixture |
| Duplicação facade divergente entre examples | Scaffold único; examples só instanciam |
| Vazamento de OCID real por copy-paste do PRD | Placeholders obrigatórios; pre-commit + revisor SI |
| Escopo virar “mais um agent” | Decisão 14 explícita; skill+KB only |
| `/validar` ficar lento | Checks FS só; sem SDK network; scope por applicability |
| Fetch Azure 403 atrasa sync | Soft-block didático; branch local `feat/oci-vault-harness` |
| Paridade Azure fraca vs OCI (lift assimétrico) | AC3 exige KB Azure com paridade conceitual mínima |

---

## SI Considerations

- **Nível a+b:** framework docs + domínio de secrets/credenciais.
- Nunca secret em log, finding `message`, URL, baseline.
- Examples: `.config.example` / map com placeholders (`ocid1.vaultsecret.PLACEHOLDER…`,
  `https://<vault>.vault.azure.net/secrets/<name>` fictício).
- Auth documentada (OCI `~/.oci/config` → Resource Principal; Azure DefaultAzureCredential
  ou equivalente) — execução real só no filho.
- Revisor-codigo: SI bloqueante se artefato novo vazar secret.
- Impacto LGPD: tipicamente sem PII no *conteúdo* do secret; se PII entrar no valor, tratar
  no filho e reabrir Assessment (c).

---

## Further Notes

- **Adversarial judge (grill):** pulado (b) — sem `01b-judge.md`.
- **Adversarial judge (PRD):** pulado (b) — sem `02b-judge.md`.
- Roadmap explícito fora deste ship: agent filho opcional; live integration tests em repo
  de produto; outros cofres.
- Naming final dos diretórios `examples/*-oci-min` pode alinhar prefixo na task de
  implementação desde que o sufixo e a exclusão do `stack_map` sejam preservados.

---

## Próximo passo (após aceite do PRD)

1. `/harness-architect` — montar/atualizar artefatos de harness desta evolução
2. Registrar `03-harness.md` → `/to-tasks` → `harness-build`
