# Adapter SCM + PR híbrido

**Status:** done  
**Blocked by:** tasks/git-hygiene-azure-devops/01-contrato-regex-testes.md, tasks/git-hygiene-azure-devops/05-comando-nova-branch.md

## What to build

Definir e documentar o adapter `scm: azure | github` por detecção do remote
(`dev.azure.com` / `visualstudio.com` → azure; `github.com` → github; ambíguo →
perguntar). Fluxo híbrido de abertura de PR: se CLI autenticada (`az` ou `gh`),
tenta criar PR com título/corpo padronizados e preferência de squash; senão,
prepara payload para a UI. Se já existir PR da branch, informar URL em vez de
duplicar quando a CLI permitir detectar.

## Acceptance criteria

- [x] Função/doc de detecção classifica URLs Azure vs GitHub vs ambíguo — tested by: teste unitário de detecção por URL (A9)
- [x] Caminho Azure documentado: `az repos pr create` se autenticado (tentar squash); fallback UI com título/corpo/checklist — tested by: no test — checklist + demo quando `az` disponível
- [x] Caminho GitHub equivalente com `gh` — tested by: no test — checklist simétrico ao Azure
- [x] Instrução explícita: PAT/tokens só via env/secret manager; nunca logs/query string — tested by: no test — revisão SI
- [x] Wiring mínimo no `harness-ship` (ou command auxiliar) descreve o fluxo híbrido — tested by: no test — diff do agent/command

## Notes

- Critérios A9, A10.
- Prefixo `Merged PR NNN:` permanece aberto — não automatizar changelog nesta task.
- Template `.azuredevops/pull_request_template.md` reutilizado no corpo (docs).
- **No test (parcial):** fluxos az/gh e SI são docs — justificados; detecção URL tem suíte `tests/git_hygiene/test_scm.py`.
- Gate: pytest git_hygiene + githooks (45 passed) + ruff + mypy em `config/git_hygiene`.
