# handoff：交接给 taskflow

把 `tasks/ongoing/{slug}` 交给 `{slug}-driver`。不写代码、不归档、不搬目录、不清绑定。之后交付进度只认 taskflow checkbox。approve 放行后同轮做，两种模式相同。

## 前提

1. 已批准：`approve/APPROVED.md` 存在。没有就先 approve。
2. driver 名固定 `{slug}-driver`（子任务 `{sub}-driver`）。已存在就复用，不新建。
3. 已 `handed-off` 且 driver 存在：报告 driver 路径，不重复交接。

## 步骤（顺序固定：先过入口门，再建 driver）

1. 有未写回的进展先写回 `TASK.md`。
2. 写 `TASK.md`「## 交接」节，只放**指针与判据**，不复制方案、画像或降级原文：

   ```text
   - 交付类别：<Web UI / 服务 / 数据 / 部署 / 文档 Skill / 不适用>
   - 适用门包：<quality-appendix.md 的类别名 / ui-delivery.md / 无>
   - 完成判据：<criterion 原文>
   - 方案：design/<topic>.md（@<git 短 hash，可选>）
   - 批准：approve/APPROVED.md
   - 带进实现的未决：<列表或无>
   - driver：{slug}-driver
   ```

   Web UI 另加 [ui-delivery.md](ui-delivery.md)「交接行」四行。
3. `TASK.md` 元信息：`status: handed-off`、`phase: propose`、`driver: "{slug}-driver"`、`handed-off` 日期。
4. 在工作区根跑 `python3 <taskflow>/scripts/check_handoff.py <root> <slug>`（`<taskflow>` 是 taskflow skill 目录；子任务的 `<slug>` 写它在 `ongoing/` 下的路径 `{parent}/subtasks/{sub}`）：exit 0 才往下；不过就按它的输出补齐再跑。
5. 按 `taskflow` 脚手架建 driver（入口门已在上一步通过）：`{task}` = `{slug}`，`--goal` = 目标 + `criterion` 原文 + 方案 / 批准路径。按 [driver-template.md](../../taskflow/references/driver-template.md) 写 `.openspec.yaml`（`skip_specs: true`）与 `proposal.md`；`tasks.md` 留给 propose。
6. INDEX 行改为 `已交接：… → {slug}-driver`（留在 Ongoing 表）。
7. 桥接 stock `openspec-propose`（选继续已有 change）。

第 5 步建不成（taskflow / openspec 不可用、定不了 planning root）：元信息改回 `status: ongoing`、`phase: approve`，`driver: null`，说明缺什么。
