# Proposal：delivery-loop 改名 task-delivery，goal 确认委托 task-goal，复杂门读方案档位

与 task-goal 的 `patches/20260929-decouple-goal-protocol/proposal.md` 同一次改造，本文件只记 task-delivery 侧。

## 改动

- 目录改名 `delivery-loop` → `task-delivery`（git mv 保留历史）；frontmatter id/name、evals `skill:`、agents/openai.yaml 的 display_name 与 default_prompt 同步。
- goal 模式：动作从「调用 task-wizard 走其 Goal 方案分支」改为「本循环内所有确认与方案审阅委托 task-goal，不列选项」；依赖清单加 task-goal（goal 模式必需）。
- 主循环 Stage 2：改为「移交方案决策：委托 task-wizard 产方案，方案原文原样带入本循环，不自产、不改写」——明确入口 ≠ 方案上游。
- 主循环 Stage 3 复杂门：删除自建复杂判据（与 task-wizard 产品交付硬指标同源两份），改为读方案的复杂度档位，非复杂退出。
- references/loop-protocol.md Stage 1 同步：删复杂信号清单与「调用 task-wizard 生成 Goal 方案」，改为方案移交；`/tmp/delivery-loop/` 路径与文中自称改为 task-delivery。

## 理由

- 消除复杂度判据两处漂移风险。
- delivery-loop 不再感知 Goal 方案内部结构，goal 行为单 owner 在 task-goal。

## 验证

全仓 `python3 -m pytest skills -q` → 282 passed, 1 skipped。grep 确认仓内活文件无 `delivery-loop` 残留（patches/evolutions 历史件除外）。

## 仓外动作（使用者侧）

安装目录 `~/.agents/skills/delivery-loop` 为字节复制残留，改名后需删除旧目录再同步安装。
