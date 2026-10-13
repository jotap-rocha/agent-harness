# Evidências e Testes Obrigatórios — Grill & Requisitos

Slug: `evidencias-testes-obrigatorios`  
Branch: `feat/evidencias-testes-obrigatorios`  
Grill fechado em: 2026-08-13  
Define enriquecido em: 2026-08-13  
Fontes: `00-ideia.md`, `00b-codebase.md`, decisões do `/grill-me`, `harness-define`

## Checklist de completude (qualquer tipo)

| Dimensão | Status |
|---|---|
| Problema real (não sintoma) | ✅ claims de “done” sem prova mecânica |
| Usuários / personas | ✅ maintainer, agente/build, revisor/ship, filho |
| Critérios de sucesso mensuráveis | ✅ (seção abaixo + testes do kernel) |
| Out of scope | ✅ Stop dual, portal, substituir `/validar`, misturar policies |
| Restrições técnicas | ✅ tipo e, SI a, ciclo inteiro, soft-block fetch |
| SLA / performance | ✅ inferido (seção SLA) — confirmar se quiser outro alvo |

## Contexto (da sessão /grill-me)

### Problema

No ciclo harness (brainstorm → ship), “done” e critérios de aceite ainda dependem de
**claims em prosa** (DoD, test-first, revisor, `entregas.jsonl` auto-relatado). O gate
mecânico `/validar` só vale se alguém rodar; Stop Claude é parcial; Cursor não tem Stop
de testes. Não há pasta/manifesto de evidências nem validador que cruze critério → teste
→ log → exit code. Resultado: alucinação de entrega e DoD inauditável.

### Usuários

| Persona | Pain |
|---|---|
| Maintainer do canônico | Precisa de freio mecânico reutilizável (como agent-policies / DE) |
| Agente / harness-build | Precisa saber o que gravar e quando está bloqueado de fechar task |
| Revisor / SI / ship | Precisa auditar prova sem confiar só no texto do LLM |
| Projeto-filho | Mesmo freio via install foundation |

### Objetivos (MoSCoW)

**MUST:**
- Kernel `evidence-gate.yaml` + `config/evidence_gate/` + CLI `collect|check`
- Manifesto por task: critério → path(s) de teste + comando + exit_code + path de log
- Pasta `.claude/projetos/{slug}/evidencias/` (+ espelho `.cursor/`)
- Campo `evidencias_ref` obrigatório em `metrics/entregas.jsonl` apontando o manifesto
- Cada critério com ≥1 teste unitário no manifesto (demo sem teste = justificativa + humano)
- `collect` **executa** o comando e grava artefato; `check` valida
- Bloqueio no fechamento de **cada task** + **revalidação no ship**
- Install foundation always-on (schema + CLI + wiring agents/commands)
- `revisor-codigo` ortogonal (soft); evidence-gate = hard
- Atualizar DoD / harness-build / harness-ship / to-tasks / metrics schema
- Testes do próprio kernel (`tests/evidence_gate/`)
- Espelho `.claude` ↔ `.cursor` nos artefatos de projeto
- Cap de log **2 MiB**; alvo `collect` ≤ **2×** o comando (sem hard timeout absoluto)
- Concorrência last-write-wins na prova atual; **trilha append-only** de auditoria
- Preferir falha do `collect` se log exceder cap (não prova truncada silenciosa)

**SHOULD:**
- Template de manifesto + SCHEMA.md no seed/install
- Comando `/evidencias` (atalho docs) além da CLI
- Cheatsheet 1 página
- ADR do kernel evidence-gate

**COULD:**
- Hooks Stop dual Claude/Cursor (Fase 2)
- Screenshots/PDF para tasks UI
- Dashboard/portal de evidências

### Out of Scope

- Hooks Stop dual obrigatórios no MVP
- Portal UI / dashboard
- E2E IDE obrigatório no CI
- Substituir `/validar` pelo evidence-gate
- Misturar com `agent-policies` (concern distinto)
- Secrets/PII em logs de evidência
- Key vault (SI a — N/A)

### Restrições

- Evolução de **framework** (tipo e); SI **a**
- Escopo = **ciclo inteiro**, não só brainstorm
- Fetch Azure pode falhar 403 — soft-block didático
- Branch: `feat/evidencias-testes-obrigatorios`
- Sem commit/push neste passo define

## Decisões numeradas (grill — fechadas)

1. Perímetro MVP: manifesto + validador mecânico (cruzar prova ↔ pytest/`/validar`); sem hooks MUST (**c**)
2. Evidência mínima: manifesto critério → testes + comando + exit_code + path log (**b**)
3. Onde gravar: `projetos/{slug}/evidencias/` + espelho + `evidencias_ref` em entregas (**d**)
4. Unitários: cada critério → ≥1 teste no manifesto; demo só com justificativa + humano; `/validar` segue como suite (**b**)
5. Quando bloqueia: fechamento de cada task **e** revalidação no ship (**c**)
6. Propagação: install **foundation always-on** (**b**)
7. Kernel: `evidence-gate.yaml` + `config/evidence_gate/` + `python -m config.evidence_gate collect|check` (**a**)
8. Produção da prova: `collect` **roda** o comando e grava log (**a**)
9. Revisor vs gate: **ortogonal** — gate hard, revisor soft (**a**)
10. Fora do ship: sem Stop dual MUST, sem portal, sem substituir `/validar`, sem misturar agent-policies (**a**)
11. Timeout collect: só alvo **2×** o comando — sem hard cap absoluto no yaml (**G1**)
12. Concorrência: **last-write-wins** (**G2-a**)
13. Cap de log: **2 MiB** (**G3-a**)
14. Auditoria: trilha **append-only extra** além de manifesto/log/ref (**G4-c**)
15. Adversarial judge (define): **(b)** pulado

### Inferidos (confirmados — não reabrir)

| # | Inferência | Status |
|---|---|---|
| I1 | `/validar` permanece (ruff+mypy+pytest); evidence-gate prova aceite por task | Confirmado (decisões 4, 10) |
| I2 | `entregas.jsonl` ganha `evidencias_ref`; scorecard/ship leem o link | Confirmado (decisão 3) |
| I3 | Canônico dogfooda o gate nas próprias tasks futuras | Confirmado (tipo e) |

## Amarras a artefatos (previsto)

| Artefato | Onde | Nota |
|---|---|---|
| Contrato | `evidence-gate.yaml` | Schema manifesto + regras de check |
| Engine/CLI | `config/evidence_gate/` | collect, check, loader |
| Evidências por projeto | `.claude/projetos/{slug}/evidencias/` (+ `.cursor/`) | Manifestos + logs |
| Delivery | `metrics/entregas.jsonl` + `metrics/README.md` | `evidencias_ref` |
| Wiring agents | `harness-build`, `harness-ship`, `revisor-codigo`, `to-tasks` | Bloqueio close |
| DoD | `rules/definicao-de-pronto` (+ `.mdc`) | Evidência mecânica |
| Install | foundation `stack_map` + generate | Always-on |
| Testes | `tests/evidence_gate/` | Kernel |
| Docs | cheatsheet + ADR | SHOULD |

## Vault / secrets cloud

- Usa cofre cloud?: **não**
- Provedor: N/A
- N/A: **sem key vault** — SI **a**; evidências = logs de gate/paths; sem wiring OCI/Azure (confirmado na ideia; não reabrir)

## Pipeline (meta — tipo e, não b/c)

N/A como produto de dados. Em meta-nível framework (padrão policies / keyvault):

| # | Pergunta (meta) | Resposta |
|---|---|---|
| 1 | Fontes | Comandos de teste/gate referenciados no manifesto (pytest paths, `/validar` quando amarrado) |
| 2 | Schema | `evidence-gate.yaml` + schema do manifesto; mudanças versionadas no canônico |
| 3 | Volume | N/A batch — 1 manifesto/logs por task; tamanho de log = lente abuso |
| 4 | Sensibilidade | SI **a**; sem PII/secrets nos artefatos de evidência |
| 5 | SLA | Ver seção SLA (latência `collect`/`check` vs Dev Loop) |
| 6 | Consumidores | harness-build (close task), harness-ship, revisor (leitura), `/scorecard`, filhos via install |
| 7 | Owner | Maintainer do canônico; no filho, dono do fluxo/DoD |
| 8 | Ambiente | Local dual IDE (Claude/Cursor); sem Stop dual no MVP |
| 9 | Qualidade | `check` exit ≠ 0 = bloqueante; waiver humano só com marcador explícito no manifesto |
| 10 | Portabilidade | Foundation always-on; pasta `projetos/{slug}/evidencias/` + `evidencias_ref` |

## SLA / performance (inferido)

Alvo orientativo para não travar o Dev Loop:

| Operação | Alvo | Nota |
|---|---|---|
| `check` (só FS/schema) | **&lt; 5 s** para manifesto típico de 1 task | Hot path de close/ship |
| `collect` (executa comando) | **≤ 2×** o tempo do próprio comando referenciado (ex.: pytest do critério) | **Sem** hard timeout absoluto no yaml (G1 fechado) |
| Falha / timeout | exit ≠ 0 → close/ship **bloqueados**; sem retry automático no MVP | Mensagem CLI em stderr |

## Especificações implícitas detectadas

1. **Falha de dependência / collect:** comando falha / não existe → `collect` grava `exit_code ≠ 0` → `check` falha → close/ship **bloqueado**. Alvo de tempo = **2×** o comando; **sem** hard timeout absoluto no yaml (G1). Sem retry automático no MVP.
2. **Concorrência (dois closes):** **last-write-wins** no manifesto/log da task (G2-a); sem mutex cross-agent no MVP; `check` valida o artefato final em disco. Append-only (G4) preserva histórico de coletas anteriores.
3. **Idempotência:** reexecutar `collect` na mesma task atualiza a prova “atual” de forma determinística; trilha append-only registra cada coleta. `check` reexecutável (leitura + validação).
4. **Autenticação/autorização:** N/A — CLI local; sem multi-tenant/RBAC. Quem fecha = quem roda o agent no repo.
5. **Dados sensíveis não declarados:** N/A — SI **a**; sem PII/secrets em logs; fixtures só paths/exit codes. Redaction leve = SHOULD.
6. **Abuso e limites (tamanho de log):** cap **2 MiB** (G3-a) no `evidence-gate.yaml`; acima do cap → `collect` falha ou marca `truncated` conforme política no PRD (preferir **falha** se truncar invalidar prova).
7. **Auditoria de evidências:** além de manifesto + log + `evidencias_ref` (+SHA), **trilha append-only extra** (G4-c) — ex. `evidencias/audit.jsonl` ou histórico versionado por coleta; detalhe de formato no PRD.
8. **Estados de erro visíveis:** CLI → exit code + stderr claro; agents param o close; sem fallback silencioso.
9. **Ciclo de vida dos dados:** evidências no git do projeto; sem TTL automático; exclusão = humano/git (SI a).
10. **Dependência de terceiros mudando:** contrato versionado; breaking = bump + `tests/evidence_gate/`; fail closed no close.

### Gaps do define — fechados (2026-08-13)

| ID | Decisão |
|---|---|
| G1 | Só alvo **2×** o comando — **sem** hard timeout absoluto no yaml |
| G2 | Concorrência **(a)** last-write-wins |
| G3 | Cap log **2 MiB** aceito |
| G4 | Auditoria **(c)** trilha **append-only extra** |
| Judge | **(b)** pulado — sem `01b-judge.md` |

## Critérios de sucesso mensuráveis

- `collect` em fixture gera log + exit_code; `check` passa só com manifesto válido
- Fechar task sem manifesto/`evidencias_ref` → CLI/check exit ≠ 0 (simulado no teste de wiring)
- Critério sem path de teste → check falha (salvo marcador de waiver humano no manifesto)
- Install fixture: CLI + schema presentes no filho (foundation)
- `/validar` do canônico verde com `tests/evidence_gate/`
- DoD/agents atualizados exigem evidence-gate antes de `done`/ship
- Zero secret/PII nos logs de exemplo/fixture
- `check` &lt; 5 s em fixture de manifesto típico (regressão de SLA)

## Soft-blocks registrados

- `git fetch` Azure 403 — trabalho na branch local `feat/evidencias-testes-obrigatorios` (não fingir sync remoto novo)
- Working tree: artefatos do projeto em `projetos/evidencias-testes-obrigatorios/` (esperado)
- Sem commit/push neste passo
- Adversarial judge: **(b)** pulado (2026-08-13)

## Próximo passo

Gaps G1–G4 e judge fechados. Requisitos estruturados neste arquivo.

Dizer **`harness-design`** para gerar o PRD (`02-prd.md`) e montar o harness.
