# Eval：execution-spine（20261011，taskflow）

## 回归

- 红绿：新增契约测试 `tests/test_execution_spine_contract.py`（22 条）
  对生产稿 **19 failed / 3 passed**；候选暂存后 22 条全过。
- 既有 taskflow 测试 40 条（含 Self-evolution 块四 skill 逐字一致锁、
  Driver 协议逐字锁、模板锁）全程不破——候选只动 SKILL.md 正文
  小节与两份 references，未触碰锁定块与模板。
- 全仓门禁：候选暂存 `python3 -m pytest skills -q` → **410 passed,
  1 skipped**（前基线 388 + 新增 22 = 410）。

## 模式

- F4 契约未冻结即并行 / F5 同类失败不升级：新增「实现者输入三件
  套（契约文件 / 门包 / 证据要求）」+「旗舰先行」+「≥2 单元同类
  失败判契约缺陷、停并行回 design」。
- F6 评审集中收尾：「增量评审」段（旗舰后必审、每批切片审、
  修复后重跑受影响层再审）+ 全量 disposition 要求。
- F8 证据无契约：证据段补「状态绑定（提交号 / dirty 摘要）」、
  「覆盖边界」、「工具不可用替代（不等于等价通过）」。
- F9 归档无机械校核：新增「收尾机械校核」节（子 change 全勾 +
  validate + 降级无 pending + findings disposition + 证据状态一致）
  + 收尾骨架新增 3.4 校核项 + 禁止 `--yes` 掩盖、归档后不可回改。
- M2 执行器绑定：rubric「评分主体与顺序」改为 MUST 经
  role-based-reviewer 结构化调用、角色按门包表、可自动化门失败
  封顶 <2.5、未覆盖按降级计、复杂档 SHOULD 异源。

## 契约

- 第一级（skill 自带测试）：22 条新增断言红绿验证；既有 40 条不破。
- 第二级（宿主仓 AGENTS.md 声明门禁）：`python3 -m pytest skills -q`
  候选暂存 410 passed 通过。
- 跨 skill 引用：`../task-confirm/references/gate-packs.md`（SKILL.md）
  与 `../../task-confirm/references/gate-packs.md`（两份 references）
  相对路径核验存在（对应 task-confirm 20261011 轮已晋升的门包真源）。

## 副作用

- 触发范围：新增均为收紧（派发前置、归档前置、评分绑定）；
  未改触发条件、权限、密钥与破坏性操作；未新增脚本或外部依赖。
- 过拟合检查：提案 / 正文 / 两份 references / eval 无项目名、
  文件名、密钥、机器路径；证据按「时间 + 次数 + 事件类型」抽象。
- 与既有纪律不冲突：共享面广播纪律（上轮）、Driver 协议逐字块、
  Self-evolution 块、simple 单切片节均未改。

## 结论

pass
