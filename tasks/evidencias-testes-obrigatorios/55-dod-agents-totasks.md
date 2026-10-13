# DoD agents totasks

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/53-wiring-build-ship.md

## What to build

Atualizar DoD (`definicao-de-pronto`), `to-tasks` e `revisor-codigo`: critérios com
tested-by alinhados ao manifesto; DoD exige evidência mecânica; revisor soft
ortogonal (não substitui check). Espelhos `.md`/`.mdc` e agents.

## Acceptance criteria

- [x] DoD menciona evidence-gate / manifesto / evidencias_ref — no test — assert strings rule
- [x] to-tasks template/skill exige path de teste por critério (compatível manifesto) — no test — assert skill
- [x] revisor-codigo: soft ≠ hard; não valida exit do manifesto no lugar do CLI — no test — assert agent
- [x] Espelho `.claude`↔`.cursor` sem drift nos arquivos tocados — tested by: diff/parity test leve se houver

## Notes

Sem agent “evidence officer” novo.

Revisor: aprovado. Gate tentativas_ate_verde=1.
