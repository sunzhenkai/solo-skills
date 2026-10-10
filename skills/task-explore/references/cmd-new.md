# `new` 命令

原 SKILL 小节迁移至此。进入本命令后执行。

## `new`

1. 若没有 `tasks/`：**询问是否在当前位置创建 `tasks/`**。未确认则停止。
2. 推断 `{task-name}`。冲突则列出已有任务并问 resume 还是换名。在已有任务下拆子方向不属于 `new`，走 `split`。
3. 创建 `tasks/ongoing/{task-name}/TASK.md`（用模板，填已知目标与 `phase`/`confirm_mode`/`tier`/`criterion` 元信息）。输入含现成方案（含上游 taskrail wizard 的流程总览方案）时，把完成判据、事实、假设、质量属性、流程总览、阻塞点、坑一并登记进「方案」小节，并可落 `wizard/plan.md`，不丢上游产物。输入里没有完成判据时不要编造。
4. 在 `tasks/INDEX.md` 的 Ongoing 表追加一行（无 INDEX 则按模板创建或按目录重建）。
5. 绑定该任务。报告路径，询问下一步：`explore`（默认建议）还是 `chat`。不要自动开始 grill。
