# Mapeamento do canônico — evidências vs claims

Foco: o que já enforça testes/evidências no ciclo harness vs o que ainda é prosa.
Gerado pelo codebase-explorer no brainstorm (2026-08-13).

## Executive Summary

- **Já enforça de verdade (mecânico):** suite `pytest` / `ruff` / `mypy` quando alguém **roda** `/validar` (comando + helper DE). No Claude, hook `Stop` em `.claude/settings.json` só dispara gate se existir `backend/` ou `src/` — neste canônico (só `tests/` + `config/`) o Stop **não** valida. Cursor **não** tem Stop equivalente (só `beforeShellExecution` anti-destrutivo).
- **Já exige em prosa (sem prova automática):** DoD, test-first no `harness-build`, “tested by” nas tasks (`to-tasks`), cobertura no `revisor-codigo`, append de `metrics/entregas.jsonl`, checklist `STATUS.md`, sync no `harness-ship`.
- **Delivery record existe** (`metrics/entregas.jsonl` + schema + `/scorecard`), mas campos `criterios_aceite.*`, `gate`, `revisor` são **auto-relato do agente** — sem validador de schema nem cruzamento com testes/git.
- **Não existe** pasta `evidencias/`, manifesto de prova, nem artefato que ligue critério → path de teste → log de execução.
- **agent-policies / hooks Cursor:** só freio Bash destrutivo — **zero** relação com testes ou evidência de aceite.
- **Gap central:** “critérios atendidos com evidência” e “test-first” são claims auditáveis só por revisão humana/LLM; o harness não bloqueia fechar task sem prova verificável além de “pytest passou em algum momento”.

## Deep Dive — Pontos de enforcement existentes

### 1. Definição de Pronto / DoD

| | |
|---|---|
| **Paths** | `.cursor/rules/definicao-de-pronto.mdc` · espelho `.claude/rules/definicao-de-pronto.md` |
| **O que exige** | Critérios testáveis; gate `/validar` verde; rules; revisor aprovado; cada critério com “evidência (teste ou demonstração)”; ADR se contestável; linha em `metrics/entregas.jsonl`; fluxo fechado só com `/sync-context` |
| **Tipo** | **Documentação / rule always-on** — não há script que verifique DoD |

### 2. `/validar`

| | |
|---|---|
| **Paths** | `.cursor/commands/validar.md` · `.claude/commands/validar.md` · helper `config/canonical_data_check/de_marker.py` · testes: `tests/data_engineering/test_validar_condicional.py` |
| **O que exige** | Sempre: `ruff check --fix` + `mypy` + `pytest -q`. Condicional: `canonical_data_check validate` se marker DE **ou** SDP/DLT **ou** vault |
| **Tipo** | **Gate mecânico se executado**. Não é hook automático no Cursor. Claude `Stop` parcial e condicionado a `backend/`/`src/` |

Hook Claude (citado pelo `/validar`):
- `.claude/settings.json` → `Stop`: ruff + mypy + pytest **só se** `backend` ou `src` existir; senão `exit 0`
- Mesmo arquivo → `Stop` drift: `check_context_drift.py --warn` (avisa, não bloqueia)

### 3. harness-build test-first

| | |
|---|---|
| **Paths** | `.cursor/agents/workflow/harness-build.md` · espelho `.claude/` · reforço em `.cursor/skills/to-tasks/SKILL.md` |
| **O que exige** | Teste por critério **antes** da lógica (deve falhar); implementar até verde; `/validar`; `revisor-codigo`; append `entregas.jsonl`; atualizar `STATUS.md` |
| **Tipo** | **Prosa de agent** — nenhum hook verifica ordem test-first nem red-before-green |

### 4. `metrics/entregas.jsonl` + schema

| | |
|---|---|
| **Paths** | `metrics/entregas.jsonl` · `metrics/README.md` · escrito por `harness-build` · lido por `/scorecard` e `harness-ship` |
| **O que exige** | 1 JSON/linha com `issue`, `titulo`, `data`, `criterios_aceite.{total,atendidos}`, `gate.*`, `revisor.*`, `intervencoes_humanas`, `commit` |
| **Tipo** | **Convenção + arquivo real**; append é instrução de agent. Sem validador; `atendidos` não aponta path de teste/log |

### 5. STATUS.md / checklist de fases

| | |
|---|---|
| **Paths** | Template do `harness-brainstorm` · exemplares em `.claude/projetos/*/STATUS.md` (espelho `.cursor/`) |
| **O que exige** | Checklist prosa fases 0–6 |
| **Tipo** | **Documentação operacional** — checkboxes manuais; sem gate mecânico |

### 6. revisor-codigo (testes/evidência)

| | |
|---|---|
| **Paths** | `.cursor/agents/dev/revisor-codigo.md` · espelho `.claude/` |
| **O que exige** | SI; invariantes; **cobertura de teste** no mesmo diff; critério sem teste precisa justificativa; skip/comentado/teste no-op = ausência |
| **Tipo** | **Soft gate LLM** — complementa o gate HARD, não substitui; veredito não validado por script |

### 7. sync-context / harness-ship (fechamento)

| | |
|---|---|
| **Paths** | `.cursor/skills/sync-context/SKILL.md` (+ `check_context_drift.py`) · `.cursor/agents/workflow/harness-ship.md` · ADR `docs/adr/001-sincronia-de-contexto-no-fechamento.md` · `DEV-LOOP.md` |
| **O que exige** | Tasks done; linha em `entregas.jsonl`; ADRs; drift limpo; `/scorecard`; `05-retro.md`; fechar STATUS |
| **Tipo** | Sync tem **scripts mecânicos**; obrigação de rodá-los no ship é **prosa**. Não exige evidência de teste além de ler jsonl/scorecard |

### 8. agent-policies / hooks

| | |
|---|---|
| **Paths** | `agent-policies.yaml` · `config/agent_policies/` · `.cursor/hooks.json` · hooks Claude PreToolUse |
| **O que exige** | Deny/ask em ops destrutivas |
| **Tipo** | Gate mecânico de **Bash** — **nada sobre pytest, DoD ou evidência** |

### 9. Pasta `evidencias/` / manifesto

| | |
|---|---|
| **Achado** | **Não existe** `evidencias/` na raiz. Prova operacional hoje = checkboxes `tested by` em tasks + linha auto-relatada em `entregas.jsonl` + (opcional) `05-retro.md` |
| **Nota** | `check_context_drift.py` usa `evidence:` só como texto de finding de **drift de docs**, não como prova de aceite |

## Gap analysis (claim vs evidência)

| Claim típico do agente | O que o harness verifica hoje | O que NÃO verifica |
|---|---|---|
| “Gate verde / `/validar` passou” | Se o agente **rodar** o comando: ruff+mypy+pytest (+ data-check condicional). Claude Stop só se `backend/`/`src/` | Que o gate rodou no fechamento da task; Cursor sem Stop; canônico sem `backend`/`src` = Stop no-op |
| “Test-first / teste falhou antes” | Nada mecânico — só instrução em `harness-build` / `to-tasks` | Ordem temporal; red-green; que o teste não é no-op |
| “Critério X atendido com evidência” | Checkbox + texto `tested by:` na task; número `atendidos` no jsonl | Existência do arquivo de teste; cobertura do critério; log/CI artifact |
| “Revisor aprovou, 0 bloqueantes” | Nada — veredito escrito pelo LLM no jsonl | Que o revisor foi invocado; persistência do parecer |
| “Delivery record gravado” | Arquivo existe; ship/scorecard leem | Schema válido; 1:1 com tasks done; SHA bate com commit |
| “Fluxo fechado (DoD 7)” | Scripts de drift **podem** falhar com `--check` | Que ship bloqueou em drift; evidência de aceite no fechamento |
| “100% critérios / scorecard bom” | Agregação aritmética sobre jsonl | Independência da fonte (agent pode forjar números) |

## Artefatos-chave (para o grill / define)

1. `.cursor/rules/definicao-de-pronto.mdc` (espelho `.claude/rules/definicao-de-pronto.md`)
2. `.cursor/commands/validar.md` + `.claude/settings.json` (hooks `Stop`)
3. `.cursor/agents/workflow/harness-build.md`
4. `.cursor/agents/dev/revisor-codigo.md`
5. `.cursor/skills/to-tasks/SKILL.md` (formato `tested by` / test-first)
6. `metrics/README.md` + amostra `metrics/entregas.jsonl`
7. `.cursor/commands/scorecard.md`
8. `.cursor/agents/workflow/harness-ship.md` + `.cursor/skills/sync-context/SKILL.md`
9. `.cursor/agents/workflow/harness-design.md` (Testing Decisions no PRD)
10. Exemplar de task: `tasks/policies-anti-destrutivas/41-contrato-yaml-loader.md`
11. Contraste: `.cursor/hooks.json` / `agent-policies.yaml` — ausência de gate de evidência
