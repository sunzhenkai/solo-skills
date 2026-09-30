# Eval：suspend-integration

## 回归

- 全仓契约测试：393 passed, 1 skipped（候选 staged 后）；红绿验证：
  9 条新断言对旧生产稿全失败、对候选稿全过。
- 跨 skill 同源纪律锁（TestPendingConfirmationSyncLock，5 条）全过：
  「执行者、子代理与审阅收敛都不算用户确认」「不静默接受、不自行确认」
  原子串保留——B 类例外以限定从句写入，未删除原防线。
- Driver 协议模板的既有逐字断言（三条件、三选一分支规则）全过：
  模板只追加一句「只停依赖该项的条目」，未改写既有句。
- 回填/评分门的数值口径（五维 ≥2、UI/UX ≥2.5）未动。
- 跨 skill 引用：suspension.md 与 quality-profile.md 相对路径核验
  存在（契约断言锁定）。

## 模式

- 死锁形态（收尾期发现降级，F2/F5）：新规则下 B 类走 provisional、
  可回填非依赖验收，收尾不再死锁；A 类照旧全额阻塞（正确的侧）。
  ✔
- 整轮停摆形态（F1）：「需要用户决策」只停依赖面 + 模板句进每个
  新 driver proposal。✔ 全部剩余条目都依赖决策时，非依赖面=无，
  五元组如实写「无」，不再出现三条件全不满足的未命名形态。
- 恢复形态（F4）：用户输入先比对授权形状，意图命中复述生效即恢复；
  未命中重申仍停。✔

## 契约

- `python3 -m pytest skills/taskflow/tests -q`：28 passed。
- `python3 -m pytest skills -q`：393 passed, 1 skipped。

## 副作用

- 触发范围：Driver 协议模板一句、「质量画像与降级确认」两条、
  「一轮结束」一段、两份 references 收尾/评分门；并行执行、委托
  契约、脚手架、实现者输入未动。
- 确认权未放宽：A 类与 confirmed 仍只有用户能写；provisional 例外
  收窄到「B 类 + 审阅收敛 + 追认前不算 confirmed」三重限定。
- 诚实记录：依赖面划分由主会话判（与 task-delivery 同一裁量），
  越界兜底靠 checkbox 纪律（不把未完成勾成完成）与 goal 层无进展轮。
  模板句只约束新 driver；存量 driver proposal 不受影响（每任务新建）。

## 结论

pass
