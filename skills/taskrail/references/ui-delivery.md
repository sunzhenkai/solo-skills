# Web UI 交付包（可选）

只在交付类别是 Web UI 时读。编排正文只写「命中 Web UI → 读本文件」，细则只在这里。

## 强度跟「是否观感交付」走

| 情况 | 做法 |
|------|------|
| 普通 UI 改动（功能为主，用户没提观感） | 沿用交付仓已有组件库 / 样式体系（adopt-only）；实现者自检 quality floor：破坏性操作有确认、键盘可达、focus 可见；结果写进验证记录。`ui_evidence_check` 可选 |
| 观感交付（用户原话要好看 / 设计感 / 体验） | 先过 [done.md](done.md)「观感验收」；页面面多或要统一视觉时，再用下面的 Active Instance 与证据门 |

## Active Instance（统一视觉时用）

- 交付项目根 `design-system/v1`，`design-system.yaml` 为 `status: frozen`，带 contract / binding / projection 三条 digest。由 design 阶段在交付仓内建立并 freeze：`tokens.css`、`DESIGN.md`、`preview.html` 按 [pretty-ui 的 system.md](../../pretty-ui/references/system.md) 产出，有参照源先从参照提炼 tokens / primitive。
- `tasks/` 只存指针与 digest（写在 `design/contract.md`），不复制 tokens / primitive 精确值。
- apply 只消费不改 core；要改共享 token / pattern 就回 design 修订并重新 freeze，刷新 digest。

## 实现方法

先做一条主流程代表页，按 [pretty-ui](../../pretty-ui/SKILL.md) 的 build 主流程 two-pass：先定方向卡与壳层，出初稿后看截图、按问题表再修一轮；其余页面从它的壳层与字阶长出。其余切片照搬它，不并行另起风格。

## 机械门

- 运行态证据：[`../scripts/ui_evidence_check.py`](../scripts/ui_evidence_check.py) 对关键路由出 `report.json` + 截图（≥2 视口、axe WCAG 2.2 AA、焦点走查、manifest 声明的四态），exit 0 才算。代码变了旧 report 作废。
- design 评审文件：评审者 ≠ 实现者，frontmatter 含 `roles: design`、`reviewer`、`implementer`、`report:`；`ui_evidence_check.py --validate-review <file>` exit 0。
- Gallery（组件 / 页面展示页）只证明设计系统没漂，不替代上面两项。
- 工具缺失（playwright / axe-core）：脚本 exit 2；写进「已做决定」说明哪项没验证。

## 交接行

交付类别是 Web UI 时，`TASK.md`「## 交接」节另写四行，由 `check_handoff.py` 核对；没用 Active Instance 就写「无（adopt-only）」：

```text
- Active Instance 根路径：<路径 | 无（adopt-only）>
- contract digest：<值 | 无>
- binding digest：<值 | 无>
- projection digest：<值 | 无>
```
