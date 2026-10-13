# Key Vault OCI vs Azure — escolha e artefatos no canônico

Slug: `keyvault-oci-azure-choice`  
Iniciado em: 2026-08-11  
Branch: `feat/oci-vault-harness` @ `2ba1ef9` (master)

## SI Assessment: Nível a + b

- a) Framework/docs sem dataset de produto
- b) Domínio de secrets/credenciais (nunca logar valor; placeholders em examples)

## Tipo: b + c + d (pipelines local/cloud + análise) — entrega = evolução do harness

## Fase atual: 5 — Todas as tasks concluídas, pronto para ship

## Checklist

- [x] 0. Ideia + SI assessment (2026-08-11)
- [x] 0b. Codebase-explorer canônico + referência PRD (2026-08-11)
- [x] 1. Grill concluído (2026-08-11)
- [x] 2. PRD gerado (2026-08-11) — `02-prd.md` (+ espelho `.cursor/`)
- [x] 2b. Adversarial judge no PRD — **(b)** pulado (2026-08-11)
- [x] 3. Harness montado (/harness-architect) (2026-08-11) — plano em `03-harness.md` (código no build)
- [x] 4. Tasks criadas (2026-08-11) — `tasks/33`–`40` (+ `tasks/README.md`)
- [x] 5. Implementação concluída (2026-08-12) — tasks 33–40 done; gate verde; commit pendente de acordo
- [ ] 6. Ship / retrospectiva

## Acordos (brainstorm + grill + architect)

| Decisão | Escolha |
|---|---|
| Branch | `feat/oci-vault-harness` |
| Slug | `keyvault-oci-azure-choice` |
| Pergunta OCI vs Azure | obrigatória + default por stack + confirmação |
| Skill | `cloud-secrets` (dual) |
| KBs | `oci-vault` + `azure-keyvault` |
| Agent no canônico | **não** |
| Examples | `examples/keyvault-oci-min/` + `examples/keyvault-azure-min/` (fora stack_map) |
| Scaffold | `config/templates/cloud-secrets/` |
| Checks | pacote E `keyvault-cloud` (DE-E*); DE-A001 permanece |
| Marker | `secret_store: oci\|azure\|multi` |
| Install | categoria **nova** `cloud_secrets` no `stack_map` — não sempre com `pipeline_dados` |
| ADR | `docs/adr/002-pacote-e-keyvault-cloud-dual-install.md` |
| Adversarial judge (grill) | **(b)** pulado — sem `01b-judge.md` |
| Adversarial judge (PRD) | **(b)** pulado — sem `02b-judge.md` |

## Soft-blocks

- `git fetch` Azure pode falhar (403) — branch a partir de master local; sem inventar sync.
- `.cursor/projetos` exige FS writable (bind mount RO no root `.cursor` em alguns hosts).
- Sem commit/push sem acordo explícito.

## Próximo passo

Diga **harness-ship** para fechar o projeto com scorecard **e sincronizar o contexto**
(após commit com acordo). Delivery record em `metrics/entregas.jsonl` só após commit.
