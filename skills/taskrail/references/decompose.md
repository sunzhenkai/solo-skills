# decompose：自动规划切片与子任务

## 目的
把总判据拆成可独立验证、可按依赖推进的交付结构，并自动建立和恢复子任务。

## 进入条件
多个可独立交付物、多项目、需要增量反馈、不同分支 / 交付节奏，或单次实施难以可靠回归。explore / design / execute 后发现这些信号也可重入。

## 跳过条件
一个连贯改动能在同一分支实施并验证；不要为了形式拆分。

## 所需输入
criterion、当前 plan、涉及仓库、已知契约与依赖。

## 执行方法
1. 先列交付边界和集成项，再判断不拆 / 切片 / 子任务。必须原子落地的是切片；能按契约独立交付的可作有依赖子任务。
2. 写 `ROADMAP.md`：项、类型、目标、子判据、涉及仓库、依赖、交付边界。子判据合计覆盖总判据，依赖无环。
3. 对每个子任务立即创建轻量 pending TASK；使用：

   ```bash
   python3 <taskrail>/scripts/task_state.py init <workspace> <child-id> --title "<目标>" --criterion "<子判据>" --parent <parent-id>
   ```

   已存在则核对是否同一项，不覆盖、不复制。子任务只拆一层，其内部再拆为切片。
4. 父任务成为协调容器：不直接写业务代码、不持实施 driver。共享契约放父 design；每子任务独立选 direct / OpenSpec。
5. 自动推进依赖已 done 的就绪项；将 pending 子任务置 active / plan。正在做的优先，其次按 ROADMAP 顺序；用户点名则照办。
6. 子任务 blocked 只停其依赖链。新增独立交付可追加 roadmap / pending TASK；已完成项不改写，criterion 变化先回 intent。

## 产出
ROADMAP.md、`subtasks/<child>/TASK.md` 及热文档、父 TASK 的下一动作和路由记录。

## 完成门
所有项有子判据与交付边界，依赖无环，目录与 roadmap 一致，下一就绪项明确；没有可执行项且无阻塞时才回 plan 修正。

## 退出与重入
父任务选就绪子任务；全部子任务 done 后父任务进 verify 做集成与总判据验证。resume 先核对 roadmap 与部分创建的目录，再幂等补齐。

## ROADMAP 模板

```markdown
| 项 | 类型 | 目标 | 子判据 | 涉及仓库 | 依赖 | 交付边界 |
|---|---|---|---|---|---|---|
| api | 子任务 | 提供异步导出 API | 可创建并查询任务 | backend | contract | 独立 API 分支 |
| web | 子任务 | 接入异步导出 | 可下载完成文件 | web | api | 独立 Web 分支 |
| integration | 集成项 | 验证跨仓主流程 | 大数据端到端通过 | backend, web | api, web | 父任务验收 |
```

`contract` 可为设计准备项，不一定是代码子任务；集成项由父任务执行，不另建子任务。
