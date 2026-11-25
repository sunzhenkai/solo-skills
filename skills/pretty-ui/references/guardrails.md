# 实现防错护栏（写代码前与改完自查）

[pretty-ui](../SKILL.md) 的 `build`、`build 轻量`、`refine` 与涉及布局/浮层/状态的 `小改` 读本页。目标是在写代码阶段直接避开最高频、会触发运行态机械门（L1/L2）的结构性 UI bug；视觉美学与规则号仍在 [rules.md](rules.md)。

## 1. 布局防爆

- **G-L1 Flex/Grid 长内容防撑爆**：Flex/Grid 子项包含长文本、代码、URL 或宽表格时，容器设 `min-w-0`，文本用 `truncate` / `line-clamp` / `overflow-wrap: anywhere`，宽表或代码块在自身容器内 `overflow-x: auto`，确保目标视口无横向溢出。
- **G-L2 外扩细线不被祖先裁切**：用 `box-shadow: 0 0 0 1px …` 或 `outline` 画细线时，带 `overflow: hidden/clip` 的祖先必须预留 ≥1px 内边距；改不了祖先容器时改用 `inset` 阴影或真 `border`。
- **G-L3 嵌套布局按容器算阈值**：正文 + 右栏/目录这类嵌套分栏，显隐与折叠阈值按「当前容器可用宽度（页面宽 − 已占列宽）」判断，不拿视口宽度直接套在内层分栏上。
- **G-L4 媒体防抖与分界**：图片、视频、画布显式声明宽高或固定比例容器防布局抖动（CLS）；用户上传或浅底图片与浅色背景之间有清晰边界；页面不留失效图片（`naturalWidth === 0`）。
- **G-L5 滚动条 0px 覆盖式、固定头分离与零挤压**：
  - **按场景分流滚动条**：
    - **应用壳 / 多栏 / 带通栏分隔线容器（首选）**：使用 **0px 占位的覆盖式（overlay）滚动条**（优先复用已有覆盖式原语如 Radix `ScrollArea` 或绝对定位悬浮滑块组件，隐藏原生滚动条 `scrollbar-width: none` + `::-webkit-scrollbar { display: none }`，以绝对定位滑块叠在内容右边缘，平时隐藏、滚动或悬停轨道时平滑淡入、停滚后淡出），确保横线贴满边缘、零布局挤压、跨 OS 一致；
    - **整页文档流（`html` 滚动）**：不给 `html` 强加占位式 `::-webkit-scrollbar` 或 `scrollbar-gutter: stable`（会截断通栏顶栏底线，且会把 macOS 原生悬浮滚动条降级为占位模式），仅声明 `color-scheme` 同步亮暗模式；
  - **CSS 反模式**：不混写 `scrollbar-width`（非 `none`）与 `::-webkit-scrollbar`（Chromium 121+ 标准属性会屏蔽 webkit 规则）；不对 `::-webkit-scrollbar-thumb` 直接写无效的 `transition`；不用 `:hover` 切换 `overflow: hidden ↔ auto`、不使用已废弃的 `overflow: overlay`、模态框锁滚不裸改 `body { overflow: hidden }` 挤动页面；
  - **固定头与滚动容器物理分离**：当顶栏或面板头需要固定且要求底线贴满右边缘、滚动条起于头部下沿时，采用外层 `flex-col overflow-hidden` + 头部 `shrink-0`（在滚动容器外）+ 下方内容区 `min-h-0 flex-1` 独立滚动，不把固定头用 `position: sticky; top: 0` 塞进滚动容器内部（滚动条永远覆盖滚动容器全高，会与 `sticky` 顶部平齐）；`position: sticky` 仅用于内容区内部随滚定位的元素（如长表格表头）；
  - 触屏设备（`@media (hover: none), (pointer: coarse)`）交给系统原生 overlay 滚动条；`@media (prefers-reduced-motion: reduce)` 关闭淡入淡出过渡。
- **G-L6 动态视口高度与截断补全**：满屏与吸底布局优先用 `100dvh` / `min-h-dvh`（避免移动端 `100vh` 被地址栏裁切），吸底操作栏预留 `env(safe-area-inset-bottom)`；被 `truncate` / `line-clamp` 截断的关键信息提供查看全貌途径（如 `title`、tooltip 或展开）；表格数字与时间列加 `white-space: nowrap` 与 `tabular-nums` 防止误折行。

## 2. 浮层与覆盖件

- **G-O1 内边距与防双线**：Drawer / Dialog / Popover / Dropdown / Tooltip 打开后，内容区必有内边距，不贴容器边框；内部卡片或分割线不与浮层外框紧贴形成双线。
- **G-O2 滚动隔离**：浮层内部可滚动区域设置 `overscroll-behavior: contain`，明确滚动边界，避免滚穿到底层页面。
- **G-O3 焦点进出与防遮挡**：模态/抽屉打开时焦点进入内部，支持 `Esc` 关闭且关闭后焦点归还触发元素；有 sticky / fixed 顶栏的页面给锚点与可聚焦元素留 `scroll-margin-top`，确保键盘聚焦不被顶栏遮挡。

## 3. 状态与连续性

- **G-S1 数据四态齐全**：每个依赖外部数据的视图都实现 `loading` / `empty` / `error` / `success`；空态说明当前是什么并只留有效入口，错误态说明原因与重试/下一步，空数据或报错时不渲染破碎界面。
- **G-S2 切页不卸载壳**：列表、目录树、标签页切换内容时，页头、导航与页面壳保持挂载不重建；新数据加载期间保留上一份内容（如 `placeholderData: keepPreviousData`），避免每次切换整页闪白或跳骨架。
- **G-S3 异步防重复提交**：表单提交与关键操作按钮在请求中进入禁用/处理态并给明确反馈，失败后恢复可点，防止连点重复触发。
- **G-S4 数据形状防御与零未捕获异常**：渲染接口数据时做可选链与空数组兜底，单个字段缺失不导致整页崩溃；交互与渲染过程不向控制台抛 `console.error` 或未捕获异常。

## 4. 交互与无障碍底线

- **G-A1 破坏性操作保护**：删除、批量清空、不可逆发布等破坏性操作必须有二次确认或可撤销（undo），不作为页面默认主操作内联强调。
- **G-A2 语义元素与可见焦点**：交互元素优先用原生 `<button>` / `<a>` / `<input>`，不用裸 `<div onClick>`；保留清晰 `:focus-visible` 样式，不裸写 `outline: none` 而不补替代焦点环。
- **G-A3 热区与可达名称**：可点击目标至少 24×24px，常规按钮与移动端触控目标建议 ≥40×40px；仅图标按钮提供 `aria-label`（与 `title`），纯装饰图标标 `aria-hidden="true"`。

---

实现完成后，按 [evidence.md](evidence.md) 做量测与看图（或跑 taskrail 的 `scripts/ui_evidence_check.py` L1/L2 机械门），上述护栏中的运行时报错、裂图、横向溢出、外扩环裁切、浮层贴边与焦点遮挡均会直接被机械门拦截。
