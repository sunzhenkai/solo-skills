# 台账：布局、索引、绑定

写 `INDEX.md` / `TASK.md` 或绑定任务前读。目录与元信息字段以 [契约](contract.md) 为准。

## 布局

- `TASKS_ROOT` = 当前仓库根下 `tasks/`；没有就直接建，一句话说明。
- `{slug}` kebab-case，由输入推断，不追问；描述为空才问要做什么。
- `tasks/INDEX.md` 是唯一允许的根级任务文件；评审、委派回收等产物只写绑定的 `{taskRoot}`。
- 是否把 `tasks/` 纳入 git 由项目决定，不改 `.gitignore`。

## 索引

- 单任务真相只在 `TASK.md`；列出、选择、搜索任务先读 INDEX。
- 建任务、保存进展、approve、handoff、archive、reopen 时同步对应行：任务名、标题、日期、一句话目标、相对 `tasks/` 的路径。不抄进展日志。
- 漂移（目录有索引无，或索引指向不存在的路径）：按 `ongoing/` 与 `archive/` 下的 `TASK.md` 重建。
- `handed-off` 行的一句话以 `→ {slug}-driver` 结尾。

## 绑定

会话绑定 `{slug}` + `{taskRoot}` = `tasks/ongoing/{slug}`。

1. 读 INDEX 的 Ongoing 表（无或漂移就重建）。
2. 自行判定：同一件事 → 恢复它；无关 → 新建；用户只说「继续」→ 恢复最近更新的那项，它属于拆过的任务时按 [large-scope.md](large-scope.md)「续跑」取下一个就绪项。用户点名了对象就照办。
3. 一句话说出决定和理由，记入「已做决定」，直接往下走。

同名 `ongoing/{slug}` 已存在时不覆盖：同一件事就恢复，否则换名并说明。

## 新建与保存

- 新建：按 [templates.md](templates.md) 建 `TASK.md`，填已知目标与元信息；上游有方案就登记进「方案」节，没有判据不编造。INDEX 追加一行。
- 保存进展：合并本轮进展，不抹掉仍有效的旧内容；改 `updated`；同步 INDEX 行。无新进展就不写。

## 恢复

读 `TASK.md`、`design/`；已 `handed-off` 的按 [契约「交接后的位置」](contract.md)从 driver 状态推导并回写 `phase`；拆过的任务再读路线图与各子任务的 `TASK.md`。按 [user-report.md](user-report.md) 的四行汇报。任务不在 `ongoing/` 就查 Archived 表与 `tasks/archive/`，告知路径，拉回走 reopen。
