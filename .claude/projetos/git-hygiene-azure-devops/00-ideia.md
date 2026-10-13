# Git Hygiene Azure DevOps no Harness

## Ideia

Integrar o uso padronizado de Git Azure DevOps nos projetos que forem usar o harness
localizado em `<raiz-do-clone>`, a partir do plano
em `sketch/portal-git/plan.md`.

A ideia central **não** é construir o “portal” completo descrito no sketch. É evoluir o
**framework canônico** com artefatos de harness (rules, commands, hooks, adapters, wiring
em agents/skills) propagáveis via `/install-harness`, para que projetos-alvo adotem de
forma padronizada:

- branch isolada (`feat|fix|chore/<escopo>`) a partir de `master` sincronizada
- Pull Request com título convencional e template `.azuredevops/pull_request_template.md`
- squash merge como convenção
- tag `prod-*` na entrega validada
- hooks locais (segredos bloqueantes; push no tronco em modo aviso gradual)
- rule `git-hygiene` agnóstica de SCM + adapter `scm: azure | github`
- fonte única `git-hygiene.yaml` (regex de branch/título)
- integração com Dev Loop, `revisor-codigo`, `harness-ship`, `/install-harness`

Estratégia do plano: **Convenção → Detecção → Policy**. Nesta etapa o canônico entrega
principalmente a camada de Convenção (Fase 1); Detecção e Policy vêm depois. Sem
`Edit policies`, nenhum gate impede de fato — o objetivo é tornar o caminho certo mais
fácil e o errado visível.

## SI Assessment

Nível: **b** — dados de usuários mas não PII direto (metadados de acesso e repositórios)

Implicações:
- Harness mínimo de SI das rules/seguranca.md permanece
- PAT / tokens Azure DevOps **somente** via variáveis de ambiente ou secret manager —
  nunca hardcoded, nunca em logs, nunca em URL query strings
- Relatórios e métricas de higiene Git **agregados por repositório**, nunca por pessoa
- Varredura de segredos no diff é bloqueante desde o dia 1
- Não exige `[AVISO_LGPD]` nem `rules/pii.md` (nível c); não exige deny list estendida
  de escrita em banco de produção (nível d)

## Tipo de Projeto

**e** — Outro: evolução do framework / Agent Harness Canônico (não é produto nem pipeline)

Stack / artefatos previstos (canônico → projetos-filho via `/install-harness`):
- Rule transversal `git-hygiene` (`.claude/rules/` + espelho `.cursor/rules/*.mdc`)
- `git-hygiene.yaml` — fonte única de regex/contrato
- Command `/nova-branch`
- Pasta versionada `.githooks/` + bootstrap de `core.hooksPath` no install
- Template `.azuredevops/pull_request_template.md`
- Adapter `scm: azure | github` no CLAUDE.md dos projetos-filho (`az` vs `gh`)
- Wiring: `dev-loop-executor` (GIT_PREFLIGHT), `harness-build`, `harness-ship`,
  `revisor-codigo`, `prompt-crafter`, `harness-brainstorm`
- Correção de propagação: incluir agents `harness-*` no `stack_map.json` (lacuna atual)
- Fora do MVP: portal UI, branch policies Azure, deploy automático, rename `master→main`,
  `repo_profile` completo (Fase 4), pipeline de detecção (Fase 2)

## Próximos passos

0. Repo já mapeado — ver `00b-codebase.md`
1. ~~`/grill-me`~~ — concluído em `01-grill.md` (2026-08-06)
2. ~~`harness-define`~~ — requisitos estruturados em `01-grill.md` (2026-08-06)
3. Próximo: `harness-design` → PRD + tasks / implementação da Fase 1
