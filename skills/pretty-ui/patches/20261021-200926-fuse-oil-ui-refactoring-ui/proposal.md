# 正文重写：把阅读页 skill 扩展为“构建好看 UI”，融合 oil-ui 与 refactoring-ui

- target: skills/pretty-ui
- mode: update
- patch: 20261021-200926-fuse-oil-ui-refactoring-ui
- risk: high
- status: proposed

## Intent

把 pretty-ui 从“把内容做成阅读页”扩展为构建好看界面的 skill：定设计方向、建设计体系、做页面或组件、看真实截图打磨与评审，阅读页成为其中一个模式（page）。方法来自两个上游，按“地板靠规则、天花板靠方向、以画面为准”融合：

- refactoring-ui-skill 提供地板：规则镜头与扫查顺序、严重度与问题字段（每条问题带规则号）、误报与矫枉过正、默认刻度、色阶与对比度脚本。
- oil-ui 提供天花板：品类与标杆、调性刻度、生成引擎、首屏骨架、方向卡与差异检验、记忆点、隔离评审手册（三秒测试、提升三项、重做与保留）、AI 默认样貌清单、中文行长阈值。
- 两者冲突时的取舍：评审不打数字分，改为三态结论（重做 / 需改 / 通过）加带规则号的问题清单；问用户只问一次（三个文字方向加推荐），goal 模式或“你定”时自选并记理由；既有设计体系先于两边的默认值。

本轮同时修掉旧版评审中实测出的问题：旧规则鼓励“用强调色编码重点和结构”“挑选足够的组件类型”，导致彩虹徽章和组件堆砌；没有看图步骤，375 视口溢出与 CDN 图解加载失败都没被发现；宽容器里正文不限宽，中文一行远超可读长度。

非目标：taskrail 的观感验收与 ui-delivery、role-based-reviewer 的 design 角色怎样引用 pretty-ui，留到下一轮（第 4 期）各自出 patch；本轮只把它们指向已删除文件的链接改到 `direction.md`。dotfiles 编目与锁文件按用户决定以后处理。

## Conflict check

- 入站引用：taskrail `references/done.md`、两个契约测试、`evals/cases.yaml`，以及 taskflow `evals/cases.yaml` 指向 `references/frontend-design/REFERENCE.md`；本轮删除该文件，两边各开一份同时间戳 patch 改指 `references/direction.md`。
- 默认输出目录从 `docs/pretty-view-html/` 改为 `docs/pretty-ui/`；已有旧目录（含 `index.html`）且用户没指定路径时继续沿用，避免出现两个根聚合页。
- `frontend-design`（Apache-2.0）原样收录副本移除，独有内容（设计思路、反模板）已在 `direction.md` 与 `rules.md` X 组重述，`NOTICE.md` 记来源。
- `html-diagram` 保留原样收录，补上游 MIT 许可全文（此前缺失），衔接说明里的 frontend-design 改为方向卡、token 与规则。
- 移植脚本只依赖标准库，文件头写明来源与许可；`licenses/` 收两份上游 MIT 全文。
- 文本中的“taskrail Active Instance”只做指针，freeze 与摘要机制仍以 taskrail `ui-delivery.md` 为准，本轮不改它。

## Rationale

- SKILL.md 只留信条、路由、主流程、十条铁律、看图门槛、交付要求与按需读取表（约 6.9KB），细则按模式下沉到五个 reference，SKILL.md 一层直链。
- 每条铁律和 P0 都能在 rules.md 找到规则号，评审意见可追溯、可争辩；中文排版数值（正文 16–18px、行高 1.6–1.75、每行 30–40 字上限 46）按中文阅读习惯定，替代英文的 45–75 字符。
- `check_page.py` 把实测踩过的坑变成确定性检查：解析不到的本地链接、站点根 / 绝对 / file:// 路径、缺 lang / viewport / title、离线模式下的联网依赖（含脚本里的 CDN import），以及渐变文字、表情符号图标、缺焦点样式、缺减少动效处理、过小字号、颜色不走变量等提示。

## Files

- 新增：`NOTICE.md`、`licenses/{oil-ui,refactoring-ui-skill}-MIT.txt`、`references/{direction,system,rules,critique,page}.md`、`references/html-diagram/LICENSE`、`scripts/{palette,contrast,check_page}.py`、`tests/test_pretty_ui_{contract,scripts}.py`
- 重写：`SKILL.md`、`evals/cases.yaml`（保留并更新 8 条阅读页 case，新增 15 条）
- 修改：`references/html-diagram/REFERENCE.md`（许可指针、衔接说明）
- 删除：`references/organization.md`、`references/visual-components.md`（内容并入 `page.md`）、`references/frontend-design/`
- 仓库级同轮配套：README skill 表把 pretty-ui 移到新的“界面与设计”分组并改用途描述

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills tests -q`；`make check-style`（SKILL.md ≤8KB、description ≤300 字符、无深链）；`make check-names`
- 实测：用虚构素材生成阅读页，本地 http 打开，1280 / 375 截图看图并跑 `check_page.py --offline`；对改名前的旧产物跑一次 review 模式。产物放仓库外。
