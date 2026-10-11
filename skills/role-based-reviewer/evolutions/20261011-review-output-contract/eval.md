# Eval：review-output-contract（20261011，role-based-reviewer）

## 回归

- 红绿：新增契约测试 `tests/test_review_output_contract.py`（14 条）
  对生产稿 **10 failed / 4 passed**（通过者即四条既有保留断言）；
  候选暂存后 14 条全过。
- 既有 role-based-reviewer 测试 8 条（门禁、角色文件结构、参照集、
  约束）全程不破。
- 全仓门禁：候选暂存 `python3 -m pytest skills -q` → **450 passed,
  1 skipped**（前基线 436 + 新增 14 = 450）。

## 模式

- F8 证据无状态绑定：新增 `产物状态` 输入项与「依据状态」输出节；
  报告只对标识状态有效，产物变更后受影响 findings 作废重审。
- F6 findings 无编号/无处置位：Blocker / Major 按 `F-<n>` 稳定编号；
  处置由调用方记录（`fixed` / `accepted-recorded`），本 skill 不代记、
  不代判收敛——与 taskflow R2「findings 全有 disposition」衔接。
- F7 未覆盖项无降级语义：「未覆盖项」升级为「未覆盖项与降级建议」，
  逐条写原因（信息不足 / 证据未提供 / 工具不可用）+ 建议处置
  （按「未覆盖即降级」含 A/B 定级）+ 工具不可用时的替代方法与能力边界。
- 门 1：结构化调用的边界列举补门包与运行态证据；边界缺项不构成
  拒审理由，但须写明缺项、受影响条目标未验证、不得把缺项当通过。

## 契约

- 第一级（skill 自带测试）：14 条新增断言红绿验证；既有 8 条不破。
- 第二级（宿主仓 AGENTS.md 声明门禁）：`python3 -m pytest skills -q`
  候选暂存 450 passed 通过。
- 跨 skill：与 task-confirm（门包表 / 未覆盖即降级 / 执行器绑定）、
  taskflow（findings disposition / 证据状态绑定）术语与链路一致。

## 副作用

- 触发范围：仅补输入与输出契约，未改三道门禁的触发条件、
  未改角色枚举与推断规则、未改「禁止静默降级为同源自审」。
- 过拟合检查：提案 / 正文 / brief-protocol / eval 无项目名、
  文件名、密钥、机器路径；证据按「时间 + 次数 + 事件类型」抽象。
- 既有约定保留：结论绑定、建议而非执行、简洁、去重、无问题就说无、
  默认不报毛刺逐字未改。

## 结论

pass
