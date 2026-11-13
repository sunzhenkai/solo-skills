# 金字塔布局与页面契约

## 三层阅读路径

| 层 | 页面 | 应回答的问题 | 建议内容 |
|---|---|---|---|
| L0 | `index.md` | 系统是什么，先读哪里 | 用户与目标、外部边界、领域地图、主业务链路 |
| L1 | `domains/<domain>/index.md` | 这个领域负责什么 | 职责边界、核心实体、主要流程、主题与图的导航 |
| L2 | `domains/<domain>/<topic>.md` | 一条具体逻辑怎样工作 | 触发、步骤、分支、异常、状态转换、数据一致性 |

一个新主题先写在已有页面的小节中；出现独立读者、复杂分支或多处引用时再拆成下钻页。每层可直接读，上级提供上下文，下级提供证据与细节。

## 页面真源

每页使用以下 YAML 子集；`level` 写字符串形式的 `0`、`1`、`2` 也可，CLI 按文本比较：

```markdown
---
title: 订单处理
level: 2
status: draft
sources:
  - src/orders
  - src/payments/gateway.py
source_digest:
verified_commit:
---

# 订单处理

[返回领域](index.md)
```

- `title`：读者看到的主题名。
- `status`：`draft` 表示范围或内容尚未核全；`verify` 复核后写 `verified`。
- `sources`：源码根相对路径，支持文件、目录和 glob。L1/L2 进入 `verified` 前至少映射一个存在的路径。
- `source_digest`：由 CLI 根据映射文件的路径和内容计算；代码或未提交文件变化会改变它。
- `verified_commit`：复核时的 Git HEAD；非 Git 项目留空。

手写页面时后两项留空。使用 `verify --page <atlas-relative-page>` 更新复核信息，不手算摘要。

## 导航与链接

- L0 必须直链每个 L1；L1 必须直链所属 L2。
- 每个 L1 链回 `index.md`，每个 L2 链回本领域 `index.md`。
- 使用相对路径，例如 `../assets/diagrams/order.svg` 或 `../../index.md`。
- Markdown 中保留 `.md` 扩展名；`build` 在 HTML 镜像中改为 `.html` 并保留锚点。
- 本地链接指向 Atlas 内已经存在的文件。源码追溯使用 `sources`，避免静态站点依赖仓库外路径。

## 内容粒度

架构页写组件职责、交互、边界和关键取舍；业务页写触发者、业务步骤、规则、异常和结果。函数逐行走读、完整文件清单、依赖版本和启动命令留在源码或项目既有文档中，只在它们解释架构契约时引用结论。

复杂分叉、状态机、跨系统时序和非平凡数据流配图；线性三步用列表即可。图片、SVG 和独立 HTML 放 `assets/`，从相关页面链接，不把大图嵌进 L0。
