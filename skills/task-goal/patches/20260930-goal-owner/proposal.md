# Proposal：goal 生命周期的 owner 条款（第三批）

## 背景

task-delivery 的 goal 模式声明「本循环其余阶段不变」，把 task-goal 当审阅服务用；而 task-goal 自带四状态、state-file 与完成门。同一个 task 的完成被两套主循环同时认领，且 **task-goal 的三档路由没有任何一条通向 task-delivery**——简单=本会话直接做、中等=openspec-propose、复杂=task-explore，delivery 的 goal 模式落地后没有入口。另有「在 goal 里」的触发判据两个 skill 各写一份，与 state-file 无生产者。

## 决定（4 文件 12 处编辑）

**task-goal**
- 触发节：声明**本节是「在 goal 里」的单一真源**，其他 skill 按本节判断，不另写一份。
- 触发节：state-file 路径由进入 side 给出——被 goal 模式委派时由委派方在 `goal-state-file:` 指定；独立 `/goal` 进入时默认 `<task 运行目录>/goal-state.yaml`，无任务运行目录则落 `<evidence_root>/goal-state.yaml`。
- 「写完之后」的复杂档**按来路分流**：本次 goal 由 task-delivery 委派进来时，执行循环归 delivery 的 Stage 1–12，路由写「已交接。执行循环归 task-delivery 的 goal 模式，本协议持状态与完成门。」，不换成 task-explore（delivery 内部本就会走 explore→design→decide→taskflow）；其余情况仍走 task-explore。

**task-delivery**
- 自我定位改为「goal 模式下是执行器」。
- 新增「goal 模式的归属」节：task-goal 持四状态、state-file、退出点与授权、完成门；本 skill 持 Stage 1–12 执行循环；每轮收口回报（带戳优先，无戳按事件推断）；**本 skill 不写 `已完成`**；「收口报告」不是完成门；停机口径来自 task-goal。
- Stage 12「完成报告」改名「收口报告」；回归门与观感类第 2 条的同一措辞同步。
- 观感类中途真人门标注「也是复杂档 B 类降级的唯一集中追认点」（防后续去重时误删）。

**task-goal/references/state-file.md**
- 落点节补三行：委派方指定 / 独立进入的默认 / goal 系统盖戳可覆盖。

**task-explore**
- 「Goal 里的确认」节的触发条件改为指向 task-goal 触发节，不再自写第三条（原写「本任务由 Goal 方案交接且方案里带完成判据」，与 task-goal 不一致）。

## 理由

- 补上 goal→delivery 这条缺失的衔接后，「goal 接管状态」才有落地入口；不补则本批其余条款都是空文。
- 状态与完成门单 owner：delivery 的 Stage 1–12 是执行循环，产出证据与分数，判定权在 task-goal。这样 goal 模式才有唯一终态写入方。
- 触发判据单真源解决两套写法：原来 task-explore 多出的第三条会让它把自己切成 goal 模式而 task-goal 不认。

## 验证

- 全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**（本批无新增断言；现有断言未被触及）。
- 交叉判读：`grep -n "已完成" skills/task-delivery/SKILL.md` 应只出现在「不写 `已完成`」的否定句里。

## 明确不改

- 状态机四状态与迁移网格、`goal_transition.py`、退出点标签集合。
- 简单 / 中等档路由。
- 授权集合封闭性。
- delivery 的 Stage 1–12 流程本身（本批只改 owner 声明与措辞）。

## 已知未覆盖

「每轮收口回报」的具体回报格式未定义（只说带戳优先、无戳按事件推断）。这依赖 goal 系统是否支持盖戳；不支持时由 delivery 的收口报告内容驱动推断，尚无运行证据。若实际运行发现推断频繁落空，需要在 state-file 的推断顺序里补一条 delivery 收口专用分支。
