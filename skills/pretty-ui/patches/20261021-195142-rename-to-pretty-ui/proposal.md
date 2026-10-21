# 改名 pretty-view-html → pretty-ui（机械改名）

- target: skills/pretty-view-html（改名后为 skills/pretty-ui）
- mode: update
- patch: 20261021-195142-rename-to-pretty-ui
- risk: medium
- status: proposed

## Intent

把 skill 的 id、name、目录名和标题从 `pretty-view-html` 改为 `pretty-ui`，为下一轮把它扩展成「构建好看 UI」的 skill 铺路。本轮只换名字：正文里的自引用（organization / visual-components 的回链、两份 vendored 参考的适配说明、evals 的 `skill:`、两份虚构素材里的 skill 名）同步改名。

非目标：行为不变。默认输出目录 `docs/pretty-view-html/` 本轮保留（改默认目录属于行为变化，放到正文重写那一轮，并带旧目录兼容规则）；工作流、视觉规则和完成检查一字不改。

## Conflict check

- 入站引用：taskrail `references/done.md` 与两个契约测试、taskflow `evals/cases.yaml` 引用了 `pretty-view-html/references/frontend-design/REFERENCE.md`，各自另开 patch 同轮改路径；README 的 skill 表同轮改名。
- `patches/` 历史随目录整体迁移（`mv`），不进 change.patch（协议不允许 patch 触及历史记录）；历史记录里的旧名保持原样。
- change.patch 的路径同时出现旧前缀和新前缀，这是改名本身决定的，属于协议「路径前缀为 `<skill-dir>/`」的必要例外。

## Rationale

纯改名，可用 grep 确定性验证：除默认输出目录外，仓内生效文件不再出现 `pretty-view-html`；全量测试保持通过。

## Files

- `skills/pretty-view-html/**` → `skills/pretty-ui/**`（不含 patches/）
- `skills/pretty-ui/SKILL.md`：id、name、标题
- `skills/pretty-ui/references/{organization,visual-components}.md`：回链文字
- `skills/pretty-ui/references/{frontend-design,html-diagram}/REFERENCE.md`：适配说明里的父 skill 名
- `skills/pretty-ui/evals/cases.yaml`、`evals/fixtures/*/SOURCE.md`：skill 名

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`rg pretty-view-html` 只剩默认输出目录与历史记录；`python3 -m pytest skills tests -q`；`make check-style`、`make check-names`
