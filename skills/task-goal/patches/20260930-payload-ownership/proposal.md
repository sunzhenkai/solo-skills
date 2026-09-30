# Proposal：完成判据由本协议产出（批 A·task-goal 侧）

## 背景

交接链上两个关键载荷在 2026-09-29 的 `decouple-goal-protocol` 拆分里失去了主人——那次拆分把 Goal 方案层从 task-wizard 整体搬进 task-goal，只改了生产者、没改消费者：

- **完成判据**：wizard 模板里「## 完成判据」小节被删（留下 `## 目标 <一句话说清完成标准>`），但 task-goal 起手节仍写「上游（task-wizard）的步骤级方案，含完成判据」，task-explore/taskflow/task-delivery 三环都要求它逐字传递。缺判据时 task-goal 的处理是「按自产方案处理，从摸底开始」——一次全量返工。
- **质量画像**：wizard 全文没有「画像」二字，但 5 处活文本宣称它产画像（`README.md:11`、`task-delivery/references/loop-protocol.md:20,23`、`task-explore/references/task-template.md:3`、`phase-decide.md:14`），另有 3 处泛称「上游」需同改。

## 决定

本 patch 负责 task-goal 侧的归属声明：**质量画像与显式降级由本协议产出**（简单和中等写「无」；上游带原文快照时逐字采用，不重做），起手节与正文模板节各加一句。

完成判据的产出权归 task-wizard（见 task-wizard 侧 patch）；本协议在上游缺判据时按「判据缺失」处理——由审阅派出的评审者给候选判据（上一批 `cut-interruptions` 已落地），不再走全量摸底。

## 理由

- 载荷有唯一产出点，链条才可验证；否则每环都假设上游会给，而没人被指定为产出者。
- 画像归 task-goal 而非 wizard：画像只是复杂档的产物，是 goal 协议的概念（含 A/B 降级确认门），wizard 不感知 goal。

## 验证

- 族级契约测试 `skills/task-goal/tests/test_task_family_contract.py::TestPayloadOwners`（本批新增）：断言 wizard 含完成判据且不含「质量画像」、goal 声明画像产出权、族内无残留的 wizard 画像归属。

## 明确不改

审阅边界与 P 级判定、降级 A/B 定义（仍在 `references/quality-profile.md`）、三档路由。
