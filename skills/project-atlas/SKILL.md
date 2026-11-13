---
id: project-atlas
name: project-atlas
description: 项目 Atlas：把架构图、业务规则和处理流程整理成可下钻的金字塔文档，维护 Markdown、HTML 与静态资源互链；按源码映射增量更新并复核代码变动造成的过期页面。用户要求项目知识地图、架构可视化、业务逻辑梳理、文档下钻、静态站点或文档自愈时使用。
compatibility: Requires Python 3.9+; Git is optional for recording the reviewed commit. Creating or updating Archify diagrams additionally requires Node.js 18+ and the archify skill.
---

# Project Atlas

在目标项目维护一套人可扫读、可逐层下钻的文档。系统总览、跨领域主链路和多视角页面解释整体，领域三层文档承载细节。Markdown 是可编辑真源，`_site/` 是可浏览的静态 HTML 镜像，源码映射说明每页应跟随哪些代码变化。

边界：一次性项目问答与代码取证走 `project-explore`；决策背景、备选方案、经验、台账和跨项目知识走 `wiki-data`。本 skill 只维护当前项目代码映射的架构与业务 Atlas，不在页面复制 wiki 的决策历史或经验正文。交互图由 `archify` 生成，Atlas 不复制其 schema 或绘图 CLI。

## 与 project-explore 联动

建立或复核页面时，可用 `project-explore` 的 `ask / explore` 获得项目结构、调用链和代码证据，也可接收其 `archive / project` 交接。ExplorationBrief 与持久化建议只是调查输入；Atlas 仍须按页面 `sources` 复核语义，再执行 `verify / build / check`，不把 Brief 直接当作已核实正文。一次性概览不要求建立 Atlas，持久化项目入口由 Atlas 按 `init` 确认和首批页面门禁完成。

## 固定结构

```text
<atlas>/
├── index.md                     # L0：系统边界、业务闭环、多视角导航与阅读路径
├── flows/<flow>.md              # L1：跨领域端到端业务链路
├── architecture/<topic>.md      # L1：在线、离线、数据、模型及运行时依赖
├── data/<topic>.md              # L1：数据归属、状态、事件与一致性
├── cross-cutting/<topic>.md     # L1：实验、权限、容灾等横切机制
├── domains/<domain>/index.md    # L1：领域职责、核心规则、主题导航
├── domains/<domain>/<topic>.md  # L2：流程、状态机、组件或规则细节
├── diagrams/<slug>.json         # Archify 图源
├── diagrams/<slug>.html         # Archify 交互图与交付回执
├── assets/                      # 图片、SVG、其他静态资源
├── .atlas.json                  # Atlas 版本与源码根
└── _site/                       # 生成物，只发布页面、图 HTML 和 assets
```

每页只讲一个主题。系统视图按实际复杂度建立，以真实内容形成覆盖；简单项目可以先只有 L0 与领域页。`flows/` 串联各领域但不复制其内部规则，`architecture/`、`data/` 与 `cross-cutting/` 分别回答运行时协作、状态一致性和全局机制。页面职责、frontmatter 与阅读验收见 [references/layout.md](references/layout.md)。

## atlasctl

`<this-skill>` 是本 skill 的安装目录。默认 `<atlas>` 是 `<project>/docs/atlas`：`init` 根据 `--source` 推导，其他命令从项目根运行时读取 `./docs/atlas`。显式 `--root` 可覆盖默认落点；`verify` 只修改指定页面的复核元数据。

```bash
ATLASCTL="python3 <this-skill>/scripts/atlasctl.py"
$ATLASCTL init --source <project> --confirm
$ATLASCTL status
$ATLASCTL verify --page <page> [page...]
$ATLASCTL build
$ATLASCTL check
```

stdout 为 JSON。退出码：0 成功，1 校验或执行失败，2 等待确认。`init` 首次先不带 `--confirm`，向用户展示 `prompt` 后再按 `confirm_args` 执行；已有 Atlas 直接进入 `status`。

## 建立与渐进扩充

1. 用 `status` 或目录列表识别已有内容；没有 Atlas 时走 `init`，然后继续建立首批真实页面，空骨架不是完成。
2. 先读入口、配置、核心模块和已有文档，写 L0：系统服务的角色、外部边界、业务闭环和按读者目标组织的阅读路径。
3. 复杂系统优先选择一条跨领域主链路写入 `flows/`，从触发走到业务结果，并链接每一步所属领域；再用 `architecture/` 和 `data/` 解释该链路的运行时协作与关键状态，全局机制按需放入 `cross-cutting/`。
4. 建立主链路涉及的 L1，复杂内部流程再建 L2。优先覆盖主业务链路，覆盖不全时保留 `draft`，不虚构完整性。
5. 为 L1/L2 填 `sources`：使用源码根相对路径，可写文件、目录或 glob。写清业务规则、关键分支、失败路径和实体关系；复杂结构需要交互图时按 [references/diagrams.md](references/diagrams.md) 调用 Archify。
6. 从 L0 链到每个 L1，从 L1 链到所属 L2，并保留返回上级的链接；主链路与相关领域互相链接。交互图放 `diagrams/`，其他静态资源放 `assets/`，使用 Atlas 根内相对链接。
7. 语义复核后运行 `verify`，再运行 `build` 和 `check`。完成标志：读者能从 L0 沿主链路走完跨领域流程并下钻到相关领域、架构与数据证据，所有本地链接有效，L1/L2 有源码映射，关联图已完成 Archify `finalize`，生成站点可打开。

## 代码变动后的自愈

`status` 比较每页记录的 `source_digest` 与当前源码内容，输出 `stale_pages`、`affected_diagrams` 和 `missing_sources`。它不依赖 Git，也能发现未提交变更；`verified_commit` 仅用于追溯。

1. 对每个过期页重新阅读其 `sources` 与相关调用链，判断业务语义、架构边界和图是否变化。
2. 只改受影响页面及其上级导航；源码路径变化时同步修正 `sources`。更新图源后必须重新运行 Archify `finalize`，交付回执会绑定 JSON 与 HTML；内容未变也要明确核对后再 `verify`，刷新摘要不能替代语义复核。
3. 新代码尚未覆盖时，把它并入现有主题或新增最小页面；未覆盖区域保持可见的草稿状态，随主链路优先级渐进补齐。
4. 重新 `build` + `check`，以 `stale_pages` 清空、断链和图交付错误为零作为本轮收口。

变更路由与静态资源处理见 [references/maintenance.md](references/maintenance.md)。自愈是「发现影响 → 人工或 agent 复核 → 更新 → 验证」的闭环，不声称能从代码自动生成正确的业务解释。

## 与 wiki-data 联动

Atlas 维护代码核实的当前系统事实。混合任务先完成 Atlas，再列出需要 `wiki-data` 摄入或复核的主题，经对应确认后由 `wiki-data` 处理；Atlas 不自动写 wiki，也不复制其正文。页面与 `_site/` 不依赖 wiki 外链，静态站点可独立发布。

## 交付

回执给出 Atlas 根、`_site/index.html`、本轮新增/更新页面与图、过期页清零结果及仍为 `draft` 的范围；有知识上下文需要沉淀或复核时，同时列出 wiki 候选主题。凭据写 `<REDACTED>`；不自动 commit / push，不改业务源码。
