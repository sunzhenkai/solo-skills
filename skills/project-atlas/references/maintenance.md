# 增量维护与自愈

## 变更路由

先运行 `status`，再按下表决定阅读范围。一个改动可命中多页，但不按文件机械建页。

| 代码变化 | 复核内容 |
|---|---|
| 状态、分支、补偿、业务规则 | 所属 L2、对应 L1 核心流程；必要时更新 L0 主链路 |
| 对外接口、消息、权限、邻接系统 | 领域边界、相关时序图和异常路径 |
| 实体、存储、事务、一致性 | 核心实体、数据流、失败与补偿规则 |
| 仅实现重构且外部行为不变 | 核对映射页的语义；确认无内容变化后 `verify` |
| 新模块未进入 Atlas | 按主链路价值并入现有 L1/L2，或增加最小下钻页 |

`stale` 是计算状态，不手写到 frontmatter。`source_digest` 不一致表示需要复核；`missing_sources` 表示映射已失效，先调整路径再复核。`affected_diagrams` 列出过期页面链接的 Archify 图。每轮只处理 `stale_pages` 与当前需求涉及的页面，无需重写整个 Atlas。

## 复核顺序

1. 读取页面全文和当前 `sources`，保留仍成立的人工说明。
2. 沿代码调用链核实主路径、关键分支和失败结果；没有证据的内容标为草稿或删除。
3. 更新当前页，再检查上级摘要、同级交叉链接和 `affected_diagrams` 是否仍成立。图源变化后按 Archify 契约重新 `finalize`；仓库证据的行号或 commit 变化也同步更新。
4. 对本轮页面运行 `verify`，随后运行 `build` 和 `check`。`check` 将断链、跨层缺链、缺失映射、过期页和无效图交付列为错误。

## 图与静态文件

- 复杂且需要探索的图使用 `diagrams/` 中的 Archify JSON + HTML；简单静态图和其他资源放 `assets/`。
- 图的标题和正文使用与页面相同的领域术语；图旁写一句阅读重点和对应业务页链接。
- Archify 的 JSON、delivery/finalize 回执和浏览器证据不发布到 `_site/`；`build` 只复制图 HTML。
- 独立静态 HTML 的 `href` / `src` 使用 Atlas 内相对路径。构建时检查目标并改写其中的 `.md` 链接。
- 删除或移动资源后运行 `check`，修复所有引用。保留仍能支持理解的资源。

`_site/` 全部由 `build` 重建，直接编辑只会被下一次构建覆盖。需要改内容时编辑 Markdown、Archify JSON 或 `assets/` 真源。

## 完成门

- `build` 成功，`_site/index.html` 能作为入口离线打开，交互图只发布 HTML。
- `check.ok=true`，`stale_pages=[]`，没有断链、缺失导航或图回执/摘要错误。
- 本轮涉及的复杂逻辑图与文字一致，Archify `finalize` 已通过，静态 HTML 中的 Markdown 链接已生成对应 HTML 跳转。
- 未覆盖范围仍标 `draft`，回执明确说明，避免把局部覆盖描述成全量覆盖。
