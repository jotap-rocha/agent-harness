# Skill de-conformidade

**Status:** done  
**Blocked by:** tasks/engenharia-de-dados-boas-praticas-canonico/25-amarrar-agents-de-kernel.md

## What to build

Criar a skill dedicada **`de-conformidade`** (única skill DE nova) seguindo o pattern
`write-a-skill`: ler findings da CLI (`validate` / `compare` / `report` / `explain`),
orientar remediação por `rule_id`, e guiar **baseline/waiver** (owner + expiry) vs
corrigir. Espelhar em `.cursor/skills/de-conformidade/`.

## Acceptance criteria

- [x] Existe `.claude/skills/de-conformidade/SKILL.md` com `description:` acionável — tested by: file/frontmatter assert (AC5)
- [x] Skill cobre findings → remediação → baseline/waiver — tested by: âncoras no SKILL/refs (AC5)
- [x] Não introduz live API nem secrets — no test — revisão SI (AC11)
- [x] Espelho `.claude` ↔ `.cursor` — tested by: assert espelho (AC10)

## Notes

- Nome fechado: `de-conformidade` (não renomear).
- Progressive disclosure: `references/rule-ids-remediation.md` + `references/baseline-waiver.md`.
- Link estável nos 10 agents DE (Kernel): `Playbook: skill \`de-conformidade\`.`
- Freeze inventário atualizado para incluir a skill (gate verde; freeze DoD = task 32).
- **Evidência:** `tests/data_engineering/test_loop3_kb_databricks_and_skill.py` (`test_ac5_*`).
- **Revisor:** aprovado com ressalvas (typo `remediár`→`remediar` corrigido).
- Sem commit.
