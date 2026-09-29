# Eval: goal-state-machine

- candidate: evolutions/20260930-goal-state-machine/{SKILL.md, references/state-machine.md, tests/test_task_goal_contract.py}
- baseline: skills/task-goal/（生产稿，含上一轮已晋升的 autocontinue 补丁）
- date: 2026-09-30

## 回归

- 基线（生产稿 + 旧测试集）：`python3 -m pytest skills/task-goal skills/task-wizard -q` → **45 passed**（沿用上一轮 eval 结论；本轮未改动既有测试）。
- 候选（隔离副本 /tmp/sm-eval/skills/，替换 SKILL.md + 新增 references/state-machine.md + 新增 TestStateMachine）：同命令作用于 task-goal 与 task-wizard → **54 passed**。
- 结论：新 reference、接入句与无进展轮兜底未打断任何既有契约断言（frontmatter、解耦接口、P 级、评审者三选一、pending 确认门、退出点）。

## 模式

- 原失败路径（2026-09-30）：命中退出点 → goal 自动续跑 → 散文规则只允许重申 → 连续 4 轮空转。
- 候选路径：每轮开头把输入归类到事件枚举（goal 自动续跑），查网格已停行 → 第 1~2 次只读查证，第 3 次 blocked 交接；语义与上一轮 autocontinue 补丁一致。
- 候选对**未覆盖的新输入形态**：事件枚举已封闭 11 种；真有未覆盖组合时走「无进展轮」兜底——禁止原样重复，最坏结局 blocked 交接而非空转。本次失败规则被泛化成结构性防线。
- 结论：该类失败与同类新失败可被避免。

## 契约

- 新增 TestStateMachine 8 个断言：reference 存在、11 事件全部出现、事件枚举封闭、四状态各成一行、已停行非空格 ≥ 9（11 减「判据成立」「步骤推进」两格允许「—」）、blocked 定义为已停交接形态、SKILL.md 引用 state-machine.md 且含无进展轮、SKILL.md 含无进展轮内容。
- 测试校准记录：首轮已停行断言阈值设为 ≥10，未计入「判据成立/步骤推进」对「已停」天然无迁移，失败一次；阈值改为 ≥9 后 54 全绿。非候选稿本身缺陷。

## 副作用

- 触发范围：未改触发条件；新增「每轮开头归类事件」是开销极小的内部动作，不外溢。
- 权限：只收紧不放宽——无进展轮禁止原样重复，最坏结局 blocked 交接；不新增授权项、不动退出点集合、不改三档路由文案。
- 一致性：网格明示「与正文或无进展轮有出入时以正文与无进展轮为准」，避免网格喧宾夺主；四处接入句都显式声明本小节规则优先。
- 耦合：正文四节新增对 references/state-machine.md 的引用；reference 内含完整定义，可独立阅读。
- 残余风险（接受）：网格本身是数据，未来新增事件需改表 + 测试 + 正文接入句三处同步；但相比散文增殖，改表是被逼回答全组合的，漏格可被测试断言（已停行非空格数）兜住。
- 无密钥、内部 URL、项目代号进入正文或进化产物。

## 结论

pass
