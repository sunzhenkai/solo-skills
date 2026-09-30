# Eval：partial-suspend

## 回归

- 全仓契约测试：384 passed, 1 skipped（候选 staged 后）；红绿验证：
  13 条新断言对旧生产稿全失败、对候选稿全过。task-delivery 首次获得
  契约测试目录。
- 安全边界未放宽：危险操作、线上、泄密、不自动 commit/push 原文未动；
  停止条件清单条目数未减，只改语义（A/B 拆分、连败措辞）。
- 异源门 (a)(b)(c) 降级顺序未动；(c) 的「停下问使用者」补了五元组
  呈现形状（原来无形态定义——审计 D2 的呈现侧）。
- 跨 skill 引用核验：suspension.md 与 quality-profile.md 相对路径
  指向 task-goal 均存在（契约断言锁定，防镜像同步后断链）。

## 模式

- 全局停摆形态：A 类降级 pending 时新规则只冻结依赖面——环境准备、
  脚手架、无关切片继续（真实 case 中 Stage 2 前的六项环境取证在新规
  则下有名分且可推进更多）。✔
- 两轮封顶形态：同 task-goal loss-streak 复盘——旧条全消 + 新增未达
  恶化闸 → 继续；同条连败两轮 → 停。✔
- 真人门缺席形态：等待期五元组呈现 + 非依赖工作继续；B 类降级追认
  与真人门合并为一次交互。✔
- 预算耗尽：恢复路径 + 授权形状进停止报告。✔

## 契约

- `python3 -m pytest skills/task-delivery/tests -q`：13 passed。
- `python3 -m pytest skills -q`：384 passed, 1 skipped。

## 副作用

- 触发范围：停止条件、Stage 9、真人门、预算语义；Stage 0-8、10
  的其余规则未动。
- 预算语义变更（repairs-per-slice→repairs-per-finding）：已有
  manifest 若带旧 key，属新一轮运行重新记录，无兼容负担（evidence_root
  每轮新建）。
- 诚实记录：依赖面/非依赖面的划分由编排者判，「环境准备、脚手架、
  只读取证、无关切片」白名单收窄了自由裁量；越界推进的兜底仍是
  goal 层无进展轮与授权封闭集合。

## 结论

pass
