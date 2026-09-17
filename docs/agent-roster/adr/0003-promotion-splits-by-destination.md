# 固化按去向分两条路，routing.md 不走 patches 审计

`SKILL.md` 原先写着 Routing Rule「只由 `$skill-upgrader` 从案例固化」，但那个 skill 的审计机制是 `<skill-dir>/patches/`，只作用于含 `SKILL.md` 的目录；`routing.md` 在使用者的私有数据目录里（见 [ADR 0001](./0001-ledger-lives-outside-this-repo.md)），它根本够不着。这条路径从写下来那天起就是悬空的。

现在按固化的**去向**拆开：进 `routing.md` 的规则带 Host 名、只对一个使用者成立，由 Orchestrator 提案、使用者确认后直接写；进 `SKILL.md` 正文或 `experience/patterns/` 的结论已脱敏、对任何人成立，仍走 `$skill-upgrader` 的 `patches/` 审计。判据是去向而不是内容的分量：`patches/` 的价值在于「公开仓的机制被改动时留下可审计的痕迹」，而私有数据仓本身就有 git 历史，再叠一层审计只会让本就唯一的那条路继续卡死。

## Consequences

Orchestrator 因此多了一项职责：写完 Trace 后要检查是否攒够了固化条件，攒够则停下来提案。这个触发点是 [ADR 0002](./0002-no-scoring-only-cases.md) 所描述的进化路径能否启动的前提——没有它，「攒够案例 → 提案 → 确认 → 写入规则」里的第二步永远不会有人发起，`routing.md` 会永久为空。
