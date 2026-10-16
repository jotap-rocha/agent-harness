# Agent Harness Canônico — guia do agente

<!-- Derivado de CLAUDE.md por .claude/skills/sync-context/scripts/sync_agents_from_claude.py — edite o CLAUDE.md, ou use blocos agents-only. -->

> Este repositório é o **framework** do Agent Harness Method.
> Não é um produto — é a fonte de verdade de agents, skills, KBs e rules
> que são propagados via `/install-harness` para projetos alvo.
>
> O template de `CLAUDE.md` para projetos-filhos está em:
> `.cursor/skills/harness-architect/references/claude-dir-templates.md`

## O que é este repositório

- **Fonte canônica:** este repositório (raiz do workspace atual). O path absoluto muda por
  máquina/clone — **não** há “canônico fixo” em disco. Para `/install-harness` em outro
  projeto, use a raiz deste clone, `--canonical <path>` ou `HARNESS_CANONICAL` (o launcher
  `./install-harness` e o script Python defaultam para a raiz do próprio clone).
- **Dois modos de uso:**
  1. Clonar como template de novo projeto → rodar `/harness-architect` no projeto clonado
  2. Apontar como fonte no `/install-harness` de outro projeto existente

## Comandos

```bash
# Instalar/atualizar harness em projeto alvo:
/install-harness    # informa path de destino no primeiro passo

# Evoluir o canônico:
agent-creator       # criar novo agente
/write-a-skill      # criar nova skill
/find-skills        # descobrir skill no catálogo aberto (skills.sh)
kb-architect        # criar ou atualizar KB de domínio
revisor-codigo      # revisar diff antes de "commitar" evolução

# Git hygiene (Camada Convenção — Fase 1):
/nova-branch        # fetch → sync --ff-only → acordo → cria tipo/escopo
/git-ajuda          # cheatsheet + contrato (git-hygiene.yaml)

# Engenharia de dados (Loops 1–3 + Key Vault):
python -m config.canonical_data_check validate <path>   # A+B ou A+D conforme perfil; C Airflow opcional; E se vault
python -m config.canonical_data_check baseline|compare|report|explain  # baseline cloud grava profiles[]
/validar            # ruff+mypy+pytest; data-check se marker DE **ou** auto-detect SDP/DLT **ou** vault (DAB isolado sem vault não)
# Skills: de-conformidade (findings) · cloud-secrets (wiring OCI/Azure)

# Agent-policies (freio anti-destrutivo dual-runtime):
python -m config.agent_policies check|generate

# Evidence-gate (prova mecânica de aceite por task):
python -m config.evidence_gate collect|check

# fluxo-events (telemetria live SDD — fail-soft):
python -m config.fluxo_events check|emit|render|truncate
/fluxo-live           # abrir/servir live.html do slug
```

## Invariantes (nunca quebrar ao evoluir o canônico)

- **Nenhum código de produto aqui** — só artefatos de framework (agents, skills, KBs, rules)
- **Agents e skills devem ser genéricos** — reutilizáveis em qualquer projeto, sem acoplamento
- **`/install-harness` é o único mecanismo de propagação** — nunca copiar manualmente para projetos
- **Ao renomear pasta:** atualizar `install-harness/SKILL.md` + guias HTML relevantes em `docs/guia/`
- **Contratos YAML ficam na raiz** (`*.yaml`): os loaders em `config/` e os projetos filhos os
  localizam ali — não mover ao "arrumar" a raiz. `docs/rascunhos/` é interno e **não** é
  propagado (exclusão em `install_harness.py`); guias instalados nos filhos vão para `docs/manuais/`
- **Ao evoluir um KB:** verificar se o KB está referenciado na tabela stack-layer de `install-harness/SKILL.md`
- **Agents e skills devem ter `description:` claro** — é o único texto que o agente vê para decidir quando usar
- **Toda edição em `.claude/{agents,skills,rules,kb,commands,guias}` deve ser espelhada em `.cursor/`**
  na mesma sessão (mesma estrutura; `rules/*.md` vira `rules/*.mdc`) — nunca deixar os dois divergirem
- **Git hygiene:** fonte de regex em `git-hygiene.yaml`; rule agnóstica de SCM; adapter em
  `config/git_hygiene/scm.py`; tag `prod-*` fora do MVP (Fase 2); §1.3 — sem Edit policies nenhum
  gate impede de fato
- **Kernel DE (Loop 1):** norma em `data-engineering.yaml`; enforcement via
  `config/canonical_data_check`; seed `.harness/data-check` com `seed: true` (re-install = KEEP);
  sql-capacity neste ship = somente leitura
- **Kernel DE (Loop 2):** perfis `databricks-sdp-medallion` / `databricks-dlt-legacy` /
  `databricks-multi` + pacote **D** `databricks-cloud` (checks FS, sem API live); auto-detect
  DAB/SDP/DLT com override via marker; `/validar` dispara data-check em marker **ou**
  SDP/DLT **ou** vault (`secret_store` / auto-detect; pacote E — ver invariante Key Vault);
  baseline persiste `profiles[]` em cloud/multi; examples `databricks-sdp-min` e
  `databricks-dlt-min` fora do install
- **Catálogo DE (Loop 3):** 10 agents + 7 commands amarrados a `DE-*` / `/validar`; skill
  `de-conformidade`; KB `databricks` (DE-D001–005); install `pipeline_dados` propaga agents,
  commands, skill e KBs DE (seed data-check permanece KEEP)
- **Key Vault (pacote E):** `keyvault-cloud` (`DE-E001`–`E003`) ortogonal ao perfil; marker
  `secret_store: oci|azure|multi` **ou** auto-detect; skill `cloud-secrets` + KBs
  `oci-vault` / `azure-keyvault`; install categoria `cloud_secrets` (não always / não
  acoplada a `pipeline_dados`); examples `keyvault-*-min` + scaffold
  `config/templates/cloud-secrets/` fora do `stack_map`; sem agent vault; sem live API
- **Agent-policies (runtime anti-destrutivo):** `agent-policies.yaml` + `config/agent_policies/`
  (load/match/generate/guard); híbrido deny-hard/ask; bypass `HARNESS_ALLOW_DESTRUCTIVE=1`;
  fail closed deny / fail open ask; Claude PreToolUse + Cursor `beforeShellExecution`;
  install foundation always-on (deny ≠ `[]`) + seed `.harness/policies` KEEP; `DE-A002`
  ortogonal; §1.3 honesty (sem Edit policies); sem agent policy officer
- **Evidence-gate (prova de aceite por task):** `evidence-gate.yaml` + `config/evidence_gate/`
  (`collect|check`); manifesto/`logs`/`audit.jsonl`; cap 2 MiB fail; LWW + audit append-only;
  `evidencias_ref` em entregas; install foundation + seed `.harness/evidence-gate/` KEEP;
  ortogonal a `/validar` e a `agent-policies` (Bash deny ≠ aceite); revisor soft ≠ gate hard;
  §1.3 honesty (manifesto forjável); sem Stop dual; sem agent “evidence officer”
- **fluxo-events (telemetria live SDD + Dev Loop):** `fluxo-events.yaml` +
  `config/fluxo_events/` (`emit|render|truncate` + `slug_from_prompt_path` + `stack`);
  `sdd_map` 0–4 e `dev_loop_map` 0–6; render bifarca por prefixo `dev-loop-*`; campos
  aditivos `event_id` / `run_id` / `parent_event_id` (UUID v4; opcionais no load legado);
  `live.html` layout **Opção C** (`build_html` em `render.py`): mapa previsto esmaecido
  (`build_flow_svg`) + trilha de execução real (`build_execution_trail_svg` — agentes,
  tasks `task_enter`/`task_exit` com `task_id`, subagentes via `parent_event_id`) + resumo
  + timeline humana; `build_causal_svg` permanece no engine (testes), **fora** do painel
  principal; wiring emit por task/delegação em `harness-build.md`; stack local
  `projetos/{slug}/fluxo/stack.json` (gitignore, fail-soft, sem mutex); paths
  `projetos/{slug}/fluxo/` (slug SDD ou `dev-loop-{nome}`); cap 2 MiB rotate keep-tail
  (warning soft); ship/EXIT_COMPLETE truncate N=100 + re-render; fail-soft (nunca bloqueia
  SDD/`/dev`); dry-run Dev **sem** emit; install foundation + seed `.harness/fluxo-events/`
  KEEP; command `/fluxo-live`; ortogonal a `/validar`, evidence-gate e agent-policies;
  §1.3 honesty (telemetria local/forjável); sem agent “fluxo officer”; orthografia PT-BR
  **fluxo** (com **x**); aviso UX 1× no enter: SDD (`harness-brainstorm` / `harness-build`)
  e Dev Loop (`prompt-crafter` / `dev-loop-executor` / `/dev`) — path `live.html` /
  `/fluxo-live`; guardrail pytest naming no pacote (`tests/fluxo_events/test_naming_ptbr.py`)
- **Cloud multi-provider (Azure/AWS/GCP):** agentes `agents/cloud/` (`cloud-data-engineer`,
  `iac-engineer`) **nunca** citam provider/serviço (skills de terceiros do skills.sh em
  `cloud_core` podem trazer exemplos de várias nuvens) — especialização só
  via KB `{provider}-{serviço}` com `provider:`/`role:` no `_index.yaml` (roles `iac-provider`,
  `warehouse`, `streaming`, `object-storage`, `stream-processing`); Passo 0 e contrato em
  `kb/cloud-resolution/`; núcleo IaC agnóstico em `kb/terraform/`; provider novo = KBs +
  categoria `cloud_<provider>`, zero mudança em agente; install `cloud_core` +
  `cloud_{azure,aws,gcp}` via `detect_clouds` (`cloud:` no CLAUDE.md › `*.tf` › deps);
  skills novas **sempre do skills.sh** (`npx skills add`, `skills-lock.json`) — lacuna sem
  skill madura vira `patterns/` de KB, não skill escrita à mão; guardrail
  `tests/install_harness/test_cloud_catalog.py` (agnosticidade + matriz role×provider)
- **Tasks por slug:** issues locais em `tasks/{slug}/NN-*.md` (mesmo `{slug}` de
  `.cursor/projetos/{slug}/`) — **não** flat na raiz de `tasks/`; numeração global `NN`

## Onde fica o quê

| O que | Onde | Qtd |
|---|---|---|
| Agents | `.cursor/agents/` | 35 (5 categorias: `workflow/`, `architect/`, `dev/`, `data-engineering/`, `cloud/`) |
| Skills | `.cursor/skills/` | 33 (9 vindas do skills.sh — ver `skills-lock.json`) |
| Rules | `.cursor/rules/` | 12 |
| KBs | `.cursor/kb/` | 38 domínios |
| Commands | `.cursor/commands/` | 24 (10 na raiz + `data-engineering/` + `visual-explainer/` + `/evidencias` + `/fluxo-live`) |
| Tasks (to-tasks) | `tasks/{slug}/NN-*.md` | alinhado a `.cursor/projetos/{slug}/` — não flat na raiz |
| Dev Loop | `.cursor/dev/` | progress/logs/templates (conceitual `DEV-LOOP.md`) — **≠** `tasks/{slug}/` do SDD |
| Design docs | `.cursor/design/` | features/, archive/, reports/ |
| Projetos do harness | `.cursor/projetos/` | histórico de evoluções |
| Guias passo-a-passo | `.cursor/guias/` | tutoriais didáticos via `/novo-guia` — ver `docs/manuais/passo-a-passo.md` |
| Guias HTML | `docs/guia/` | 16 slides (01–16) |
| Manuais | `docs/manuais/` | `harness-guide`, `como-usar`, `install-harness-cli`, `passo-a-passo` |
| Cheatsheets | `docs/cheatsheets/` | 1 página por kernel + `scm-pr-hibrido` |
| Rascunhos | `docs/rascunhos/` | planos/pesquisas internas — não propagado aos filhos |
| Mapa de `config/` | `config/README.md` | pacote ↔ contrato ↔ CLI |
| Contrato Git hygiene | `git-hygiene.yaml` | fonte única de regex (branch + título PR) |
| Rule Git hygiene | `.cursor/rules/git-hygiene.mdc` | invariantes SCM-agnósticos (espelho `.mdc`) |
| Cheatsheet Git | `docs/cheatsheets/git-hygiene-cheatsheet.md` | 1 página + declaração §1.3 |
| Adapter SCM / PR híbrido | `config/git_hygiene/` · `docs/cheatsheets/scm-pr-hibrido.md` | azure \| github |
| Githooks locais | `.githooks/` | pre-commit (segredos), commit-msg, pre-push |
| Template PR Azure | `.azuredevops/pull_request_template.md` | checklist versionado |
| Testes Git hygiene | `tests/git_hygiene/` | contrato + fixtures + scm |
| Norma DE (Loops 1–2 + E) | `data-engineering.yaml` | Universal + `spark-yarn-airflow` + perfis `databricks-*` + pacotes D/E |
| Loader DE | `config/data_engineering/` | contrato tipado (padrão `git_hygiene`) |
| CLI DE | `config/canonical_data_check/` | validate / baseline / compare / report / explain (+ RO report); registry A–E |
| Detect / marker DE | `config/canonical_data_check/de_marker.py` | marker + auto-detect SDP/DLT/DAB + vault (`secret_store`); resolve perfil/cofre |
| Checks cloud (D) | `config/canonical_data_check/checks/package_d.py` | DAB, SDP, DLT+quarentena, schema rescue, UC FS |
| Checks vault (E) | `config/canonical_data_check/checks/package_e.py` | facade, map IDs/URIs, consumidores sem SDK |
| Seed data-check | `config/canonical_data_check/templates/data-check/` | → `.harness/data-check/` no filho (`seed: true`); SCHEMA com `profiles[]` + `secret_store` |
| Scaffold cloud-secrets | `config/templates/cloud-secrets/` | facade dual + maps placeholders |
| Examples DE | `examples/spark-yarn-airflow-min/` · `examples/databricks-sdp-min/` · `examples/databricks-dlt-min/` · `examples/keyvault-oci-min/` · `examples/keyvault-azure-min/` | greenfield A+B(+C), A+D e A+B+E; fora do `stack_map` |
| Testes DE | `tests/data_engineering/` | contrato, CLI, baseline `profiles[]`, detect, packages D/E, install vault, `/validar` |
| Contrato agent-policies | `agent-policies.yaml` | famílias / patterns / severity (deny\|ask) |
| Engine agent-policies | `config/agent_policies/` | load · match · generate · guard · CLI · hooks adapters |
| Seed policies | `config/agent_policies/templates/policies/` | → `.harness/policies/` (`seed: true` KEEP) |
| Cheatsheet policies | `docs/cheatsheets/agent-policies-cheatsheet.md` | 1 página + §1.3 + cross-link DE-A002 |
| Hooks dual | `.claude/hooks/` · `.cursor/hooks.json` + `.cursor/hooks/` | PreToolUse + beforeShellExecution |
| Contrato evidence-gate | `evidence-gate.yaml` | schema manifesto · cap 2 MiB · fator 2× · check rules |
| Engine evidence-gate | `config/evidence_gate/` | load · collect · check · close · audit · CLI |
| Seed evidence-gate | `config/evidence_gate/templates/evidencias/` | → `.harness/evidence-gate/` (`seed: true` KEEP) |
| Cheatsheet evidence-gate | `docs/cheatsheets/evidence-gate-cheatsheet.md` | 1 página + §1.3 + cross-link policies/`/validar` |
| Testes evidence-gate | `tests/evidence_gate/` | contrato · collect · check · audit · wiring · install |
| Contrato fluxo-events | `fluxo-events.yaml` | schema eventos · cap 2 MiB · rotate keep-tail · `sdd_map` 0–4 · `dev_loop_map` 0–6 · IDs causais aditivos |
| Engine fluxo-events | `config/fluxo_events/` | load · emit · stack · render Opção C + dual-map · slug_from_prompt · rotate · truncate · CLI (`build_causal_svg` testável) |
| Seed fluxo-events | `config/fluxo_events/templates/fluxo/` | → `.harness/fluxo-events/` (`seed: true` KEEP) |
| Cheatsheet fluxo-events | `docs/cheatsheets/fluxo-events-cheatsheet.md` | 1 página + Opção C + delegação task/subagente + Dev Loop + naming PT-BR + §1.3 |
| Command `/fluxo-live` | `.cursor/commands/fluxo-live.md` | abrir/servir `live.html` do slug |
| Testes fluxo-events | `tests/fluxo_events/` | contrato · emit · stack · exec trail · delegação · causal SVG · dual-map · Dev Loop · naming · wiring · install · dogfood |
| Agents de nuvem | `.cursor/agents/cloud/` | `cloud-data-engineer`, `iac-engineer` — agnósticos |
| Contrato multi-cloud | `.cursor/kb/cloud-resolution/` | Passo 0 · roles · contrato de KB de serviço |
| KBs de serviço de nuvem | `.cursor/kb/{azure,aws,gcp}-*` | 5 roles × 3 providers |
| Testes multi-cloud | `tests/install_harness/test_cloud_catalog.py` | agnosticidade · matriz · detecção · espelho |
| Template CLAUDE.md | `.cursor/skills/harness-architect/references/claude-dir-templates.md` | — |
| Schema do manifest | `.cursor/skills/install-harness/references/install-manifest-schema.md` | — |
| Guia de uso do harness | `docs/manuais/harness-guide.md` | — |
| Setup de template (clone) | `docs/manuais/como-usar.md` | — |
| Guia da CLI de install (standalone) | `docs/manuais/install-harness-cli.md` | — |
| Conceito Dev Loop (execução ágil de tarefa pontual) | `DEV-LOOP.md` | — |

<!-- agents-only:start -->
## Como usar no Cursor

Todos os artefatos estão espelhados em `.cursor/` para acesso via `@`-mention:

```
@.cursor/agents/workflow/harness-brainstorm.md      → entrevista inicial de projeto
@.cursor/agents/workflow/harness-build.md           → implementar tasks com gates
@.cursor/skills/install-harness/SKILL.md   → processo de install em outro projeto
@.cursor/skills/harness-architect/SKILL.md → montar .claude/ de um projeto
@.cursor/skills/grill-me/SKILL.md          → aprofundar requisitos
@.cursor/skills/excalidraw-diagram/SKILL.md → gerar diagramas Excalidraw com argumentação visual
@.cursor/skills/find-skills/SKILL.md        → descobrir skills no catálogo aberto (skills.sh)
@.cursor/kb/fastapi/                        → KB de FastAPI
@.cursor/kb/langgraph/                      → KB de LangGraph
@.cursor/kb/rag/                            → KB de RAG e busca semântica
@.cursor/rules/                             → todas as rules como contexto adicional
```

## Referência rápida de agents e skills

Ver `docs/manuais/harness-guide.md` para a lista completa com descrição de cada agent e skill.
<!-- agents-only:end -->
