# review 小修打包：10 个 skill 的门禁表述、边界声明与结构修订

- target: skills/{agent-roster-flow,task-wizard,taskflow,trouble-grill,commit-push,project-init,lark-cli,repo-manager,pretty-view-html,service-manager}
- mode: update（多 skill 打包）
- patch: 20260929-151706-review-findings-small-fixes
- risk: low
- status: proposed

## Intent

review（2026-09-29，glm-5.3 版）low/medium 级小修一次收口。role-based-reviewer
与 delivery-loop 另有进行中进化，本轮跳过。

## Changes

1. agent-roster-flow：tracks.md 收尾行「探索任务已在 handoff 归档」与
   task-explore 的 archive 独立阶段语义冲突，改为保持 handed-off；stages.md
   的 ocr 缩写补来源说明。
2. task-wizard：完成程度写入规则改显式条件分支（P0/P1 有无优先于审阅者
   定级，原表述易反向误读）；quality-profile 的 icon 四问去掉内嵌具体答案
   （与「不规定具体取值」自相矛盾）。
3. taskflow：rubric 全量通过线补「UI/UX 六子项均值 ≥2.5、任一子项为 0
   不通过」（原只在表格单独看会漏）；删 delivery-quality-loop 指向不存在
   术语节的落空引用。
4. trouble-grill：无台账时的落盘位置补基准（循工作区既有约定，无约定先问，
   不在任意 cwd 造目录）。
5. commit-push：description 补「何时不用」；「何时问用户」补共享远程/默认
   分支推送前单独确认。
6. project-init：前端分层表 Next.js 两行合一（Build/Framework 双行易读成
   两个选层决定）。
7. lark-cli：CLI 缺失时安装建议主次调换（通用 npm 命令在前，dotf 环境等效
   提法在后）。
8. repo-manager：正文 439 → 382 行，「踩坑（可复用经验）」61 行下沉
   references/pitfalls.md（正文每次触发全量进上下文，体量即成本）；补
   grepom 源码链接（原全文无上游来源，外部用户无从获得依赖）。
9. pretty-view-html：description 补「何时不用」（原任何「生成 HTML」请求
   都会命中）；vendored frontend-design 补上游来源注记并随附上游
   LICENSE.txt（Apache-2.0，出处 anthropics/skills，原声明 LICENSE.txt
   却未附带）。
10. service-manager：开发服务默认不改监听配置（原默认补绑 0.0.0.0 是作者
    个人 LAN 工作流，公开仓受众下有暴露面），宽绑定改为需明确需求 + 网络
    可信确认；.service-manager.md 自动创建改先询问（对齐 repo-manager 台账
    「创建前先询问」门禁哲学）；对应 eval case 同步。

## Files

见 Changes 各条；全部为 SKILL.md / references / evals 文本修订。

## Validation

- python3 -m pytest skills -q 全绿
- repo-manager SKILL.md 行数下降约 57 行，pitfalls.md 内容与原节一致
- LICENSE.txt 与上游逐字一致（raw 下载）
