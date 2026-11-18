---
id: ui-kit
name: ui-kit
description: 可复用的 UI 设计语言与复制即用的 React 模板（Vite + Tailwind CSS Variables + shadcn/Radix + Storybook/Playwright 像素验收）：用模板从零新建前端、升级模板、定制或校验主题 token、写项目 DESIGN.md、查阅设计语言。用户要统一 UI 设计语言、按模板搭项目或升级、定制主题、做视觉一致性验收时使用。
---

# ui-kit

一套设计语言，由模板仓里的代码实现；项目复制同一份代码，只在白名单内改主题。目标是：换主题后仍是同一产品族，除自定义外视觉一致，不同模型做出的结果也一致。

两条信条贯穿所有模式：

- **外观只在代码里**：token、组件、blocks、应用骨架、页面模板都以代码发布，项目复制使用；文档讲用法，不靠模型读文档重画外观。
- **模型只写内容**：页面由页面模板与认证组件拼装，填数据与文案；外观差异只来自主题白名单。

与 pretty-ui 的边界：pretty-ui 负责定方向、打磨与评审（包括打磨模板本身）；ui-kit 负责把定下的语言固化成可复制、可校验的模板契约。

## 模板仓

模板代码在 `github.com/sunzhenkai/ui-templates-skill`，按 tag 取用。本机已有 checkout 时设 `UI_TEMPLATES_DIR` 指向它，否则浅克隆指定 tag 到 `/tmp`。下文 `<kit>` 指该 checkout 根目录。

## 路由

| 请求 | 做法 |
| --- | --- |
| 从零新建前端 | 按 [references/init.md](references/init.md) 生成骨架并写页面 |
| 升级项目里的模板 | 按 [references/update.md](references/update.md) 看状态、升级、处理合并 |
| 验收、检查视觉是否一致 | 按 [references/verify.md](references/verify.md) 跑完整验收 |
| 问设计语言、某类元素该怎么做 | 按 [references/language.md](references/language.md) 回答，指到对应小节 |
| 校验主题、风格包或项目 `theme.css` | 按 [references/tokens.md](references/tokens.md) 跑校验脚本，逐条修到 0 error |
| 定制主题色、圆角、字体、暗色 | 只改白名单内 token（tokens.md「可自定义」），改完跑验收，在 DESIGN.md 记录 |
| 写或更新项目 `DESIGN.md` | 按 [references/design-md.md](references/design-md.md) 模板填写 |

混合请求按“新建或升级 → 定制 token → DESIGN.md → 验收”的顺序串起来并说明。已有项目迁入模板尚未支持，先说明再与用户商定。

## 校验

```bash
python3 <kit>/skills/ui-template-apply/scripts/validate_package.py package <风格包目录>
python3 <kit>/skills/ui-template-apply/scripts/validate_package.py project <项目根>
python3 <kit>/skills/ui-template-apply/scripts/verify_fidelity.py --project <项目根>
```

完成：validate 0 error，且保真比对 `fidelity: pass`（项目验收的完整顺序见 verify.md）。对比度不达标时调明度（L），不降门槛；缺 token 就补 token，不在组件里写字面值。

## 交付

说明用了哪个风格包与版本、改了哪些白名单 token 及理由、验收各项结果（没跑的写“未验证”）、DESIGN.md 位置。

## 按需读取

| 文件 | 何时读 |
| --- | --- |
| [references/init.md](references/init.md) | 新建项目：生成命令、文件归属、写页面的约束 |
| [references/update.md](references/update.md) | 升级：状态含义、主题三方合并、冲突处理 |
| [references/verify.md](references/verify.md) | 验收命令、结果怎么读、保真比对的原理 |
| [references/language.md](references/language.md) | 设计语言：原则、分层与所有权、表面、排版、色彩、动效、状态、页面模式、保真定义 |
| [references/tokens.md](references/tokens.md) | token 契约结构、校验码、可自定义白名单、新增 token 的流程 |
| [references/design-md.md](references/design-md.md) | 项目 DESIGN.md 模板 |

经验沉淀与正文演进走 `skill-upgrader`。
