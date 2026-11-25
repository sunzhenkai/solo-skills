# 补齐按项目信号触发的打 tag / 发布 / 部署必查确认项

- target: skills/session-wrap
- mode: update
- patch: 20261125-100000-release-deploy-signal-check
- risk: medium
- status: proposed

## Intent

将「是否需要打 tag / 发布 / 部署」做成 `session-wrap` 中**按项目信号触发的必查确认项**：

1. **按信号触发，不盲目追问**：有代码、配置或产物改动时，先只读检查是否命中发布或部署信号（会话/变更信号、项目发布信号、环境与现状信号）；命中时纳入收尾检查与拍板清单，未命中则跳过。
2. **新增 `references/release-deploy.md`**：承接只读信号识别、只读核对（合入与验证前提、版本与 tag 现状、渠道与目标环境、生效验证与回滚指向）、推荐与逐项拍板规则，以及确认后复用项目既有脚本/CI/`repo-manager` 等渠道落地与汇报。
3. **补全主文、授权隔离与清单排序**：在 `SKILL.md` 和 `references/plan-synthesis.md` 中把「打 tag / 发布 / 部署（命中项目信号时）」纳入代码交付闭环、依赖排序与「需要你拍板」；明确「合入不等于授权打 tag / 发版或部署，打 tag / 发版不等于授权部署，测试环境部署不等于授权生产部署」，且发版与部署、不同目标环境各自一题。
4. **同步测试与 eval**：在 `tests/test_session_wrap_contract.py` 补充契约守卫测试，在 `evals/cases.yaml` 补充命中信号与未命中信号两条案例。

## Conflict check

- 与既有 `references/branch-merge.md` 的分支合入闭环及授权隔离规则完全兼容，按「合入主分支 → 打 tag / 发布 / 部署」依赖顺序衔接。
- 未触碰其他 skill 内部约束，未新增跨 skill 相对链接；仅按既有名称引用 `repo-manager`、`commit-push`、`taskrail` 等。
- `README.md` 根目录的 `session-wrap` 一行简介将随仓同步更新，不含在本 skill 的 `change.patch` 内。

## Rationale

`f9fa9b8` 精简后代码交付闭环只追到「合入 / 提 MR/PR → 清理 worktree」，导致有版本 tag、发布流水线或部署目标的项目在收尾时不会主动核对是否需要打 tag、发版或部署。通过「按项目信号触发」的机制，既能避免无发布机制的仓库被无效追问，又能确保命中信号的项目在收尾时逐项拍板并守住授权隔离。

## Files

- `skills/session-wrap/SKILL.md`（更新 description、代码交付闭环、依赖排序、拍板范围、授权隔离与路由执行）
- `skills/session-wrap/references/release-deploy.md`（新增：按信号触发的发布与部署检查细则）
- `skills/session-wrap/references/plan-synthesis.md`（更新「需要你拍板」事项、排序、提问授权隔离与反例）
- `skills/session-wrap/tests/test_session_wrap_contract.py`（新增信号检查与授权隔离契约测试）
- `skills/session-wrap/evals/cases.yaml`（新增命中信号与未命中信号两条 eval 案例）

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261125-100000-release-deploy-signal-check/change.patch`
- `git diff --check -- skills/session-wrap README.md`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-style && make check-names && wc -c skills/session-wrap/SKILL.md`
