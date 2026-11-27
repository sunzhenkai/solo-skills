# 补齐拍板选项完整性（必含本次执行）与部署/线上数据变更分题隔离

- target: skills/session-wrap
- mode: update
- patch: 20261127-165200-complete-options-and-data-ops-split
- risk: medium
- status: proposed

## Intent

完善 `session-wrap` 的拍板选项设计规则与高风险外部动作拆分机制：

1. **选项必须覆盖完整决策空间（含「本次执行」）**：只要动作具备可执行前提，每道拍板题的选项都必须同时包含「本次执行」与「暂不执行 / 留待后续」两个方向，且选项之间互斥、有实质区分；对高风险动作通过标注前置保护（如先 `dry-run`、备份、验证与回滚）或调整推荐项来控风险，不再出现只给多个本质都是「本次不做」的保守变体、逼用户手写补充的情况。
2. **线上数据变更与服务部署分题隔离**：将线上存量数据清理、schema/数据迁移或历史回填纳入 `release-deploy.md` 的信号识别与只读核对，并明确与「打 tag / 发版」「服务部署」各自一题，授权互不外延（部署不等于授权线上数据变更）。
3. **同步契约测试与 eval**：在 `tests/test_session_wrap_contract.py` 补充守卫断言，在 `evals/cases.yaml` 补充生产部署与线上存量数据清理分题及选项完整性案例。

## Conflict check

- 与现有 `SKILL.md` 的两轮确认、逐项授权及 8KB 体量上限完全兼容。
- 延续 `references/plan-synthesis.md` 与 `references/release-deploy.md` 的既有分层，未触碰其他 skill 或新增跨 skill 链接。

## Rationale

高风险收尾场景（如生产部署伴随存量数据清理）中，存在两类常见退化：一是把部署与线上数据变更硬捆成一题，造成选项组合爆炸与授权混杂；二是模型因保守倾向只给出「本次不动」与「下次再看」两个同义变体，省略了「本次执行」选项，迫使用户在自定义输入里手写「部署 + 清理」。将其抽象为通用的选项完整性与一题一事规则，可在所有收尾拍板场景中消除该类缺陷。

## Files

- `skills/session-wrap/SKILL.md`（在拍板与授权隔离要点中锚定选项正反完整与部署/线上数据变更隔离，保持体量 <= 8KB）
- `skills/session-wrap/references/plan-synthesis.md`（补充选项设计规则：正反完整、实质区分、一题一事与反例）
- `skills/session-wrap/references/release-deploy.md`（纳入伴随数据变更的信号、只读核对、选项完整性示例与分题授权隔离）
- `skills/session-wrap/tests/test_session_wrap_contract.py`（新增选项完整性与部署/数据变更隔离契约测试）
- `skills/session-wrap/evals/cases.yaml`（新增生产部署与存量数据清理分题及执行选项案例）

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261127-165200-complete-options-and-data-ops-split/change.patch`
- `git diff --check -- skills/session-wrap`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-style && make check-names && wc -c skills/session-wrap/SKILL.md`
