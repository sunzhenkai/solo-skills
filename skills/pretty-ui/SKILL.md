---
id: pretty-ui
name: pretty-ui
description: 通用 UI 设计、实现与评审引擎：定设计方向、建设计体系（token、组件）、做页面或组件、看真实截图打磨与评审、做 UI 工程化检查，或把已有内容做成静态 HTML 阅读页。用户点名 pretty-ui 时使用。
---

# Pretty UI

做出一眼看得出被设计过的界面。三条信条贯穿所有模式：

- **地板靠规则**：按 [rules.md](references/rules.md) 扫查层级、间距、排版、色彩、对比和状态，每个问题都指得到规则号。
- **天花板靠方向**：从品类、受众和内容推出北极星与方向卡，集中做一个记忆点，其余安静。
- **以画面为准**：看过真实截图才算看过；源码一致不代表好看。

方向、取值和取舍由本 skill 定：陈述句写决定和理由，接着做。

## 路由

| 请求 | 模式 | 做法 |
| --- | --- | --- |
| 点名改色、调间距、改文案、删元素 | 小改 | 直接改；动布局/浮层/状态先对 [guardrails.md](references/guardrails.md) 自查，动样式看目标视口改动处与相邻元素；报遮挡、缺线、看不清的转 refine |
| 单组件打磨、小范围改版 | build 轻量 | 写轻量方向卡，跳过主流程第 3 步；对照 guardrails.md 防错，基础档看图，按 critique.md 自查 |
| 新界面、整体改版、照参考图还原 | build | 走主流程；照图还原以参考图为方向，同视口并排比到位 |
| 已有界面不好看、要优化 | refine | 截图诊断带规则号的问题，按序修复并对照 guardrails.md 自查，沿用既有体系，交付前后对比 |
| 只要评审 | review | 只读，不改文件；按 [critique.md](references/critique.md) 出问题清单 |
| 设计系统、工程化检查、token / 组件统一、UI 架构优化 | system | token 按 [system.md](references/system.md)；工程化按 [engineering.md](references/engineering.md) |
| 文件、报告、方案做成浏览器阅读页 | page | 按 [page.md](references/page.md) 从模板落盘，写轻量方向卡 |

混合意图按顺序串起来并说明，例如没有设计系统的项目里做设置页，就是 system 再 build。脚手架先 project-init；多角色评审走 role-based-reviewer；以图为主的讲解页或独立架构 / 流程 / 时序图优先交 `visualize`（本 skill 承接文字为主的阅读页与降级图解）。

## build 主流程

每步达到“完成”再进下一步。

1. **探测**：技术栈、已有 token / 组件库 / 品牌规范、暗色模式、交付形态。完成：设计说明列出沿用什么、缺什么。
2. **简报**：用户、主任务、真实内容、设备；内容分主 / 次 / 辅，动作分一个主操作、几个次要、若干辅助。完成：主任务和主操作各一句，目标视口按 evidence.md 选定并记录。
3. **方向**（未定才做）：按 [direction.md](references/direction.md) 自选一个方向，写方向卡和理由，直接说决定、接着做。已有品牌、参考图或明确风格时只补方向卡缺栏；用户点名要多个方案时才出三个候选。完成：方向卡各栏具体，过了两遍法。
4. **体系**：按 system.md 取值；新色阶用 `scripts/palette.py`，真实文字 / 背景配对用 `scripts/contrast.py` 校验。完成：配对都达标。
5. **构建**：先按 [guardrails.md](references/guardrails.md) 避开布局、浮层、状态与交互硬伤，写出代表页或关键流程，再按“灰度层级 → 间距分组 → 行长节奏 → 色彩 → 深度 → 收尾”自查；空、加载、出错状态和真实感数据随功能完成。完成：代表页能在目标视口打开。
6. **看图**：按 [evidence.md](references/evidence.md) 截基础档并量测，修掉重叠、裁切、溢出和孤字。完成：量测无越界，`check_page.py` 无报错。
7. **批评**：新界面和整体改版派隔离评审，制作者只做减法、眯眼看和处理检查结果；否则按 rules.md 完整扫查。怎么改、何时停按 critique.md「迭代与停止」，那一节是唯一标准。

## 轻量方向卡

page、build 轻量和上游计划的“视觉方向”用它：北极星、字体、色彩三层（底色、主强调色、派生态）与来源、一个特征元素，再列参照（作品或既有页面，写清取它哪一点）和放弃什么。新产品和整体改版写 direction.md 第 6 节的完整方向卡。

## 十条铁律

每个任务都适用，阈值以 rules.md 为准：

1. **每屏一个主角**：强调靠压低旁元素（H1）。
2. **先灰度后上色**：字号、字重、明度和留白先分层，颜色只做强调和语义状态（H2、C3）。
3. **取值来自刻度**：字号、间距、色阶、圆角、阴影、边框从体系取，缺就先补 token（S2、T1、C1）。
4. **组外距离大于组内**：标题贴近下文，标签贴近自己的控件（S3）。
5. **正文限宽**：中文每行约 30–40 字（上限 46）；宽表格、代码、图解在自己的容器里用满宽或横向滚动（T2、S4）。
6. **可读是门槛**：中文阅读页正文 16–18px，正文对比度至少 4.5:1（T4、C4）。
7. **有色底上用同色相降对比**；含义同时由文字或图标承载（C6、C5）。
8. **结构即信息**：编号、眉标、卡片、标签只编码真实语义；一处分隔只用一种手段（S9、X8、X9）。
9. **内容像真的**：用真实长度的数据和说清动作的按钮文字，只呈现输入里真实存在的事实（F6、X11）。
10. **既有体系优先**：沿用项目 token、组件、品牌色、字体和命名；与刻意约定冲突时约定先行，并在交付说明写明。

## 看图与确认

- 截图与量测按 evidence.md：响应式验桌面 1280 / 手机 375，首轮首屏、交付整页。无法截图时标“未渲染验证”，问题标 `code-only`。
- 静态页面跑 `python3 scripts/check_page.py <路径>`（相对本 skill 目录）：报错修好再交，提示逐条改掉或在交付说明写理由。
- **goal 模式或无人值守**：不停下等确认；隔离评审者（另一个模型）对照参照页看改前改后截图下结论，按结论迭代。
- **human 模式**（独立使用默认）：评审后把改前改后截图交给用户，用户说可以才算完成。
- 截图、设计说明和评审记录放任务目录或项目约定位置，本 skill 目录保持只读。

## 交付

说明方向与理由（或沿用的体系）、改动与未做项、截图与证据路径、评审方式 / 轮次 / 结论、减法删了什么、未验证项。

## 按需读取

| 文件 | 何时读 |
| --- | --- |
| [references/direction.md](references/direction.md) | 完整方向卡、多个方案 |
| [references/system.md](references/system.md) / [engineering.md](references/engineering.md) | 体系、补 token、工程化 |
| [references/guardrails.md](references/guardrails.md) | 写代码前与改完布局、浮层、交互后的防错自查 |
| [references/evidence.md](references/evidence.md) | 截图档位、打开方式、量测 |
| [references/rules.md](references/rules.md) | refine、review、完整自查 |
| [references/critique.md](references/critique.md) | 自查、隔离评审、问题清单、迭代停止 |
| [references/page.md](references/page.md) | page 模式 |
| [assets/reading-page.html](assets/reading-page.html) | 阅读页模板 |
| [references/html-diagram/REFERENCE.md](references/html-diagram/REFERENCE.md) | 架构、流程、关系、状态、时序等图解 |

来源与许可见 [NOTICE.md](NOTICE.md)。经验沉淀与正文演进走 `skill-upgrader`。
