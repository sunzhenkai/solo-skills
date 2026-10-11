# Eval：design-contract-and-handoff-gate（20261011，task-explore）

## 回归

- 红绿：新增契约测试 `tests/test_design_contract_and_handoff_gate.py`
  （10 条）对生产稿 **8 failed / 2 passed**；候选暂存后 10 条全过。
- 既有 task-explore 54 条与族内跨 skill 契约（载荷归属、真源、
  相对链接可达）全程不破——新增的
  `../../task-confirm/references/gate-packs.md` 经自动可达性测试通过。
- 全仓门禁：候选暂存 `python3 -m pytest skills -q` → **436 passed,
  1 skipped**（前基线 426 + 新增 10 = 436）。

## 模式

- F4 契约未冻结即并行（探索侧）：design 门禁新增「命中门包必须含
  契约文件指针与证据计划，缺则按缺口停下」；写入表新增
  `design/contract.md` 行；边界明确「只留指针，契约本体落交付仓」。
- F8 证据无契约：证据计划（形式 / 状态绑定 / 覆盖边界）成为 design
  产物，执行段只按计划取证。
- 交接前置：handoff 门禁新增第 5 条（契约指针与证据计划就绪 +
  契约本体已在 `必须` 仓，否则停在门禁、先回 design）；载荷补
  交付类别 / 门包 / 基准物与契约指针进 driver proposal，且明确
  不把契约本体复制进 `tasks/`。
- 命令面：`design` 与 `handoff` 命令段各补一句与本轮门禁一致的指引。

## 契约

- 第一级（skill 自带测试）：10 条新增断言红绿验证；既有 54 条不破。
- 第二级（宿主仓 AGENTS.md 声明门禁）：`python3 -m pytest skills -q`
  候选暂存 436 passed 通过。
- 跨 skill：门包真源（task-confirm）与执行段脊梁（taskflow）、
  taskrail 载荷表三处引用链在链路测试下可达且术语一致。

## 副作用

- 触发范围：新增均为「产物要求 + 交接前置门」，未改命令集合、
  未改归档 / reopen 门禁、未新增脚本或依赖。
- 过拟合检查：提案 / 正文 / 两份 references / eval 无项目名、
  文件名、密钥、机器路径；证据按「时间 + 次数 + 事件类型」抽象。
- 与既有测试兼容：design 门禁既有各条、handoff 门禁 1–4 条、
  「**不要写 `tasks.md`。**」逐字保留。

## 结论

pass
