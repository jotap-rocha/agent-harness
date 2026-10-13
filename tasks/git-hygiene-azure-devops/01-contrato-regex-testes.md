# Contrato regex + fixtures

**Status:** done  
**Blocked by:** none

## What to build

Entregar a fonte única do contrato Git hygiene (`git-hygiene.yaml`) com regex de
nome de branch e de título de PR, mais fixtures/testes que provam válidos e
inválidos (tipos `feat|fix|chore`, escopo kebab ≤40, proibidos, título
`tipo(escopo): resumo`). Qualquer validação futura (comando, hooks, agents)
deve consumir essa fonte — não duplicar regex.

## Acceptance criteria

- [x] Existe `git-hygiene.yaml` na raiz do canônico com padrões de branch e título de PR — tested by: arquivo presente + schema mínimo documentado no próprio YAML ou README curto adjacente
- [x] Casos válidos de branch (`feat/gate-branch-isolada`, `fix/parser-data-nula`, `chore/atualiza-dependencias`) passam na validação — tested by: fixture/unit test das regex
- [x] Casos inválidos (`tmp`, acento, >40 chars, `nova-branch`, tipo fora da lista) falham — tested by: fixture/unit test das regex
- [x] Casos válidos/inválidos de título de PR respeitam o padrão e limite de resumo — tested by: fixture/unit test das regex

## Notes

- Critérios A1 (parte yaml) e A3 do PRD.
- Sem regra `.md`/`.mdc` nesta task — isso fica na task 02.
- Preferir Python stdlib/`pytest` se o canônico já tiver caminho de teste; senão script + fixtures com exit code.
- Test-first: falha inicial `ModuleNotFoundError: config.git_hygiene.contract` (evidência em sessão); depois 22 passed.
- Gate proporcional: `ruff check` + `mypy` + `PYTHONPATH=. python3 -m pytest tests/git_hygiene/` (sem `uv` no ambiente) — verde em 1 tentativa pós-implementação.
- Revisor (`revisor-codigo`): **aprovado com ressalvas** (0 bloqueantes). Ressalvas remanescentes: (a) drift entre fragments de regex no YAML (types vs patterns) — mitigado parcialmente com check `group(1) ∈ types` + nota no YAML; geração única fica para task futura; (b) `yaml_loader` sem suíte unitária própria (cobertura indireta via load); (c) “data solta” = escopo inteiro (fullmatch), documentado no YAML.
- Nome de pessoa: documentado em `branch.limits.person_name` — sem regex impossível.
