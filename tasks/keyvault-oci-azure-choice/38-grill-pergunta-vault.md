# Grill pergunta vault

**Status:** done  
**Blocked by:** none

## What to build

Tornar a pergunta OCI vs Azure **obrigatória** no fluxo grill/define quando o projeto
usa key vault / secrets cloud: default por stack (Databricks/Azure→Azure; sinal OCI→OCI;
ambíguo→sem default) + **sempre** confirmação humana. Escopo só grill/define (não
install, não commands DE).

## Acceptance criteria

- [x] Checklist/prompt em harness-define (e grill-me se aplicável) inclui pergunta vault — no test — diff agents/skills; fixture de prompt se já existir padrão
- [x] Defaults documentados: Azure host→Azure; OCI→OCI; senão forçar escolha — no test — texto do checklist
- [x] Confirmação humana exigida mesmo com default — no test — texto explícito no agent/skill
- [x] Espelho `.claude`↔`.cursor` dos arquivos tocados — no test — checklist simétrica

## Notes

Não adicionar pergunta em `install-harness` (B1).
Arquivos: `harness-define.md`, `grill-me/SKILL.md` (+ espelho).
Commit pendente de acordo explícito.
