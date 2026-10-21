# task-explore、task-intent 并入 taskrail；新增 `taskrail intent` 轻入口

- target: skills/taskrail
- mode: update
- patch: 20261021-202819-merge-explore-intent
- risk: high
- status: proposed

## Intent

task 系列复审第 2 步。用户在会话里选定「按三步走：先修卡点 → 合并 task-explore / task-intent → 再做拆分」，task-intent 按「并入 taskrail，保留 `taskrail intent` 轻入口」处理。本 patch 只搬家、不改行为。风险定为 high（改 description 触发条件、删除两个 skill），用户选定该方案即为授权。

- 拆成三个 skill 时，taskrail 每个阶段都要「委托」另一个 skill，模型要在三个 SKILL.md 之间来回跳；task-explore 与 task-intent 都声明「由 taskrail 委派」，单独点名的场景很少，且它们的规则真源本来就在 taskrail 契约里。
- task-explore 的 9 份 references 原样平移进 `taskrail/references/`（只把跨 skill 链接改成同目录链接，把「回 taskrail 绑定」「回 task-intent 纠偏」改成指向同目录文件）。
- task-intent 的 SKILL.md 正文（先定做多少、流程、守住这几条）并到 `references/intent.md` 开头，原有第 1–7 节编号不变（confirm-protocol、check_output_style 按节号引用）。
- SKILL.md：主循环表从「委托 X」改为「读 references/X.md」；绑定节直链 ledger / templates / ledger-concurrency；新增 `taskrail intent <一句话目标>`：只做意图确认，已绑定任务时落 `wizard/intent.md`，没有任务目录就只在对话里给复述，不建任务。description 补「要先确认理解对不对」这一触发。
- 契约、phase-wizard、confirm-protocol、user-report 里指向两个旧 skill 的地方改成同目录文件。
- task-intent 的 29 条 eval 追加进 `evals/cases.yaml`（原文件第 237 行 `given` 含未加引号的冒号，YAML 解析失败，并入时改写为不含冒号的同义句）；两个旧 skill 的测试平移进 `tests/` 并改读新位置，新增轻入口与「两个旧目录已不存在」的断言。

非目标：阶段划分、停点、判据规则都不变；explore 与 design 是否合并、拆分机制留到第 3 步。

## Conflict check

- 旧 skill 目录 `skills/task-explore/`、`skills/task-intent/` 整体删除（按仓内先例 b0487af、69919ef：并入后删目录，历史由 git 保留）。本轮第 1 步对这两个 skill 的 patch 记录（`20261021-201813-unblock-flow`）尚未提交，随目录一起删除；其改动内容已随文件平移进来，意图与理由见 taskrail 同名 patch 的 proposal。
- 同轮 patch：taskflow（模板与入口门提示改指 taskrail）、agent-roster（Complex 轨道改绑 `$taskrail`）、trouble-grill、role-based-reviewer（指针改名）。
- 仓级：`scripts/check_output_style.py` 与 `tests/test_output_style.py` 改查 `taskrail/references/intent.md`；README、AGENTS、`docs/task-flow/README.md` 同步。
- 已安装到各 agent 目录的旧 task-explore / task-intent 副本需要使用者重新同步后移除。
- 另一会话同时在改 `references/done.md`、`references/ui-delivery.md` 与观感测试；本 patch 不碰这些文件。

## Rationale

按调用关系看，task-explore 与 task-intent 只是 taskrail 的阶段细则；并进来后模型只在一个 skill 里按 phase 读 reference，「委托」这一跳消失，触发词也只留一个入口。行为不变由平移过来的原有测试保证。

## Files

- `skills/taskrail/SKILL.md`
- `skills/taskrail/references/{contract,phase-wizard,confirm-protocol,user-report}.md`
- 新增 `skills/taskrail/references/{intent,explore-design,design-detail,approve,handoff,ledger,ledger-concurrency,templates,archive-reopen,large-scope}.md`
- `skills/taskrail/evals/cases.yaml`、`skills/taskrail/examples/README.md`
- `skills/taskrail/tests/`：改 5 份，新增 6 份（平移）

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills tests -q`；`make check-style`（含引用链一层检查）；`make check-names`；evals YAML 可解析
