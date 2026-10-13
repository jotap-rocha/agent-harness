# Boas práticas DE no canônico — Decisões de Harness (Loop 1)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-06  
Branch: `feat/de-boas-praticas-canonico`  
Fontes: `02-prd.md`, `01-grill.md`, `00b-codebase.md`, skill `harness-architect`  
Modo: **evolução do framework canônico** — NÃO greenfield de app/pipeline de domínio  
Judge PRD: **b)** pulado

> **Estado deste artefato:** Harness Plan **aprovado**. Tasks `09`–`16` criadas. Próximo: `harness-build`.

---

# Harness Plan — Kernel de conformidade DE (Loop 1 / Ship 1)

## Inferências confirmadas (PRD — sem lacunas bloqueantes)

| Cluster | Inferido do PRD/grill |
|---|---|
| Produto | Framework canônico; kernel normativo executável |
| Perfil piloto | `spark-yarn-airflow` (Universal + 1 perfil) |
| Checks | A+B blockers; C Airflow condicional |
| Norma | `data-engineering.yaml` na raiz (padrão `git-hygiene.yaml`) |
| CLI | `canonical-data-check`: validate / baseline / compare / report (+ SHOULD explain) |
| Baseline | Ratchet + waiver (owner + expiry) em `.harness/data-check/` no filho |
| Install | Pacote mínimo verificável; **sem** 10 agents |
| Gate | `/validar` condicional a marker/perfil DE |
| SI | c+d; sql-capacity RO; secrets/PII estático |
| Agents novos | **Proibido** no Loop 1 (gate de redundância: 10 agents DE já existem; falta enforcement) |

Lacunas restantes são de implementação (nome exato do pacote Python, layout interno dos checks),
não de harness — resolvem-se em tasks/ADRs, não em entrevista adicional.

---

## Invariantes (sempre valem no Loop 1)

1. **Kernel antes de catálogo** — YAML + CLI + example + install mínimo + testes antes de agents/skills/KBs novas.
2. **Fonte normativa única** — IDs e severidades vivem em `data-engineering.yaml`; prose em `rules/pipeline` aponta para o YAML; não duplicar norma em KB.
3. **Espelho** `.claude/` ↔ `.cursor/` em toda promoção de commands/rules/skills tocadas.
4. **sql-capacity somente leitura** — relatório RO no canônico/CI; zero escrita no repo alvo.
5. **Falsa conformidade = anti-DoD** — install DE deve incluir CLI utilizável + seed `.harness/data-check/`.
6. **Sem novos agents/skills/KBs DE** neste ship.
7. **Git hygiene** — branch de trabalho; commit/push só com acordo; fetch 403 = soft-block didático.

---

## Mapa decisão → artefato → pilar

> Adaptação: “artefato” aqui é caminho no **canônico** (framework), não um `.claude/` greenfield de produto.

| Decisão | Artefato no canônico | Pilar | Quem lê |
|---|---|---|---|
| Norma versionada Universal + perfil `spark-yarn-airflow` | `data-engineering.yaml` (raiz) | Estado / validação | CLI, CI, agents futuros (L3), humanos |
| Loader + contrato tipado (espelho git-hygiene) | `config/data_engineering/` (`yaml_loader`, `contract`, `__init__`) | Ferramentas / validação | pytest, CLI |
| CLI enforce (validate / baseline / compare / report) | Pacote `canonical_data_check` (sob `config/` ou `scripts/`; entrypoint CLI) | Ferramentas / validação | Dev, CI, `/validar`, install |
| SHOULD explain + report json\|md | Mesmo pacote CLI | Ferramentas | Engenheiro DE |
| Checks A (Universal) + B (perfil) blockers; C condicional | Módulos de check no pacote CLI + IDs no YAML | Validação | CI / compare |
| Baseline ratchet + waiver owner/expiry | Schema template no canônico; runtime em `.harness/data-check/` do filho | Estado / validação | CLI compare, git do filho |
| Example greenfield PASS A+B | `examples/spark-yarn-airflow-min/` | Validação / execução | pytest, DoD, demos |
| Install pacote mínimo (sem 10 agents) | `stack_map.json` categoria `pipeline_dados` ampliada + templates install (norma subset, CLI, rule, KB pipeline, seed `.harness/data-check/`) | Ferramentas / execução | `install-harness`, projetos-filho |
| Path no filho | `.harness/data-check/project_profile.yaml` + `baseline.json` (+ waivers) | Estado | CLI, `/validar` |
| Gate condicional | `.claude/commands/validar.md` + espelho `.cursor/` — invoca data-check só se marker/perfil DE | Validação | Agente / humano no filho e no canônico (example) |
| Prose aponta para norma | `.claude/rules/pipeline.md` + `.cursor/rules/pipeline.mdc` — referência a IDs/`data-engineering.yaml` | Estado | Agentes ao tocar pipeline |
| Testes kernel | `tests/data_engineering/` (contrato YAML + CLI no example + ratchet/waiver + soft-fail path) | Validação | CI canônico |
| Relatório RO brownfield | Artefato/job no canônico (ex. `reports/` ou output CI) apontando path sql-capacity RO; soft-fail se ausente | Validação | Mantenedor / CI |
| Docs mínimas do example | README curto em `examples/spark-yarn-airflow-min/` (COULD) | Estado | Humanos |
| Inventário CLAUDE/AGENTS | Atualizar contagens/tabelas só se mudarem artefatos espelhados (commands/rules) | Estado | Agentes do canônico |

### Pilares cobertos

| Pilar | Como o Loop 1 cobre |
|---|---|
| **Estado/memória** | YAML normativo; baseline/perfil no filho; rules apontando IDs; STATUS/projetos |
| **Ferramentas** | CLI + loader; install propagando pacote mínimo |
| **Execução** | Example como alvo de validate; `/validar` condicional; CI do canônico |
| **Validação** | A+B(+C); ratchet; testes; RO report; exit codes |

---

## O que NÃO entra agora (e por quê)

| Item | Loop | Por quê |
|---|---|---|
| Perfis Databricks / SDP / DLT / DAB / UC | **2** | Perfil piloto acordado = spark-yarn-airflow |
| Quarentena DLT, schema rescue cloud | **2** | Dependem do perfil cloud |
| Novos agents DE, skills P0 DE, KBs medalhão duplicadas | **3** | Kernel deve provar conformidade antes |
| Propagar 10 agents + 7 commands DE no install | **3** | Evitar falsa conformidade e catálogo sem checks |
| `install-harness --scaffold` | depois | Fora do MoSCoW Ship 1 |
| Escrever no repo sql-capacity | nunca neste ship | RO explícito (SI + grill) |
| Revisor lanes PASS/FAIL/WAIVED amarradas a rule_id | **3** (ou 1.1+) | SHOULD futuro; não bloqueia DoD Ship 1 |
| Criar agents `pipeline-architect` / `schema-guardian` novos | — | Já existem; Loop 1 não gera agents de produto |
| Implementação em massa neste passo architect | — | Architect exige “de acordo” no plan antes de gerar |

---

## O que foi “gerado” pelo /harness-architect (neste passo)

Neste turno o architect **só documenta o plan** (Ralph mínimo para evolução do canônico).

### Agentes criados

- **Nenhum.** Gate de redundância: 10 agents DE já cobrem o domínio; criar mais sem kernel viola `00b` + sketch §3.

### Rules criadas/adaptadas (planejado — pós-aprovação)

- **Adaptar** `rules/pipeline.md` (+ espelho `.mdc`): declarar que a fonte normativa de IDs/severidade é `data-engineering.yaml`; prose Medallion/contratos permanece, mas enforcement = CLI.
- **Não** criar `schema-evolution.md` / `observability.md` novas só por reflexo de pipeline greenfield.

### KBs criados

- **Nenhum novo.** Continua propagando `kb/pipeline` existente via install (já no `stack_map`).

### Skills criadas

- **Nenhuma skill P0 DE nova.** Evoluir `install-harness` (stack_map + comportamento de cópia/seed) e o command `/validar`.

### Settings.json

- Sem mudança obrigatória no Loop 1; gate hard permanece ruff/mypy/pytest + data-check condicional via `/validar` (não exige hook novo no ship mínimo).

### Artefatos de código/framework (planejados — implementação após “de acordo”)

1. `data-engineering.yaml`
2. `config/data_engineering/` (loader/contract)
3. CLI `canonical-data-check`
4. `examples/spark-yarn-airflow-min/`
5. `tests/data_engineering/`
6. Ampliação `pipeline_dados` em `stack_map.json` + templates seed `.harness/data-check/`
7. Extensão `/validar` (condicional)
8. Ajuste `rules/pipeline` (+ espelho)
9. Job/script de relatório RO sql-capacity

---

## Ordem de implementação sugerida (para `/to-tasks`)

Alinhada ao sketch adversarial (não invertível):

1. Contrato `data-engineering.yaml` + loader/tests  
2. CLI validate (checks A+B+C skip)  
3. Example greenfield PASS A+B  
4. baseline / compare / waiver + testes ratchet  
5. report (+ SHOULD explain)  
6. Relatório RO sql-capacity (soft-fail path)  
7. install-harness pacote mínimo + fixture teste  
8. `/validar` condicional + ajuste `rules/pipeline` + espelhos  
9. Atualizar `CLAUDE.md`/`AGENTS.md` se contagens/comandos mudarem · `/sync-context` no fechamento

**Materializado em:** `tasks/09`–`16` (ver `tasks/README.md`).

---

## Decisões contestáveis (ADRs futuros sugeridos — não criar agora)

| Tema | Sugestão | Por quê ADR |
|---|---|---|
| Nome/local do pacote Python da CLI (`config/data_engineering` vs `scripts/`) | Preferir espelhar `config/git_hygiene/` | Contestado por layout de packaging |
| Semver do YAML (MINOR/MAJOR) | Como no PRD `[inferido]` | Quebra consumidores install |
| Marker exato do `/validar` (arquivo perfil vs keyword) | Preferir existência de `.harness/data-check/project_profile.yaml` | Afeta falsa positiva/negativa |
| Soft-fail sql-capacity | Exit 0 com aviso vs exit dedicado | Política de CI |
| Waiver store (arquivo único vs lista no baseline) | Lista com owner+expiry | Auditoria SI |

---

## Drift detectado (pré-implementação)

| Situação atual | Gap vs plan |
|---|---|
| `stack_map` `pipeline_dados` só copia `kb/pipeline` + `rules/pipeline` | Sem CLI, sem `.harness/data-check/`, sem norma YAML |
| `/validar` = ruff+mypy+pytest genérico | Sem lane condicional DE |
| `rules/pipeline` = prosa Medallion | Sem ponte para IDs executáveis |
| Sem `data-engineering.yaml` / CLI / example | Kernel ausente (gap central do `00b`) |

---

## Aprovação necessária

**Status:** Harness Plan **aprovado** pelo usuário (2026-08-06). Tasks criadas. Próximo: `harness-build`.

---

## Próximo passo

1. ~~Aguardar aprovação explícita deste plan.~~ **Aprovado.**  
2. ~~Rodar `/to-tasks`.~~ **Feito** — `tasks/09`–`16` + `tasks/README.md`.  
3. `harness-build` / `implement task 09` para implementar o kernel.  
4. **Não** abrir Loop 2/3 até DoD Loop 1 verde.
