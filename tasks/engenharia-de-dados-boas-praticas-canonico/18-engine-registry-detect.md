# Engine registry + auto-detect Databricks

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/17-yaml-perfis-pacote-d.md

## What to build

Trocar o dispatch hardcoded A/B/C do engine por registry/dispatch que aceite o pacote D.
Implementar auto-detect de sinais DAB/DLT/SDP no filesystem, resolve de perfil efetivo
(override via `project_profile.yaml` vence) e ambiguidade SDP+DLT → `databricks-multi`
(união de checks). Ampliar `de_marker` / helpers usados pelo `/validar` e pela CLI.

## Acceptance criteria

- [x] Engine despacha pacote D quando o perfil cloud/multi o declara — tested by: unit/integration validate com stub D
- [x] Auto-detect identifica sinais DAB, DLT e SDP (globs documentados) — tested by: fixtures de tree (AC5)
- [x] Override em `project_profile.yaml` vence auto-detect — tested by: teste unitário
- [x] Tree com SDP+DLT → profile efetivo `databricks-multi` + união — tested by: teste (AC4)
- [x] Sem sinais cloud e sem marker → comportamento Loop 1 preservado — tested by: regressão

## Notes

- Sem credenciais Databricks live.
- Globs de detect = decisão de implementação coberta por testes (PRD `[inferido]`).
- Pacote D usa handler vazio intencional como seam; regras DE-D001–D005 são escopo da Task 19.
- DAB isolado é detectado para o trigger futuro do `/validar`, mas não infere SDP vs DLT;
  sem sinal de pipeline, o perfil efetivo permanece no fallback Loop 1.
- Risco MVP aceito: `import dlt` também pode representar dltHub e causar falso positivo;
  refinamento contextual da heurística fica para evolução posterior.
- A revisão alinhou o sinal SDP por decorator exatamente `@dp.` e o engine passou a
  compartilhar a mesma varredura de arquivos com o resolver, sem scan duplicado.
- GIT_PREFLIGHT: `git fetch origin` falhou por autenticação Azure DevOps; execução sem novo
  fetch foi autorizada explicitamente após branch/base locais verificadas (`0 0`).

### Evidências (Task 18)

| Etapa | Resultado |
|---|---|
| RED (test-first) | coleção falhou com `ImportError` para os novos helpers antes da implementação |
| GREEN focado | `pytest test_engine_registry_detect.py test_validate_cli.py test_validar_condicional.py` → 34 passed |
| Gate DE | `pytest tests/data_engineering/` → 90 passed após ressalvas |
| Lint focado | `ruff check` → OK nos arquivos da Task 18 |
| Tipos focado | `mypy` → OK nos 8 arquivos/módulos da Task 18 |
| Gate global | `ruff check .` encontrou 2 erros F541 preexistentes nos espelhos de `excalidraw-diagram`; `mypy` sem alvo configurado retorna erro de uso |
| Revisor | **aprovado com ressalvas** — 0 bloqueantes; decorator `@dp.`, DAB isolado, marker inválido e scan único cobertos |
