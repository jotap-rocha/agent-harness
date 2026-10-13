# Evidências e Testes Obrigatórios — Decisões de Harness

Slug: `evidencias-testes-obrigatorios`  
Branch: `feat/evidencias-testes-obrigatorios`  
Data: 2026-08-13  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Lacunas de naming fechadas no architect (sem entrevista): ver seção abaixo

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **a** (sem PII/secrets em evidências)
- Sem agent “evidence officer” / gate dedicado no canônico — estender agents existentes
- Evidence-gate = **hard**; `revisor-codigo` = **soft** ortogonal; kernels não unificados
- `/validar` permanece suite global; evidence-gate prova aceite **por task** (não substitui)
- `agent-policies` ortogonal — só cross-link opcional; não misturar freio Bash com prova de aceite
- Install foundation **sempre-on** (contrato + CLI + wiring DoD/agents/commands)
- Honesty §1.3: gate local ≠ impossibilidade de manifesto forjado; sem Edit policies
- Cap log **2 MiB** com **fail** se exceder (sem prova truncada silenciosa)
- `collect` ≤ **2×** o comando — **sem** hard timeout absoluto no yaml (G1)
- Concorrência **last-write-wins** na prova atual (G2); audit **append-only** (G4)
- Espelho `.claude` ↔ `.cursor` na mesma sessão de promoção (artefatos de projeto + wiring)
- Commit/push só com acordo explícito

## Naming fechado no architect (não bloqueava; alinhado ao padrão)

| Item | Escolha | Motivo |
|---|---|---|
| Contrato | `evidence-gate.yaml` (raiz) | Espelha `git-hygiene.yaml` / `agent-policies.yaml` |
| Pacote engine | `config/evidence_gate/` (`contract.py`, `yaml_loader.py`, collect, check, `__main__`) | Padrão `git_hygiene` / `agent_policies` / `data_engineering` |
| CLI | `python -m config.evidence_gate collect\|check` | Espelha `python -m config.agent_policies` / `canonical_data_check` |
| Pasta de provas | `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/projetos/.../evidencias/`) | Grill decisão 3 |
| Manifesto por task | `evidencias/tasks/<task_id>.yaml` | Um arquivo/task; LWW sobrescreve este path |
| Logs de collect | `evidencias/logs/<task_id>/<criterion_id>.log` | Isola critério; facilita check e cap por artefato |
| Audit append-only | `evidencias/audit.jsonl` (1 JSON/linha por evento `collect`) | Opção PRD FR8; espelha `metrics/entregas.jsonl` |
| Campo delivery | `evidencias_ref` em `metrics/entregas.jsonl` = path relativo ao manifesto da task | Grill decisão 3 / AC8 |
| Waiver humano | no critério: `waiver: { human: true, reason: "..." }` (obrigatório se sem teste) | AC4 explícito |
| Cap no contrato | `limits.max_log_bytes: 2097152` (2 MiB); `limits.collect_time_factor: 2` (alvo, não hard kill) | G3 + G1 |
| Seed / SCHEMA | `config/evidence_gate/templates/evidencias/` → SCHEMA.md + exemplo de manifesto (`seed: true` KEEP no filho sob `.harness/evidence-gate/` se install gravar seed) | Como `agent_policies/templates/policies/` |
| Docs SHOULD | `docs/evidence-gate-cheatsheet.md` + ADR em `docs/adr/` | Como git-hygiene / agent-policies |
| Command SHOULD | `.claude/commands/evidencias.md` (+ `.cursor/commands/`) | Atalho docs → CLI; não substitui o módulo |
| Testes | `tests/evidence_gate/` (+ fixtures sob `tests/evidence_gate/fixtures/`) | Espelha `tests/agent_policies/` |
| Cross-link policies | cheatsheet / DoD: “Bash deny ≠ aceite” | Ortogonalidade FR7 |

### Layout lógico da pasta `evidencias/` (por projeto)

```text
.claude/projetos/{slug}/evidencias/
├── tasks/
│   └── <task_id>.yaml          # manifesto atual (LWW)
├── logs/
│   └── <task_id>/
│       └── <criterion_id>.log  # saída do collect
└── audit.jsonl                 # append-only (G4)
```

Espelho idêntico sob `.cursor/projetos/{slug}/evidencias/` quando dual-tree.

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Contrato schema/check/cap/2× | `evidence-gate.yaml` (raiz) | validação | loader + CI + CLI |
| Engine load/collect/check | `config/evidence_gate/` | validação | CLI + agents + install |
| CLI collect\|check | `python -m config.evidence_gate` | ferramentas | harness-build / ship / maintainer |
| Manifesto + logs + audit | `projetos/{slug}/evidencias/` (+ espelho) | estado | check + revisor + humano |
| Link no delivery | `metrics/entregas.jsonl` + `metrics/README.md` (`evidencias_ref`) | estado | scorecard / ship |
| Bloqueio close task | wiring `harness-build` + DoD | validação | agente build |
| Revalidação ship | wiring `harness-ship` | validação | agente ship |
| Critérios → testes nas tasks | skill `to-tasks` (formato tested-by alinhado ao manifesto) | execução | autor de tasks |
| Revisor soft ortogonal | `revisor-codigo` (não valida exit do manifesto) | validação | revisão LLM |
| DoD mecânico | `rules/definicao-de-pronto` (+ `.mdc`) | estado | todo agente |
| `/validar` intacto | `commands/validar` (sem substituir) | validação | CI / build |
| Install foundation | `install-harness` / `stack_map` + seed `.harness/evidence-gate/` | ferramentas | `/install-harness` |
| Seed SCHEMA + exemplo | `config/evidence_gate/templates/evidencias/` | ferramentas | install + filho |
| Cheatsheet + `/evidencias` | `docs/evidence-gate-cheatsheet.md` + command SHOULD | estado | agente JIT |
| Testes kernel | `tests/evidence_gate/` | validação | `/validar` |
| Contagem/docs canônico | `CLAUDE.md` / `AGENTS.md` / CONTEXT no ship | estado | próximo agente |
| ADR | `docs/adr/` (kernel evidence-gate + LWW/audit/cap) na implementação | estado | humano + agent |
| Cross-link policies/DE | docs / cheatsheet (sem unificar) | estado | SI + maintainer |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs listados acima — andaime real no `harness-build` após
`/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent “evidence officer” / gate dedicado no canônico (gate de redundância —
  responsabilidades cabem em build/ship/revisor + CLI)

### Agents/skills a estender (build)
- `harness-build` — collect → check antes de done / append `entregas.jsonl` com
  `evidencias_ref`
- `harness-ship` — revalidar `check` das tasks do fluxo antes de fechar
- `revisor-codigo` — reforçar ortogonalidade (soft ≠ hard); ler manifesto se útil, sem
  substituir CLI
- `to-tasks` — critérios com paths de teste compatíveis com manifesto
- `install-harness` / `stack_map` — foundation always-on: contrato + engine + wiring +
  seed KEEP
- `definicao-de-pronto` (rule) — evidência mecânica via evidence-gate
- (SHOULD) command `/evidencias` + cheatsheet; sem skill MUST nova no MVP (playbook =
  cheatsheet; revisitar se crescer)

### Rules
- Estender `definicao-de-pronto` (+ `.mdc`) — MUST
- Ponte curta opcional em `seguranca` (nunca secret/PII em logs de evidência) — SI a
- Sem rule nova `evidence-gate.md` obrigatória; cheatsheet em `docs/` (SHOULD)

### KBs
- **Nenhum** KB de domínio novo obrigatório neste ship (framework de gate, não stack de
  produto)

### Kernel / seed / testes (a criar no build)
- `evidence-gate.yaml` + `config/evidence_gate/` (collect executa; check valida)
- Seed `config/evidence_gate/templates/evidencias/` → `.harness/evidence-gate/` (SCHEMA +
  exemplo, KEEP)
- Layout `evidencias/tasks|logs|audit.jsonl`
- `evidencias_ref` no schema de `metrics/`
- Testes `tests/evidence_gate/` (collect, check, cap, waiver, LWW+audit, install fixture)
- Dogfood: wiring agents/DoD no canônico; uso real nas tasks futuras deste/outros ships

## O que NÃO entra neste ship

- Hooks Stop dual Claude/Cursor obrigatórios (Fase 2 / COULD)
- Portal UI / dashboard de evidências
- E2E obrigatório Claude Code / Cursor IDE no CI
- Substituir `/validar` pelo evidence-gate
- Misturar/unificar com `agent-policies` ou DE kernel
- Secrets/PII em logs de evidência; key vault / pacote E
- Mutex cross-agent; hard timeout absoluto no yaml
- Prova truncada silenciosa acima de 2 MiB
- Screenshots/PDF como MUST
- Agent dedicado “evidence officer”
- Tag `prod-*` / Fase 2 git hygiene
- Skill MUST `evidence-gate` (cheatsheet basta no MVP)

## Decisões contestáveis (ADR na implementação)

1. Kernel **separado** `evidence-gate` (não fundir com `/validar`, agent-policies ou DE) —
   prova de aceite por task ≠ suite global ≠ freio Bash ≠ checks cloud
2. Install **foundation always-on** (não categoria opt-in) — DoD auditável default nos filhos
3. `collect` **executa** (não só declara) — prova = artefato de run
4. Cap **2 MiB** com **fail-on-exceed** (não truncate) — prova parcial inválida
5. Concorrência **LWW** + audit **append-only** (`evidencias/audit.jsonl`) — MVP sem mutex
6. Sem skill MUST no MVP (cheatsheet + wiring agents) — evitar proliferação; revisitar se
   playbook crescer
7. Seed sob `config/evidence_gate/templates/evidencias/` → `.harness/evidence-gate/` —
   pacote dono do contrato (padrão policies)

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local `feat/evidencias-testes-obrigatorios`
- Working tree: artefatos untracked em `projetos/evidencias-testes-obrigatorios/`
- Sem commit/push neste passo
- Adversarial judge define: **(b)** pulado (2026-08-13)
- Adversarial judge PRD: **(b)** pulado (2026-08-13) — sem `02b-judge.md`

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (tracer bullets)
2. `harness-build` — implementar com `/validar` + `revisor-codigo`
3. Ao fechar: `/sync-context` + delivery record em `metrics/entregas.jsonl` (com
   `evidencias_ref` quando o kernel já existir — dogfood)
