# Contrato YAML + loader

**Status:** done  
**Blocked by:** none

## What to build

Criar o contrato `fluxo-events.yaml` (schema de evento, mapa SDD 0–4, cap 2 MiB,
default truncate N=100, G1-c sem SLA numérico) e o pacote `config/fluxo_events/` com
loader tipado. Base importável no padrão `evidence_gate` / `agent_policies`.

## Acceptance criteria

- [x] Contrato na raiz carrega com limits, mapa 0–4 e N=100 — tested by: `tests/fluxo_events/test_contract_loader.py::test_loads_defaults`
- [x] YAML inválido falha sem silently empty — tested by: `tests/fluxo_events/test_contract_loader.py::test_invalid_contract_fails`
- [x] Sem alvo numérico de latência no contrato (G1-c / AC15) — tested by: `tests/fluxo_events/test_contract_loader.py::test_no_sla_latency_field`
- [x] Pacote importável — tested by: `tests/fluxo_events/test_contract_loader.py::test_package_importable`

## Notes

Slug: `visao-grafica-fluxo-agentes`. Branch: `feat/visao-grafica-fluxo-agentes`.  
Fontes: `02-prd.md`, `03-harness.md`. AC PRD: AC1, AC15.

- Gate: ruff + mypy + pytest `tests/fluxo_events/` verde (2 tentativas — 1ª falhou por
  list-of-maps incompatível com MinimalYamlLoader; `sdd_map` virou mapping por fase).
- Revisor (`revisor-codigo`): **aprovado com ressalvas** — 0 bloqueantes.
  Ressalva restante: rejeição SLA/latency só em `root`/`limits` (não recursiva em
  paths/sdd_map). Outras ressalvas (assert event_types, mensagem list vs mapping,
  chave `"00"`) mitigadas no mesmo ciclo.
- Evidence-gate: collect 4 critérios + check verde;
  `evidencias_ref=.claude/projetos/visao-grafica-fluxo-agentes/evidencias/tasks/58.yaml`
  (check com `--entregas` via CLI usa `ref_base=metrics/` — validar com
  `ref_base=repo root` via API, padrão dos refs em `entregas.jsonl`).
- Commit: **pending** (sem acordo do usuário). Sem push.
- Espelho evidencias: `.cursor/projetos/visao-grafica-fluxo-agentes/evidencias/`.
