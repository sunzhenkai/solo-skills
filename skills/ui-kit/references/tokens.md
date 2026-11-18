# Token 契约

[ui-kit](../SKILL.md) 校验、定制主题时读本页。契约真源是模板仓的 `skills/ui-template-apply/contract/tokens.json`，它和消费这些变量的组件一起发版；本页解释结构与用法，不重复列值。

## 1. 结构

| 字段 | 含义 |
| --- | --- |
| `colors.core` | shadcn 核心颜色角色（背景、前景、卡片、主色、边框、侧栏、图表等） |
| `colors.extensions` | 语言扩展角色：`success` `warning` `warning-foreground` `info` `brand` `brand-foreground` `faint-foreground` `app-shell` |
| `scale.required` | 必备刻度：字体、`text-xs`…`text-xl`、`radius`、`surface-shadow`、`floating-shadow` |
| `scale.optional` | 可选刻度：`text-2xl`、`duration-fast`、`duration-base`、`ease-out`、`font-heading` |
| `contrast` | 必须达标的前景 / 背景配对与最低对比度 |
| `tints` | 文字压在语义色低透明度底上的配对，最低 4.5 |
| `customizable` | 项目可改的颜色角色与刻度（白名单） |

## 2. 主题文件的写法

- 颜色角色在 `:root`（亮）与 `.dark`（暗）各定义一遍，值一律 `oklch()`；暗色是重新映射，不是取反。
- `@theme inline` 把每个角色映射成 `--color-<角色>: var(--<角色>)`，Tailwind v4 才能生成 `bg-<角色>` 等工具类。
- 字号刻度写在 `@theme`（`--text-sm` 与 `--text-sm--line-height` 成对）；圆角只定 `--radius`，各档由 `@theme inline` 按倍数派生。

## 3. 校验码

| 码 | 含义 | 修法 |
| --- | --- | --- |
| T01 / T02 | 亮色 / 暗色缺颜色角色 | 补齐该角色 |
| T03 | 角色没有映射到 `@theme inline` | 加 `--color-<角色>` 映射 |
| T04 | 颜色不是 `oklch()` | 换算成 oklch |
| T05 / T06 | 缺 `--text-sm` / 缺其他必备刻度 | 补刻度 |
| C01 | 配对对比度不足 | 调明度 L，色相与彩度尽量不动 |
| C02 | 语义色浅底上的文字对比度不足 | 调该语义色的明度 |
| J12 | 项目主题在白名单外偏离了锁定的风格包 | 改回包值；确要偏离就记入 `theme_deviations` |

## 4. 可自定义

项目只改 `customizable` 列出的项：主色与品牌色（`primary` `brand` 及其前景、`ring`、侧栏主色）、图表色阶、`--radius`、`--font-sans` / `--font-heading`。

- 改在项目 `src/styles/theme.css`，亮暗两套同时改，改完跑校验。换字体时同时改 `src/styles/fonts.css` 的 `@import` 并装对应字体包。
- 换品牌色时保持中性色不动，只换色相与彩度，明度以对比度达标为准。
- 白名单外的改动视为偏离：J12 报错；确要保留就把 token 名写进项目 `ui-decisions.yaml` 的 `theme_deviations` 列表，同时写进 DESIGN.md「偏离」并说明理由，该部分不在保真保证内。

## 5. 新增 token

新角色或新刻度意味着组件要消费它，属于模板改动而不是主题改动：

1. 在模板仓改组件，让它消费新 token。
2. 在 `tokens.json` 加入对应字段（必备或可选），必要时加对比度配对。
3. 所有已发布风格包补上该 token，跑 `make check`。
4. 必备 token 的增加对风格包是破坏性变更，升主版本并写 CHANGELOG。
