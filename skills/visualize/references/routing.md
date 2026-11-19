# 下游路由

[visualize](../SKILL.md) 第 3 步读本页：按简报的主形态和约束选定一个主下游，探测可用性，不可用时沿降级链往下选。

## 1. 单图还是讲解页

先按读者问题选第 2 节的形态，形态决定下游。指向 archify 的形态出单图，材料来自一次复盘或评审也一样：故障时间线是 `timeline`，不是讲解页。

- **单图**：读者问题能被一张结构图回答 → archify。来自仓库证据、要列全 ER 字段、要分享深链的结构图同样走 archify，由它的校验门禁兜住结构正确。
- **讲解页**：读者问题要的是结论与证据、取舍或一组数字，单张结构图回答不了 → visual-explainer。
- 讲解页里需要一张严格校验的结构图时，由 archify 单独出图放进子目录，讲解页用相对链接指向它；两套渲染各出各的文件。

## 2. 形态 → 下游

| 主形态 | 读者问题 | 下游 |
| --- | --- | --- |
| 拓扑 / 架构 | 由哪些部分组成，谁连谁，边界在哪 | archify `architecture` |
| 流程 | 先做什么后做什么，哪里分叉、谁审批 | archify `workflow` |
| 时序 | 谁调用谁，来回几次，在哪返回 | archify `sequence` |
| 数据流 | 数据从哪来、经过哪些加工、给谁用 | archify `dataflow` |
| 状态 | 现在处于什么状态，怎么流转、何时终止 | archify `lifecycle` |
| 实体关系 | 有哪些表或实体，键和基数如何 | archify `erd` |
| 类型契约 | 类、接口与它们的依赖、继承 | archify `class` |
| 层级 | 单父包含关系，如模块树、能力拆解 | archify `tree` |
| 时间线 | 事件何时发生，按来源分道 | archify `timeline` |
| 耗时 | 一次请求或运行的时间花在哪 | archify `waterfall` |
| 对比 / 取舍 | 选哪个，差在哪 | visual-explainer |
| 数量 | 多大、多少、占比、趋势 | visual-explainer（archify 不画数值图表） |
| 概念讲解、评审、复盘 | 是什么、怎么运作、结论与证据 | visual-explainer |

archify 类型拿不准时，运行 `node <archify>/bin/archify.mjs guide "<场景>" --json`。

## 3. 探测可用性

1. 找到下游目录：宿主列出的可用 skill 里有它，或在常见 skill 目录找到 `<id>/SKILL.md`——`~/.agents/skills/`、`~/.claude/skills/`、`~/.cursor/skills/`、`~/.codex/skills/`，以及项目内的 `.agents/skills/`、`.claude/skills/`。下文 `<archify>`、`<visual-explainer>` 指找到的目录。
2. 运行 `node --version`：archify 要求 18 及以上，visual-explainer 的渲染同样需要 Node.js。
3. 下游自检：archify 运行 `node <archify>/bin/archify.mjs doctor`，末行为 `Archify is ready.`；visual-explainer 确认 `<visual-explainer>/kit/render.mjs` 存在。

这三项只用于 archify 与 visual-explainer，都通过才算可用。`pretty-ui` 找到其 `SKILL.md` 即可用；Mermaid 源码不依赖安装。

## 4. 降级链

| 选定 | 不可用时依次改用 |
| --- | --- |
| archify 单图 | visual-explainer 单图页（One diagram 形态）→ `pretty-ui` page 模式手画图解 → Mermaid 源码 |
| visual-explainer 讲解页 | `pretty-ui` page 模式（阅读页 + 图解，结构图仍可由 archify 出）→ Markdown + Mermaid |

- 降级到 `pretty-ui` 时，页面以文字为主、图解为辅，在「读法」里写明。落到阅读页或 Mermaid 之前，按 SKILL.md 第 3 步先问用户。
- 只剩 Mermaid 时，交付 `<slug>.mmd` 源码与渲染方式，核对行写「未渲染验证」。
- 缺失的下游：在「读法」里说明用途和补齐方式，用户同意后走 `skills-store` 先审计再安装。archify 用 `npx skills add tt-a1i/archify -s archify`；visual-explainer 按其 README 把仓库的 `plugins/visual-explainer/` 复制到当前 agent 的 skill 目录。缺的是 Node.js 时，写明 archify 要 18 及以上、visual-explainer 渲染需要 Node.js，安装方式指向 nodejs.org。

## 5. 调用要点

只列与本 skill 衔接的部分；字段、示例和修复细则以下游当版 SKILL.md 为准。

### archify

- 输入：简报的结论句、事实清单和省略项；仓库证据图按其 repository authoring 细则读源码。
- 输出：`<输出目录>/<figure>/`，`candidate.json` 与 `<figure>.html` 同目录；`meta.output` 写相对工作目录的路径。
- 门禁：`node <archify>/bin/archify.mjs finalize <type> <candidate.json> <output.html> --quality showcase --json`，仓库证据图加 `--repo-root <repo>`。非零退出即失败，按其修复流程处理，修复轮使用它要求的 `--out-dir`。
- 看图：finalize 通过不代表看过画面；需要看图时按其 Optional capture evidence 截图到 `<figure>/visual-check`。

### visual-explainer

- 输入：简报的结论句作首屏，事实清单作每张图的标签来源。
- 输出：`<输出目录>/<slug>.src.html`，渲染为同目录的 `<slug>.html`。
- 门禁：`node <visual-explainer>/kit/render.mjs <slug>.src.html`（需要预览时加 `--open`）；修完它列出的每个 `✗`，有截图拼版 `<slug>.sheet.png` 时看一遍，再过它的 Before delivery 清单。
- 风格：沿用它的 register 与 style guide；项目有设计体系时按它的优先级「用户要求 → 项目设计体系 → style guide」。
- 离线：页面引用 Chart.js、three.js、Mermaid 等库时依赖 CDN；简报要求离线时，选用它自带的手绘 SVG 与内置图形组件。
