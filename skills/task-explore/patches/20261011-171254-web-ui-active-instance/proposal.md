# Web UI design/approve/handoff digest 门禁

- target: skills/task-explore
- mode: update
- patch: 20261011-171254-web-ui-active-instance
- risk: medium
- status: proposed

## Intent

design 无 freeze 则移交 ui-template-design；contract.md 必含三条 digest；approve 结构门校验；handoff 把 digest 写入 driver。

## Conflict check

不复制 DS 0–9；禁止在 tasks/design 重写 tokens。

## Rationale

探索侧负责方案与交接指针，与门包档位硬门对齐。

## Files

- skills/task-explore/SKILL.md
- skills/task-explore/references/phase-design.md
- skills/task-explore/references/phase-approve.md
- skills/task-explore/references/phase-handoff.md
- skills/task-explore/tests/test_design_contract_and_handoff_gate.py

## Validation

- `python3 -m pytest skills/task-explore -q`
