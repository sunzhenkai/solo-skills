# Proposal：移除对 ui-templates-* 系列 skill 的依赖（taskrail 侧）

- target: skills/taskrail
- mode: update
- patch: 20261014-remove-ui-templates-dependency
- risk: medium
- status: applied

## Intent

用户要求移除对仓外 `sunzhenkai/ui-templates-skill`（`ui-template-design` / `ui-template-apply` / `ui-template-author`，及 apply 内置的 vendor frontend-design）的依赖；dotfiles 编目已于同日下掉该组并删除审计锁，正文继续移交 / 委托这些 skill 会让 agent 调用不存在的能力。

要改变的行为：

1. 「移交 `ui-template-design`」→ 回 design 阶段在交付项目根建立 / 修订 Active Instance 并 freeze（交付仓自有，不依赖仓外 skill）。
2. 「委托 `ui-template-apply` + vendor frontend-design」→ 消费 frozen Active Instance，按代表页 two-pass 方法实现。
3. `adopt published package` → adopt-only：沿用交付仓已有组件库 / 样式体系（仍须登记并确认显式降级）。
4. `check_active_instance.py` / Phase 8 等 ui-templates 专有工具 / 阶段 → 项目约定的 Active Instance 校验 / `ui_evidence_check` current-build 证据。

非目标：Active Instance / freeze / digest / Gallery / 代表页 / 旗舰切片等概念与档位硬门、`ui_evidence_check` 运行态证据门、design 评审门全部保留，不放宽任何门禁。历史 `patches/` / `evolutions/` 中的旧引用不改（审计记录）。

## Conflict check

- 门禁强度不变：medium/complex 无 freeze 仍不得 approve；simple 无 freeze 仍须已确认显式降级；运行态证据门全档位不变。
- 文本契约测试同步改为断言新措辞并 `assertNotIn("ui-template-")`，防回退。
