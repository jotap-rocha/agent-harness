# Audit append only

**Status:** done  
**Blocked by:** tasks/evidencias-testes-obrigatorios/50-collect-run-logs.md

## What to build

Trilha `evidencias/audit.jsonl`: cada `collect` faz append de 1 JSON (timestamp,
task, criterion, exit_code, paths). Prova atual continua LWW; histórico não é
apagado pelo re-collect.

## Acceptance criteria

- [x] Collect appenda linha em audit.jsonl — tested by: pytest audit
- [x] Dois collects → duas linhas; manifesto atual reflete só o último — tested by: pytest
- [x] Check não exige reescrever audit (leitura/consistência mínima) — tested by: pytest
- [x] Formato JSONL estável documentado no SCHEMA/contrato — no test — presença SCHEMA ou assert campos

## Notes

G4-c. Sem SIEM externo. Sem PII nos eventos.

Revisor: aprovado. Gate tentativas_ate_verde=1.
