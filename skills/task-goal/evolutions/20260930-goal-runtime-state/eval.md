# Eval: goal-runtime-state

- candidate: evolutions/20260930-goal-runtime-state/{SKILL.md, scripts/goal_transition.py, references/state-file.md, tests/test_goal_transition.py}
- baseline: skills/task-goal/（生产稿，含前两轮 goal-state-machine、goal-transition-script）
- date: 2026-09-30

## 回归

- 基线（生产稿 + 既有测试集）：83 passed（沿用上一轮 eval）。
- 候选（隔离副本 /tmp/sm-eval4/skills/，替换 SKILL.md + scripts/goal_transition.py + 新增 references/state-file.md + 重写 tests/test_goal_transition.py + 更新 test_task_goal_contract.py）：作用于 task-goal 与 task-wizard → **91 passed**。
- 结论：未打断任何既有契约断言（frontmatter、解耦接口、P 级、评审者三选一、pending 确认门、退出点、TestStateMachine、TestGoalTransitionScript 全部）。

## 模式

- 原失败路径（2026-09-30）：执行者每轮从对话历史重建「第几次重申」「当前状态」，推理非机械。
- 候选路径（端到端模拟验证）：
  - 写入初始 state-file（autocontinue_count=0），连续 4 轮 `--event-tag auto-continue --write`：
    - Round 1: action=只读查证；count→1
    - Round 2: action=只读查证；count→2
    - Round 3: action=blocked 交接；count→3；blocked=true
    - Round 4: action=blocked 交接；count→4；blocked=true（不再空转，保持 blocked）
  - 一次性调用语义不变：`--autocontinue-count N` 表示「这次是第 N 次」，
    count=1/2 → 只读，count≥3 → blocked。
- 事件分类：生产者戳路径走 `--event-tag`，无需 goal 系统配合的降级路径走
  references/state-file.md 的「事件推断顺序」（6 步逐条比对，命中即停）。
- 结论：状态、计数、事件分类三步全部从推理变机械。

## 契约

- test_goal_transition.py（35 个用例）：网格解析、迁移判定、state-file 读写
  （roundtrip / 未知字段忽略 / 缺字段跳过 / 缺失文件返回空）、CLI 带 state-file
  （驱动 state+count、write-back 递增、第 3 次标 blocked、event-tag 映射、
  未知 tag 报错、非自动续跑事件清零计数）、事件推断顺序表存在性。
- test_task_goal_contract.py 新增 3 个断言：state-file 冒烟、event-tag 冒烟、
  references/state-file.md 存在。
- 测试校准记录：
  - 首轮 2 个 state-file 用例失败——off-by-one：state-file 存的 count 是「已发生 N 次」，
    传给 decide 时应是 N+1；同时区分两种调用语义（state-file：存的 N；一次性：传的 N）。
  - 修复后 91 全绿。非语义改动，是计数边界澄清。

## 副作用

- 触发范围：SKILL.md 触发节改写一句，把「调脚本查表」扩为「读 state-file → 看戳/推断 → 调脚本 → 回写」；正文其余各节未动。
- 权限：脚本读写仅限调用方指定的 state-file 路径，不写其它文件；不新增授权项。
- 一致性：SKILL.md 显式声明「脚本只是查表器 + 状态文件读写器，不替代正文」；
  references/state-file.md 红线「只存计数器，不存迁移规则」，避免与网格双真源。
- 数据唯一真源：迁移规则仍只在 references/state-machine.md；state-file 是计数器实例。
- YAML 解析：手写最简 parser，字段封闭（6 个 key），未知 key 静默忽略——守住 stdlib-only 红线。
- 残余风险（接受）：模型仍可能跳过脚本直接答。但脚本输出（含 wrote_back）与
  state-file 内容可被外部独立审计——模型不走脚本就没有 wrote_back: true，
  state-file 也不更新，偏离立即可见。
- 无密钥、内部 URL、项目代号进入正文或进化产物。

## 结论

pass
