# task 系列深度复审落地（taskrail）

背景：复审发现 human 闸口「停不停」两种读法都成立、停的条件散在五处、按模板建的 TASK.md 过不了 check_handoff、skip 档与 worktree 的衔接未定、契约内容重复。

改动：
- confirm-protocol 改成「停点」表：human 只在 wizard 定稿（意图复述 + plan 要点一条消息）和 approve 停，其余阶段说决定接着做；删掉无执行步骤的 design 定稿闸口；「另一个模型审」成为 goal 闸口、goal 意图、观感共用的唯一派审规则（含 rbr 派不出时由调用方自审标把握低、P0=Blocker / P1=Major）。
- user-report 第 5 节加「卡住才停」，phase-wizard / done 的停点改指针；contract 的三组「对用户说话」前后对比挪进 user-report（check_output_style 随之改查 user-report）。
- SKILL.md：resume 沿用 TASK.md.confirm_mode；主循环只在停点停；提交只落任务 worktree 的任务分支、不 push；grilling 标可选。
- contract 瘦身：删 Skill 归属表、职责收敛段、授权术语（已在 confirm-protocol）；元信息写 frontmatter 并补按需字段；skip 不建 worktree、skip 升 full 用 HEAD 基线带改动；tasks/ 与 OpenSpec 留主工作树；术语加严重级映射。
- phase-wizard 第 2 步改为复用 intent 摸底只补实现入口。
- evals：resume 四行、human 停点按新规则改写；契约测试同步。
- 仓级：docs/task-flow/README.md 停点与流程图；scripts/check_output_style.py 与 tests/test_output_style.py 改查 user-report「前后对比」。
