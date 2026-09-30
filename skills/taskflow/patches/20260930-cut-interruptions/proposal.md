# Proposal：缺依赖 skill 不反复停（taskflow 侧）

## 背景

「委托契约」节原文：「委托前确认当前 agent 环境能读到它们；不可用就停下报告并给出可选项（跑 `dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调），不要自行发明等价命令。」选项已经列全，但仍写成「停下」——用户不在场时这轮就空转。

## 决定

改为：不可用就**在同一条回复里给全可选项与推荐项**——`dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调——用户选完即继续，不反复停。保留「不要自行发明等价命令」。

## 理由

选项集合未变，只把「停下等一轮」改成「一轮内给全」。不新增等价命令，不绕过委托绑定（planning root + change name 的要求原样保留）。

## 验证

- `python3 -m pytest skills/taskflow -q` 全过。

## 明确不改

driver 脚手架三步、`proposal.md` 模板与 Driver 协议固定文本、进度归属、一轮结束三条件、并行执行、实现者输入。
