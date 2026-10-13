# PRD — Kernel de conformidade DE (Loop 1 / Ship 1)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Repo: Agent Harness Canônico (framework — **não** produto ETL de domínio)  
Branch: `feat/de-boas-praticas-canonico`  
Data: 2026-08-06  
Tipo: **e** — evolução do framework de conformidade de Engenharia de Dados  
SI: **c + d**  
Fontes: `00-ideia.md`, `00b-codebase.md`, `01-grill.md` (13 decisões), sketch  
`sketch/data-engineering/pesquisa-4-repos-pipelines-boas-praticas.md`

> Este PRD descreve **somente o Loop 1**. Loops 2 (Databricks) e 3 (skills/agents/KBs DE) aparecem em *Further Notes* como roadmap futuro — **não** são MUST deste ship.

---

## Problem Statement

O canônico já documenta boas práticas de Engenharia de Dados (10 agents DE, 7 commands, ~11 KBs, `rules/pipeline`), mas **não prova** conformidade. Projetos-filhos que passam pelo `install-harness` recebem prosa (`kb/pipeline` + `rules/pipeline`) sem validador executável, baseline brownfield ou pacote mínimo verificável.

O problema real (não o sintoma) é a ausência de um **kernel normativo executável**: norma versionada → checks → CI/baseline/waiver → example greenfield → install mínimo → gate condicional. Sem isso, o harness **explica** boas práticas sem **provar** que os projetos as seguem — risco central do sketch adversarial e do mapeamento `00b`.

Mantenedores do canônico e engenheiros DE em filhos precisam de um DoD mensurável no perfil piloto `spark-yarn-airflow`, sem expandir o catálogo agentic antes do enforcement existir.

---

## Solution

Entregar no canônico o **Ship 1 / Loop 1** do kernel de conformidade DE, espelhando o padrão já estabelecido por `git-hygiene.yaml` + `config/git_hygiene/`:

1. **`data-engineering.yaml` na raiz** — fonte normativa única (Universal + perfil `spark-yarn-airflow`), com IDs, categorias e severidades.
2. **CLI** (`canonical-data-check` ou nome equivalente) com `validate`, `baseline`, `compare` e `report` (json|markdown); SHOULD: `explain <rule_id>`.
3. **Checks A+B blockers**; **C Airflow condicional** (skip se sem DAG).
4. **Example** `examples/spark-yarn-airflow-min/` que passa A+B (fora do install automático).
5. **Relatório somente-leitura** do brownfield  
   `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd` — **sem escrever** nesse repo.
6. **`install-harness`**: pacote mínimo verificável (norma subset + CLI + rule + perfil default + KB pipeline; **sem** 10 agents).
7. No filho: **`.harness/data-check/`** (`project_profile.yaml` + `baseline.json`) com **baseline ratchet** e waiver pontual (owner + expiry).
8. **`/validar` condicional**: CLI sempre disponível; check DE só se marker/perfil DE.
9. **Testes no canônico** (contrato YAML + comportamento CLI no example) + espelho `.claude/` ↔ `.cursor/` em toda promoção.

Ordem adversarial (não invertível no curto prazo): governance → validator → baseline/waiver → example → install → gate — **antes** de novos agents/skills/KBs.

---

## User Stories

### Mantenedor do canônico / CI do harness

1. As a mantenedor do canônico, I want a `data-engineering.yaml` versionado na raiz, so that regras DE têm fonte única auditável (como `git-hygiene.yaml`).
2. As a mantenedor do canônico, I want a CLI com `validate` / `baseline` / `compare` / `report`, so that conformidade é executável e não só documentada.
3. As a mantenedor do canônico, I want pacotes A+B como blockers e C condicional, so that o MVP bloqueia o essencial sem exigir Airflow em todo alvo.
4. As a mantenedor do canônico, I want `examples/spark-yarn-airflow-min/` passing A+B, so that o DoD do Ship 1 é demonstrável no próprio framework.
5. As a mantenedor do canônico, I want pytest covering YAML contract + CLI against the example, so that regressões do kernel quebram CI do harness.
6. As a mantenedor do canônico, I want a RO compliance report against sql-capacity without writing there, so that brownfield gaps are visible without mutating the PRD repo.
7. As a mantenedor do canônico, I want soft-fail when sql-capacity path is missing, so that CI of the example stays green in environments without that path.
8. As a mantenedor do canônico, I want mirror `.claude` ↔ `.cursor` on every promotion, so that Cursor and Claude stay in sync.
9. As a mantenedor do canônico, I want NOT to create new DE agents/skills/KBs in Loop 1, so that we avoid catalog growth without enforcement.
10. As CI do canônico, I want validate on the example to finish within ~60s, so that the gate stays practical.

### Engenheiro DE / projeto-filho

11. As an engenheiro DE, I want `install-harness` to install a minimal verifiable DE package (not 10 agents), so that I get real checks without false conformity.
12. As an engenheiro DE, I want `.harness/data-check/` with `project_profile.yaml` and `baseline.json`, so that profile and ratchet live in my repo.
13. As an engenheiro DE, I want baseline ratchet (new findings fail; known ones do not), so that brownfield can improve progressively.
14. As an engenheiro DE, I want point waivers with owner + expiry, so that exceptions are explicit and time-bounded.
15. As an engenheiro DE, I want `/validar` to run data-check only when DE marker/profile exists, so that non-DE projects are not blocked.
16. As an engenheiro DE, I want CLI `explain <rule_id>` (SHOULD), so that failures are actionable without reading the whole YAML.
17. As an engenheiro DE, I want report in json and markdown (SHOULD), so that humans and machines can consume findings.
18. As CI do filho, I want `compare` against committed baseline, so that only regressions fail the gate.

### Segurança / SI (c+d)

19. As a responsável por SI, I want Universal checks for secrets and destructive ops with gate, so that prod risk (d) is surfaced statically.
20. As a responsável por SI, I want static detection of PII patterns in logs/code paths where feasible, so that LGPD expectations (c) start at the kernel.
21. As a responsável por SI, I want RO sql-capacity reports without dumping sensitive file contents, so that findings stay path/rule-id focused.

### Aceite testável (DoD Ship 1 — mapeado às stories)

| # | Critério | Evidência |
|---|---|---|
| AC1 | `data-engineering.yaml` existe na raiz e carrega com `version` + perfil `spark-yarn-airflow` | teste de contrato / loader |
| AC2 | CLI `validate` no example → **PASS A+B** | pytest + comando |
| AC3 | Pacote C no example → skip **ou** PASS se DAG presente | pytest |
| AC4 | `baseline` + `compare` demonstram ratchet (finding novo falha; baselineado não) | teste unitário/integração |
| AC5 | Waiver pontual exige owner + expiry; sem isso não silencia blocker | teste |
| AC6 | Relatório RO sql-capacity gerado (json e/ou md) **sem** escrita no repo alvo | artefato no canônico/CI + assert RO |
| AC7 | Path sql-capacity ausente → soft-fail documentado; validate do example continua verde | teste / doc de job |
| AC8 | Install pacote mínimo (fixture) cria `.harness/data-check/` + CLI utilizável; **não** copia 10 agents | teste install / dry-run |
| AC9 | `/validar` sem marker DE → não invoca data-check; com marker → invoca | teste condicional |
| AC10 | Espelho `.claude`/`.cursor` nas promoções deste ship | checklist / diff simétrico |
| AC11 | Nenhuma escrita em sql-capacity; nenhum agent/skill/KB DE nova neste ship | revisão + DoD |

---

## Implementation Decisions

Referência às **13 decisões do grill** (preservadas):

| # | Decisão | Escolha neste PRD |
|---|---|---|
| 1 | Escopo MVP | Universal + um perfil piloto |
| 2 | Perfil piloto | `spark-yarn-airflow` |
| 3 | Checks | A+B blockers; C Airflow condicional |
| 4 | Alvos | Greenfield no canônico + brownfield PRD RO |
| 5 | Brownfield path | sql-capacity — **somente leitura** |
| 6 | Baseline | ratchet + waiver pontual (owner + expiry) |
| 7 | Install | pacote mínimo verificável (**sem** 10 agents) |
| 8 | Scaffold | `examples/spark-yarn-airflow-min/` (fora do install auto) |
| 9 | Gate | CLI sempre + `/validar` condicional |
| 10 | Onde vive baseline | no filho via install; sql-capacity sem baseline gravada |
| 11 | Path filho | `.harness/data-check/` |
| 12 | Norma | `data-engineering.yaml` na raiz |
| 13 | DoD | YAML + CLI + example A+B + RO report + install mínimo + `/validar` + testes |

### Detalhe dos pacotes de check (decisão 3)

| Pacote | Conteúdo | Severidade | Aplicabilidade |
|---|---|---|---|
| **A** | secrets; destrutivo com gate; layout mínimo (`config/`, `pipelines/` ou `src/jobs/`, `tests/`); `run_id`/logging declarado; owner declarado | blocker | Universal |
| **B** | camadas medalhão/landing→processed; ban `select *` em transform; contrato de dados mínimo versionado | blocker | perfil `spark-yarn-airflow` |
| **C** | tags DAG; pré→carga→pós; spark-submit via `config/spark.conf` | condicional | só se Airflow/DAG detectado |

### Módulos / superfícies (sem paths rígidos demais)

- **Contrato YAML** na raiz + loader/tests no padrão de `config/git_hygiene/` (schema, version semver documental: MINOR aditivo; MAJOR remoção/renome de IDs ou layout incompatível).
- **Pacote Python da CLI** sob `config/` ou `scripts/` (nome acordado na implementação, ex. `canonical_data_check`): subcomandos `validate`, `baseline`, `compare`, `report`; SHOULD `explain`.
- **Example greenfield** `examples/spark-yarn-airflow-min/` — layout mínimo que satisfaz A+B.
- **`install-harness` / `stack_map`**: categoria/perfil DE mínimo — norma subset + CLI + rule pipeline apontando ao YAML + KB pipeline + seed `.harness/data-check/`; **não** propagar 10 agents.
- **`/validar`**: extensão condicional (marker/perfil DE).
- **Rule `pipeline`**: atualizar para referenciar IDs do YAML como fonte normativa; **não** recriar agents.
- **Job/artefato RO**: relatório do sql-capacity emitido no lado do canônico/CI.

### Exit codes `[inferido]`

- `0` — pass (ou somente warnings/recomendadas).
- `≠0` — blockers novos vs baseline, ou erro de execução.
- Mensagens: `rule_id` + path; sem dump de conteúdo sensível.

### SLA `[inferido]`

- Validate A+B no example: ≤ 60s.
- Relatório RO sql-capacity: ≤ 5 min; path ausente = soft-fail.

### Sketch adversarial

Sequência e superfície CLI alinhadas ao sketch (§3 ordem; §11 comandos `validate` / `baseline` / `compare` / `report` / `explain`). Evidências dos 4 repos informam os checks A/B/C, mas o ship não reimplementa Databricks (Loop 2).

---

## Testing Decisions

**Bom teste:** comportamento externo observável (exit code, findings por `rule_id`, artefatos gerados, ausência de escrita no sql-capacity) — não detalhes internos de parsers.

**Seams preferidos (mais altos primeiro):**

1. CLI como processo — `validate` / `compare` / `baseline` / `report` sobre o example e fixtures.
2. Loader do contrato — YAML inválido rejeitado; versão/perfil carregados.
3. Fixture de projeto-filho — install mínimo cria `.harness/data-check/` e CLI invocável.
4. Condicional `/validar` — com/sem marker.
5. Assert RO — após relatório sql-capacity, working tree do alvo inalterada (ou path ausente → soft-fail).

**Prior art:** `tests/git_hygiene/` (contrato + fixtures + adapter) — espelhar estrutura para DE.

**Cobertura mínima Ship 1:** contrato YAML; A+B PASS no example; C skip/PASS; ratchet; waiver schema; soft-fail path; install fixture; `/validar` condicional.

---

## Out of Scope

**Explicitamente fora do Loop 1 / Ship 1:**

- Perfis Databricks (`sdp-medallion`, `dlt-legacy`), SDP/DLT/DAB/UC, quarentena DLT, schema rescue → **Loop 2**
- Skills P0 DE, novos/reescritos agents DE, KBs “boas práticas” extras, propagar 10 agents + 7 commands → **Loop 3**
- `install-harness --scaffold` (bootstrap de projeto novo)
- Escrever/commitar qualquer arquivo em `data-sql-capacity-evolution-prd`
- Full enforcement sem baseline em brownfield remoto (sql-capacity neste ship = relatório RO apenas)
- Pager/RBAC externo; store central de auditoria da CLI
- Segundo framework de checks paralelo ao YAML

---

## SI Considerations

Nível **c + d** (de `00-ideia.md`):

| Tema | Implicação no Ship 1 |
|---|---|
| **c) PII / LGPD** | Canônico não processa PII de negócio. Checks estáticos para secrets e padrões de PII em logs/código. Relatórios: paths + rule IDs; sem dumps sensíveis. Filhos com PII: template CLAUDE `[AVISO_LGPD]` / `rules/pii.md` permanece orientação (enforcement profundo pode evoluir). |
| **d) Produção / destrutivo** | Check Universal A: operações destrutivas com gate; deny list alinhada a `seguranca`; ADR antes de DDL/DML destrutivo em prod (já rule transversal). |
| **sql-capacity** | Somente inspeção estática RO; não executar jobs; não ler datasets produtivos. |
| **Secrets** | Nunca em código versionado; check A detecta padrões; `.env` permanece ignored. |

Impacto em SI/LGPD de ADRs futuros deste kernel: qualquer check que toque paths com possível PII deve documentar minimização no ADR.

---

## Further Notes

### Roadmap (futuro — não escopo deste ship)

| Loop | Foco |
|---|---|
| **1 (este PRD)** | Kernel `spark-yarn-airflow` — YAML + CLI + baseline/waiver + example + install mínimo + `/validar` + testes + RO report |
| **2** | Databricks (mesmo YAML + CLI; perfis cloud) |
| **3** | Skills + agents + KBs DE amarrados a IDs; propagação install ampliada **após** kernel estável |

### Invariantes

- Produto = framework; zero pipeline de negócio no canônico.
- Não criar agents DE novos até o kernel existir.
- Espelho `.claude` ↔ `.cursor`.
- Install sem CLI = falsa conformidade = anti-DoD.
- `git fetch` 403 neste ambiente — sync remoto não confirmado; commit/push só com acordo.

### Itens `[inferido]` contestáveis

SLA 60s/5min; owner = mantenedor canônico; semver YAML; soft-fail path ausente; exit codes; concurrency last-write-wins no baseline do filho.

### Próximo passo do fluxo harness-design

1. (Opcional) adversarial-judge sobre este `02-prd.md`.
2. Harness Plan de **evolução do canônico** (não greenfield de app) → `03-harness.md`.
3. `/to-tasks` para fatiar implementação.
