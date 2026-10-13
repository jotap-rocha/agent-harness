# Boas práticas de Engenharia de Dados no canônico — Grill & Requisitos

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data grill: 2026-08-06 · Define estruturado: 2026-08-06  
Branch: `feat/de-boas-praticas-canonico`  
Escopo deste artefato: **somente Loop 1 / Ship 1**  
Tipo: **e** — framework de conformidade DE (não pipeline de domínio único)  
SI: **c + d**  
Contexto: `00-ideia.md` + `00b-codebase.md` + sketch  
`sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`

> **Inferências do define:** itens marcados `[inferido]` foram preenchidos a partir dos artefatos + padrão `git-hygiene`. Contestáveis antes do PRD — diga o que mudar.

---

## Contexto (da sessão /grill-me)

### Problema

Prática de Engenharia de Dados documentada no canônico (agents, KBs, `rules/pipeline`) sem **enforcement automático**. Projetos-filhos herdam prosa, não prova. Risco: harness que **explica** boas práticas sem **provar** conformidade (gap central do sketch §3 e do `00b`).

Problema real (não sintoma): ausência de kernel normativo executável (norma versionada → checks → CI/baseline/waiver → example → install mínimo).

### Usuários / Personas `[inferido]`

| Persona | Pain / necessidade no Loop 1 |
|---|---|
| **Autor do canônico** (mantenedor harness) | Evoluir o framework com DoD verificável; não expandir catálogo agentic antes do kernel |
| **Engenheiro DE em projeto-filho** | Receber via `install-harness` um pacote mínimo que **valida** o repo (`spark-yarn-airflow`), sem falsa conformidade |
| **CI do canônico** | Rodar testes do contrato YAML + CLI no example; gerar relatório RO do sql-capacity sem escrever nele |
| **CI / gate do projeto-filho** (pós-install) | `validate` + `compare` com ratchet; `/validar` só dispara check se marker/perfil DE |

### Objetivos (MoSCoW) — Loop 1 / Ship 1

**MUST**

- `data-engineering.yaml` na raiz do canônico (norma versionada; Universal + perfil `spark-yarn-airflow`)
- CLI (`canonical-data-check` ou equivalente): `validate`, `baseline`, `compare` (+ report conforme sketch §11)
- Pacotes de check **A + B** como **blockers**; **C** Airflow **condicional** (skip se sem DAG)
- Example greenfield `examples/spark-yarn-airflow-min/` passando A+B (fora do install automático)
- Relatório RO do brownfield `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd` (sem gravar baseline lá)
- `install-harness`: pacote mínimo verificável (norma subset + CLI + rule + perfil default + KB pipeline; **sem** 10 agents)
- Path no filho: `.harness/data-check/` (`project_profile.yaml` + `baseline.json`)
- Baseline **ratchet** + waiver pontual (owner + expiry)
- `/validar` condicional: CLI sempre disponível; check DE só se marker/perfil
- Testes no canônico (contrato YAML + comportamento CLI no example)
- Espelho `.claude/` ↔ `.cursor/` em toda promoção

**SHOULD**

- `explain <rule_id>` e `report --format json|markdown` na CLI (sketch §11)
- Tempo de execução dentro do SLA declarado abaixo
- Soft-fail claro se path sql-capacity ausente no ambiente de CI

**COULD**

- Diff markdown amigável no relatório RO
- Documentação curta de uso da CLI no README do example

### Out of Scope (Ship 1 / Loop 1)

- Perfis Databricks (`sdp-medallion`, `dlt-legacy`) e modernização SDP → **Loop 2**
- Skills P0 / novos ou reescritos agents / KBs DE “boas práticas” → **Loop 3**
- Propagar 10 agents + 7 commands DE no install → **Loop 3**
- `install-harness --scaffold` (bootstrap de projeto novo)
- Escrever arquivos no repo sql-capacity
- Quarentena DLT / schema rescue Databricks → **Loop 2**
- Full enforcement sem baseline em brownfield remoto

### Restrições

- Tipo **e**: produto = framework; não implementar pipeline de negócio no canônico
- sql-capacity: **somente leitura**; qualquer escrita futura exige acordo explícito
- Não criar agents DE novos até o kernel existir (`00b` + sketch §3)
- `git fetch` 403 neste ambiente — sync remoto do canônico não confirmado
- Working tree com untracked (`sketch/`, `projetos/`) — commit só com acordo explícito
- SI c+d: checks de secrets/PII em logs; não processar dados de negócio do sql-capacity além de inspeção estática RO

---

## Decisões do grill (preservadas — 13)

| # | Tema | Escolha |
|---|---|---|
| 1 | Escopo MVP do kernel | **Universal + um perfil piloto** |
| 2 | Perfil piloto ship 1 | **`spark-yarn-airflow`**; Databricks depois |
| 3 | Checks bloqueantes | **A + B blockers**; **C Airflow condicional/opcional** |
| 4 | Alvos de piloto | **Greenfield no canônico + brownfield PRD** |
| 5 | Brownfield | `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd` — **somente leitura** neste ship |
| 6 | Baseline / waiver | **Baseline ratchet** (falha nova quebra; waiver pontual com owner + expiry) |
| 7 | `install-harness` | **Pacote mínimo verificável** (norma subset + CLI + rule + perfil default + KB pipeline; **sem** 10 agents ainda) |
| 8 | Scaffold greenfield | **`examples/spark-yarn-airflow-min/`** (fora do install automático) |
| 9 | Gate diário | **CLI sempre** + **`/validar` chama check só se perfil/marker DE** |
| 10 | Onde vive baseline | **No projeto-filho via install** (não baseline do sql-capacity no canônico); sql-capacity = relatório RO neste ship |
| 11 | Path no projeto | **`.harness/data-check/`** (`project_profile.yaml` + `baseline.json`) |
| 12 | Fonte normativa canônico | **`data-engineering.yaml` na raiz** (padrão git-hygiene) + prose em `.claude/rules/` / `.cursor/rules/` |
| 13 | DoD Ship 1 | YAML + CLI validate/baseline/compare + example passando A+B + relatório RO sql-capacity + install pacote mínimo + `/validar` condicional + testes no canônico |

### Detalhe dos checks (decisão 3)

| Pacote | Conteúdo | Severidade | Aplicabilidade |
|---|---|---|---|
| **A** | secrets; destrutivo com gate; layout mínimo (`config/`, `pipelines/` ou `src/jobs/`, `tests/`); `run_id`/logging declarado; owner declarado | blocker | Universal |
| **B** | camadas medalhão/landing→processed; ban `select *` em transform; contrato de dados mínimo versionado | blocker | perfil `spark-yarn-airflow` |
| **C** | tags DAG; pré→carga→pós; spark-submit via `config/spark.conf` | condicional | só se Airflow/DAG detectado; senão skip |

### Baseline (decisões 6, 10, 11)

- Ratchet: CI falha só em **regressão** (finding novo vs baseline).
- Template/schema no canônico; artefato vivo em **`.harness/data-check/`** do projeto (criado pelo install).
- sql-capacity: **não gravar** baseline lá neste ship; só leitura + relatório no canônico/CI do harness.

---

## Roadmap de loops (acordo pós-grill)

Ordem **não invertível** (kernel prova conformidade antes de expandir catálogo agentic):

| Loop | Foco | Notas |
|---|---|---|
| **1 (atual)** | Kernel `spark-yarn-airflow` — YAML + CLI + baseline/waiver + example + install mínimo + `/validar` condicional | Sem novos agents/skills DE |
| **2** | **Databricks** (SDP/DLT, DAB, UC, checks condicionais do perfil cloud) | Reusa o mesmo `data-engineering.yaml` + CLI |
| **3** | **Skills + agents + KBs** só de boas práticas de Engenharia de Dados | Evoluir os 10 agents / 7 commands / KBs existentes; amarrar a IDs de regras; propagar via install **só depois** do kernel estável nos loops 1–2 |

---

## Framework Loop 1 — 10 perguntas adaptadas (tipo e)

Adaptação: produto = kernel de conformidade + example + install; perfil `spark-yarn-airflow` define o que se assume sobre filhos/example.

1. **Fontes (o que o validator “ingere”):** filesystem do repo-alvo — layout de pastas, configs (`config/`), SQL/PySpark em `pipelines/` ou `src/jobs/`, testes, DAGs Airflow se existirem, marker/perfil em `.harness/data-check/project_profile.yaml`. **Frequência:** a cada `validate` / CI / `/validar` condicional — não há ingestão de dados de negócio em runtime.

2. **Schema (das regras):** `data-engineering.yaml` versionado na raiz. Evolução `[inferido]`: campo `version` inteiro (padrão `git-hygiene.yaml`); **MINOR** = regras/checks aditivos ou severidade não breaking; **MAJOR** = remoção/renome de IDs, mudança de severidade blocker→relax ou layout incompatível com CLI anterior. Prose em rules espelhada, não é fonte normativa.

3. **Volume:** N/A em GB. Volume operacional = nº de checks A/B/C + tamanho estático dos alvos (example pequeno; sql-capacity RO inspeção estática). Sem backfill de dados.

4. **Sensibilidade / PII (SI c+d):** canônico não processa PII de negócio. Checks devem detectar secrets e padrões de PII em logs/código estático. sql-capacity: **somente inspeção estática RO** — não executar jobs, não ler datasets produtivos, não expor PII em output do LLM/relatório além do necessário para o finding (paths/rule IDs; sem dumps de conteúdo sensível).

5. **SLA `[inferido]`:** CLI no **example** (validate A+B): **≤ 60s** em máquina típica de CI. Relatório RO sql-capacity: **≤ 5 min**. Timeout configurável; estouro = falha do job de CI do canônico (exceto soft-fail de path ausente — ver lente abaixo).

6. **Consumidores do “Gold” (output do kernel):** CI do canônico; engenheiros DE (stdout/markdown/json); `/validar` condicional; `install-harness` (propaga CLI + norma); futuramente `revisor-codigo` / lanes PASS/FAIL/WAIVED (Loop 3 — não obrigatório no Ship 1).

7. **Owner / notificação `[inferido]`:** owner do `data-engineering.yaml` e do kernel = **mantenedor do canônico / equipe harness** (autor do projeto). Quebra de check no canônico (example/CI) → falha de CI na branch do harness; sem pager externo no Loop 1. Em projeto-filho pós-install: owner declarado no perfil/projeto (check A).

8. **Ambiente:** Loop 1 = on-prem **`spark-yarn-airflow`**. Cloud Databricks = **Loop 2**. Portabilidade futura via mesmo YAML + perfis.

9. **Qualidade (blocker vs log):** A+B = **fail (blocker)**; C = skip se sem Airflow, senão blocker do pacote C. Findings já no baseline = não falham (ratchet). Waiver pontual = WAIVED com owner + expiry (não silencioso). Warnings/recomendadas (categoria Recomendada/Informativa do sketch §6): **LOG** no Loop 1 se presentes no YAML — não bloqueiam DoD Ship 1 além de A+B(+C se aplicável).

10. **Portabilidade:** pacote install em projetos-filhos; artefatos em `.harness/data-check/`; perfis futuros (Databricks) reusam CLI + YAML sem segundo framework.

---

## Especificações implícitas detectadas

1. **Falha de dependência externa:** sql-capacity path ausente ou inacessível → `[inferido]` **soft-fail** no job de relatório RO (aviso + exit não bloqueante do kernel/example); CI do canônico continua verde para validate do example. Rede/SCM 403 no fetch do canônico → soft-block didático (já documentado); não bloqueia desenvolvimento local do kernel.

2. **Concorrência `[inferido]`:** dois jobs CI no **mesmo** `baseline.json` do filho → escrita serializada / last-write-wins documentado; recomendação: um job de gate por pipeline. No canônico, example e relatório RO não compartilham baseline mutável do sql-capacity.

3. **Idempotência `[inferido]`:** `validate` e `compare` são seguros de reexecutar (somente leitura + exit code). `baseline` (gerar/atualizar) é idempotente no sentido de sobrescrever o artefato de forma determinística a partir do estado atual — **não** deve mutar o repo sql-capacity; no filho, exige acordo de processo (commit do baseline).

4. **Autenticação/Autorização:** N/A no Loop 1 para a CLI (filesystem local). Multi-tenant = perfis por projeto-filho, não isolation runtime. Quem dispara: desenvolvedor, CI, `/validar`. Sem RBAC novo no Ship 1.

5. **Dados sensíveis:** coberto pela pergunta 4 / SI c+d — não repetir.

6. **Abuso e limites `[inferido]`:** sem rate limit de rede (CLI local). Limite prático = timeout SLA; escopo de scan = árvore do repo-alvo (respeitar ignores típicos: `.git`, venv, etc. — detalhar no design).

7. **Auditoria:** findings e waivers devem ser rastreáveis (rule_id, path, severidade, waiver owner/expiry). Trilha “quem rodou a CLI” = logs de CI do consumidor; sem store central no Loop 1.

8. **Estados de erro:** exit codes distintos `[inferido]` — 0 = pass (ou só warnings); ≠0 = blockers novos / erro de execução. Mensagens apontam rule_id + path. Retry = reexecução manual/CI (idempotente).

9. **Ciclo de vida dos dados:** N/A — o kernel não persiste dados de negócio. Baseline/waiver têm expiry no waiver; baseline vivem no repo-filho sob git.

10. **Dependência de terceiros / contrato externo:** schema do YAML e layout do example são o contrato. Mudança breaking → MAJOR. Se Airflow/Spark APIs mudarem, checks C/B podem precisar de ajuste no Loop 1.1+; sql-capacity layout drift → relatório RO reflete findings, sem auto-fix.

---

## Critérios de sucesso mensuráveis (Loop 1)

| Métrica | Alvo |
|---|---|
| Example `examples/spark-yarn-airflow-min/` | **PASS** nos pacotes A+B (`validate`) |
| Pacote C no example | skip **ou** PASS se DAG presente (conforme scaffold) |
| Relatório RO sql-capacity | artefato gerado (json e/ou markdown) sem escrita no repo alvo |
| Path sql-capacity ausente | soft-fail documentado; não quebra validate do example |
| Install pacote mínimo | dry-run / install em fixture de projeto-filho cria `.harness/data-check/` + CLI utilizável |
| `/validar` | sem marker/perfil DE → **não** invoca data-check; com marker → invoca |
| Testes canônico | pytest (ou suite do repo) cobre schema/contrato do YAML + CLI no example |
| SLA CLI example | ≤ 60s `[inferido]` |
| Falsa conformidade | install **inclui** CLI; ausência de checks = anti-DoD |

---

## Riscos e invariantes

1. **RO no sql-capacity** — qualquer escrita futura exige acordo explícito.
2. **Não criar agents novos** até o kernel (YAML + CLI) existir — reforçado pelo `00b`.
3. **Espelho** `.claude/` ↔ `.cursor/` em toda promoção.
4. **Falsa conformidade** — install sem checks é anti-objetivo; pacote mínimo deve incluir a CLI.
5. `git fetch` 403 neste ambiente — sync remoto do canônico pode estar desatualizado; revalidar antes de push.
6. Itens `[inferido]` contestáveis no design se o usuário discordar.

---

## Próximo passo

Requisitos do **Loop 1** estruturados neste arquivo.

1. (Opcional) adversarial-judge via OpenRouter neste grill.
2. **`harness-design`** — gerar o PRD e montar o plano de implementação do kernel (YAML → CLI → example → install → `/validar` → testes → relatório RO).
3. **Não** abrir Loop 2 (Databricks) nem Loop 3 (skills/agents/KBs) até o DoD do Loop 1 estar verde.
