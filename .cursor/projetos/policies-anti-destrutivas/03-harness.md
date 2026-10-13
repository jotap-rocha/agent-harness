# Policies Anti-Destrutivas — Decisões de Harness

Slug: `policies-anti-destrutivas`  
Branch: `feat/policies-anti-destrutivas`  
Data: 2026-08-12  
PRD: `02-prd.md`  
Judge: define (b) + PRD (b) pulados — sem `01b-judge.md` / `02b-judge.md`  
Lacunas de naming fechadas no architect (sem entrevista): ver seção abaixo

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **d** (ops destrutivas)
- Sem agent “policy officer” no canônico
- Paridade **política** Claude ↔ Cursor (mesmo catálogo/severity); UI pode diferir
- `DE-A002` ortogonal — só cross-link; kernels não unificados
- Soft policy `seguranca` permanece; githooks permanecem secrets-only
- Honesty §1.3: deny/hooks ≠ Edit policies server-side; bypass e clone sem hooks existem
- Install foundation **sempre-on** (core + engine + hooks dual); extras via profile KEEP
- Espelho de hooks/scripts `.claude` ↔ `.cursor` na mesma sessão de promoção
- Commit/push só com acordo explícito

## Naming fechado no architect (não bloqueava; alinhado ao padrão)

| Item | Escolha | Motivo |
|---|---|---|
| CLI | `python -m config.agent_policies generate\|check` | Espelha `python -m config.canonical_data_check` |
| Pacote engine | `config/agent_policies/` (`contract.py`, `yaml_loader.py`, match, generate, adapters) | Padrão `git_hygiene` / `data_engineering` |
| Seed template | `config/agent_policies/templates/policies/` → `.harness/policies/` (`seed: true` KEEP) | Como `canonical_data_check/templates/data-check/` |
| Profile filho | `.harness/policies/project_profile.yaml` com `families[]` | Grill decisão 14 |
| Guard entry | módulo compartilhado + adapters finos Claude/Cursor (scripts sob hooks/) | Um matcher; dois contratos stdin/stdout |
| Docs SHOULD | ponte curta em `rules/seguranca` + cheatsheet `docs/agent-policies-cheatsheet.md` | Como git-hygiene (rule + 1 página) |
| Bypass env | `HARNESS_ALLOW_DESTRUCTIVE=1` | Grill/PRD fechado |

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Contrato famílias/patterns/severity | `agent-policies.yaml` (raiz) | validação | loader + CI + generate |
| Engine load/match/generate | `config/agent_policies/` | validação | CLI + hooks + install |
| CLI generate\|check | `python -m config.agent_policies` | ferramentas | maintainer / install |
| Deny Claude + PreToolUse | `.claude/settings.json` hooks + scripts sob `.claude/hooks/` | validação | Claude Code |
| Cursor beforeShellExecution | `.cursor/hooks.json` + `.cursor/hooks/` | validação | Cursor |
| Core always-on + extras opt-in | generate + profile `families[]` | validação | install + filho |
| Seed KEEP | `config/agent_policies/templates/policies/` → `.harness/policies/` | ferramentas | install-harness |
| Install foundation (deny ≠ []) | `install_harness` generate + `stack_map` foundation | ferramentas | `/install-harness` |
| Bypass + audit trail | guard short-circuit env + log (sem secret) | validação | SI + operador |
| Fail closed/open | comportamento do guard por severity | validação | runtime |
| SI + §1.3 honesty | ponte `rules/seguranca` (+ `.mdc`) + CONTEXT / cheatsheet | estado | agente + revisor |
| Cross-link DE-A002 | docs / cheatsheet / remediação textual | estado | DE + SI |
| Testes | `tests/agent_policies/` (matcher, guard fixtures, install) | validação | `/validar` |
| Contagem/docs | `CLAUDE.md` / `AGENTS.md` / CONTEXT no ship | estado | próximo agente |
| ADR | `docs/adr/` (kernel agent-policies + dual-runtime + fail closed) na implementação | estado | humano + agent |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs listados acima — andaime real no `harness-build` após
`/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent “policy officer” / anti-destrutivo dedicado no canônico

### Agents/skills a estender (build)
- `install-harness` / `stack_map` / generate de settings — foundation always-on:
  engine + core families + hooks dual; corrigir `deny: []`
- (Opcional JIT) menção em `harness-architect` templates se PreToolUse/deny aparecerem
  como exemplo — **não** inventar skill/agent novos de produto
- Sem skill nova obrigatória no MVP; playbook = cheatsheet + ponte `seguranca`
  (SHOULD). Se no build surgir necessidade de playbook longo, preferir skill curta
  `agent-policies` espelhada — **não** neste mapa como MUST

### Rules
- Ponte curta em `seguranca` (deny/ask/bypass + §1.3) — sem rule nova `agent-policies.md`
  obrigatória; cheatsheet em `docs/` (SHOULD)
- `git-hygiene` / §1.3: reforçar honesty (gates locais ≠ Edit policies)

### KBs
- **Nenhum** KB de domínio novo obrigatório neste ship (framework de policies, não stack
  de produto). Cross-links nos docs existentes bastam.

### Kernel / hooks / seed (a criar no build)
- `agent-policies.yaml` + `config/agent_policies/`
- Hooks Claude PreToolUse + Cursor `hooks.json` / `beforeShellExecution`
- Seed `.harness/policies/project_profile.yaml` (`families[]`, KEEP)
- Bypass `HARNESS_ALLOW_DESTRUCTIVE=1` + fail closed/open
- Testes `tests/agent_policies/`
- Dogfood canônico: settings/hooks alinhados ao generate (SHOULD: core+extras; limpar
  paths de máquina)

## O que NÃO entra neste ship

- Edit policies / branch protection server-side / portal UI
- Live API cloud no CI para “provar” destroy
- Agent dedicado “policy officer”
- Remover `seguranca` ou unificar/deprecar `DE-A002`
- E2E obrigatório Claude Code / Cursor IDE no CI
- Transformar githooks em anti-shell
- Key vault / pacote E (ortogonal; N/A)
- Prompt-hook Cursor além de command-hook (COULD)
- Métricas de bloqueio em `metrics/` (COULD)
- Tag `prod-*` / Fase 2 git hygiene

## Decisões contestáveis (ADR na implementação)

1. Kernel **separado** `agent-policies` (não fundir com DE / git-hygiene) — runtime Bash ≠
   código versionado / SCM
2. Install **foundation always-on** (não categoria opt-in) — SI d exige freio default
3. Fail **closed** só em deny-hard; fail **open** em ask/opt-in — equilíbrio SI vs Dev Loop
4. Seed template sob `config/agent_policies/templates/policies/` (não
   `config/templates/` solto) — pacote dono do contrato
5. Sem skill MUST no MVP (cheatsheet + ponte) — evitar proliferação; revisitar se playbook
   crescer

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local `feat/policies-anti-destrutivas`
- Working tree: artefatos untracked em `projetos/policies-anti-destrutivas/`
- Sem commit/push neste passo
- Adversarial judge PRD: **(b)** pulado (2026-08-12)

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (tracer bullets)
2. `harness-build` — implementar com `/validar` + `revisor-codigo`
3. Ao fechar: `/sync-context` + delivery record em `metrics/entregas.jsonl`
