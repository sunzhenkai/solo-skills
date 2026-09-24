# decision — 20260924-scriptify-rest

promote

理由：
- 用户对方案「开工」即执行指令。六个脚本逐一对应方案 P0/P1/P2，全部真实样本实测通过
  （eval.md）；实现中发现并修正一处方案未预见的缺陷（probe --write 挤掉 L3 记录）。
- 语义环节（路由、Trace 撰写、固化确认）未脚本化，与方案一致。
- 候选 diff 与 proposal 一致，无夹带；无密钥、内部 URL、项目名入库（复核对 <provider>/
  MiniMax-M3 占位形态）。

后续：commit 由编排者执行；push 属线上动作，需用户单独确认。
