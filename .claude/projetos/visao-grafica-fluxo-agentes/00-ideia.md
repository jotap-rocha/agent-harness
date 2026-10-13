# Visão Gráfica do Fluxo de Agentes

## Ideia

Quer uma **versão gráfica** (live) para saber:

1. Qual é o **fluxo de agentes** (SDD / harness / Dev Loop / etc.)
2. **O que cada um está fazendo** em tempo (quase) real ou por fase
3. Em cada fluxo SDD/harness — em especial na fase **build** — ver graficamente **o que está sendo feito** e **qual subagente** está em uso — visão de fluxo de processos de AI

Em resumo: **visão gráfica de fluxo do processo** (mapa + status/atividade por agent/subagent), evolução do harness canônico.

### Mockup aprovado

Mockup visual live aprovado pelo usuário em 2026-08-13 ("Agora sim. Ficou muito bom."):

`<cursor-projects>/<workspace-slug>/assets/mockup-visao-grafica-fluxo-live.png`

### Estrutura SDD canônica (mapa estrutural obrigatório)

Fonte confirmada pelo usuário — deve aparecer no mapa gráfico:

```
Fase 0 IDEIA:        brainstorm (harness-brainstorm)
Fase 1 REQUISITOS:   grill-me, harness-define
Fase 2 PRD+HARNESS:  harness-design, to-prd, harness-architect
Fase 3 IMPLEMENTAR:  to-tasks, harness-build, revisor-codigo
Fase 4 ENCERRAR:     harness-ship, /scorecard
```

### Resposta à pergunta: “conseguirei ver TODOS os subagentes em cada fase?”

Sim, em **dois modos** complementares (ambos no escopo da ideia):

| Modo | O que mostra | Cobertura |
|---|---|---|
| **Mapa estrutural** | Todas as fases SDD 0–4 + agents/skills/comandos listados (como no diagrama ASCII acima) | Completa — catálogo do fluxo canônico, mesmo sem execução |
| **Live** | Destaque do agent/subagent **ATIVO** + task em andamento + timeline de eventos | Em tempo (quase) real; MVP mínimo = telemetria live na fase **Build**; ideal = live em **todas** as fases |

Ou seja: o mapa mostra **todos** os subagentes/papéis possíveis por fase; o live destaca **quem está rodando agora** (e o histórico recente na timeline).

### Decisões fechadas (fase 0)

- Branch: `feat/visao-grafica-fluxo-agentes`
- Modo: **Live** (não estático HTML/Excalidraw como entrega principal)
- Tipo: evolução do harness canônico (ferramenta transversal)
- SI: apenas metadados de processo (nome de agent, fase, task id) — sem PII
- Gap atual no canônico (confirmado pelo codebase-explorer): STATUS.md = checklist prosa; visuals = estáticos; hooks = só shell deny/ask; sem event log de “qual agent está rodando agora”

## SI Assessment

Nível: **a** — Não — apenas dados abertos / metadados de processo (sem PII)

Implicações:
- Harness mínimo de SI (rules/seguranca.md já cobrem)
- Event log / telemetria: só metadados (agent name, phase, task id, timestamps) — nunca prompts com PII, secrets ou conteúdo de usuário
- Sem `[AVISO_LGPD]` / `rules/pii.md` neste escopo

## Tipo de Projeto

**e** — Outro: evolução do **harness canônico** / ferramenta transversal de observabilidade do fluxo SDD

Stack prevista:
- Artefatos canônicos existentes (agents workflow, STATUS.md, evidence-gate, metrics)
- Nova camada: event log + transport live + UI gráfica (mockup aprovado)
- Reuso possível: modelo de fases SDD, STATUS/entregas/audit como fontes históricas; visual-explainer/Excalidraw só como referência estática, não como produto live

## Próximos passos

0. Repo já mapeado — ver `00b-codebase.md` antes do grill
1. Rode `/grill-me` para aprofundar a ideia (live vs fontes de verdade, schema de eventos, onde a UI vive, MVP Build-only vs todas as fases)
2. Ao terminar, use `harness-define` para estruturar os requisitos
3. Depois: `harness-design` → PRD + harness-architect
