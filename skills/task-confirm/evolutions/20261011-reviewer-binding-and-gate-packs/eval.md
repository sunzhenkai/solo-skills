# Eval：reviewer-binding-and-gate-packs（20261011）

## 回归

- 红绿：新增契约测试 `tests/test_reviewer_binding_contract.py`（15 条）
  对生产稿 **9 failed + 6 errors**（gate-packs.md 不存在），候选暂存后
  全过；task-confirm 既有 41 条测试始终全绿。
- 全仓门禁：候选暂存 `python3 -m pytest skills -q` → **388 passed,
  1 skipped**（前基线 373 passed + 新增 15 = 388，其余零回归）。
- 既有断言无一被改写削弱：三选一表仍在（role-based-reviewer /
  agent-roster 条目保留），仅 subagent 行措辞收紧为条件回退，
  `test_three_choice_table_intact` 锁住。

## 模式

- F1 静默降级：新增「执行器绑定」——命中即 MUST 结构化调用
  （`mode=review` + 完整 `roles=` + 审阅边界）；降级须写明不可用原因
  并记入评审意见路径；退出点新增「评审降级未记录」。
- F2 基准错置：门包通则第 1 条明文「禁止把外部产品或参考实现当
  验收基准」，参照集降为输入与差值判定。
- F3 门路由缺失：新增 `references/gate-packs.md` 作交付类别门包
  **唯一真源**（Web UI / 服务 / 数据 / 部署密钥 / 文档 Skill），
  每类给基准物、必载专家能力、可自动化门、运行态证据、主观项处理。
- F7 未验证即通过：新增「未覆盖即降级」段，接既有 A/B 降级门。
- F11 同源评审：交付验收 SHOULD 异源（`model=` / `endpoint=`）。

## 契约

- 第一级（skill 自带测试）：15 条新增断言红绿验证；既有 41 条不破。
- 第二级（宿主仓 AGENTS.md 声明门禁）：solo-skills 自动化门禁为
  `python3 -m pytest skills -q`；候选暂存后 388 passed 通过。

## 副作用

- 触发范围：只改 task-confirm 审阅节 / 退出点 / 相关资产与新增
  一个 reference；未改权限、未改触发条件、未引入脚本副作用。
- 过拟合检查：proposal / eval / 正文 / 门包表均无项目名、文件名、
  密钥、机器路径；证据按「时间 + 次数 + 事件类型」抽象。
- 依赖检查：门包表引用 `role-based-reviewer` 与 quality-profile 均为
  同族既有资产；未新增外部依赖。

## 结论

pass
