# solo-code-review 接入 OCR v1.12 能力（单 commit / delegate fallback / 新 flag）

- target: skills/solo-code-review
- mode: update
- patch: 20261016-122203-ocr-v1-12
- risk: medium
- status: proposed

## Intent

把 skill 对齐到本机已装的 OCR v1.12.9，接入 review 时确认的差距（不改主干流程）：

1. **单 commit 审查**：新增 mode=commit，`ocr review -c <hash>`；reviewctl change-name 支持 `--commit`，review.md frontmatter/Meta 渲染 commit 字段。
2. **delegate fallback**：`ocr llm test` 失败从「硬停」改为二选一——配置 LLM，或按新增 `references/delegate-mode.md` 走委托模式（OCR 做文件筛选/规则解析，当前 agent 出审查），产物与确认门不变。原「不要用通用 agent 逐文件替代」的表述改为「delegate 模式须由用户选择且以 ocr delegate preview/rule 为准」。
3. **新 flag 接入**：`-o/--output` 原生落盘（替代 shell 重定向）、`--effort`、`--exclude`、`--max-tokens-budget`、`--resume`、`-B/--background-file`、`ocr session export`（回放）、CLI 版本过低时的升级提示。
4. **severity 映射**：reviewctl normalize_comments 分级次序改为 显式 priority > severity(critical/high/medium/low→P0~P3) > 内容启发式（delegate 模式与新版 OCR 输出都带 severity）。
5. **scan 边界**：正文明确「无 diff 的全仓静态扫描直接用 ocr scan，不经本 skill」。
6. **配套**：evals/cases.yaml 追加 commit-mode-scope、delegate-fallback-when-no-llm 两条 case；新增 tests/test_skill_contract.py（SKILL.md 与 delegate-mode.md 的文本契约，覆盖确认门、fetch-only、凭据禁令、评论确认门、产物落点、总结打印）；tests/test_reviewctl.py 增补 commit 命名、severity 映射、commit 模式落盘用例。

非目标：不改 MR/PR fetch 编排、确认门结构、产物目录布局、总结打印协议；不接 CI 集成与 MCP/viewer。

## Conflict check

- 相邻 skill 无冲突：commit-push / repo-manager 只把「diff 级评审」指回本 skill，职责不变。
- 上游官方 open-code-review-delegate skill 存在，但本仓不安装它；delegate-mode.md 是内嵌精简版，落点与确认门沿用本 skill 的台账协议，与上游插件互不干扰。
- frontmatter description 增「单个 commit」触发词，仍 <300 字符（225）。
- 与 self-upgrade 轮（20261016-114928）无重叠：本轮不动 examples/experience。

## Rationale

- 单 commit 审查是 review 中确认的 P1 差距：`ocr review -c` 原生支持，skill 此前只能落到整分支 diff。
- delegate fallback 修复「LLM 未配置即死路」：OCR 官方给 host-agent 的路径正是 delegate（无需 OCR 侧 key）。
- severity 映射有实测依据：v1.12.9 JSON comments 带 severity 字段（zread 文档 + 本机 --help 印证），启发式正则只兜底。
- 全部 flag 以本机 `ocr review --help` / `ocr delegate --help` 实测为准；delegate preview/rule 的 JSON 输出结构已在本机跑通验证。
- 8KB 指导线：正文压缩（GitLab 认证段合并、命令示例改 mode→flag 表、MUST 节去重复命令块）后 8188 B。

## Files

- skills/solo-code-review/SKILL.md — 正文更新（description、前置、范围表、跑 ocr、落盘、总结、边界）
- skills/solo-code-review/references/delegate-mode.md — 新增，delegate 模式七步细则
- skills/solo-code-review/scripts/reviewctl.py — severity 映射、change_name commit 支持、渲染 commit 字段、CLI 参数 --commit
- skills/solo-code-review/tests/test_reviewctl.py — 增补 3 个用例
- skills/solo-code-review/tests/test_skill_contract.py — 新增文本契约测试
- skills/solo-code-review/evals/cases.yaml — 追加 2 条 case

## Validation

- 应用前：`git apply --check --recount` 通过；b 树 pytest 31 passed；SKILL.md 8188 B ≤ 8192；禁令词 4 处（0.5/KB）
- 应用后：`python3 -m pytest skills/solo-code-review/tests -q` 全绿；`make check-style` 无告警；grep 检查引用 delegate-mode.md 的路径存在
