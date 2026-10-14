# Proposal：Web UI 检查按档调度，去掉 simple 档的过度检查（role-based-reviewer 侧）

- target: skills/role-based-reviewer
- mode: update
- patch: 20261014-ui-overreach-speed
- risk: medium
- status: applied

## Intent

用户反馈 taskrail + role-based-reviewer 对 UI 过度检查、拖慢任务。原规则对 **全档位（含 simple）** 硬性要求 `ui_evidence_check`（双视口 + axe + 键盘 + 四态截图）、独立 design 评审文件、代表页 two-pass 与 Gallery，simple 档的小改动也要走完整 UI 证据链。

要改变的行为：

- taskrail gate-packs「Web UI」改为**档位调度**：complex 维持全量硬门；medium 硬门但允许精简 manifest（单路由 / 单桌面视口 / 四态可批量 not_applicable）；simple 的 `ui_evidence_check` 与 design 评审改为 SHOULD，未跑须登记 B 类显式降级，quality floor 由实现者自检。
- simple 不强制 `roles=design`、不强制代表页 two-pass / Gallery；adopt-only 豁免重型证据门。
- 完成门第 7 条同步按档。
- role-based-reviewer design 角色新增「调用范围与速度」：边界为 simple / adopt-only / 小修时只报 quality floor 🔴 条，不启服务、不截图。

非目标：不删 quality floor（破坏性确认、键盘可达、focus 可见）；complex 门禁不放宽；不改其它交付类别门包。

## 关联

与同日 `20261014-remove-ui-templates-dependency` 叠加；`change.patch` 为相对 HEAD 的累计 diff（含两次改动中涉及这些文件的部分）。
