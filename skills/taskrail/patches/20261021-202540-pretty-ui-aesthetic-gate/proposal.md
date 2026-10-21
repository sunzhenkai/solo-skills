# 观感验收与 Web UI 交付改用 pretty-ui 的方向卡、取证、评审手册与体系产出

- target: skills/taskrail
- mode: update
- patch: 20261021-202540-pretty-ui-aesthetic-gate
- risk: medium
- status: proposed

## Intent

pretty-ui 重写后（`skills/pretty-ui/patches/20261021-200926-fuse-oil-ui-refactoring-ui/`）有了轻量方向卡、取证与量测、隔离评审手册、带规则号的问题表和设计体系产出。taskrail 的观感验收和 Web UI 交付包仍是改名前的写法：视觉方向只列配色、字体、版式；评审没有手册，“观感 Blocker / Major”没有判定依据；Active Instance 的内容和代表页做法没有方法来源。本 patch 让这几处直接引用 pretty-ui，判定标准有了出处，goal 模式自迭代也有了停止条件：

- 「视觉方向」改为按 `direction.md` 第 6 节写轻量方向卡（多了“放弃什么”）。
- 「截图」补一句：视口与行长量测按 `critique.md` 第 1 节。
- 「另一个模型审」：材料与评审手册按 `critique.md` 第 3–4 节，问题带规则号，P0 / P1 即观感 Blocker / Major；要连交互、无障碍一起审时再加 `role-based-reviewer roles=design`。goal 子条写明结论是重做或需改就继续迭代。
- `ui-delivery.md`：Active Instance 的 `tokens.css` / `DESIGN.md` / `preview.html` 按 pretty-ui `system.md` 产出；代表页按 pretty-ui build 主流程 two-pass。

非目标：goal / human 两种确认方式、证据门（`ui_evidence_check.py`、`--validate-review`）、freeze 与三条 digest、交接四行全部不变；评审文件的 frontmatter 格式不变。

## Conflict check

- 测试锁定的字串全部保留：`## 观感验收`、`pretty-ui/references/direction.md`、`goal：不停下问人`、`human：`、`用户说可以才算完成`、`演示数据`、`改前 / 改后`、`观感交付`、`ui_evidence_check.py`、`--validate-review`。
- 级别映射与 taskrail 契约一致（contract 已有 P0 = Blocker、P1 = Major）；pretty-ui `critique.md` 第 7 节「同一个 P0 两轮没改好」与本文件「卡住」规则一致，两边互相指向。
- pretty-ui `system.md` 第 7 节已写明“在 taskrail 任务里，这三个文件就是 Active Instance 的内容；版本目录、freeze 与摘要规则按 ui-delivery.md 执行”，本 patch 补上另一侧的指针。
- 工作区里同时有另一轮 task 系列改动（`20261021-201813-unblock-flow`）在改 taskrail 的其他文件；本 patch 只碰 `done.md`、`ui-delivery.md` 与 `test_aesthetic_goal_contract.py`，两者不重叠。

## Rationale

观感是最容易“凭感觉”通过或卡住的验收项。把方向、取证、评审和问题表接到同一套方法上，评审意见能指到规则号、能逐条复核，goal 模式迭代到“没有 P0 / P1”时就有据可停。

## Files

- `skills/taskrail/references/done.md`
- `skills/taskrail/references/ui-delivery.md`
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`（新增 critique 指针、P0 / P1 映射、ui-delivery 指针与跨 skill 链接可解析的断言）

## Validation

- 应用前：在仓库外的干净副本上 `git apply --check --recount`，应用后与候选树一致
- 应用后：`git diff --check`；`python3 -m pytest skills/taskrail/tests -q`；全量 `python3 -m pytest skills tests -q`；`make check-style`；`make check-names`
