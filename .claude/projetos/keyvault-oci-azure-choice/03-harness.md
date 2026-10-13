# Key Vault OCI vs Azure — Decisões de Harness

Slug: `keyvault-oci-azure-choice`  
Branch: `feat/oci-vault-harness`  
Data: 2026-08-11  
PRD: `02-prd.md`  
Judge: grill (b) + PRD (b) pulados  
Lacunas fechadas no architect: examples `keyvault-*-min`; install categoria vault (2b);
scaffold `config/templates/cloud-secrets/` (3b)

> Este ship **evolui o canônico** (framework). Não cria `.claude/` de produto-filho.
> Implementação dos artefatos abaixo fica para `/to-tasks` → `harness-build`.

## Invariantes (sempre valem)

- Entrega = evolução do framework; SI **a+b**
- Sem agent vault no canônico; skill `cloud-secrets` + KBs só
- Facade + map só IDs/URIs; sem SDK vault nos consumidores; sem live API no CI
- `DE-A001` permanece; pacote **E** adicional
- Examples fora do `stack_map`; espelho `.claude` ↔ `.cursor`
- Commit/push só com acordo explícito

## Mapa decisão → artefato → pilar

| Decisão | Artefato | Pilar | Quem lê |
|---|---|---|---|
| Pergunta OCI/Azure + default + confirm | `agents/workflow/harness-define.md` + `skills/grill-me` | execução | `/novo-projeto` |
| Playbook dual | `.claude/skills/cloud-secrets/` (+ `.cursor/`) | ferramentas | agente JIT |
| Domínio OCI | `.claude/kb/oci-vault/` (+ espelho) | estado | agente JIT |
| Domínio Azure | `.claude/kb/azure-keyvault/` (+ espelho) | estado | agente JIT |
| Norma DE-E* | `data-engineering.yaml` → `packages.E` | validação | loader + CI |
| Checks FS | `config/canonical_data_check/checks/package_e.py` + registry | validação | CLI |
| Marker + auto-detect + multi | `de_marker.py` + SCHEMA `templates/data-check/` | validação | `/validar` |
| Scaffold facade | `config/templates/cloud-secrets/` | ferramentas | examples + skill |
| Dogfood | `examples/keyvault-oci-min/`, `examples/keyvault-azure-min/` | validação | pytest |
| Install condicional | `stack_map.json` — **categoria nova** (flag vault / `secret_store`) → skill+KBs | ferramentas | install-harness |
| SI bridge | ponte curta em `rules/seguranca` (+ `.mdc`) | estado | agente + revisor |
| Remediação DE-E* | `de-conformidade` + remediations YAML | validação | pós-finding |
| Contagem/docs | `CLAUDE.md` / `AGENTS.md` no ship | estado | próximo agente |
| ADR | `docs/adr/` (pacote E + dual-cloud) na implementação | estado | humano + agent |

## O que o architect NÃO gera agora (fica para build)

Artefatos de código/docs de domínio listados acima — andaime real no `harness-build`
após `/to-tasks`. Este arquivo é o **contrato do plano**, não o dump dos arquivos.

### Agentes criados
- **Nenhum** agent vault no canônico (decisão 14 / gate redundância)

### Agents/skills a estender (build)
- `harness-define` + `grill-me` — pergunta obrigatória + default por stack + confirmação
- `cloud-secrets` (nova skill)
- `de-conformidade` — remediação `DE-E*`
- `install-harness` / `stack_map.json` — categoria vault condicional

### Rules
- Ponte curta em `seguranca` (nunca logar secret / placeholders) — sem `keyvault.md` nova

### KBs (a criar no build)
- `oci-vault` — lift padrões (auth dual, facade, map OCID, nunca logar)
- `azure-keyvault` — paridade conceitual (URI, credential chain, map)

### Kernel / examples (a criar no build)
- Pacote E `keyvault-cloud` (`DE-E001`–`E003` alvo)
- Marker `secret_store: oci|azure|multi`
- Scaffold `config/templates/cloud-secrets/`
- Examples `examples/keyvault-oci-min/` e `examples/keyvault-azure-min/`

## O que NÃO entra neste ship

- Agent `key-oci-expert` (canônico ou install)
- Live calls vault no CI
- Outros cofres (AWS/HashiCorp)
- Pergunta vault em install-harness / commands DE
- Install sempre via `pipeline_dados` (rejeitado — só categoria vault)
- Propagar examples via `stack_map`

## Decisões contestáveis (ADR na implementação)

1. Pacote **E** separado de A–D (wiring vault ≠ literal secret A001)
2. Skill dual única vs duas skills — dual `cloud-secrets` (grill)
3. Install por categoria vault (não acoplar a todo `pipeline_dados`)
4. Scaffold em `config/templates/cloud-secrets/` (não sob `canonical_data_check/templates/`)

## Soft-blocks

- `git fetch` Azure 403 — trabalho na branch local
- Working tree: artefatos untracked em `projetos/keyvault-oci-azure-choice/`
- Sem commit/push neste passo

## Próximo passo

1. `/to-tasks` — fatiar o PRD em tasks implementáveis (tracer bullets)
2. `harness-build` — implementar com `/validar` + `revisor-codigo`
3. Ao fechar: `/sync-context` + delivery record em `metrics/entregas.jsonl`
