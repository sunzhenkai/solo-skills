promote

理由：
- 提案为上一轮（同会话）预置、用户选 A 拍板下轮执行，本轮用户点名 skill-evolver 即为执行指令。
- Evaluate pass：6 态判定含 2 个真实历史 run + 4 个合成用例；修正了一处实现 bug（同 id 多响应取末个）。
- 候选 diff 与 proposal 一致（新增 scripts/run_status.py；契约 +1 条、SKILL.md 指针句改写），无夹带。

后续：晋升到源仓库生产稿；commit 由编排者执行；push/lock/sync 属线上动作，需用户单独确认。
