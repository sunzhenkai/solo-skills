# task 系列：一页地图

规则真源在各 skill 文件；本页与之冲突时以真源为准。契约总真源（阶段、档位、目录、术语）：[skills/taskrail/references/contract.md](../../skills/taskrail/references/contract.md)。

task 系列只做三件事：**按步骤把任务做完且符合预期**（taskrail）、**先理解意图**（task-intent）、**用人话交流**（user-report）。

## 谁干什么

| skill | 一句话 |
|---|---|
| `taskrail` | 唯一编排入口：绑定 `tasks/` 台账，按阶段推进，按完成清单收口 |
| `task-intent` | 开工前对齐意图：只读探索 → 1–3 句口语复述 → 纠偏到确认 |
| `task-explore` | explore（grill 自问自答）/ design / approve / handoff |
| `taskflow` | 交接后执行：建 `{task}-driver`，拆 OpenSpec change，进度只认 checkbox |
| `role-based-reviewer` | 可选的岗位化只读评审 |

## 流程

```mermaid
flowchart LR
  W[wizard<br/>task-intent 意图复述 + plan.md + criterion]
  W -->|skip| S[直接实现 + 验证]
  W -->|full| E[explore] --> D[design] --> A[approve] --> H[handoff<br/>check_handoff.py]
  H --> P[taskflow<br/>propose / apply]
  S --> DONE{完成清单 done.md}
  P --> DONE
  DONE -->|过| X[done → archive]
  DONE -->|不过，skip| S
  DONE -->|不过，full| P
```

## 两个档位

| 档位 | 什么时候 | wizard 之后 |
|---|---|---|
| `skip` | 局部修改，一句话说得清 | 直接实现 + 验证 → done |
| `full` | 其余 | explore → design → approve → handoff → propose → apply → archive |

旧任务里的 `simple` 按 `skip` 读，`medium` / `complex` 按 `full` 读。

## human 与 goal

| | human（默认） | goal（`/goal` 或 `goal:`） |
|---|---|---|
| 停几次 | wizard 定稿时看意图复述和计划要点；full 档 approve 时看方案。说「继续」即放行，其余阶段说决定接着做 | 不停，另一个模型审，收敛就继续 |
| 意图 | 你看复述，说对或指出哪里不对 | 另一个模型按清单审，最多两轮 |
| 一定停下 | 删数据、改共享配置、线上 / 对外发送、改完成标准、缺凭据或只有你知道的信息 | 同左 |

## 按需才读的包

- Web UI：`taskrail/references/ui-delivery.md`
- 质量画像 / 打分：`taskrail/references/quality-appendix.md`
- 多 worker 并行：`taskflow/references/multi-worker.md`
- 大范围拆子任务：`task-explore/references/large-scope.md`
- 台账并发写：`task-explore/references/ledger-concurrency.md`

## 怎么用

```text
taskrail <一句话目标>          # 新任务（human）
taskrail goal: <一句话目标>    # 新任务（goal）
taskrail resume [slug]         # 恢复
taskrail list                  # 列任务
```

## FAQ

- **会问很多吗？** 不会。有取舍就按推荐定下并说一句理由，只有上表「一定停下」的情况才停。规则：`taskrail/references/user-report.md`。
- **它会没看资料就猜吗？** 不会。先读一手资料，能查到的不问；你纠正后先重查再改。见 `task-intent/references/intent.md`。
- **自己定的事我怎么知道？** 难回头的单独一行「我定了 X，因为 Y」，全部记在 `TASK.md`「已做决定」。
- **怎么算做完？** `taskrail/references/done.md` 逐条核对。
- **要好看的界面怎么验收？** 加一条观感验收：goal 下另一个模型对照参照审截图自己迭代，human 下评审过了再给你看截图。见 `done.md`「观感验收」。
