# Hooks dual runtime

**Status:** done  
**Blocked by:** tasks/policies-anti-destrutivas/43-bypass-fail-modes.md, tasks/policies-anti-destrutivas/45-generate-dual-artifacts.md

## What to build

Adapters finos: Claude PreToolUse e Cursor `beforeShellExecution` chamam o guard
compartilhado. Fixtures stdin JSON provam deny / ask / allow / bypass nos dois
contratos de I/O. Espelho de scripts `.claude/hooks/` ↔ `.cursor/hooks/` conforme
invariante.

## Acceptance criteria

- [x] Adapter Claude: deny-hard → bloqueio (exit/deny) — tested by: pytest fixture stdin Claude
- [x] Adapter Cursor: deny-hard → `permission: deny` — tested by: pytest fixture stdin Cursor
- [x] Ask nos dois lados → ask (não allow silencioso) — tested by: pytest adapters
- [x] Bypass env respeitado nos dois adapters — tested by: pytest + env
- [x] Scripts/hooks versionados sem divergência Claude↔Cursor de política — tested by: pytest ou diff de generate

## Notes

Cursor: `.cursor/hooks.json` + `beforeShellExecution`. Claude: PreToolUse em
settings + script sob hooks/. E2E IDE real = dogfood manual (fora do CI).

## Notes (fechamento)
Ressalvas revisor: Claude ask=exit0 (UI assimétrica vs Cursor); hooks dependem de cwd=raiz.

