# Proposal：「在 goal 里」的判据改为指向真源（第三批·task-explore 侧）

## 背景

本 skill 的「Goal 里的确认」节自写了一份触发判据：消息里有 `/goal`，**或当前有进行中的 goal**，**或本任务由 Goal 方案交接且方案里带完成判据**。第三条是 task-goal 触发节没有的，而 task-goal 的第三条是「被上游 skill 以 goal 模式委派」。两套判据不同源，会出现本 skill 认定自己在 goal 里、task-goal 不认（或反之）的错位。

## 决定

该节第一段的触发条件改为指向 task-goal 的「触发」节，声明判据以那里为单一真源，本 skill 不另写一份。其余内容（走审阅、推荐默认取法、收敛即继续、停下条件）一律不变。

## 理由

判据只该有一处。方向选 task-goal 而非 task-explore，是因为 goal 协议与状态机都在 task-goal，它才是「是否处在 goal 里」的定义方。

## 验证

- 全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**（既有 `test_goal_confirmations_go_to_review` 断言的是审阅行为，未触及触发条件措辞，故全过）。

## 明确不改

「Goal 里的确认」节的其余内容、`decide` / `handoff` 的 goal 分支、非 goal 下的确认规则。
