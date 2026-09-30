# Result：缺依赖 skill 不反复停

已 `git apply` 应用。

## 应用后的正文变化

「委托契约」节原文「不可用就停下报告并给出可选项（跑 `dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调）」改为：

> 不可用就在同一条回复里给全可选项与推荐项——跑 `dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调——用户选完即继续，不反复停，**不要自行发明等价命令**。

## 测试

`python3 -m pytest skills/taskflow -q` 全过；全仓 415 passed, 1 skipped。

## 遗留

- 无。选项集合未变，只把「停下等一轮」改为「一轮内给全」。

## 未验证 / 待观察

无新机制，只是措辞与交互轮次的调整。
