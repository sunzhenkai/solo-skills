# archive 与 reopen

原则：不覆盖、先列未结项、多项检查合成一次说明。

## archive

把用户确认关闭的任务整树移到 `tasks/archive/{yyyy-mm-dd}/{slug}`。方案已冻结、含实施动作且未 `handed-off` 时不归档，改走 handoff（用户明确放弃或不实施时不拦）。

**搬之前一次说清**：未结子任务（有则停）；未决条数（可随归档关闭）；曾交接的 driver 进度（读不到写「进度未知」，只报告不回写）；指向旧路径的链接（我会改指新路径）。目标路径已存在：停下说明冲突，不改任何文件。

用户明确说关闭才搬。**步骤**：写回进展 → `status: archived` + `archived` 日期 + 归档记录（结论、关闭原因、未决、driver 现状）→ 写 `SUMMARY.md`（一屏内人读时间线，读不到写「未记录」）→ 移动整树 → 更新 INDEX → 确认新路径可读、旧路径已不存在 → 清除绑定。

## reopen

把归档任务搬回 `ongoing/`，或撤回 `handed-off`（目录不动，只改状态）。状态以 `TASK.md` 为准，不按目录猜。

**动之前**：目标路径已存在则停；曾交接的报告 driver 现状，driver 不删；用户明确说 reopen 才动。

**步骤**：`status` 回 `ongoing`，加 `reopened` 日期，已有记录不删不改 → 归档任务整树搬回；`handed-off` 的只在交接节追加撤回原因 → INDEX 改回 Ongoing、去掉 `→ driver` 尾注 → 绑定并按四行汇报。
