# Boas práticas DE no canônico — Decisões de Harness (Loop 2)

Slug: `engenharia-de-dados-boas-praticas-canonico`  
Data: 2026-08-07  
Branch: `feat/de-databricks-loop2`  
Fontes: `08-loop2-prd.md`, `07-loop2-grill.md`, `00c-codebase-loop2.md`, `03-harness.md` (Loop 1)  
Modo: **evolução do framework canônico** — estende kernel Loop 1; NÃO greenfield de app  
Judge PRD: **b)** pulado

> **Estado deste artefato:** Harness Plan **aprovado** (2026-08-07). Tasks `17`–`24` criadas. Próximo: `harness-build`.

---

# Harness Plan — Kernel DE Databricks (Loop 2 / Ship 2)

## Inferências confirmadas (PRD — sem lacunas bloqueantes)

| Cluster | Inferido do PRD/grill |
|---|---|
| Produto | Mesmo kernel; perfis Databricks no YAML + pacote D |
| Perfis | `databricks-sdp-medallion`, `databricks-dlt-legacy`, `databricks-multi` |
| Checks | Sempre **A + D**; D condicional por sinal SDP/DLT; B/C intactos (spark-yarn) |
| Examples | Dois greenfield: `databricks-sdp-min`, `databricks-dlt-min` |
| Seleção perfil | Auto-detect + override `project_profile.yaml`; multi = união |
| Baseline | + `profiles[]` (compat `profile` legado) |
| `/validar` | Marker **ou** auto-detect Databricks |
| Install | `pipeline_dados` **inalterado** |
| Agents novos | **Proibido** (Loop 3) |
| SI | c+d; checks UC/DAB só filesystem; sem credenciais live |

Lacunas restantes = globs exatos de auto-detect e IDs finais DE-Dnnn — fecham em tasks/testes, não em nova entrevista.

---

## Invariantes (sempre valem no Loop 2)

1. **Estender, não duplicar** — mesma norma + mesma CLI; sem segundo framework.
2. **A sempre com cloud** — secrets/destrutivo continuam blockers em trees Databricks.
3. **Kernel antes de catálogo** — sem agents/skills/KBs DE novas.
4. **Espelho** `.claude/` ↔ `.cursor/` se `/validar` ou `rules/pipeline` mudarem.
5. **stack_map `pipeline_dados` congelado** — sem keywords Databricks neste ship.
6. **Sem live Databricks API** no CI do canônico.
7. **Git hygiene** — branch `feat/de-databricks-loop2`; commit/push só com acordo.

---

## Mapa decisão → artefato → pilar

| Decisão | Artefato no canônico | Pilar | Quem lê |
|---|---|---|---|
| Perfis Databricks + pacote D no YAML | `data-engineering.yaml` (estender) | Estado / validação | CLI, testes, humanos |
| Contrato tipado | `config/data_engineering/contract.py` (se schema exigir) | Ferramentas | loader, pytest |
| Registry/dispatch pacotes | `config/canonical_data_check/engine.py` + `checks/` | Validação | validate |
| Checks D (`databricks-cloud`) | `checks/package_d.py` (ou equivalente) + IDs no YAML | Validação | CI / examples |
| Auto-detect DAB/DLT/SDP | módulo detect (ex. `detect_databricks.py`) + `de_marker` | Validação / gate | `/validar`, CLI |
| Profile resolve + multi | engine / profile resolver | Validação | validate, baseline |
| Baseline `profiles[]` | `baseline.py` + `SCHEMA.md` + templates seed | Estado | compare, filhos |
| Example SDP | `examples/databricks-sdp-min/` | Validação / execução | pytest, DoD |
| Example DLT | `examples/databricks-dlt-min/` | Validação / execução | pytest, DoD |
| `/validar` trigger ampliado | `.claude/commands/validar.md` (+ espelho) + `de_marker.py` | Validação | agentes/humanos |
| Prose pipeline (se necessário) | `rules/pipeline` — mencionar perfis D / IDs | Estado | agentes |
| Testes Loop 2 | `tests/data_engineering/` (novos + regressão Loop 1) | Validação | CI |
| Docs examples | README curto em cada example | Estado | humanos |
| Sync contexto no ship | `CLAUDE.md` / `CONTEXT.md` / `AGENTS.md` | Estado | agentes |

### Pilares cobertos

| Pilar | Como o Loop 2 cobre |
|---|---|
| **Estado/memória** | YAML estendido; baseline `profiles[]`; rules/CONTEXT |
| **Ferramentas** | CLI + detect + registry |
| **Execução** | Dois examples; `/validar` ampliado |
| **Validação** | A+D; multi; testes; exit codes |

---

## O que NÃO entra agora (e por quê)

| Item | Loop | Por quê |
|---|---|---|
| Keywords/categoria `pipeline_dados` Databricks | depois / 2.1 | Acordo grill: install inalterado |
| Brownfield RO Databricks | fora Ship 2 | Grill: só greenfield |
| Live UC / workspace API | fora | SI + CI sem secrets |
| Novos agents/skills/KBs DE | **3** | Kernel cloud primeiro |
| Propagar 10 agents no install | **3** | Falsa conformidade |
| Reescrever pacote B para “medallion genérico” | fora | Grill: pacote D separado |

---

## O que foi “gerado” pelo /harness-architect (neste passo)

Só o **plan** (Ralph mínimo). Nenhuma geração de agents/KBs.

### Agentes / Skills / KBs

- **Nenhum novo.**

### Rules / commands (planejado pós-aprovação)

- Adaptar `/validar` (+ espelho) para trigger marker **ou** auto-detect.
- Opcional: nota em `rules/pipeline` sobre perfis `databricks-*` e pacote D.

### Artefatos de código (planejados)

1. Extensão `data-engineering.yaml` (perfis + D)
2. Registry/dispatch no engine + `package_d` (checks condicionais)
3. Auto-detect + resolve profile (incl. `databricks-multi`)
4. Baseline `profiles[]` + SCHEMA/templates
5. `examples/databricks-sdp-min/` + `examples/databricks-dlt-min/`
6. Testes + `/validar` + espelhos
7. Sync contexto no ship Loop 2

---

## Ordem de implementação sugerida (para `/to-tasks`)

1. YAML: perfis Databricks + pacote D (IDs/regras) + testes contrato  
2. Engine registry/dispatch + stub/package D  
3. Auto-detect + profile resolve (override + multi)  
4. Checks D bloqueantes (DAB, SDP, DLT quarantine, schema rescue, UC FS)  
5. Baseline `profiles[]` + compat legado + testes ratchet  
6. Example `databricks-sdp-min` PASS  
7. Example `databricks-dlt-min` PASS  
8. `/validar` + `de_marker` ampliado + testes condicional  
9. Freeze assert `pipeline_dados` inalterado + regressão Loop 1 example  
10. Ship: sync-context + retro Loop 2  

**Numeração sugerida de tasks:** `17`–`N` (continuar após 16).

---

## Decisões contestáveis (ADRs futuros sugeridos — não criar agora)

| Tema | Sugestão | Por quê ADR |
|---|---|---|
| Semver YAML ao adicionar perfis/pacote D | MINOR se só aditivo | Consumidores install |
| Forma de `profiles[]` vs bump `version: 2` | Campo adicional + `profile` legado | Compat filhos Loop 1 |
| Globs canônicos de auto-detect | Lista versionada em código + testes | Falsos positivos |
| Nome módulo `package_d` vs `databricks_cloud` | Alinhar a A/B/C | Consistência |

---

## Drift detectado (pré-implementação)

| Situação atual (pós Loop 1) | Gap vs plan Loop 2 |
|---|---|
| Um perfil no YAML | Faltam 3 perfis Databricks + D |
| Engine A/B/C hardcoded | Sem registry para D |
| `de_marker` = existência arquivo | Sem auto-detect / read profile |
| Baseline `profile` singular | Sem `profiles[]` |
| Só example spark-yarn | Sem sdp-min / dlt-min |
| `/validar` só marker | Sem trigger por sinal Databricks |

---

## Aprovação necessária

**Status:** Harness Plan **aprovado** pelo usuário (2026-08-07). Tasks `17`–`24` criadas.

---

## Próximo passo

1. ~~Aguardar aprovação explícita deste plan.~~ **Aprovado.**  
2. ~~`/to-tasks`.~~ **Feito** — `tasks/17`–`24` + `tasks/README.md`.  
3. `harness-build` / `implement task 17`.  
4. **Não** abrir Loop 3 até DoD Loop 2 verde.
