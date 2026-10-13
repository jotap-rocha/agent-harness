# Policies Anti-Destrutivas

## Ideia

Evoluir o projeto canônico agent-harness-canonico-v2 com policies para evitar comandos
destrutivos — local Linux (ex.: `rm -rf`, `docker compose down -v`, volume prune), banco de
dados (DROP/TRUNCATE/DELETE destrutivo, dropdb, etc.), Databricks / cloud (workspace delete,
clusters delete e equivalentes UC/SQL), e outros alvos relevantes no ecossistema do harness
(git force/reset hard já parcialmente coberto).

Mecanismos pretendidos: `settings.json` → `permissions.deny` / `permissions.allow`, e hooks
(Claude/Cursor PreToolUse / PostToolUse / etc.).

Estado já existente (não reinventar do zero): deny parcial em `.claude/settings.json`; rule
transversal `seguranca` (confirmação humana + ADR para DDL em prod); kernel DE com finding
sobre destructive ops (`DE-A002`); githooks locais (`.githooks/`) para secrets — camada
diferente de Edit policies do agent runtime. Honestidade §1.3: sem Edit policies / branch
protection, nenhum gate impede de fato; `--no-verify` e clone sem hooks contornam.

## SI Assessment

Nível: d — banco de produção / risco de operações de escrita/deleção (ops destrutivas)

Implicações:
- Deny list extendida (e/ou hooks PreToolUse) para barrar ops destrutivas no runtime do agente
- ADR obrigatório antes de qualquer escrita/DDL destrutivo em produção
- Rule `seguranca` permanece como soft policy; enforcement mecânico via settings/hooks onde o runtime permitir
- Declarar limites honestos (§1.3): deny/hooks ≠ Edit policies server-side; bypass humano e clone sem hooks existem
- Sem `[AVISO_LGPD]` / `rules/pii.md` neste escopo (nível d, não c) — a menos que o grill descubra PII

## Tipo de Projeto

e — Evolução do harness canônico (Edit policies + hooks)

Stack prevista:
- Artefatos de framework: `.claude/settings.json` (permissions + hooks), espelho Cursor se aplicável
- Hooks PreToolUse (guard de comando) + PostToolUse/Stop existentes (lint/gate)
- Rules SI (`seguranca`) e eventualmente ADR + documentação §1.3
- Kernel DE `DE-A002` (estático, código versionado) — camada ortogonal ao runtime Bash
- Propagação via `/install-harness` (hoje gera `deny: []` nos filhos — gap a fechar no grill)
- Testes de conformidade do deny/hook (hoje inexistentes para runtime)

## Próximos passos

0. Repo já mapeado — ver `00b-codebase.md` antes do grill
1. Rode `/grill-me` para aprofundar a ideia (MVP de camadas, dual Claude↔Cursor, allow vs deny, bypass, taxonomia, install, testes)
2. Ao terminar, use `harness-define` para estruturar os requisitos
3. Depois: `harness-design` → PRD + harness-architect (flavor: evolução do canônico)
