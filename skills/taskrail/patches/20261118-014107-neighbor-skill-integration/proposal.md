# 环节接入相邻 skill，清理 examples 索引的已删除路径

- target: skills/taskrail
- mode: update
- patch: 20261118-014107-neighbor-skill-integration
- risk: medium
- status: proposed

## Intent

让 taskrail 对外的引用指向当前真实存在的机制：

1. diagnose：多轮或易发散的根因排查按 `trouble-grill` 执行，记录写 `evidence/diagnose.md`；未安装时按本文件方法。
2. explore：项目有 Atlas / 知识 wiki 时先读入口与相关页，证据层级可按 `project-explore`，过期或冲突以源码为准。
3. close：项目有 Atlas 时跑 `status`，过期页交 `project-atlas` 或列入 SUMMARY 后续项；经验、踩坑、操作台账交 `wiki-data`；skill 改进交 `skill-upgrader`。
4. examples 索引：去掉已删除的 `wizard/intent.md` 与失效的节号，标明 minimal-webui 是旧 handoff 兼容样例。

非目标：路由算法、完成门、done 条件与台账结构不变；只按名称指向相邻 skill，不新增跨 skill 相对链接。

## Conflict check

none。trouble-grill、project-explore、project-atlas、wiki-data 已在各自正文声明这些分工，taskrail 此前未回指；session-wrap 第 6 节的知识落点表与本改动一致。

## Rationale

经 taskrail 交付的代码改动会让项目 Atlas 静默过期，而 Atlas 的 `status` 自愈正是为这一步设计的；diagnose 与 trouble-grill 两套根因方法此前互不引用。

## Files

- skills/taskrail/references/diagnose.md：执行方法第 5 步。
- skills/taskrail/references/explore.md：执行方法第 1 步。
- skills/taskrail/references/close.md：执行方法第 2 步的落点分流。
- skills/taskrail/examples/README.md：两条索引。
- skills/taskrail/tests/test_neighbor_skill_contract.py：新增守卫断言。

## Validation

- `python3 -m pytest skills/taskrail/tests -q`
- 全量测试与 `make check-style`
