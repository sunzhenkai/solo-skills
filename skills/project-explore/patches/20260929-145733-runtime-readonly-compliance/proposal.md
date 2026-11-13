# 运行时只读合规：移除向 skill 目录写盘的指示

- target: skills/code-explore
- mode: update
- patch: 20260929-145733-runtime-readonly-compliance
- risk: medium
- status: proposed

## Intent

review（2026-09-29，glm-5.3 版）实证本 skill 正文与仓库最高纪律冲突：

1. Self-evolution 节指示任务后向 skill 内 `examples/`、`experience/` 写盘。
   安装是字节复制镜像，写入下次同步即丢；AGENTS.md「运行时只读：运行产物
   一律落仓库之外」直接禁止。
2. 「公共复用清理」节是私有源仓时代的导出指引，公开仓中已失语境，且与
   仓库级 AGENTS.md 公开仓纪律重复。
3. 与 llm-wiki 的边界只有单向声明（它让渡代码探索），本 skill 未反向声明
   知识 wiki 维护不在范围内，「整理进知识库」类请求可双触发。

## Changes

1. Self-evolution 节（约 85 行）替换为「经验回灌」节：产物落工作区；正文
   改进走源仓 skill-evolver / skill-upgrader update 显式流程；保留「单次
   失败或单次纠正不改 skill」门槛。
2. 删除「公共复用清理」节（脱敏原则由仓库纪律与本 skill `<REDACTED>`
   规则覆盖）。
3. 阶段选择节补一行：知识 wiki 维护（typed 页面重组、lint、健康检查）归
   llm-wiki，本 skill 只写项目知识库。

## Files

- `skills/code-explore/SKILL.md`（唯一改动文件）

## Validation

- change.patch 取自实际 `git diff`，反向可核对
- `python3 -m pytest skills -q` 全绿
- 全文 grep 确认不再有向 skill 目录写盘的指示
