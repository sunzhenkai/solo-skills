# 说决定，不提问

- target: skills/task-explore
- mode: update
- patch: 20261015-224500-statements-not-questions
- risk: medium
- status: applied

## Intent

grill 自问自答：自己查证并给推荐结论落纪要，给用户只报结论；只有真阻塞才停。commands / archive-reopen 的询问改为陈述。

背景：用户反馈意图复述里的「要我…还是…？我建议后者」多此一举——按推荐直接陈述，有问题用户自己会说。规则唯一出处为 taskrail references/user-report.md「说决定，不提问」，其余为指针。

## Conflict check

不改安全底线：线上 / 不可逆 / 对外发送、改完成标准、只有用户能给的阻塞信息仍会停，只是改用陈述句说明需要什么。human 闸口仍等用户说「继续」，但以已定决定呈现。

## Files

见 change.patch。
