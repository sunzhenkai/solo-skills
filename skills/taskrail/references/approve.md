# approve：按需批准方案

## 目的
在大型项目、重大改动、架构调整、难逆高风险、用户指定或重要外部行为变化时，先用人话对齐方案并获得明确放行。

## 进入条件
大型项目 / 新建子系统；重大重构或架构 / 公共契约调整；用户要求审批；方案难逆 / 高风险；改变 criterion 或重要外部行为；父任务子任务超出 ROADMAP 范围。不因改动在 git 分支内可逆或属于同任务内部切片而跳过。

## 跳过条件
仅限小范围、沿用既有架构的可逆改动且用户未要求审批。子任务在父 ROADMAP 范围与子判据内，由父批准覆盖，不逐个停。

## 所需输入
criterion、不做、推荐方案、验证策略、未决与回滚；无 design 需要时可用 PLAN。

## 执行方法
1. 自查判据可检查、方案走得到判据、ROADMAP 子判据覆盖总判据且依赖无环。
2. human 及命中大型项目 / 重大改动 / 架构调整的首次 goal 方案：按 [confirm-protocol.md](confirm-protocol.md) 与 [user-report.md](user-report.md) 用人话呈现整体方案、关键取舍、影响面与回退，停等用户明确放行；用户本会话原话明确豁免方案对齐的 goal（须照录原话）或非重大 goal，派异源模型审，收敛即放行。
3. 写 `reviews/APPROVED.md`（兼容旧 `approve/APPROVED.md`）：结论、确认 / 豁免依据（用户确认或原话豁免 / 异源审）、方案路径、评审路径、未决和适用范围。
4. 决定写 decisions.md，旧决定用 superseded 关联。

## 产出
批准文件与路由记录。若本任务选择 OpenSpec，handoff 引用该文件；未选 OpenSpec 不强制 handoff。

## 完成门
human 明确放行，或 goal 已取得首次重大方案用户放行（或原话明确豁免后异源审无 P0 / P1）且非重大审阅无 P0 / P1，批准文件落盘且范围与当前 plan / design 一致。

## 退出与重入
返回 router 选择 decompose / execute。范围或判据变化时重新 approve；同一 P0 / P1 两轮未解按真阻塞停。
