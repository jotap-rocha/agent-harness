# Glossário de domínio

> Vocabulário do canônico (framework) — não implementação de produto.
> Termos abaixo refletem o que está **implementado** após:
> - `git-hygiene-azure-devops` (Fase 1 — Camada Convenção)
> - `engenharia-de-dados-boas-praticas-canonico` (Loop 1 — kernel DE spark-yarn-airflow)
> - `engenharia-de-dados-boas-praticas-canonico` (Loop 2 — kernel DE Databricks SDP/DLT)
> - `engenharia-de-dados-boas-praticas-canonico` (Loop 3 — catálogo agentic DE + install completo)
> - `keyvault-oci-azure-choice` (pacote E keyvault-cloud + skill dual + install vault)
> - `policies-anti-destrutivas` (kernel agent-policies dual-runtime + install foundation)
> - `evidencias-testes-obrigatorios` (kernel evidence-gate collect/check + foundation)
> - `visao-grafica-fluxo-agentes` (kernel fluxo-events telemetria live SDD + `/fluxo-live` + aviso UX task 66)
> - `chore-tasks-por-slug` (layout `tasks/{slug}/` + ship da chore)
> - `fluxo-events-dev-loop-live` (`dev_loop_map` + slug `dev-loop-*` + wiring `/dev` + guardrail naming PT-BR + backfill 58–65)
> - `fluxo-grafo-visual-agentes` (fluxograma SVG canônico no `live.html`)
> - `fluxo-grafo-causal` (`event_id`/`run_id`/`parent_event_id` + stack + `build_causal_svg`)
> - `fluxo-live-exec-dual` (live Opção C: previsto esmaecido + trilha de execução real)
> - `fluxo-live-task-delegation` (tasks/subagentes no live + wiring `harness-build`; PR 216748)

---

## Termos do domínio

| Termo | Definição | Não é |
|---|---|---|
| **Camada Convenção** | Pacote Fase 1: contrato yaml, rule, cheatsheet, hooks locais, `/nova-branch`, adapter PR híbrido, wiring `GIT_PREFLIGHT`, propagação via install-harness | Portal UI, Edit policies, tag `prod-*` |
| **GIT_PREFLIGHT** | Soft-block nos agents/Dev Loop: fetch → tronco → sync `--ff-only` → working tree limpa → branch de trabalho | Gate server-side; bloqueio hard |
| **Soft-block** | O agente para e pede acordo humano; não executa a ação sozinho | Deny rule / hook que impede mecanicamente |
| **Contrato (`git-hygiene.yaml`)** | Fonte única de regex e tipos de branch/título PR | Documentação solta duplicada em prose |
| **Adapter SCM** | Detecta `azure` \| `github` \| `ambiguous` pelo remote; abre PR via CLI se autenticada ou payload para UI | Rule que crava Azure |
| **§1.3 — limites reais** | Declaração: sem Edit policies / branch protection, nenhum gate impede de fato; `--no-verify` e clone sem hooks contornam; **agent-policies** (deny/hooks) também é freio local — bypass `HARNESS_ALLOW_DESTRUCTIVE=1` existe | Promessa de bloqueio server-side |
| **Agent-policies** | Contrato `agent-policies.yaml` + engine `config/agent_policies/` (match/generate/guard) + hooks Claude/Cursor | Soft policy só; DE-A002 (código versionado) |
| **Deny-hard / ask** | Severidades do catálogo: irreversível bloqueia; git force / deletes Databricks pedem confirmação | Allow silencioso |
| **Seed policies** | `.harness/policies/project_profile.yaml` (`families[]` extras); `seed: true` KEEP | Marker DE data-check |
| **Dogfood** | Canônico usa os próprios artefatos (ex.: `core.hooksPath=.githooks`) antes de propagar | Só documentação sem bootstrap |
| **Norma DE (`data-engineering.yaml`)** | Fonte normativa de IDs e severidade (Universal + `spark-yarn-airflow` + perfis `databricks-*` + pacotes D/E) | Rule/prose que redefine IDs |
| **canonical-data-check** | CLI de enforcement: `validate` / `baseline` / `compare` / `report` / `explain` (+ job RO); registry despacha pacotes A–E | Segunda norma em KB |
| **Pacotes A/B/C/D/E** | A Universal + B perfil yarn = blockers; C Airflow = condicional; D `databricks-cloud` = checks FS SDP/DLT/DAB/UC; E `keyvault-cloud` = wiring vault FS | Severidade inventada em agent |
| **Perfis Databricks** | `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` (união SDP+DLT) — sempre A+D | Runtime Databricks / SDK live |
| **Auto-detect DE** | Sinais DAB/SDP/DLT no filesystem (`de_marker`); override via `project_profile.yaml` vence | Credencial ou API Unity Catalog |
| **Baseline ratchet** | Compare falha só em finding **novo**; dívida conhecida no baseline não quebra | Full enforce sem baseline em brownfield remoto |
| **`profiles[]`** | Campo opcional no baseline cloud/multi (além de `profile` singular legado Loop 1) | Breaking bump obrigatório do schema seed yarn |
| **Marker DE** | `.harness/data-check/project_profile.yaml` — presença faz `/validar` invocar data-check; pode declarar `secret_store` | Keyword solta no repo |
| **`/validar` DE** | Data-check se marker **ou** sinal útil SDP/DLT **ou** vault; DAB isolado **sem** vault **não** ativa sem marker | Hook Stop com data-check obrigatório |
| **Pacote E (`keyvault-cloud`)** | Checks FS `DE-E001`–`E003`: facade, map só IDs/URIs, consumidores sem SDK vault; ortogonal ao perfil A–D | Live API OCI/Azure Vault no CI |
| **`secret_store`** | Campo do marker: `oci` \| `azure` \| `multi` — override sobre auto-detect; `multi` = união | Enum de outros cofres (AWS/HashiCorp) |
| **Skill `cloud-secrets`** | Playbook dual OCI/Azure (wiring, auth, SI); sem agent vault no canônico | Agent `key-oci-expert` product-bound |
| **Install `cloud_secrets`** | Categoria condicional no `stack_map` (flag vault / `secret_store`) — propaga skill+KBs; **não** always / **não** acoplada a `pipeline_dados` | Examples keyvault no install |
| **Examples keyvault** | `examples/keyvault-oci-min/` e `examples/keyvault-azure-min/` + scaffold `config/templates/cloud-secrets/` — fora do `stack_map` | Credenciais/OCIDs reais |
| **Seed-once** | Artefato `seed: true` no stack_map: 1º COPY; re-install = KEEP (preserva baseline/waivers) | AUTO_UPDATE de runtime do filho |
| **Pacote `pipeline_dados` (Loop 3)** | Norma + rule/KB pipeline + seed + **10 agents** + **7 commands** + skill `de-conformidade` + KBs DE (incl. `databricks`) | Pacote mínimo Loop 1/2 (só norma/rule/seed) |
| **Skill `de-conformidade`** | Playbook findings CLI → remediação / baseline / waiver (owner+expiry); sem live API | Check executável novo |
| **KB `databricks`** | Domínio JIT alinhado a DE-D001–005 (DAB, SDP, DLT, schema rescue, UC FS) | Segunda fonte de severidade |
| **Amarras agentic DE** | Agents/commands DE citam IDs/`/validar` e política corrigir vs baseline/waiver | Agents desacoplados do kernel |
| **Examples Databricks** | `examples/databricks-sdp-min/` e `examples/databricks-dlt-min/` — greenfield estático A+D, fora do `stack_map` | Piloto em cluster real |
| **Evidence-gate** | Contrato `evidence-gate.yaml` + engine `collect\|check` + manifesto/logs/`audit.jsonl` + `evidencias_ref` | Soft review; `/validar` suite global; agent-policies Bash |
| **Manifesto de evidências** | `evidencias/tasks/<id>.yaml` — critério → testes/comando/exit/log (LWW) | Claim em prosa na task |
| **`evidencias_ref`** | Campo obrigatório em `metrics/entregas.jsonl` apontando o manifesto | Path opcional / scorecard sem prova |
| **fluxo-events** | Kernel de telemetria live SDD + Dev Loop (`fluxo-events.yaml` + `config/fluxo_events/` + CLI emit/render/truncate + `slug_from_prompt_path` + `stack`); `sdd_map` 0–4 / `dev_loop_map` 0–6; IDs aditivos; live Opção C; orthografia PT-BR **fluxo** (x) | Evidence-gate; agent-policies; SSE; “flujo” (ES) |
| **Opção C (live)** | Layout `build_html`: mapa previsto esmaecido + trilha temporal de agentes + resumo + timeline humana (sem `event_type` cru) | Grafo causal como painel principal; SSE |
| **Trilha de execução** | `build_execution_trail_svg`: `agent_enter` colapsados + setas; pills `task NN` e `→ subagente` sob o agente pai (`parent_event_id`) | UUID visível; grafo causal no HTML |
| **Delegação (emit)** | `task_enter`/`task_exit` + `task_id`; subagente = `agent_enter`/`exit` filho; wiring documentado em `harness-build.md` — **sem emit não aparece** | Hook automático Cursor Task; backfill obrigatório |
| **`--print-event-id`** | Flag CLI: stdout só o UUID do `event_id` (`BUILD_ENTER_EVENT_ID=$(…)`); `--json` alternativa | Default legado `ok: appended …` quebrado |
| **`build_causal_svg`** | Função pura no engine + testes (`test_render_causal.py`); árvore `phase_enter` + `agent_enter` + `task_enter` — **não** renderizada no `live.html` atual | Painel live principal desde Opção C |
| **`dev_loop_map`** | Mapa fases 0–6 (LOAD→…→SYNC) com agents `prompt-crafter` / `dev-loop-executor`; escolhido no render quando slug começa com `dev-loop-` | Fork do kernel; event_types novos |
| **Slug `dev-loop-{nome}`** | Path sintético sob `projetos/` derivado do stem `PROMPT_*.md` via `slug_from_prompt_path` | Slug SDD do `/novo-projeto`; flat em `.claude/dev/` |
| **IDs causais** | `event_id` / `run_id` / `parent_event_id` (UUID v4); emit gera se omitido; load legado sem campos ok | Backfill de logs históricos; PII |
| **`stack.json`** | Pilha local fail-soft em `projetos/{slug}/fluxo/stack.json` (gitignore); parent explícito > topo | Mutex; versionar no git; stack cross-machine |
| **`live.html`** | Painel Opção C: previsto esmaecido + execução real + resumo + timeline (`config/fluxo_events/render.py` `build_html`) | Substitui STATUS/scorecard/DoD; grafo causal no HTML |
| **ship_truncate** | Evento + ação de ship (ou `EXIT_COMPLETE` Dev): keep-tail N=100 no `events.jsonl` + re-render | Delete destrutivo do trail |
| **`/fluxo-live`** | Command para abrir/servir o HTML live do slug | Agent “fluxo officer” |
| **Tasks por slug** | Issues locais em `tasks/{slug}/NN-*.md` (mesmo slug do projeto); numeração global `NN` | Flat `tasks/NN-*.md` na raiz; Dev Loop `.claude/dev/` |
| **Aviso UX painel live** | No enter SDD (`harness-brainstorm` / `harness-build`) e Dev Loop (`prompt-crafter` / `dev-loop-executor` / `/dev`), agente avisa 1× path `live.html` + http.server opcional + `/fluxo-live` | Emit silencioso; dry-run Dev (zero emit) |

## Acrônimos e siglas

| Sigla | Significado |
|---|---|
| SCM | Source Control Management (Azure Repos / GitHub) |
| PR | Pull Request (Azure) / Pull Request (GitHub) — mesmo fluxo híbrido |
| DoD | Definição de Pronto (`rules/definicao-de-pronto`) |
| SI | Segurança da Informação |
| DE | Engenharia de Dados |
| RO | Somente leitura (ex.: relatório sql-capacity sem escrita no alvo) |
| SDP | Spark Declarative Pipelines (sinal/perfil medallion no canônico) |
| DLT | Delta Live Tables (sinal/perfil legacy + quarentena) |
| DAB | Databricks Asset Bundle (`databricks.yml` / `bundle*.yml`) |
| UC | Unity Catalog — grants/linhagem **em filesystem** no pacote D (sem API live) |
| KV | Key Vault (OCI Vault / Azure Key Vault) — wiring no pacote E |

## Regras de negócio implícitas

- Trabalho no tronco (`master`/`main`) só com **acordo explícito** do usuário (exceção registrada).
- Tag `prod-*` está **fora do MVP** (Fase 2).
- PAT/tokens **somente** via env / secret manager — nunca no diff, logs ou query string.
- Critérios de aceite da Fase 1 **não** afirmam bloqueio server-side (§1.3).
- Loops 1–3 shipados; pacote E (keyvault dual) implementado (ADR 002) — commit/ship do projeto conforme STATUS.
- Checks cloud/vault só filesystem (sem API live UC/Databricks/Vault).
- `data-sql-capacity-evolution-prd` neste ship: **somente leitura** (relatório no canônico); lift de padrões vault sem product keys.
- Telemetria `fluxo-events` é **fail-soft** e complementar — não substitui DoD, evidence-gate, `/validar` nem scorecard.
- Live Opção C + delegação task/subagente shipados (`master` @ PR 216748); ADR 005 addendum Opção C **pendente** (cheatsheet descreve layout atual).
