# 收尾主轴对齐零遗留与未完成中止门禁

- target: skills/session-wrap
- mode: update
- patch: 20261126-203800-zero-tail-and-abort-gate
- risk: medium
- status: proposed

## Intent

从「完成后不再需要继续关注遗漏；未完成时先确认是否中止」的收尾意图出发，重构 `session-wrap` 主流程与配套细则：

1. **先判完成度，未完成走三选一中止门禁**：只读核对目标与证据后先裁决主线是否完成；未完成时进入 `references/incomplete-abort.md`（继续做完 / 暂停挂起 / 彻底放弃），跳过合入主分支、打 tag、发版与部署检查。
2. **完成态补全多仓、非代码交付与隐性清场**：代码交付核对覆盖多仓/多 worktree；非代码交付核对最终产物落位与发送；现场清空补充调试痕迹（日志/mock/跳过开关/临时配置）还原与容器/端口/`git stash` 检查。
3. **消除静默遗留与模糊放手**：无持久台账与外部 tracker 的遗留不再默认静默留在聊天里，须在第一轮拍板选择目标位置或明确确认不跟踪；第二轮开头收敛为四种明确放手结论（彻底收工 / 本地收尾剩外部等待 / 已暂停挂起 / 已确认中止），未合入且未开自动合并的 MR 归为外部等待项。
4. **弯路复盘与知识沉淀按信号附带**：保留 `detour-review.md` 与 `plan-synthesis.md` 知识分流，但明确为命中信号时附带，不干扰主收尾决策。

## Conflict check

- 与 `taskrail` `close` 的 `done` / `archived` 语义对齐：完成态交 `taskrail` `close`（`done`），暂停挂起保持 `active` 并更新断点，彻底放弃交 `taskrail` `close` 按未完成关闭（`archived`）。
- 其他 skill（`trouble-grill`、`way-to-fix`、`anti-lazy`、`taskrail`）仅按名引用 `session-wrap`，无跨 skill 相对链接或悬空引用冲突。
- 仓库根 `README.md` 同步更新 `session-wrap` 一行简介，不含在本 skill 的 `change.patch` 内。

## Rationale

既有 `session-wrap` 默认主线已完成并直接列代码合入清单，导致半途收尾或验收失败时缺少中止确认，且无台账遗留沉入聊天记录、未合入 MR 与彻底收工边界不清。将完成度裁决前置、拆分暂停与彻底放弃、补齐零遗留落宿与四种放手结论，可让每次收尾都有可验证的终止态。

## Files

- `skills/session-wrap/SKILL.md`（重写 `description` 与主流程，新增未完成门禁入口与四种放手结论，直链 `references/incomplete-abort.md`）
- `skills/session-wrap/references/incomplete-abort.md`（新增：未完成判定、三选一门禁、暂停保现场与放弃撤场细则）
- `skills/session-wrap/references/plan-synthesis.md`（修正无台账遗留落点规则，补充未完成与四态结论示范及反例）
- `skills/session-wrap/references/branch-merge.md`（补充多仓/多 worktree 核对，未合入 MR 归入外部等待项）
- `skills/session-wrap/tests/test_session_wrap_contract.py`（新增未完成门禁、暂停/放弃语义、零遗留四态结论契约测试）
- `skills/session-wrap/evals/cases.yaml`（更新边界 case 并新增 5 条覆盖未完成、暂停、放弃、外部等待与无台账遗留的 eval 案例）

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261126-203800-zero-tail-and-abort-gate/change.patch`
- `git diff --check -- skills/session-wrap README.md`
- `wc -c skills/session-wrap/SKILL.md`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-style && make check-names`
