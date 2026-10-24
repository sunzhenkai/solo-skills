# handoff：仅 OpenSpec 执行的入口门

只有 `execution: openspec` 时读本文件。direct 不建 driver、不走本门。OpenSpec 内容始终在 workspace，代码仍在各修改仓 worktree。

## 前提

- criterion 非空，当前 plan / design 指针可用，driver 为 `<task-id>-driver`。
- 有 approve 要求时 `reviews/APPROVED.md` 或旧 `approve/APPROVED.md` 已存在；无需 approve 时记录理由。
- 同名 driver 已存在时先核对属于当前任务，复用而非新建。

## 步骤

1. 在 TASK「## 交接」写指针与判据，不复制完整方案：

   ```text
   - 交付类别：<Web UI / 服务 / 数据 / 部署 / 文档 Skill / 不适用>
   - 适用门包：<类别 / 无>
   - 完成判据：<criterion 原文>
   - 方案：<PLAN.md / design 路径>
   - 批准：<reviews/APPROVED.md、approve/APPROVED.md 或 not-required: 理由>
   - 带进实现的未决：<列表或无>
   - driver：<task-id>-driver
   ```

   Web UI 另加 ui-delivery 的交接行。
2. 用热状态脚本写 `status: active`、`current_ref: execute`、`execution: openspec` 和 driver；不写 handed-off / phase。
3. 在 workspace 跑：

   ```bash
   python3 <taskflow>/scripts/check_handoff.py <workspace> <task-path>
   ```

   子任务 task-path 为 `<parent>/subtasks/<child>`；exit 非 0 先补齐，不绕过。
4. 按 taskflow 脚手架在 workspace 建 driver，`.openspec.yaml` 写 `skip_specs: true`，proposal 含 Driver 协议；tasks.md 留给 propose。
5. 建不成时保持 active，current_ref 回 plan / approve，driver 置 null，记录缺失依赖；不改成 done，不影响其他就绪子任务。

用户原话明确要求绕过 taskrail 时仍可按 taskflow 的 gate_bypass 规则；理由只能照录原话。
