# 锁死先确认后执行、补齐未合入主分支 MR/PR 闭环、改写说人话输出

- target: skills/session-wrap
- mode: update
- patch: 20261124-233200-confirm-mr-plain-language
- risk: medium
- status: applied

## Intent

解决实际使用 `session-wrap` 暴露的三个核心问题，并从收尾目标（交付闭环、现场清理、遗留留痕）精简主文：

1. **锁死先确认后执行**：移除「直接执行」分类与「无选择题时直接执行」逃生通道；改为「需要你拍板 / 准备帮你做 / 顺手记下的遗留」，只要涉及任何写文件、改 git、停服务或外部动作，第一轮一律先亮清单等用户确认；仅完全无事可做时直接结束。
2. **补齐代码交付闭环**：将「推送与提 MR/PR 或合入主分支」纳入主路径必查项，不因工作区干净而跳过；新增 `references/branch-merge.md` 承接分支合入裁决与 `repo-manager` / `gh` / `glab` 实际创建 MR/PR 的落地流程。
3. **说人话与控长度**：去除面向用户的内部术语，规定每条一行短句、半屏内看完、结构化提问工具与正文不重复、第二轮用自然结论句开头，并在 `references/plan-synthesis.md` 提供第一轮/第二轮示范与反例。
4. **瘦身主文**：`SKILL.md` 压至 4 步并下沉分支合入与知识分流细则，字节数降至 5890B。

## Conflict check

- 与原「没有需你选择的项时直接执行并进入第二轮」规则冲突，本次有意移除以消除未确认直接执行的漏洞。
- 其他 skill（`anti-lazy`、`taskrail`、`trouble-grill`）仅按名引用 `session-wrap`，无悬空内部术语引用。
- 仓级 `README.md` 同步更新 `session-wrap` 一行简介。

## Files

- `skills/session-wrap/SKILL.md`
- `skills/session-wrap/references/branch-merge.md`（新增）
- `skills/session-wrap/references/plan-synthesis.md`
- `skills/session-wrap/references/detour-review.md`
- `skills/session-wrap/tests/test_session_wrap_contract.py`
- `skills/session-wrap/evals/cases.yaml`

## Validation

- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-style && make check-names && git diff --check`
