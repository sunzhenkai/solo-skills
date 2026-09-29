# Proposal：「Goal 里的确认」改为指向 task-goal 的指针

与 task-goal 的 `patches/20260929-decouple-goal-protocol/proposal.md` 同一次改造，本文件只记 task-explore 侧。

## 改动

- description 与「Goal 里的确认」节：审阅协议从「走 task-wizard 的『审阅』」改为「走 task-goal 的『审阅』；派审规则、核对循环、收敛与停止条件以 task-goal 为准，本 skill 不复制第二份」。
- 删除节内自建的派审提示词与完成程度判定（与 task-goal 重复的机制），保留探索侧专属规则：推荐默认取法（该处默认建议；无默认时取能让完成判据成立、不覆盖目录、不泄密、不做未点名危险操作的那一条）、审阅收敛即采纳并同轮继续、冻结未决并交接时收敛即 decide+handoff、task-goal 读不到则停并给安装选项。
- 契约测试同步：断言改指 task-goal。

## 不改

references 里「上游 task-wizard 的步骤级方案 / 质量画像」表述——task-wizard 仍是方案产出者；decide / handoff 的 pending 降级门不动。

## 验证

`python3 -m pytest skills/task-explore/tests -q` 全过；全仓 282 passed。
