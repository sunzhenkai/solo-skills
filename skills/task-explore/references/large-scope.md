# 大范围拆分（附录）

默认一个任务一条线。只有一个目标里出现 ≥2 个可独立推进的方向（design 发现，或 approve 认为范围过大）时读本文件。

- **拆**：在当前任务下建子任务 `ongoing/{parent}/{sub}/`，`TASK.md` 带 `parent:`；`{sub}` 全仓唯一，只拆一层。子任务继承父判据中可拆的部分，写自己的子判据。父 `TASK.md` 加「子任务」小节登记一行，INDEX 追加 `{parent}/{sub}` 行。拆分属于记账，一句话说出决定即可。
- **父是纯伞**：只登记范围、不做与拆分原则；`status` 恒 `ongoing`，不 handoff、不建 driver。
- **子任务**走完整的 explore → design → approve → handoff，各自建 `{sub}-driver`。
- **对父点名交接**：逐个交接已批准、未交接的子任务；未批准的跳过并说明；任一失败即停，已交接的不回滚。
- **归档**：子任务都 `handed-off` 或 `archived` 后父才可归档，整树一起搬。
- 同一冻结方案里的多条实施线不拆子任务，建成 driver 的子 change。
