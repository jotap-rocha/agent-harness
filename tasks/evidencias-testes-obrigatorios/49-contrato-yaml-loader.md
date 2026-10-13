# Contrato YAML + loader

**Status:** done  
**Blocked by:** none

## What to build

Criar o contrato `evidence-gate.yaml` (schema de manifesto, caps 2 MiB, fator 2×) e o
pacote `config/evidence_gate/` com loader tipado. CLI `check` valida schema do contrato
(sem ainda exigir provas em disco). Base para collect/check.

## Acceptance criteria

- [x] Contrato na raiz carrega com limits e schema tipados — tested by: pytest loader
- [x] YAML inválido falha sem silently empty — tested by: pytest casos negativos
- [x] CLI `python -m config.evidence_gate check --contract` (ou equivalente) exit ≠ 0 em contrato inválido — tested by: pytest CLI
- [x] Pacote importável no padrão agent_policies/git_hygiene — tested by: import smoke

## Notes

Slug: `evidencias-testes-obrigatorios`. Branch: `feat/evidencias-testes-obrigatorios`.
Naming: `python -m config.evidence_gate collect|check` (03-harness).

Revisor: aprovado com ressalvas (constantes mortas removidas; hard_timeout qualquer
valor rejeitado; CLI exige `--contract` explícito ou `--root`+`--task`).
Gate: pytest 8 passed + ruff + mypy; tentativas_ate_verde=2.
