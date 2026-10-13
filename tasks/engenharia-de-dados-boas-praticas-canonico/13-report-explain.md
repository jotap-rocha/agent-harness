# Report e explain

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/10-cli-validate-abc.md

## What to build

Completar a CLI com `report` nos formatos **json** e **markdown**, e o SHOULD `explain <rule_id>` que devolve texto acionável a partir do `data-engineering.yaml` (sem dumpar o YAML inteiro).

## Acceptance criteria

- [x] `report --format json` emite findings com rule_id, severidade, path — tested by: pytest parse JSON
- [x] `report --format markdown` emite relatório legível — tested by: pytest substring/estrutura
- [x] `explain <rule_id>` retorna descrição/aplicabilidade/remediação do YAML; rule_id inexistente falha claro — tested by: pytest (SHOULD do PRD)
- [x] Report não inclui conteúdo sensível desnecessário (foco path/rule) — tested by: fixture com pseudo-secret; assert que valor raw não aparece no report (ou é mascarado)

## Notes

- Usado pela task 14 (relatório RO) e por humanos no filho.
- Alinhado a SI: minimizar exposição de PII/secrets no output.
- GIT_PREFLIGHT: soft-block remoto ACKNOWLEDGED; execução no estado local da branch `feat/de-boas-praticas-canonico`, preservando Tasks 09–12.
- RED test-first: `python -m pytest -q tests/data_engineering/test_report_explain_cli.py` → **4 failed**; argparse rejeitou `report` e `explain` como subcomandos inexistentes.
- GREEN: 4 testes específicos; área DE 47 passed; suíte completa 93 passed.
- Gate: verde em 2 execuções (antes e após correções da revisão): `ruff` OK; `mypy` OK; testes DE e suíte completa OK.
- Revisor: 1ª rodada `aprovado com ressalvas`, 0 bloqueantes; corrigidos docstring, constante `EXIT_OK`, exceção de domínio para rule ID e assert JSON. 2ª rodada aprovou o código, restando apenas fechar status/ACs nesta task.
- Decisões aceitas na revisão: `ReportFinding` e `BaselineEntry` permanecem distintos (status vs fingerprint); erro `DE-USAGE` no report continua sanitizado por SI.
- Delivery record pendente: `metrics/entregas.jsonl` exige SHA; sem commit autorizado, não registrar.
