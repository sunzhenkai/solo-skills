# 完成清单（唯一真源）

`status: done` 前逐条核对；driver 归档、checkbox 全勾、目录已归档都不能代替本清单。

1. **判据成立**：criterion 原文成立，有当前代码的命令与结果。direct 证据在 PLAN / evidence，OpenSpec 在 driver proposal 验证记录。
2. **意图未漂移**：输出形态、“不做”和用户限制均满足。
3. **交付标准**：PLAN / design 中的交付标准全过。
4. **关键未知闭环**：影响 criterion 的 `U-n` 均已解决；其余 `F-n` 已写入 SUMMARY 的剩余风险或后续项。
5. **父子闭环**：所有直接子任务 done，父 ROADMAP 集成项和总判据已验证。
6. **评审处置**：Blocker / Major 均 fixed；未修复项的 accepted-recorded 在 human 下必须有用户明确接受，goal 不放行。
7. **观感**：用户原话有观感目标时，下方验收已过。
8. **知识闭环**：SUMMARY.md 已写结果、验证、认知更正、可复用经验、剩余风险和合入方式。
9. **不少交付**：未验证项不能算过；验证不足、接受剩余风险、缩小 criterion 或交付面必须按确认协议获放行，否则保持未完成。

## 观感验收

- 动手前按 [pretty-ui](../../pretty-ui/SKILL.md) 的「轻量方向卡」写视觉方向，整体改版用完整方向卡；规则见 [direction.md](../../pretty-ui/references/direction.md)，记录于 PLAN 质量属性。
- 用接近真实的演示数据，按 [evidence.md](../../pretty-ui/references/evidence.md) 在同路由同视口留改前 / 改后证据；代码变更后旧证据失效。
- 按 [critique.md](../../pretty-ui/references/critique.md) 派另一个模型审，问题带规则号，P0 / P1 即观感 Blocker / Major；迭代与停止以该文件「迭代与停止」为准。
- **goal：不停下问人**，按证据自迭代；**human：**评审过后由用户看截图，用户说可以才算完成。每轮结论与证据路径写验证记录。

命中才读 [ui-delivery.md](ui-delivery.md)、[quality-appendix.md](quality-appendix.md) 和上述 pretty-ui 细则。
