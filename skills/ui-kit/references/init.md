# 新建项目

从零搭一个按 ui-kit 设计语言的 React 应用。外观全部来自复制进来的模板代码，模型只写页面内容。

## 1. 生成

```bash
python3 <kit>/skills/ui-template-apply/scripts/install_registry.py --project <目录> --package quiet-inset --init
cd <目录> && npm ci && npx playwright install chromium
```

`--init` 先拷骨架（已存在的文件不覆盖，打印 `kept`），再装全部模板文件并写 `ui-template.lock.json`。没有点名风格包时用 `quiet-inset`。

## 2. 文件归属

| 文件 | 归属 | 能否改 |
| --- | --- | --- |
| `src/main.tsx`、`src/root.tsx`、`src/pages/*`、`src/lib/api.ts`、配置文件 | 项目 | 可改 |
| `src/styles/theme.css`、`src/styles/fonts.css` | 风格包 | 只改白名单（tokens.md），J12 把关 |
| `src/components/{ui,blocks,page-templates}/*`、`src/hooks/*`、`src/lib/{utils,vocab}.ts` | 模板 | 不改，lock 哈希 |
| `src/index.css`、`.storybook/*`、`playwright.fidelity.config.ts`、`tests/ui-kit/*`、`src/stories/ui-kit/*` | 模板 | 不改，决定保真比对怎么渲染 |

`src/lib/vocab.ts` 例外：领域状态词加在这里，按 ui-template-apply 的约定记 `local_edits`。

## 3. 写页面

- 骨架带一个示例设置页：改 `src/root.tsx` 的品牌名与导航，在 `src/pages/` 加页面，在 `src/main.tsx` 注册路由。
- 页面 = 页面模板 + 数据。先找 `src/components/page-templates/`，再用 blocks 与 surfaces 组合；不写颜色、边框、圆角、间距类（lint 拦截）。
- 没有合适的页面模板时，用 blocks 组合并在 DESIGN.md「页面与页面模板」记为模板缺口；同类页面出现两次，回馈模板仓做成页面模板。
- 服务端数据用 TanStack Query；响应经 Zod 解析后再进组件（骨架的 `fetchJson(url, schema)`）。

## 4. 收尾

1. 需要定制主题时按 tokens.md「可自定义」改。
2. 按 design-md.md 写 `DESIGN.md`。
3. 按 verify.md 跑完整验收，全部通过才算完成。
