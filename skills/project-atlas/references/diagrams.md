# Archify 交互图

需要架构图、复杂业务流、跨系统时序、数据流或状态机时，加载已安装的 `archify` skill 并遵循其当版 schema 与 authoring 细则。Atlas 只规定图如何进入文档和自愈闭环，不复制 Archify 的字段定义。

Archify 是可选依赖：已有文档和普通静态资源不需要 Node.js；新建或更新交互图时需要 Node.js 18+ 与 Archify。安装外部 skill 前沿用使用环境的审计流程。

## 类型路由

| 内容 | Archify type |
|---|---|
| 组件、服务、存储与边界 | `architecture` |
| 业务处理、审批、补偿 | `workflow` |
| 跨系统调用与返回 | `sequence` |
| 数据加工、流转与血缘 | `dataflow` |
| 状态、重试与终态 | `lifecycle` |
| 表、字段、键与关系 | `erd` |
| 模块或能力的单父包含关系 | `tree` |

其他类型按 Archify 当版 Type router 选择。线性三步直接用文字列表，不为了有图而画图。

## 持久路径

每张图使用同名源和产物：

```text
<atlas>/diagrams/<slug>.json
<atlas>/diagrams/<slug>.html
```

从 `<atlas>` 运行命令，`meta.output` 写 `diagrams/<slug>.html`。该目录同时保存 Archify 的 delivery、finalize 和浏览器检查回执；Atlas 构建只发布 `.html`。

```bash
node <archify-skill>/bin/archify.mjs finalize <type> \
  diagrams/<slug>.json diagrams/<slug>.html \
  --repo-root <project> --quality showcase --json
```

仓库证据图必须带 `--repo-root <project>`；描述性图可省略。首次和每次修复都直接运行完整 `finalize`，沿用 Archify 的诊断与修复上限。同一图持续复用原 JSON，保持节点 ID 稳定，避免已有 `#focus=`、`#route=` 等深链失效。

修复轮按 Archify 要求使用 `--out-dir <review-dir>` 时，finalize 摘要会写入该 review 目录。成功后把 `<review-dir>/<slug>.finalize-summary.json` 原样复制为 `diagrams/<slug>.finalize-summary.json`，作为 Atlas 的规范摘要；保留摘要字节与证据路径，不修改回执内容。

## 页面链接

在相关 L0/L1/L2 用普通 Markdown 链接打开独立交互图：

```markdown
[打开订单处理时序图](../diagrams/order-submit.html)
```

首版不嵌 `iframe`，也不把 Archify 回执或 JSON 发布到 `_site/`。简单静态图仍可放 `assets/`，无需伪造 Archify 回执。

## 交付门禁

`atlasctl check` 对页面引用的 Archify 图检查：

- 同名 JSON、HTML、`.delivery.json` 与 `.finalize-summary.json` 存在。
- finalize 回执 `ok=true`，delivery 为当前成功状态。
- 回执中的 specification/artifact SHA-256 与字节数匹配当前 JSON/HTML。
- 不存在 `.delivery-pending.json`、`.delivery-lock.json` 或 `.archify-delivery-lock.json`。

修改 JSON 或 HTML 后重新 `finalize`，不手改回执。Archify 失败时保留最后一份通过检查的图，完成修复前页面不能通过 `verify`。
