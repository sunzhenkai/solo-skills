---
id: ui-kit
name: ui-kit
description: 默认 UI 总入口：为新建或既有 Web UI 选择实现路线，衔接通用设计、React 模板、设计语言、风格包、评审与专项 UI skills。用户要做页面或组件、美化或评审 UI、统一设计体系、定制主题、写 DESIGN.md，或点名 ui-kit 时使用。
---

# ui-kit

默认 UI 总入口。先识别交付类型、现有技术栈和是否使用模板，再选择**唯一主承接方**；默认入口不等于统一框架。用户点名具体 skill 时按点名执行，本 skill 负责未点名 UI 请求的分派。

两条路线共用既有体系优先原则，但实现合同不同：

- **通用路线**：沿用项目现有框架、组件库、token 与测试，由 pretty-ui 定方向、实现、打磨和评审；非 React 项目也走这里，不生成 React 模板文件。
- **模板路线**：**外观只在代码里**，token、组件、blocks、应用骨架和页面模板以代码发布；**模型只写内容**，页面组合认证组件并填数据，外观差异只来自主题白名单。

与 pretty-ui 的边界：ui-kit 负责默认分派和模板契约；pretty-ui 负责通用设计、实现、打磨与评审，也可被用户直接点名。

## 总路由

| 场景 | 主承接与做法 |
| --- | --- |
| 已有项目、非 React、小改、refine、review、通用 system / page | 按 [pretty-ui](../pretty-ui/SKILL.md) 的对应模式执行，沿用项目技术栈与既有设计体系 |
| 已有 `ui-template.lock.json`，或新建项目明确选择 React 模板路线 | 走下方模板路由；模板升级与保真验收由本 skill 负责 |
| 新建项目尚无技术栈 | 按需求、团队与既有生态选择框架；React 模板适合时说明理由并走模板路线，否则由 pretty-ui 配合 project-init 实现 |
| 为模板路线从品牌推导新风格包 | 读 `<kit>/skills/ui-template-design/SKILL.md`，产出 `meta.yaml + theme.css` |
| 从仓库、网站或截图提炼并发布模板风格包 | 读 `<kit>/skills/ui-template-author/SKILL.md`；落地页面仍交 ui-template-apply |
| 非模板项目要建设计体系或 `DESIGN.md` | 走 pretty-ui system，不套用 ui-template 的 token 与 DESIGN.md 契约 |
| HTML 演示文稿 | 交 `frontend-slides`，不进入产品 UI 实现路线 |

混合请求先选主路线再串步骤。例如非 React 设置页缺设计体系，是 pretty-ui system → build；React 模板项目换主题，是定制 token → DESIGN.md → 验收。已有项目迁入模板尚未支持，先说明再与用户商定。

## 模板仓与模板路由

模板代码在 `github.com/sunzhenkai/ui-templates-skill`，按 tag 取用。本机已有 checkout 时设 `UI_TEMPLATES_DIR` 指向它，否则浅克隆指定 tag 到 `/tmp`。下文 `<kit>` 指该 checkout 根目录；实现页面读 `<kit>/skills/ui-template-apply/SKILL.md`。

| 请求 | 做法 |
| --- | --- |
| 从零新建 React 模板前端 | 按 [references/init.md](references/init.md) 生成骨架并写页面 |
| 升级项目里的模板 | 按 [references/update.md](references/update.md) 看状态、升级、处理合并 |
| 验收、检查视觉是否一致 | 按 [references/verify.md](references/verify.md) 跑完整验收 |
| 问模板设计语言、某类元素该怎么做 | 按 [references/language.md](references/language.md) 回答，指到对应小节 |
| 校验主题、风格包或项目 `theme.css` | 按 [references/tokens.md](references/tokens.md) 跑校验脚本，逐条修到 0 error |
| 定制主题色、圆角、字体、暗色 | 只改白名单内 token（tokens.md「可自定义」），改完跑验收，在 DESIGN.md 记录 |
| 写或更新模板项目 `DESIGN.md` | 按 [references/design-md.md](references/design-md.md) 模板填写 |

## 专项与编排衔接

- 快速代码清理、只读证据审计、无障碍、metadata、动效性能分别可交 `baseline-ui`、`improve-ui`、`fixing-accessibility`、`fixing-metadata`、`fixing-motion-performance`；组件或自由实验画布交 `component-canvas` / `create-canvas`。它们是可选专项下游，主路线与验收责任仍由本 skill 选定。
- 通用 `DESIGN.md` 重建可交 `create-design-md`；模板项目仍用本 skill 的 design-md 契约。
- `taskrail` 负责 Web UI 任务编排与证据门；`role-based-reviewer` 的 design 角色负责独立评审。视觉返修回本 skill 分派，评审规则号仍来自 pretty-ui。

## 模板校验

```bash
python3 <kit>/skills/ui-template-apply/scripts/validate_package.py package <风格包目录>
python3 <kit>/skills/ui-template-apply/scripts/validate_package.py project <项目根>
python3 <kit>/skills/ui-template-apply/scripts/verify_fidelity.py --project <项目根>
```

完成：validate 0 error，且保真比对 `fidelity: pass`（项目验收的完整顺序见 verify.md）。对比度不达标时调明度（L），不降门槛；缺 token 就补 token，不在组件里写字面值。通用路线按 pretty-ui 的截图、量测与评审标准验收，不跑模板保真命令。

## 交付

先说明选定路线、技术栈与承接方及理由。模板路线再说明风格包与版本、白名单 token、验收结果和 DESIGN.md 位置；通用路线按 pretty-ui 交付截图、评审和未验证项。

经验沉淀与正文演进走 `skill-upgrader`。
