# 说决定，不提问

- target: skills/task-intent
- mode: update
- patch: 20261015-224500-statements-not-questions
- risk: medium
- status: applied

## Intent

复述不提问：歧义按推荐说成决定并带理由；覆盖清单「要你拍板的」改为「我的决定」+「需要你提供的（只限真阻塞）」；示例改写（含拓扑初始数据例）；纠偏不再二选一提问。

背景：用户反馈意图复述里的「要我…还是…？我建议后者」多此一举——按推荐直接陈述，有问题用户自己会说。规则唯一出处为 taskrail references/user-report.md「说决定，不提问」，其余为指针。

## Conflict check

不改安全底线：线上 / 不可逆 / 对外发送、改完成标准、只有用户能给的阻塞信息仍会停，只是改用陈述句说明需要什么。human 闸口仍等用户说「继续」，但以已定决定呈现。

## Files

见 change.patch。
