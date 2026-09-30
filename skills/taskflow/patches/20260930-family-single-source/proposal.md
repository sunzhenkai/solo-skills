# Proposal：修三处跨 skill 坏链（批 B·taskflow 侧）

## 背景

`SKILL.md` 三处指向 task-goal 的相对链接写成 `../../task-goal/...`，而 `SKILL.md` 位于 `skills/taskflow/`，退一层即到 `skills/`——多退的一层使其成为坏链（实测 `is_file()` 为假）。此前无人发现，因为各 skill 的契约测试只查自己目录下的 references 是否存在。

## 决定

三处 `../../task-goal/...` 改为 `../task-goal/...`：

- A/B 降级定级引用 → `../task-goal/references/quality-profile.md`
- 授权节引用 → `../task-goal/SKILL.md`
- 挂起五元组引用 → `../task-goal/references/suspension.md`

## 理由

只改链接深度，不改任何措辞与语义。配套在批 B 新增的族级测试里加了「族内相对链接全可达」断言，防止同类问题再出现。

## 验证

- 族级测试 `TestFamilyLinksResolve::test_all_relative_links_reachable`。
- 反向验证：改回 `../../` 时该测试报出具体文件与目标路径。

## 明确不改

Driver 协议模板、脚手架三步、进度归属、一轮结束三条件、并行执行、实现者输入。
