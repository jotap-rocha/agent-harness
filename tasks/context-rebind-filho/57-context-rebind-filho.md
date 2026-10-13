# Task 57 — context-rebind-filho

**Status:** done  
**Blocked by:** none

## What to build

1. Foundation do install gera `README.md` mínimo do projeto-filho (nome + stub + ponte `/make-readme`).
2. Banner anti-canônico no topo de `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md` e `README.md` gerados.
3. Passo **CONTEXT_REBIND** no 1º round (brainstorm / architect / install pós-install): soft-block se contexto ainda for placeholder ou assinatura do canônico.
4. Pytest: destino pós-generate sem título canônico; banner + README presentes. KEEP se já customizado.

## Acceptance criteria

- [x] `stack_map.json` (foundation) declara `README.md` kind `generate` (espelho `.claude`/`.cursor`)
- [x] `generate_content` emite README + banner anti-canônico nos 4 artefatos
- [x] Agents/skills de entrada documentam CONTEXT_REBIND (soft-block) + espelho dual-tree
- [x] `tests/install_harness/test_context_rebind.py` verde: sem título canônico; banner; README; KEEP

## Notes

- Sem commit/push nesta fatia (acordo explícito pendente).
- Fetch 403 no preflight = soft-block didático (não bloqueia implementação local).
- Revisor: aprovado com ressalvas (marcadores placeholder afinados; schema README; helpers soft; filecmp dual-tree no teste).
- Gate: pytest 6 passed; ruff ok; mypy pré-existente em signals (não introduzido).
- Evidence: `.claude/projetos/context-rebind-filho/evidencias/tasks/57.yaml`
