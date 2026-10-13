# Loop 3 — Retrospectiva de Ship

Ship em: 2026-08-07  
Branch: `feat/de-agents-skills-loop3`

## Métricas de entrega (tasks 25–32)

| Métrica | Valor |
|---|---|
| Tasks entregues | 8 |
| Critérios de aceite atendidos | 100% (32/32) |
| Tentativas medianas até gate verde | 1–2 |
| Veredito do revisor: aprovado / ressalvas / bloqueado | 1 / 7 / 0 (após corrigir entregas 25–27) |
| Intervenções humanas | 0 mid-task |
| Taxa de autonomia | 100% |
| Gate final | pytest 205 · ruff OK · mypy 57 files OK |

## O que funcionou bem

- Kernel Loops 1–2 como âncora estável: amarras agentic só citaram IDs existentes.
- Espelho `.claude`↔`.cursor` disciplinado (agents, commands, KBs, skill, stack_map).
- Rebaseline consciente dos freezes Loop 2 (não “contornar” asserts).
- Skill `de-conformidade` + KB `databricks` fecharam o gap catálogo ↔ enforcement.

## O que melhorar

- Delivery records 25–27 esquecidos no lote intermediário — DoD exige append por task.
- Contagens CLAUDE/CONTEXT ficaram stale até o ship — sync-context deveria ser mid-loop após inventário mudar.
- Duplicação de inventário frozen em múltiplos testes (já anotado na task 32).

## Armadilhas encontradas

- Ampliar `pipeline_dados` sem reescrever `test_freeze_stackmap_regressao` / `test_install_pacote_minimo` = vermelho certo.
- Commit com literais de assignment de credencial em testes de example → pre-commit (usar `_secret_fixtures`).
- Fetch Azure 403 continua soft-block; ship/build rodaram com aviso + `origin/master` local.

## ADRs desta implementação

- Nenhum ADR novo (decisões contestáveis já no grill/PRD Loop 3; sem live API / sem write prod).

## Harness — o que aprendemos

- Freeze de inventário é feature: força rebaseline explícito quando o catálogo cresce.
- Agents DE sem ponte ao kernel eram “documentação que mente conformidade”.
- Install completo + seed KEEP coexistem: runtime do filho permanece protegido.
