# Result

- target: agents/skills/task-wizard（现 `skills/task-wizard`）
- mode: update
- patch: 20260925-064335-goal-confirm-via-review
- risk: high
- status: applied
- applied-at: 2026-09-25T06:51+08:00（`dotfiles f873970 fix task-wizard goal`）
- removed-at: 2026-09-29T17:25+08:00（`solo-skills cd1d135 task-goal: 新建承接 goal 执行协议；task-wizard 收窄为方案层`）
- closure: **retroactive**（补记于 2026-09-29；应用当时没写 result.md，本条是事后用 git 历史复原的）

## Validation

判据与结论（重点是判据本身，见 Notes 的教训）：

- **`git log -S<新增行>` 是唯一有效判据**：探针句「处在 goal 里时减少确认：凡要向用户确认的决定…」在两仓全历史命中
  —— `dotfiles f873970`（引入）与 `solo-skills cd1d135`（移除）。曾进入生产稿 ⇒ 本 patch **确已应用**。
- 新增行落地率 **0/5**（当前生产稿里一行都不在）——原因是那套规则整体被 `cd1d135` 搬去 `task-goal`，不是没应用。
- `git apply -p3 --check` 正向**能干净套上**：正因为内容已被删除，历史 patch 今天重新插入当然合法。

## Notes

方向变化是实质的，但发生在应用**之后**：本 patch 让 task-wizard 自己承担 goal 里的确认；两天后 `cd1d135` 把这套协议抽成独立 skill
`task-goal`，生产稿转而写「处在 goal 里的执行与确认由 task-goal 接管，本 skill 不感知 goal」。姊妹 patch
`task-explore/20260925-064334`（同日）内容仍在，只是审阅归属被一并重定向。

教训（本条为什么要写）：落地率 0% + 正向可 apply，两个信号都指「忘了应用」，几乎把我带进错误结论并差点记成「从未应用」。
判"遗忘了什么"只能靠 git 历史，不能靠文本比对。缺一纸 result.md 的代价就在这里——有它，这一条 10 秒就能定性。
