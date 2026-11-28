# 增加按需过程复盘

- target: skills/session-wrap
- mode: update
- patch: 20261123-181146-process-review
- risk: medium
- status: proposed

## Intent

用户要求复盘、分析过程或优化流程时，基于已有证据分析主要耗时、坑与返工、可精简项和有效做法，并给出对应的优化方案。普通收尾不增加该环节，不引入计时、评分、额外扫描或报告文件。

## Conflict check

保留 anti-lazy、taskrail close 与 detour-review 的既有职责；过程复盘不代替意图检查、任务收口或坑候选沉淀。优化建议不自动修改其他 skill。

## Rationale

现有流程覆盖交付缺口和排查弯路，但缺少对整个会话执行过程的按需检查。新增单个 reference 承接分析规则，并用文本契约与案例约束触发条件、证据和输出，改动可验证且不增加普通收尾成本。

## Files

- skills/session-wrap/SKILL.md：增加按需过程复盘入口及输出衔接。
- skills/session-wrap/references/process-review.md：定义取证、分析、优化和输出规则。
- skills/session-wrap/tests/test_session_wrap_contract.py：增加过程复盘文本契约。
- skills/session-wrap/evals/cases.yaml：增加显式复盘与普通顺利收尾案例。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、session-wrap 测试、全仓测试、`make check-names` 和 `make check-style`。
- 检查新增引用存在、无隐私信息，实际 diff 仅限 proposal 声明文件。
