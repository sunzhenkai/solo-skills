# human 闸口强制带推荐

- target: skills/task-confirm
- mode: update
- patch: 20261010-105830-human-gate-recommend
- risk: medium
- status: proposed

## Intent

把 human 闸口从「可写推荐」升为可执行输出契约：每个未决口子必须含问题 / 推荐 / 一句话理由；禁止只列问题；调用方 human 与 goal 均须给「推荐默认」；缺则「理解不够」。不改变 goal 审阅收敛、退出点与授权规则；不编排档位。

## Conflict check

none。与 taskrail wizard「问前必给推荐」一致；契约 human 行由下一轮 taskrail 薄对齐补「含推荐」。

## Rationale

规则已写「列选项（含推荐）」，但缺输出模板与禁令，执行时易空问。补可测契约即可提升闸口体验。

## Files

- `skills/task-confirm/SKILL.md` — human 呈现硬约束、闸口输入、模板
- `skills/task-confirm/evals/cases.yaml` — 新增空问禁令 case
- `skills/task-confirm/tests/test_task_confirm_contract.py` — 文本契约断言

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/task-confirm/tests -q`
