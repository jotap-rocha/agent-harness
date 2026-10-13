# Docs ADR fluxo-live

**Status:** done  
**Blocked by:** tasks/visao-grafica-fluxo-agentes/58-contrato-yaml-loader.md, tasks/visao-grafica-fluxo-agentes/59-cli-emit-jsonl.md, tasks/visao-grafica-fluxo-agentes/60-render-live-html.md, tasks/visao-grafica-fluxo-agentes/61-rotate-truncate-ship.md

## What to build

Documentar o kernel fluxo-events: cheatsheet de 1 página, ADR, command `/fluxo-live`
(SHOULD), honesty §1.3 e ortogonalidade vs evidence-gate / agent-policies / STATUS /
scorecard. Waivers humanos onde critério for só review (sem teste mapeável).

## Acceptance criteria

- [ ] Cheatsheet `docs/fluxo-events-cheatsheet.md` cobre CLI, cap/truncate, §1.3, ortogonalidade — tested by: review — no test — waiver humano
- [ ] ADR em `docs/adr/` registra kernel separado + fail-soft + foundation — tested by: review — no test — waiver humano
- [ ] Command `/fluxo-live` (+ espelho `.cursor/`) documenta emit/render/http.server opcional — tested by: file presence smoke / dual-tree
- [ ] Docs não unificam com evidence-gate nem agent-policies (AC13) — tested by: review — no test — waiver humano
- [ ] Honesty §1.3: telemetria local ≠ fidelidade perfeita (AC18) — tested by: review — no test — waiver humano

## Notes

AC PRD: AC13, AC18. Sem skill MUST nova; cheatsheet basta no MVP.
