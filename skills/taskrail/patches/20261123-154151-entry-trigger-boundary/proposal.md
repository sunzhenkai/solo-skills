# 收窄 taskrail 入口并增加分诊

- target: skills/taskrail
- mode: update
- patch: 20261123-154151-entry-trigger-boundary
- risk: high
- status: proposed

## Intent

将 taskrail 的自动触发收敛到显式命令、`/goal` 和需要持久任务轨道的编排场景；在绑定台账前区分元层讨论、普通交付与任务编排；未绑定会话只通过显式 `taskrail resume` 恢复任务。保留现有动态 references、执行适配器、确认协议和完成门，不改为纯手动 skill。

## Conflict check

`agent-docs-writer` 负责只读评审 agent 文档，`skill-upgrader` 负责修改已有 skill，taskrail 不再把这类元层请求当成开发目标。`taskflow` 的执行职责不变。显式 taskrail 命令、`/goal`、跨会话台账、父子任务及多阶段或跨项目编排仍进入 taskrail。

## Rationale

常驻 description 决定模型是否加载 skill，正文入口分诊决定误加载后是否产生台账副作用，两处需要同时收紧。裸“继续”只有在当前会话已有绑定或显式 resume 时才有明确任务身份。入口 eval 覆盖语义路由，文本契约测试守卫分诊顺序和恢复条件。

## Files

- skills/taskrail/SKILL.md：收窄 description，在输入与绑定前加入口分诊。
- skills/taskrail/references/ledger.md：限定裸“继续”和显式 resume 的恢复身份。
- skills/taskrail/evals/cases.yaml：增加元层请求、普通交付、未绑定继续与显式入口案例。
- skills/taskrail/tests/test_taskrail_contract.py：守卫入口分诊和恢复边界。

## Validation

- 在仓库根运行 `git apply --check --recount skills/taskrail/patches/20261123-154151-entry-trigger-boundary/change.patch`。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m pytest skills/taskrail/tests -q`。
- 运行 `make check-names`、`make check-style` 和 `python3 -m pytest skills tests -q`。
- eval 无自动 runner，入口语义案例供实际 agent 人工或模型评审，不以文本契约测试冒充触发率验证。
