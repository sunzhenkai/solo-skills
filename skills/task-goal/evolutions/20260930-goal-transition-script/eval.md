# Eval: goal-transition-script

- candidate: evolutions/20260930-goal-transition-script/{SKILL.md, scripts/goal_transition.py, tests/test_goal_transition.py}
- baseline: skills/task-goal/（生产稿，含上一轮已晋升的 goal-state-machine）
- date: 2026-09-30

## 回归

- 基线（生产稿 + 当前测试集）：上一轮已验证 54 passed；本轮在基线之上加脚本与 TestGoalTransitionScript。
- 候选（隔离副本 /tmp/sm-eval3/skills/，替换 SKILL.md + 新增 scripts/goal_transition.py + 新增 tests/test_goal_transition.py + 更新 test_task_goal_contract.py）：作用于 task-goal 与 task-wizard → **83 passed**。
- 结论：新脚本、SKILL.md 触发节改写、TestGoalTransitionScript 6 个断言未打断任何既有契约（frontmatter、解耦接口、P 级、评审者三选一、pending 确认门、退出点、TestStateMachine 全部）。

## 模式

- 原失败路径（2026-09-30）：执行者自行推导「第几次重申」「当前状态」——推理非机械。
- 候选路径：执行者把输入归类到事件后调用脚本，脚本输出 `{next_state, action, reply_shape}`；分类仍由模型做（脚本不做自然语言理解），但迁移与计数由脚本强制。
- 未定义组合：脚本返回 `defined: false` + `note: 走无进展轮`，与上一轮兜底语义对齐。
- 结论：迁移与计数从推理变为查表执行，该类失败族进一步收敛。

## 契约

- test_goal_transition.py（24 个用例）：网格解析、每个非空格迁移、autocontinue 计数边界（1/2/3/5）、缺 count 拒绝、未定义组合、未知状态、未知事件、事件简称匹配、回复形状提取。
- test_task_goal_contract.py 新增 TestGoalTransitionScript（6 个断言）：脚本存在、stdlib-only 顶层 import、已定义组合 exit 0 且含 next_state、第 3 次自动续跑 blocked、未定义组合 exit 1 含无进展轮提示、未知事件 exit 1。
- 测试校准记录：首轮 `test_event_prefix_match` 失败——脚本只支持前缀匹配，「自动续跑」vs「goal 自动续跑」是子串关系；改为「前缀 → 唯一子串」两级回退后 83 全绿。非语义改动，是匹配鲁棒性补齐。

## 副作用

- 触发范围：SKILL.md 触发节改了一句，把「查网格」改成「调用 scripts/goal_transition.py」；正文其余各节未动。
- 权限：脚本只读 references/state-machine.md，不写文件、不发网络；不新增授权项、不动退出点集合。
- 一致性：SKILL.md 显式声明「脚本只是查表器，不替代正文；网格与正文或『无进展轮』有出入时以正文与无进展轮为准」。
- 数据唯一真源：脚本从 references/state-machine.md 的网格行解析迁移数据，不另存副本；改表 = 改脚本行为。
- 残余风险（接受）：模型仍可能绕过脚本直接答。但脚本可被人类/契约测试独立调用验证，模型不走脚本就缺少脚本输出作为证据，易于审计发现。
- 无密钥、内部 URL、项目代号进入正文或进化产物。

## 结论

pass
