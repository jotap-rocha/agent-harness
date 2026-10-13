# Evidências e Testes Obrigatórios

## Ideia

Incluir no repositório canônico que, ao fazer processos de qualquer tipo usando o fluxo
harness (harness-brainstorm / ciclo completo), deve:

1. **Forçar testes unitários**
2. **Exigir coletar evidências** do que foi feito — não acreditar só em texto; obter
   evidências verificáveis

Motivação: reduzir alucinação de “done” e tornar a Definição de Pronto (DoD) auditável.

**Escopo confirmado:** ciclo inteiro — brainstorm → define → design → build → ship,
incluindo DoD, `/validar`, `revisor-codigo` e `metrics/entregas.jsonl` — não só
brainstorm/STATUS.

Contexto já existente (não reinventar): DoD (`definicao-de-pronto`), `/validar`,
test-first no `harness-build`, `revisor-codigo`, delivery records, agent-policies (ship
recente), git-hygiene. Gap: enforcement mecânico de evidência além de claims em prosa.

## Hipóteses propostas (confirmar no grill)

Marcar como **proposto — confirmar no grill**; não são decisões fechadas:

| Tema | Hipótese |
|------|----------|
| Evidência mínima | Saída de `/validar` ou pytest com exit 0 + path do log/artefato + referência em `metrics/entregas.jsonl` e/ou pasta de evidências por projeto |
| Unitários | Obrigatórios no `harness-build` (test-first) + gate `/validar` (pytest) como enforcement mecânico |
| Onde gravar | `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/`) com manifesto por task |

## A fechar no grill

- Evidência mínima exacta (pytest log? paths? commit SHA? só `entregas.jsonl`?)
- Unitário **além** de `/validar`, ou `/validar` basta como gate de testes
- Onde gravar de fato: `metrics/` vs `projetos/{slug}/evidencias/` vs hook Stop (Claude/Cursor)
- Como tornar DoD/revisor/ship bloqueantes com prova verificável (não só LLM claim)
- Dual-runtime: Claude Stop parcial vs Cursor sem Stop equivalente (ver `00b-codebase.md`)

## SI Assessment

Nível: a — sem dados sensíveis (apenas dados abertos, sintéticos ou públicos)

Implicações:
- Harness mínimo de SI (já presente em `rules/seguranca`)
- Sem `[AVISO_LGPD]` / `rules/pii.md`
- Evidências não devem incluir secrets/PII (logs de gate e paths de artefato apenas)

## Tipo de Projeto

e — Evolução do harness canônico (framework, não produto)

Stack prevista:
- Rules (DoD), agents (`harness-build`, `revisor-codigo`, ship), commands (`/validar`, `/scorecard`)
- `metrics/entregas.jsonl` + possível pasta `projetos/{slug}/evidencias/` + manifesto
- Hooks/gates mecânicos (pytest/ruff/mypy; eventual extensão Stop/Cursor)
- Propagação via `/install-harness` para projetos-filhos
- Testes de conformidade do próprio enforcement

## Próximos passos

0. Repo já mapeado — ver `00b-codebase.md` antes do grill
1. Rode `/grill-me` para aprofundar a ideia (evidência mínima, gates mecânicos, pasta vs metrics, dual Claude↔Cursor)
2. Ao terminar, use `harness-define` para estruturar os requisitos
3. Depois: `harness-design` → PRD + harness-architect (flavor: evolução do canônico)
