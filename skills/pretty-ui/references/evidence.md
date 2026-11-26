# 看图取证

[pretty-ui](../SKILL.md) 的看图步骤、page 模式的检查、上游流程的截图与量测读本页。截图分三档，按场合取，不多截。

## 1. 工具与打开方式

- 截图工具按序选：宿主的浏览器工具 → 项目已有的截图或 e2e 工具 → taskrail 的 `scripts/ui_evidence_check.py`（需要 playwright）。都用不了时，结论标“未渲染验证”，问题标 `code-only`。
- 本地页面用 `python3 -m http.server --bind 127.0.0.1 <端口>` 起服务再打开，部分浏览器工具拦截 `file://`；用完关掉服务。
- 同一任务复用本地服务和浏览器会话；每个视口连续完成尺寸调整、量测与截图，不为单张图重启服务或浏览器。首轮首屏完成即可交评审，最终整页按档位补齐。
- 页面开了 `scroll-behavior: smooth` 时，截某一区域前用 `window.scrollTo({ top, behavior: "instant" })` 跳过去，免得截到滚动中途。

## 2. 视口选定与三档截图

主视口默认桌面 1280（手机专用则为 375），走下方完整三档截图与评审；手机 375 按「明确要求必须 + 未明说自动推断」落入三档之一，并在简报记录选定结果与依据（上游另有视口硬门时按上游）：

| 移动端 375 档位 | 触发条件（明确要求 / 自动推断） | 做法 |
| --- | --- | --- |
| 跳过（默认） | 桌面专用、后台工具，或未提及移动端且项目无移动端布局/交付线索 | 只验 1280；交付说明的未验证项写明「移动端 375 未检查（按需开启）」 |
| 基础检查 | 用户要求兼容手机/响应式（未要求移动端观感验收），或自动推断为桌面为主但需兼顾窄屏（如公开内容页、落地页、已有响应式断点的多端页、`page` 阅读页） | 交付前复用当前浏览器会话切一次 375，跑第 3 节 DOM 量测并截 1 张首屏快看；只修 P0 破损（横向溢出、重叠遮挡、裁切、裂图、极小热区 `<24px`、环被裁），不补整页与状态档、不入隔离评审的精致度/设计感打磨 |
| 完整验证（必须） | 用户明确要求移动端体验或移动端观感验收、上游硬门要求；或自动推断为手机专用 / 移动优先 / 双端并重产品（如 H5、移动端 WebApp、项目以移动端布局为主） | 375 作为正式目标视口走完整三档与评审（手机专用仅 375，双端并重则 1280 + 375）；基础检查暴露移动端核心布局风险时亦升入本档 |

以下各档针对选定的完整验证目标视口：

| 档 | 何时 | 截什么 |
| --- | --- | --- |
| 基础档 | 首轮看图与评审、refine 改前诊断 | 每个目标视口截首屏并跑一次第 3 节的量测；refine 改前与整页诊断再截整页；静态页面跑 `check_page.py` |
| 状态档 | 交付前的最后一轮，截一次 | 每个目标视口补整页，首屏已覆盖整页时复用首屏；另截本次新增或改动涉及的状态：空、加载、出错、长文本、数据很多；有交互的再截默认、悬停或聚焦、选中、禁用 |
| 复审档 | 第二轮起 | 只截上一轮问题涉及的区域和视口，同一路由、同一份演示数据 |

- 三秒测试用的缩略图（首屏缩到 480 宽；375 走完整验证时手机图缩到 180 宽）由基础档截图缩小得到，不另截；遮掉文字的版本只在评审者要求时另截。
- 关键区域按 100% 看，精致度按 200% 看，放大已有截图即可。
- **改前改后**：refine 和上游要求对比时，改前、改后按同一目标视口、路由和演示数据留基础档与最终整页；仅做基础检查的 375 无需改前改后对照。

## 3. 量一量

浏览器工具能执行脚本时，在每个视口跑一次下面的片段，把结果和截图放在一起：

```js
(() => {
  const px = (v) => parseFloat(v) || 0;
  const out = (s) => {   // 画在 border-box 外的装饰：非 inset 阴影的 spread、outline
    let m = s.outlineStyle === "none" ? 0 : px(s.outlineWidth) + px(s.outlineOffset);
    for (const seg of (s.boxShadow === "none" ? "" : s.boxShadow).split(/,(?![^(]*\))/)) {
      const len = seg.match(/-?[\d.]+px/g) || [];
      if (!/inset/.test(seg) && len.length >= 4) m = Math.max(m, px(len[3]));
    }
    return m;
  };
  const r = { 横向溢出: document.documentElement.scrollWidth > innerWidth, 溢出元凶: [], 裂图: [], 极小热区: [], 移动端偏小热区: [], 缺锚点留白: 0, 行太长: [], 字太小: [], 行高过紧: [], 环被裁: [] };
  const name = (x) => x.tagName.toLowerCase() + (x.getAttribute("class") ? "." + x.getAttribute("class").trim().split(/\s+/)[0] : "");
  if (document.documentElement.scrollWidth > innerWidth + 1) {
    for (const el of document.querySelectorAll("body *")) {
      if (!el.offsetWidth) continue;
      const b = el.getBoundingClientRect();
      if (b.right > innerWidth + 1 || b.left < -1) {
        r.溢出元凶.push(name(el));
        if (r.溢出元凶.length >= 3) break;
      }
    }
  }
  for (const img of document.querySelectorAll("img")) {
    if (img.offsetWidth && img.complete && img.naturalWidth === 0) r.裂图.push(img.getAttribute("src") || "<img>");
  }
  for (const el of document.querySelectorAll('button, [role="button"], input:not([type="hidden"]), select, textarea, a[href]')) {
    if (!el.offsetWidth || el.disabled) continue;
    if (el.tagName === "A" && el.closest("p, li, dd, blockquote, td") && getComputedStyle(el).display === "inline") continue;
    const b = el.getBoundingClientRect(), minSide = Math.min(b.width, b.height);
    const desc = el.tagName.toLowerCase() + " (" + Math.round(b.width) + "x" + Math.round(b.height) + ")";
    if (minSide < 24) r.极小热区.push(desc);
    else if (innerWidth <= 480 && minSide < 40) r.移动端偏小热区.push(desc);
  }
  const hasTopBar = [...document.querySelectorAll("*")].some((el) => {
    const s = getComputedStyle(el);
    if (s.position !== "sticky" && s.position !== "fixed") return false;
    const b = el.getBoundingClientRect();
    return b.top <= 16 && b.height >= 32;
  });
  if (hasTopBar) {
    for (const el of document.querySelectorAll("[id], h2, h3")) {
      if (el.offsetWidth && parseFloat(getComputedStyle(el).scrollMarginTop) <= 0) r.缺锚点留白++;
    }
  }
  for (const el of document.querySelectorAll("p, li, dd, blockquote, td")) {
    const t = el.textContent.trim(), s = getComputedStyle(el), size = parseFloat(s.fontSize);
    if (t.length < 30 || !el.offsetWidth) continue;
    const zh = /[\u4e00-\u9fff]/.test(t), w = el.getBoundingClientRect().width;
    const perLine = Math.round(zh ? w / size : w / (size * 0.5));
    const lh = s.lineHeight === "normal" ? 1.2 : parseFloat(s.lineHeight) / size;
    const tag = el.tagName.toLowerCase() + "「" + t.slice(0, 12) + "」";
    if (perLine > (zh ? 46 : 95)) r.行太长.push(tag + " 约 " + perLine + (zh ? " 字" : " 字符"));
    if (size < 12.5) r.字太小.push(tag + " " + size + "px");
    if (lh < (zh ? 1.5 : 1.4)) r.行高过紧.push(tag + " " + lh.toFixed(2));
  }
  for (const el of document.querySelectorAll("*")) {
    const d = out(getComputedStyle(el));
    if (d <= 0 || !el.offsetWidth) continue;
    let a = el.parentElement;
    for (; a; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (s.overflowX !== "visible" || s.overflowY !== "visible") break;
    }
    if (!a) continue;
    const e = el.getBoundingClientRect(), b = a.getBoundingClientRect(), s = getComputedStyle(a);
    const sx = a.scrollWidth > a.clientWidth, sy = a.scrollHeight > a.clientHeight, edge = [];
    if (e.left - d < b.left + px(s.borderLeftWidth) - 0.5 && !sx) edge.push("左");
    if (e.right + d > b.right - px(s.borderRightWidth) + 0.5 && !sx) edge.push("右");
    if (e.top - d < b.top + px(s.borderTopWidth) - 0.5 && !sy) edge.push("上");
    if (e.bottom + d > b.bottom - px(s.borderBottomWidth) + 0.5 && !sy) edge.push("下");
    if (edge.length) r.环被裁.push(name(el) + " 被裁" + edge.join("") + "，裁它：" + name(a));
  }
  return r;
})()
```

表格单元格里的短行不算行太长；它只是线索，结论以截图为准。「环被裁」指用 `0 0 0 1px` 这类外扩阴影或 outline 画的细线，被祖先的 `overflow` 裁掉——内容没被裁，`横向溢出` 抓不到它。可滚动容器里滚得到的那一侧不算；判 1px 级细线时用 `deviceScaleFactor: 2` 截图并按像素取样，1x 下环只有 1 个物理像素，落在小数坐标上会被抗锯齿摊薄。另注意 Playwright Headless 默认使用 overlay 滚动条（gutter 0），单看 headless 截图容易漏掉桌面浏览器中占位滚动条造成的右侧横线空隙；涉及固定头与滚动区时需核查头部是否独立于滚动容器之外、滚动条起点是否对齐头部下沿且不占布局宽度。

## 4. 证据路径

截图、量测结果、评审记录放任务目录或项目约定位置，交付说明里写路径。
