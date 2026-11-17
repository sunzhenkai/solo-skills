# description 去掉产物路径与输出格式

- target: skills/solo-code-review
- mode: update
- patch: 20261118-014613-description-trim
- risk: high
- status: proposed

## Intent

description 保留能力（审查范围）与全部触发词，把「完整结果写入 docs/reviews/{日期}/{change-name}，对话只打印 P0~Pn 总结」压成「结果按 P0~Pn 分级落盘」。非目标：触发词、正文流程与产物目录不变（正文第 4 节已写明）。

## Conflict check

none。

## Rationale

description 常驻上下文，按 AGENTS.md 只写 WHAT + WHEN；原文 225 字，是全仓最长。

## Files

- skills/solo-code-review/SKILL.md：description。
- skills/solo-code-review/tests/test_skill_contract.py：新增 `DescriptionTest`。

## Validation

- `python3 -m pytest skills/solo-code-review/tests -q`
