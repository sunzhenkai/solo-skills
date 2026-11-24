# 滚动条体验、模板护栏对齐与静态检查/脚本增强

- target: skills/pretty-ui
- mode: update
- patch: 20261125-001000-scrollbar-and-review-fixes
- risk: low
- status: applied

## Intent

1. 落地滚动条美观性与体验闭环：细化（约 6px）、平时完全隐藏、滚动时平滑淡入、停滚后淡出（`@property` + `.is-scrolling` + `color-scheme`），并用 `scrollbar-gutter: stable` 与透明占位轨道防止显隐挤压已有元素。
2. 对齐阅读页模板 `reading-page.html` 与 `guardrails.md`（`color-scheme: light dark`、`scroll-margin-top`、`overflow-wrap: break-word`、`--z-sticky`、细滚动条与零挤压）。
3. 统一热区最小尺寸口径（`24×24px` 为 P0 底线，常规/移动端建议 `≥40×40px`），补充 `dvh` 安全区与 `z-index` 层级刻度。
4. 修复 `check_page.py` 漏扫本地外部 CSS 与 `[C1]` 误报，并新增滚动条反模式与暗色 `color-scheme` 提示；增强 `contrast.py` 支持 `rgba()` / 8 位 hex 合成对比度；增强 `evidence.md` 量测脚本输出溢出元凶、移动端偏小热区与缺失 `scroll-margin-top` 提示。
5. 增补 `evals/cases.yaml` 与单元测试覆盖上述改动。

## Files

- `skills/pretty-ui/SKILL.md`：`build 轻量` 与 `refine` 路由补齐 `guardrails.md` 衔接（7707 B < 8192 B）。
- `skills/pretty-ui/references/guardrails.md`：新增 `G-L5`（滚动条细化、平时隐藏/滚动显示与零挤压）与 `G-L6`（`100dvh`、安全区与截断补全）。
- `skills/pretty-ui/references/rules.md`：统一 `S8` 热区口径，`C9`/`F1`/`F5` 纳入 `color-scheme` 与滚动条，补充两条误报条目。
- `skills/pretty-ui/references/system.md`：补 `z-index` 层叠刻度、`scrollbar-gutter` 与滚动条/暗色 `color-scheme` 语义变量说明。
- `skills/pretty-ui/references/evidence.md`：量测脚本增加 `溢出元凶`、`移动端偏小热区`、`缺锚点留白`。
- `skills/pretty-ui/assets/reading-page.html`：内置细滚动条（平时隐藏、滚动显示）、`scrollbar-gutter: stable`、`color-scheme: light dark`、`scroll-margin-top`、`overflow-wrap: break-word`。
- `skills/pretty-ui/scripts/check_page.py`：支持扫描本地外链 `.css`、修复 `@property` 与黑白阴影 `[C1]` 误报、增加 `[G-L5]` 与 `[C9]` 提示。
- `skills/pretty-ui/scripts/contrast.py`：支持 `#rgba`/`#rrggbbaa`、`rgb()`/`rgba()` 与 `rgb(r g b / a)` 背景合成对比度。
- `skills/pretty-ui/evals/cases.yaml`：新增 4 条评估案例。
- `skills/pretty-ui/tests/test_pretty_ui_contract.py` & `skills/pretty-ui/tests/test_pretty_ui_scripts.py`：同步契约与脚本单测。
