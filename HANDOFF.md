# HANDOFF — Agent Harness Canônico

> Ponto de continuidade da sessão. Atualizado em 2026-10-13.

## Estado atual

| Item | Valor |
|---|---|
| Branch | `main` (protegida: PR obrigatório, sem force-push) |
| Repositório | público — https://github.com/jotap-rocha/agent-harness (MIT) |
| PRs mergeados | #1 hooks (pre-commit rápido, +x), #2 estrutura (`docs/manuais`, `docs/cheatsheets`, `docs/rascunhos`) |
| Testes | 24 falhas pré-existentes no Windows (instalador / evidence-gate / fluxo install); nenhuma nova |

## Entregue recentemente

1. Hooks `.githooks/*` mais rápidos e executáveis; testes leem o modo no índice git
2. `.github/pull_request_template.md`, `.gitattributes`, `LICENSE`
3. Raiz enxuta; guias em `docs/manuais/`; mapa em `README.md` e `config/README.md`
4. Instalador ignora `docs/rascunhos` e instala guias em `docs/manuais/` nos filhos

## Pendências fluxo live (próximos loops)

- Hook automático Cursor `Task(...)`
- Dogfood/backfill `silver-checklist-odcs/events.jsonl`
- ADR 005 addendum Opção C (via `/new-adr`, não editar ADR existente)
- Emits reais no próximo SDD build (agora com `--print-event-id` utilizável)

## Referências

- `.claude/dev/tasks/PROMPT_FLUXO_EMIT_RUNTIME.md`
- `docs/cheatsheets/fluxo-events-cheatsheet.md`
- `config/fluxo_events/cli.py`
