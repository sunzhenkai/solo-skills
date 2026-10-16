# handoff：交接给 taskflow

把 `tasks/ongoing/{slug}` 交给 `{slug}-driver`。不写代码、不归档、不搬目录、不清绑定。之后交付进度只认 taskflow checkbox。goal 里不问是否交接，approve 收敛就直接做。

## 前提

1. 已批准：`approve/APPROVED.md` 存在，或「已做决定」写明采纳方案。没有就先 approve。
2. driver 名固定 `{slug}-driver`（子任务 `{sub}-driver`）。已存在就复用，不新建。
3. 已 `handed-off` 且 driver 存在：报告 driver 路径，不重复交接。

## 步骤

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

   Web UI 另加 [ui-delivery.md](../../taskrail/references/ui-delivery.md)「交接行」四行。
3. 按 `taskflow` 脚手架建 driver：`--goal` = 目标 + `criterion` 原文 + 上面的方案 / 批准路径。按 [driver-template.md](../../taskflow/references/driver-template.md) 写 `.openspec.yaml`（`skip_specs: true`）与 `proposal.md`；**不写 `tasks.md`**。
4. `TASK.md`：`status: handed-off`、`phase: propose`、`driver`、`handed-off` 日期；INDEX 行改为 `已交接：… → {slug}-driver`（留在 Ongoing 表）。
5. 跑 `python3 taskflow/scripts/check_handoff.py <root> <slug>`，exit 0 才算交接成立；不过就按它的输出补交接节再跑。
6. 桥接 stock `openspec-propose`（选继续已有 change）。

taskflow / openspec 不可用、或定不了 planning root：停下说明缺什么，任务保持 `ongoing` 不变。
