# Result

- target: skills/pretty-ui
- mode: update
- patch: 20261021-200926-fuse-oil-ui-refactoring-ui
- risk: high
- status: applied
- applied-at: 2026-10-21T20:22:12+08:00

## Validation

- `git apply --check --recount`: pass（在仓库外的干净副本上应用：改前树 + change.patch 与候选树逐文件一致）
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/pretty-ui/tests -q` → 40 passed；全量 `python3 -m pytest skills tests -q` → 450 passed, 3 skipped；`make check-style` → OK（0 条告警，SKILL.md 约 6.9KB）；`make check-names` → OK
- privacy check: pass（实测素材是虚构的 `evals/fixtures/beacon-ttl`；对旧产物的评审记录留在仓库外）
- mode check: pass

## 实测

产物、截图与评审记录都在仓库外。

- **page 模式**：用虚构素材生成一页事故复盘阅读页，按流程写轻量方向卡、跑 `check_page.py --offline`（0 报错 0 提示）、本地 http 打开、1280 / 375 截图并量行长。自查改掉 6 处，其中 4 处是通用缺口，已补进正文后重新生成本 patch：
  - 正文列宽写成 `em` 时，小字说明按自己的字号算、比正文窄一截 → `page.md` 改为用 `px` 或 `rem` 写在列容器上，`system.md` 同步。
  - 代码字体的连字把 `<=` 显示成别的符号；标题末行孤字；元信息之间的 `/` 换行后悬在行首 → `page.md` 加「换行」条和关连字。
  - 页面开了平滑滚动，截到滚动中途 → `critique.md` 取证加「滚动截图」。
  - 深色主色生成的 900 不够深、语义色浅底漂到邻近色相 → `system.md` 写明 `--darkest` 与 `--cap` 的用法。
- **review 模式**：对一份改名前生成的旧阅读页跑评审。`check_page.py` 确定性地复现了旧版评审里手工发现的问题（运行时从 CDN 加载图解、10–11px 小字、中文页面里的英文大写标签、颜色不走变量）；渲染后看到时序图只剩 “Syntax error in text”，规则里没有对应条目，于是新增 **I6**（图解随页面交付）并列入 P0。结论「需改」，8 条问题都带规则号，另有一行「保留：」。

## Notes

- 同轮配套：taskrail、taskflow 各一份改链接 patch（同一时间戳）；README 的 skill 表新增「界面与设计」分组（仓库级，不属于任何 skill）。
- 下一轮（第 4 期）：taskrail `done.md` / `ui-delivery.md` 与 role-based-reviewer design 角色改为引用本 skill 的方向卡、体系产出与规则号，各自出 patch。
- 仓外待办：dotfiles 编目与锁文件仍写 `pretty-view-html`，按用户决定以后处理。
