# Relatório RO sql-capacity

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/10-cli-validate-abc.md, tasks/engenharia-de-dados-boas-praticas-canonico/13-report-explain.md

## What to build

Job/script no **canônico** que roda `validate`/`report` em modo **somente leitura** contra `/DATALAKE/workspace/prd/data-sql-capacity-evolution-prd`, grava o artefato de saída **no canônico** (ex. `reports/` ou output de CI), e faz **soft-fail** documentado se o path estiver ausente — sem nunca escrever no repo alvo.

## Acceptance criteria

- [x] Relatório gerado (json e/ou md) no canônico apontando findings do sql-capacity — tested by: teste com fixture path ou mock de target; integração opcional se path existir (AC6)
- [x] Nenhuma escrita no tree do sql-capacity — tested by: assert RO (tmpdir read-only ou spy de open/write) (AC6, AC11)
- [x] Path ausente → soft-fail (aviso + exit não-bloqueante do job do example/CI conforme política) — tested by: pytest path missing (AC7)
- [x] Não grava `baseline.json` dentro do sql-capacity — tested by: assert ausente / RO

## Notes

- Acordo explícito: sql-capacity é RO neste ship.
- Não commitar dumps com conteúdo sensível; findings = path + rule_id.
- GIT_PREFLIGHT: `git fetch` falhou por autenticação Azure após retry com rede; soft-block explicitamente reconhecido. Branch `feat/de-boas-praticas-canonico`; working tree das Tasks 09–13 preservada.
- RED test-first: `python -m pytest -q tests/data_engineering/test_ro_sql_capacity_report.py` → **4 failed** por `ModuleNotFoundError` do job ainda inexistente.
- GREEN: 5 testes específicos cobrem JSON, markdown, target fisicamente RO, ausência de baseline, output fora do target e soft-fail de path ausente.
- Integração RO real: `reports/sql-capacity-compliance.json` gerado no canônico; exit `1` por findings esperados. Digest de `git status --porcelain=v2` do alvo antes/depois permaneceu `b1c1c7a5c6d5db89d96d4d0388585bae3e933d0f6c8363845ef6e4a556d2c458`.
- Gate: verde em 2 execuções (antes e após cobrir markdown): `ruff` OK; `mypy` OK; área DE **52 passed**; suíte completa **98 passed**.
- Revisor: `aprovado com ressalvas`, 0 bloqueantes. Ressalva de cobertura markdown corrigida; distinção entre path ausente e path não-diretório aceita como não bloqueante.
- Delivery record pendente: `metrics/entregas.jsonl` exige SHA; sem commit autorizado, não registrar.
