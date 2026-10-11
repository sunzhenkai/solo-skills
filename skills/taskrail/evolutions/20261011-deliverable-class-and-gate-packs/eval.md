# Eval：deliverable-class-and-gate-packs（20261011，taskrail）

## 回归

- 红绿：新增契约测试 `tests/test_deliverable_class_contract.py`（16 条）
  对生产稿 **11 failed / 5 passed**；候选暂存后 16 条全过。
- 既有 taskrail 27 条与族内跨 skill 契约（载荷归属、真源、删除 id、
  **相对链接可达**、phase 枚举封闭）全程不破——新增的
  `../task-confirm/references/gate-packs.md` 与
  `../../task-confirm/references/gate-packs.md` 经自动可达性测试通过。
- 全仓门禁：候选暂存 `python3 -m pytest skills -q` → **426 passed,
  1 skipped**（前基线 410 + 新增 16 = 426）。

## 模式

- F2 基准错置：wizard 原则新增「交付类别必判」，明文禁止把外部
  产品或参考实现写成验收方式；模板新增「交付类别与门包」节
  （交付类别 / 适用门包 / 基准物 / 未覆盖登记）。
- F3 门路由缺失：主循环 wizard 行动作写明 plan 含交付类别与门包；
  阶段载荷表四行（explore/design、design、approve、propose）分别
  携带门包、契约文件指针、基准物；目录节补 design/ 契约指针与
  证据计划。
- F6/F7 完成门不机械：完成门新增第 5 条（门包覆盖 + 未覆盖已登记
  降级）与第 6 条（findings disposition 逐条核对），并写明逐条
  机械核对、任一条缺证据不标 done。

## 契约

- 第一级（skill 自带测试）：16 条新增断言红绿验证；既有 27 条不破。
- 第二级（宿主仓 AGENTS.md 声明门禁）：`python3 -m pytest skills -q`
  候选暂存 426 passed 通过。
- 跨 skill：门包真源（task-confirm，上一轮晋升）与 taskflow 执行段
  脊梁（上上轮晋升）两处引用链在链路测试下可达。

## 副作用

- 触发范围：新增均为「产出要求 + 完成门收紧」；未改档位定义、
  未改 phase 枚举、未改闸口与授权规则、未新增脚本或依赖。
- 过拟合检查：提案 / 正文 / 两份 references / eval 无项目名、
  文件名、密钥、机器路径；证据按「时间 + 次数 + 事件类型」抽象。
- 与既有测试的兼容：phase 枚举行、载荷表既有行、完成门 1–4 条、
  `**不**标 done` 规则逐字保留。

## 结论

pass
