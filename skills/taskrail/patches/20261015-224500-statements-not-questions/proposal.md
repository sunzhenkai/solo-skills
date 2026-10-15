# 说决定，不提问

- target: skills/taskrail
- mode: update
- patch: 20261015-224500-statements-not-questions
- risk: medium
- status: applied

## Intent

user-report 第 5 节改为「说决定，不提问」（真阻塞清单 + 陈述句示例），报告顺序第 4 项改「我做的决定」，resume 模板去掉提问；contract 对比示例去问句；confirm-protocol human 闸口以已定决定呈现、陈述式收口；phase-wizard 先查后定。

背景：用户反馈意图复述里的「要我…还是…？我建议后者」多此一举——按推荐直接陈述，有问题用户自己会说。规则唯一出处为 taskrail references/user-report.md「说决定，不提问」，其余为指针。

## Conflict check

不改安全底线：线上 / 不可逆 / 对外发送、改完成标准、只有用户能给的阻塞信息仍会停，只是改用陈述句说明需要什么。human 闸口仍等用户说「继续」，但以已定决定呈现。

## Files

见 change.patch。
