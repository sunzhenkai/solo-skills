promote

理由：
- 使用者在本轮开头显式点名 skill-evolver 并指示「直接更新源代码库」，视为 Proposal 展示与全流程的预授权（risk: medium，已在上文完整展示 proposal.yaml）。
- 证据充分：同一模式（适配器特异性只能靠 L3 冒烟暴露）在 2026-09-17/09-23/09-24 三个不同任务累计 3+ 次；受控执行缺口在同轮造成小时级假等待与漏判。
- Evaluate 为 pass；候选 diff 与 proposal 一致（SKILL.md +2 行指针、契约 +claude 口径/+冒烟门禁/+受控执行），无夹带。

后续：晋升到源仓库生产稿 skills/agent-roster/；提醒使用者跑 sync（dotf agents -c / sync.sh）刷新 ~/.agents 镜像，不擅自 sync 或 commit。
