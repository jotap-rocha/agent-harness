# Key Vault OCI vs Azure — Grill & Requisitos

Slug: `keyvault-oci-azure-choice`  
Branch: `feat/oci-vault-harness`  
Grill fechado em: 2026-08-11  
Fontes: `00-ideia.md`, `00b-codebase-canonico.md`, `00b-codebase-referencia-prd.md`, decisões do `/grill-me`

## Contexto (da sessão /grill-me)

### Problema

Projetos-filho que precisam de key vault na nuvem não têm no canônico: pergunta formal
OCI vs Azure, KB/skill dual-cloud, example greenfield, nem checks de *wiring* além do
`DE-A001` (regex de literais). A decisão some do `/novo-projeto` e o install não propaga
artefatos de vault. O PRD `data-sql-capacity-evolution-prd` já prova um padrão OCI
(facade + map de IDs + auth dual), mas isso está product-bound e sem paridade Azure.

### Usuários

| Persona | Pain |
|---|---|
| Autor do harness / maintainer do canônico | Precisa de artefatos genéricos reutilizáveis (KB, skill, example, checks) sem acoplar a um produto |
| Eng. de dados / agente em projeto-filho (tipo b/c/d) | Precisa escolher cofre, wiring seguro e dogfood estático sem live API |
| Revisor / SI | Precisa de invariantes auditáveis: nunca logar secret; placeholders; ponto único SDK |

### Objetivos (MoSCoW)

**MUST:**
- Pergunta OCI vs Azure obrigatória no grill/define, com default por stack + confirmação
- Skill dual `cloud-secrets` + KBs `oci-vault` e `azure-keyvault` (paridade; sem agent no canônico)
- Pacote E `keyvault-cloud` (DE-E*) no kernel; facade + map só IDs/URIs; ponto único (sem SDK nos consumidores)
- Marker `secret_store: oci|azure|multi` **ou** auto-detect; `/validar` dispara E quando aplicável
- Examples `…-oci-min` e `…-azure-min` (placeholders; fora do `stack_map`)
- Install condicional: skill + KBs quando a stack pede secrets
- Espelho `.claude` ↔ `.cursor`

**SHOULD:**
- Default: host Databricks/Azure → Azure; sinal OCI → OCI; senão sem default (forçar escolha)
- Scaffold template canônico; examples instanciam
- União multi quando OCI+Azure no tree
- Pontes curtas em KBs/rules SI existentes (`seguranca`, cloud-platforms se fizer sentido)

**COULD:**
- Menção explícita “outro cofre” (fora de escopo de implementação)
- Agent `key-oci-expert` no projeto-filho (fora do MVP canônico)

### Out of Scope

- Agent dedicado no canônico / propagar `key-oci-expert` via install
- Live calls OCI/Azure Vault no CI do canônico
- Outros cofres (AWS Secrets Manager, HashiCorp, etc.) — só menção “outro”
- Pergunta vault em `install-harness` / commands DE (permanece só grill/define — B1)
- Remover ou substituir `DE-A001` (permanece)
- PII (SI c) e write em produção (SI d) — fora do Assessment atual

### Restrições

- Entrega = evolução do **framework** (não produto pipeline único); tipos b+c+d como consumidores
- SI a+b: nunca logar/expor valor de secret; placeholders em examples/templates
- Sem SDK vault nos consumidores — só via facade / ponto único
- Fetch Azure pode falhar 403 — soft-block didático; trabalho em `feat/oci-vault-harness`
- Sem commit/push neste passo define

## Decisões numeradas (grill — fechadas)

1. Pergunta OCI vs Azure: **obrigatória** + default por stack + confirmação humana
2. Skill dual **`cloud-secrets`** + KBs **`oci-vault`** e **`azure-keyvault`**
3. Examples: `…-oci-min` e `…-azure-min`
4. Checks: facade + map só IDs/URIs + ponto único (sem SDK nos consumidores)
5. Applicability: marker `secret_store` **OR** auto-detect
6. Pacote **E** `keyvault-cloud` (IDs `DE-E*`)
7. OCI+Azure no tree → união (**multi**)
8. Install **condicional**: skill + KBs quando stack pede secrets
9. Default: Databricks/Azure host → Azure; sinal OCI → OCI; senão **sem default**
10. Scaffold: template canônico + examples instanciam
11. Nome da skill: **`cloud-secrets`**
12. Marker: `secret_store: oci|azure|multi` em `project_profile.yaml`
13. Outros cofres **fora** (só menção “outro”)
14. Agent no canônico: **NÃO**

### Inferidos (confirmados neste grill doc — não reabrir)

| # | Inferência | Status |
|---|---|---|
| I1 | Examples fora do `stack_map` (padrão DE examples) | Confirmado |
| I2 | `/validar` dispara pacote E quando marker/auto-detect aplicável | Confirmado |
| I3 | `DE-A001` permanece (pacote E é adicional, não substituto) | Confirmado |

## Amarras a artefatos (previsto)

| Artefato | Onde (canônico) | Nota |
|---|---|---|
| Skill `cloud-secrets` | `.claude/skills/cloud-secrets/` (+ espelho `.cursor/`) | Dual OCI/Azure |
| KB `oci-vault` | `.claude/kb/oci-vault/` | Lift padrões do PRD (não product keys) |
| KB `azure-keyvault` | `.claude/kb/azure-keyvault/` | Paridade conceitual |
| Pacote E | `data-engineering.yaml` + `config/canonical_data_check/checks/` | `DE-E*` |
| Marker | `.harness/data-check/project_profile.yaml` → `secret_store` | oci \| azure \| multi |
| Examples | `examples/*-oci-min/`, `examples/*-azure-min/` | Fora `stack_map`; placeholders |
| Scaffold facade | template canônico (path a fechar no PRD) | Examples instanciam |
| Grill/define wiring | agents workflow + checklist define | Pergunta + default + confirmação |
| Install | `install-harness` stack_map condicional | Skill + KBs se secrets |
| SI bridges | `rules/seguranca`, pontes KB | Nunca logar secret |

Referência de lift (somente padrões): `00b-codebase-referencia-prd.md`  
Gaps do canônico hoje: `00b-codebase-canonico.md`

## Pipeline — 10 perguntas (consumidores b/c; framework responde no meta-nível)

Este projeto **não** é um pipeline de produto; as respostas abaixo amarram o que o
harness deve **exigir/documentar** para projetos-filho, não volumes reais de um dataset.

1. **Fontes:** Cofres cloud — Oracle OCI Vault e Azure Key Vault; mapeamento só IDs/URIs (OCID / secret URI); sem live no CI do canônico.
2. **Schema:** Contratos de ID/URI estáveis no map; valor do secret opaco; mudança de contrato de fonte = lente implícita (ver abaixo).
3. **Volume:** N/A no canônico — examples estáticos mínimos; backfill/histórico é concern do filho.
4. **Sensibilidade/PII:** SI **a+b** — secrets/credenciais; tipicamente sem PII no *conteúdo* do secret; **nunca** logar valor; placeholders em examples. SI c/d fora.
5. **SLA:** N/A operacional no canônico; checks FS/estáticos no gate `/validar` (pacote E), sem API live.
6. **Consumidores do Gold:** Agentes/skills em projetos tipo b/c/d; BI/ML do filho ficam fora deste MVP.
7. **Owner/Notificação:** Maintainer do canônico para falha de check E no CI do harness; no filho, owner do pipeline (documentar na skill/KB).
8. **Ambiente:** Dual — on-prem (b) e cloud Databricks/Azure (c) + análise (d); default Azure em host Databricks/Azure; sinal OCI → OCI; senão sem default.
9. **Qualidade — bloqueante vs log:** Wiring sem facade/ponto único / map com literal secreto → **fail** (DE-E*); menção “outro cofre” = doc only; `DE-A001` continua bloqueante para literais.
10. **Portabilidade:** Marker `oci|azure|multi` + examples separados; install condicional; multi = união quando ambos no tree; replicar catalog/env é do filho.

## Especificações implícitas detectadas

| Lente | Decisão |
|---|---|
| 1. Falha de dependência externa | Sem live vault no CI canônico — N/A para gate; skill/KB documentam timeout/auth fail no filho |
| 2. Concorrência | Checks FS estáticos — sem race de write no canônico; filhos: facade idempotente na leitura de secret |
| 3. Idempotência | Reprocessamento/backfill no filho deve re-resolver via facade (mesmo ID → mesmo secret); examples estáticos idempotentes |
| 4. AuthZ | Quem dispara pipeline = concern do filho; canônico: auth dual OCI (config → Resource Principal) e padrão Azure equivalente na KB; sem multi-tenant no framework |
| 5. Dados sensíveis | Coberto por SI a+b / pergunta Sensibilidade — **não repetir**; nunca secret em log/URL/finding |
| 6. Abuso/limites | N/A no canônico (sem API); skill pode mencionar rate limits dos SDKs como nota |
| 7. Auditoria | Findings DE-E* e pre-commit: trilha de *detecção* sem valor; audit de *quem leu secret* = filho |
| 8. Estados de erro | Check E falha no `/validar` com `rule_id` + remediation; skill `cloud-secrets` / `de-conformidade` orientam |
| 9. Ciclo de vida | N/A LGPD esquecimento no MVP; rotação de secret fica a cargo do projeto-filho (KB troubleshooting) |
| 10. Contrato externo muda | Schema/ID de vault muda → map atualiza; check E valida formato ID/URI e presença de facade — não o valor |

## Critérios de sucesso mensuráveis

- Pergunta OCI vs Azure presente e obrigatória no fluxo grill/define, com default por stack + confirmação
- Skill `cloud-secrets` + KBs `oci-vault` e `azure-keyvault` versionados e espelhados `.claude`/`.cursor`
- Pacote E (`DE-E*`) registrado em `data-engineering.yaml` e executado via `canonical_data_check` quando marker/auto-detect
- `/validar` dispara E nos casos aplicáveis; `DE-A001` permanece verde/independente
- Examples `*-oci-min` e `*-azure-min` passam validate estático (placeholders; sem live; fora `stack_map`)
- Install propaga skill+KBs **somente** quando stack pede secrets
- Zero secret real / OCID real em repo; revisor SI sem bloqueante por vazamento nos artefatos novos
- Adversarial judge (opcional): **(b)** pulado — sem `01b-judge.md`

## Soft-blocks registrados

- `git fetch` Azure → HTTP 403 — prosseguido com branch local `feat/oci-vault-harness`
- Working tree: artefatos untracked sob `projetos/keyvault-oci-azure-choice/` (esperado neste fluxo)
- Adversarial judge: **(b)** pulado (2026-08-11)

## Próximo passo

Dizer **`harness-design`** para gerar o PRD (`02-prd.md`) e montar o harness desta evolução.
