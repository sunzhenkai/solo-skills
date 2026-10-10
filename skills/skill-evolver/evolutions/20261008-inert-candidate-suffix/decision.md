# Decision

`promote`

## Reason

- 用户先确认 Evolution Proposal，再确认候选 diff 与晋升。
- Evaluate 为 `pass`：复现实验证明新规则消除失败模式（原样复制 → collection 中断；加 `.candidate` → `438 passed, 1 skipped`）。
- 候选与生产的 diff 只含 Proposal 声明的两处（§4 布局 + 规则 6、§5 契约两级判据），未夹带无关编辑，未改动门禁触发条件与安全约束。

## Action

- 已用候选 `SKILL.md` 覆盖生产稿 `skills/skill-evolver/SKILL.md`。
- 本轮候选目录只含 `SKILL.md`（正文允许的名字）+ `proposal.yaml` / `eval.md` / `decision.md`，未携带需加后缀的其他候选；实验用临时文件已删除。
- 历史 4 种避让命名按规则不追溯改名。
- 未执行 git commit，未同步 `~/.agents/skills/` 安装镜像（需使用者经安装通道自行同步）。
