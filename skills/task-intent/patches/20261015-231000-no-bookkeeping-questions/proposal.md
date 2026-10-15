# 可回头的记账不提问

- target: skills/task-intent
- mode: update
- patch: 20261015-231000-no-bookkeeping-questions
- risk: medium
- status: applied

## Intent

用户实测 taskrail 开新任务时仍问「新建还是挂到已有事项？」并附「理解偏了请纠正」，还转贴术语表。改为：建任务 / 恢复 / 起名 / 建 tasks/ / 更新台账 / approve 遇脏工作树 / driver 遇 dirty 仓（带改动 git switch -c）/ rbr 角色推断超 2 个，一律按推荐自行决定、一句话说明、记入「已做决定」；去掉结尾邀请与噪音转贴。真阻塞（删数据、共享配置、线上、改判据、缺凭据、受派方会改到用户未提交改动）保持停下，以陈述句说明。agent-roster 的 Endpoint 选择问询（用户偏好数据）保留。

## Conflict check

接续 statements-not-questions / decision-ledger-boundary；规则出处 taskrail user-report「说决定，不提问」。agent-roster gate_lines 同步改写被锁定的可写前置句（语义不变：仍停下，改为陈述）。

## Files

见 change.patch。
