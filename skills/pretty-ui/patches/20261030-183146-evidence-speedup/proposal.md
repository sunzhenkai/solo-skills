# 按目标视口分阶段取证并减少重复等待

- target: skills/pretty-ui
- mode: update
- patch: 20261030-183146-evidence-speedup
- risk: medium
- status: proposed

## Intent

减少 pretty-ui 首轮看图、外部标杆和复审中的固定开销：

- 简报按设备与既有断点选择目标视口；桌面或手机专用页面只验目标视口，响应式或无法判断时仍验 1280 与 375，发现风险可补入另一视口。
- 首轮每个目标视口截首屏并量测，交付前补整页；一屏页面复用首屏，refine 改前仍做完整诊断。
- 同一任务复用本地服务与浏览器会话，首轮首屏完成即可评审。
- 默认取一家标杆首屏，品类不清或多个方向时才取第二家；一次搜索和一次打开未得画面即标记后继续。
- 复审聚焦上轮问题与新增 P0，新 P2 和提升写入交付说明，不单独触发新轮次或状态截图。

非目标：不改变响应式页面的双视口质量门槛、P0/P1 收敛标准、goal/human 确认方式、`check_page.py`、taskrail 的运行态证据硬门与其他 Skill。

## Conflict check

- `rules.md` S8 与 `page.md` 完成检查仍写死双视口，需同步指向目标视口；阅读页默认仍为响应式。
- taskrail `references/done.md` 只引用 evidence.md，无需改动；其 `ui_evidence_check.py` 双视口硬门独立存在，evidence.md 明确上游硬门优先。
- frontmatter、脚本接口、输出路径与评审三态结论不变。

## Rationale

把设备选择和首屏/整页时机统一收进 evidence.md，减少桌面专用页面的无效手机取证，并让首轮评审更早开始；完整 DOM 量测与最终整页截图继续覆盖首屏以下。浏览器复用和标杆止损降低工具与网络等待，复审范围约束避免低优先级建议造成额外循环。契约测试与 evals 可直接守卫这些行为分支。

## Files

- `skills/pretty-ui/SKILL.md`：简报与构建完成判据改按目标视口，看图段指向统一取证契约。
- `skills/pretty-ui/references/evidence.md`：目标视口、首屏/整页时机、一屏去重与浏览器复用。
- `skills/pretty-ui/references/rules.md`：S8 对齐目标视口与响应式双视口。
- `skills/pretty-ui/references/page.md`：截图步骤与完成检查改指统一契约。
- `skills/pretty-ui/references/direction.md`：标杆默认一家与取证止损。
- `skills/pretty-ui/references/critique.md`：复审范围与低优先级问题停止规则。
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`：更新并新增行为契约断言。
- `skills/pretty-ui/evals/cases.yaml`：更新旧期望并覆盖桌面专用、响应式、整页去重和复审停止分支。

## Validation

- 应用前：`git apply --check --recount skills/pretty-ui/patches/20261030-183146-evidence-speedup/change.patch`。
- 应用后：`git diff --check -- skills/pretty-ui`（排除 patch 文件）；`python3 -m pytest skills/pretty-ui/tests -q`；`python3 -m pytest skills -q`；`make check-names`；`make check-style`。
- 核对实际 diff 与 proposal 一致、frontmatter 合法、引用存在、无隐私信息、未改安装镜像或历史 patch。
