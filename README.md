# Agent Harness Canônico

> Framework do Agent Harness Method — fonte de verdade de agents, skills, KBs, rules e
> kernels de qualidade propagados via `/install-harness` para projetos alvo. Não é um produto
> de aplicação; é o ambiente que governa como Claude Code e Cursor agem no seu projeto.

## Por onde começar

| Quero… | Vá para |
|---|---|
| Usar como template de projeto novo | [docs/manuais/como-usar.md](docs/manuais/como-usar.md) |
| Entender o método e os fluxos | [docs/manuais/harness-guide.md](docs/manuais/harness-guide.md) |
| Instalar o harness num projeto existente | [docs/manuais/install-harness-cli.md](docs/manuais/install-harness-cli.md) |
| Aprender fazendo (tutorial didático) | [docs/manuais/passo-a-passo.md](docs/manuais/passo-a-passo.md) |
| Consultar um kernel em 1 página | `docs/cheatsheets/` |
| Ver decisões de arquitetura | `docs/adr/` |

**Mapa da raiz:** `*.yaml` = contratos dos kernels (lidos pelos loaders em `config/`; ficam na
raiz porque os projetos filhos os procuram ali) · `config/` = engines Python (ver
[config/README.md](config/README.md)) · `docs/` = toda a documentação · `.claude/` e `.cursor/` =
artefatos do harness (espelhados) · `tests/` = testes dos kernels.

## O que é

Este repositório é o **framework** do Agent Harness Method. É a fonte canônica de agents,
skills, KBs e rules instalados em projetos filhos. O path absoluto do clone muda por
máquina — use a raiz deste clone, `--canonical <path>` ou `HARNESS_CANONICAL` no
`./install-harness`.

**Dois modos de uso:**

1. **Clonar como template** de projeto novo → rodar `/harness-architect` (ou `/novo-projeto`)
   para especializar o `.claude/` ao domínio.
2. **Apontar como fonte** no `/install-harness` de um projeto existente → o instalador detecta
   a stack e traz só os artefatos relevantes.

Espelho Cursor: `.cursor/` replica `.claude/` (rules como `.mdc`).

## Os 3 níveis de uso

| Nível | O quê | Comando | Tempo |
|---|---|---|---|
| 1 — Vibe coding | Prompt solto, sem estrutura | (nenhum) | < 30 min |
| 2 — Dev Loop | `PROMPT_*.md` dirigido, exit criteria, recovery | `/dev` | 1–4 h |
| 3 — Harness completo | SDD 0–4, PRD, gate + revisor, ship | `/novo-projeto` | multi-dia |

Detalhe do Dev Loop: [DEV-LOOP.md](DEV-LOOP.md).

## Pré-requisitos

- [Claude Code CLI](https://claude.ai/code) ou Cursor (artefatos em `.cursor/`)
- `git` no PATH
- `python3` 3.10+ — instalador (`install_harness.py`) usa só standard library
- `uv` — gate `/validar` e projetos Python de destino (`ruff`, `mypy`, `pytest`)
- `gh` (opcional) — `/to-issues` com GitHub; adapter SCM também suporta Azure DevOps
- `npx` + Node 20+ — MCP Context-7 (ver comentário em `.mcp.json`)

## Início rápido

### Modo 1 — clonar como template

```bash
git clone <este-repo> meu-projeto
cd meu-projeto
cp .env.example .env   # preencher; nunca commitar .env

/novo-projeto          # na sessão Claude Code / Cursor
```

Passo a passo: [docs/manuais/como-usar.md](docs/manuais/como-usar.md).

### Modo 2 — instalar/atualizar num projeto existente

```bash
./install-harness
# ou, na pasta do projeto alvo:
/install-harness
```

CLI completa (flags, `--json`, automação): [docs/manuais/install-harness-cli.md](docs/manuais/install-harness-cli.md).

## Fluxo SDD (nível 3)

```
/novo-projeto       → ideia + SI assessment (harness-brainstorm)
/grill-me           → entrevista da ideia
harness-define      → requisitos + specs implícitas
/to-prd             → PRD.md
harness-design      → /harness-architect
/to-tasks           → tasks/{slug}/NN-*.md
harness-build       → implementação task a task (/validar + revisor-codigo)
harness-ship        → scorecard + retrospectiva
```

Referência pós-install: [docs/manuais/harness-guide.md](docs/manuais/harness-guide.md).

## Kernels e gates (canônico)

Contratos YAML na raiz + engines em `config/`. Ortogonais entre si (aceite ≠ telemetria ≠ Bash deny).

| Kernel | Contrato | CLI / comando | Cheatsheet |
|---|---|---|---|
| Validação | — | `/validar` (ruff + mypy + pytest; data-check condicional) | `.claude/commands/validar.md` |
| Eng. dados | `data-engineering.yaml` | `python -m config.canonical_data_check validate …` | skill `de-conformidade` |
| Agent-policies | `agent-policies.yaml` | `python -m config.agent_policies check\|generate` | [docs/cheatsheets/agent-policies-cheatsheet.md](docs/cheatsheets/agent-policies-cheatsheet.md) |
| Evidence-gate | `evidence-gate.yaml` | `python -m config.evidence_gate collect\|check` | [docs/cheatsheets/evidence-gate-cheatsheet.md](docs/cheatsheets/evidence-gate-cheatsheet.md) |
| fluxo-events | `fluxo-events.yaml` | `python -m config.fluxo_events …` · `/fluxo-live` | [docs/cheatsheets/fluxo-events-cheatsheet.md](docs/cheatsheets/fluxo-events-cheatsheet.md) |
| Git hygiene | `git-hygiene.yaml` | `/nova-branch` · `/git-ajuda` | [docs/cheatsheets/git-hygiene-cheatsheet.md](docs/cheatsheets/git-hygiene-cheatsheet.md) |

Telemetria live (`live.html`, layout Opção C): mapa previsto esmaecido + trilha de execução
real (agentes, tasks `task_enter`/`task_exit`, subagentes delegados via `parent_event_id`) +
resumo + timeline. Fail-soft — omitir emit não quebra DoD.

## Comandos (evoluir o canônico)

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

## Desenvolvimento (neste repositório)

```bash
# Gate completo (mesmo contrato do /validar)
uv run ruff check --fix . && uv run mypy . && uv run pytest -q

# Pacotes de teste por kernel
uv run pytest tests/fluxo_events/ -q
uv run pytest tests/evidence_gate/ -q
uv run pytest tests/data_engineering/ -q
uv run pytest tests/git_hygiene/ -q
```

`requirements.txt` na raiz é marcador — o install-harness não exige `pip install`.
Dependências de dev (`ruff`, `mypy`, `pytest`) vêm do ambiente `uv` do clone.

## O que vem no canônico

| O que | Onde | Qtd |
|---|---|---|
| Agents | `.claude/agents/` | 33 — `workflow/`, `architect/`, `dev/`, `data-engineering/` |
| Skills | `.claude/skills/` | 24 |
| Rules | `.claude/rules/` | 13 |
| KBs | `.claude/kb/` | 21 domínios |
| Commands | `.claude/commands/` | 24 (raiz + `data-engineering/` + `visual-explainer/` + `/evidencias` + `/fluxo-live`) |
| Tasks SDD | `tasks/{slug}/NN-*.md` | alinhado a `.claude/projetos/{slug}/` |
| Dev Loop | `.claude/dev/` | progress/logs/templates — ver `DEV-LOOP.md` |
| Examples DE | `examples/` | spark-yarn, databricks-sdp/dlt, keyvault oci/azure |

Catálogo: [`.claude/agents/README.md`](.claude/agents/README.md) ·
[`.claude/commands/README.md`](.claude/commands/README.md).

## SI / Segurança

- **Agent-policies** — deny-hard / ask em Bash (Claude PreToolUse + Cursor `beforeShellExecution`);
  bypass consciente `HARNESS_ALLOW_DESTRUCTIVE=1`; ver [docs/cheatsheets/agent-policies-cheatsheet.md](docs/cheatsheets/agent-policies-cheatsheet.md)
- **Rules** — `seguranca.md` (LGPD, PII, produção somente-leitura por padrão, sem secrets
  hardcoded) e `definicao-de-pronto.md` (aceite testável, gate verde, revisor, `metrics/entregas.jsonl`)
- **Githooks** — `.githooks/pre-commit` (heurística de segredos), commit-msg, pre-push
- **Hooks Claude** — `PostToolUse` (ruff format/fix), `Stop` (ruff + mypy + pytest), agent-policies

## Variáveis de ambiente

Copie `.env.example` → `.env` (gitignored). Grupos declarados no example:

| Grupo | Exemplos |
|---|---|
| Ambiente | `ENVIRONMENT`, `PIPELINE_ENV` |
| Banco | `DATABASE_URL`, `DATABASE_URL_READONLY` |
| LLM | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_*` (adversarial-judge) |
| Observabilidade | `LANGFUSE_*` |
| Databricks / Airflow / storage | `DATABRICKS_*`, `AIRFLOW__*`, `MINIO_*` |

## MCP

Configurado em `.mcp.json`:

- **Context-7** — docs oficiais de bibliotecas em runtime
- **Postgres** — placeholder `[POSTGRES_CONNECTION_STRING]`, `access-mode=restricted`

## Estrutura do repositório

```
.
├── CLAUDE.md · AGENTS.md · CONTEXT.md
├── docs/manuais/harness-guide.md · docs/manuais/como-usar.md · docs/manuais/install-harness-cli.md · DEV-LOOP.md
├── install-harness
├── agent-policies.yaml · evidence-gate.yaml · fluxo-events.yaml
├── data-engineering.yaml · git-hygiene.yaml
├── config/                    # engines: fluxo_events, evidence_gate, agent_policies,
│                              # canonical_data_check, git_hygiene, data_engineering
├── docs/
│   ├── adr/                   # ADRs 001–005
│   ├── guia/                  # 16 guias HTML
│   └── *-cheatsheet.md
├── examples/                  # perfis DE mínimos (fora do install stack_map)
├── metrics/entregas.jsonl     # delivery records → /scorecard
├── tasks/{slug}/              # issues locais do SDD
├── tests/                     # pytest por kernel + install
└── .claude/                   # agents, skills, rules, kb, commands, dev, design, projetos
    └── (espelho .cursor/)
```

## Decisões arquiteturais

| # | Título | Link |
|---|---|---|
| 001 | Sincronia de contexto no fechamento do fluxo | [docs/adr/001-sincronia-de-contexto-no-fechamento.md](docs/adr/001-sincronia-de-contexto-no-fechamento.md) |
| 002 | Pacote E keyvault-cloud + install vault | [docs/adr/002-pacote-e-keyvault-cloud-dual-install.md](docs/adr/002-pacote-e-keyvault-cloud-dual-install.md) |
| 003 | Kernel agent-policies dual-runtime | [docs/adr/003-kernel-agent-policies-dual-runtime.md](docs/adr/003-kernel-agent-policies-dual-runtime.md) |
| 004 | Kernel evidence-gate | [docs/adr/004-kernel-evidence-gate.md](docs/adr/004-kernel-evidence-gate.md) |
| 005 | Kernel fluxo-events (telemetria live SDD) | [docs/adr/005-kernel-fluxo-events.md](docs/adr/005-kernel-fluxo-events.md) |

Índice: [docs/adr/README.md](docs/adr/README.md).

## Guias HTML

Abra `docs/guia/` (16 slides):

| Arquivo | Tema |
|---|---|
| `01-conceitos.html` | Vocabulário: skills, agents, KBs, gates |
| `02-fluxo.html` | Fluxo completo de fases |
| `03-harness.html` | Anatomia do `.claude/` |
| `04-tracking.html` | STATUS, HANDOFF, métricas |
| `05-fluxo-guiado.html` | `/novo-projeto` passo a passo |
| `06-seguranca.html` | SI/LGPD/PII |
| `07-pipeline-arquitetura.html` | Medallion, lineage, contratos |
| `08-pipeline-praticas.html` | SOLID, Databricks, Airflow |
| `09-agentes-sdd.html` | Agents harness-* |
| `10-rag-search.html` | RAG e busca |
| `10-workshop-harness-vs-sdd.html` | Workshop harness vs SDD |
| `11-langgraph.html` | LangGraph |
| `12-supabase.html` | Supabase |
| `13-observabilidade.html` | Observabilidade |
| `14-multi-tenant.html` | Multi-tenant |
| `15-testing.html` | Testing |
| `16-install-harness.html` | `/install-harness` |

## Personalização

- Clone template: [docs/manuais/como-usar.md](docs/manuais/como-usar.md)
- Install em projeto existente: [docs/manuais/install-harness-cli.md](docs/manuais/install-harness-cli.md)
- Uso do harness instalado: [docs/manuais/harness-guide.md](docs/manuais/harness-guide.md)
