---
id: pretty-view-html
name: pretty-view-html
description: 把已有上下文、文件、报告、方案或评审内容整理成适合浏览器阅读的静态 HTML 阅读页（单页或多页）。用户要求生成 HTML、网页阅读页、漂亮的 HTML 文档时使用。
---

# Pretty View HTML

把用户提供的上下文或文件转成美观、简洁、优雅且适合阅读的 HTML 文档。保留原内容的事实、术语和层次；可以重组信息以改善阅读，只表达输入里真实存在的内容。产物是可离线打开的阅读页；真实网站、组件开发或需部署的页面交给前端开发流程，独立图表产物交给对应图表 skill。

默认输出到 `docs/pretty-view-html/`。用户指定其他路径时，以用户要求为准。

## 工作流

1. 阅读全部输入，确认主题、读者、内容边界与主要阅读任务。
2. 检查现有根聚合页和相关输出的标题、摘要与路径，判断是否存在可与本次内容共同维护的相同主题。
3. 若发现相同主题，先按 [references/organization.md](references/organization.md)「同主题内容包」提出归类方案，用户明确确认后再写入、移动或覆盖 HTML（重组会改动已有路径）。没有可靠同主题内容时直接继续。
4. 判断单页或多页。默认单页；只有内容由多个可独立阅读、分享或维护的主题组成，或用户明确要求时才拆成多页。篇幅长本身不是拆页理由。目录布局、相对链接计算与同名处理按 [references/organization.md](references/organization.md)。
5. 生成前读取 [references/frontend-design/REFERENCE.md](references/frontend-design/REFERENCE.md)，按本次主题确定配色、字体、版式和一个克制的视觉特征；导航、表达组件与阅读布局按 [references/visual-components.md](references/visual-components.md)。
6. 若内容需要架构图、流程图、关系图、状态图、时序图或其他 diagram，先读取 [references/html-diagram/REFERENCE.md](references/html-diagram/REFERENCE.md)，按其模型选择与绘制原则生成，并嵌入当前阅读页（默认不另建独立 diagram 文件）；图解配色与页面壳层使用同一套为本次内容选定的视觉语言。优先 HTML/CSS/SVG；仅在信息规模确需时使用 Canvas/WebGL，且保持可离线打开。
7. 直接生成可在浏览器打开的 `.html`；输入 Markdown 只是内容来源，不需要另建 Markdown 副本。
8. 更新内容入口与根聚合页（[references/organization.md](references/organization.md)「根聚合页」），然后逐条过下方完成检查。

## 完成检查

- 输入中的核心事实、代码、表格、术语和结论没有遗漏或篡改。
- 页面没有溢出、遮挡、过小文字、失效资源或明显的模板化装饰。
- 单页可返回根聚合页；多页具有包首页、完整页面地图和一致导航。
- 根 `index.html` 已包含本次内容的唯一入口。
- 发现同主题内容时，归类方案已获用户明确确认，实际路径与确认内容一致。
- 页面使用与主题相符的配色与表达组件，重点和状态有明确配色编码；吸顶顶部导航与偏宽自适应布局在窄屏下仍可用；若含 diagram，已按 html-diagram 选型并嵌入阅读页。
- 每个本地链接都以来源 HTML 文件所在目录解析，目标存在，且没有站点根路径、绝对磁盘路径或 `file://` 链接。
- 所有本地链接与资源路径有效，页面可直接在浏览器中打开。
