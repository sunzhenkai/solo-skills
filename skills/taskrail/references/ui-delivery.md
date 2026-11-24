# Web UI 交付包（可选）

只在交付类别是 Web UI 时读。编排正文只写「命中 Web UI → 读本文件」，细则只在这里。

## 强度跟「是否观感交付」走

| 情况 | 做法 |
|------|------|
| 普通 UI 改动（功能为主，用户没提观感） | 沿用交付仓已有组件库 / 样式体系（adopt-only）；先按实现防错护栏避坑，改完默认跑 **L1 快检**（`ui_evidence_check.py --quick --base-url <url> --routes <路径>`）兜住运行时报错、裂图、横向溢出、外扩环裁切与焦点可见/遮挡，并自检破坏性操作确认；环境缺 playwright 时降级记录未验证项 |
| 观感交付（用户原话要好看 / 设计感 / 体验） | 先过 [done.md](done.md)「观感验收」；页面面多或要统一视觉时，再用下面的 Active Instance 与 **L2 完整证据门** |

## Active Instance（通用路线统一视觉时用）

- 交付项目根 `design-system/v1`，`design-system.yaml` 为 `status: frozen`，带 contract / binding / projection 三条 digest。由 design 阶段在交付仓内建立并 freeze：`tokens.css`、`DESIGN.md`、`preview.html` 按 `pretty-ui/references/system.md` 产出，有参照源先从参照提炼 tokens / primitive。
- `tasks/` 只存指针与 digest（写在 `design/contract.md`），不复制 tokens / primitive 精确值。
- apply 只消费不改 core；要改共享 token / pattern 就回 design 修订并重新 freeze，刷新 digest。

## 实现方法

先按 `ui-kit/SKILL.md` 选择唯一主路线：既有/非 React 项目走 pretty-ui；已有 ui-template lock 或明确选择 React 模板的项目走 ui-kit 模板流程（未安装 `ui-kit` / `pretty-ui` 时沿用交付仓既有体系，仍执行下方机械门）。

通用路线先做一条主流程代表页，按 `pretty-ui/SKILL.md` 的 build 主流程 two-pass：先定方向卡与壳层，出初稿后看截图、按问题表再修一轮；其余页面从它的壳层与字阶长出。其余切片照搬它，不并行另起风格。模板路线按 ui-kit 的 init / update / verify 执行，以模板 lock 与像素保真作为体系证据；两条路线都保留下面的运行态与独立 design 评审门。

## 机械门

- **L1 快检**（普通改动默认）：[`../scripts/ui_evidence_check.py`](../scripts/ui_evidence_check.py) `--quick --base-url <url> --routes /a,/b`，免写 manifest，自动拦截 `pageerror` / `console.error` / 资源 4xx-5xx、裂图、横向溢出、外扩环被裁、热区 `<24px`、焦点不可见或被 sticky/fixed 遮挡（找到 `axe-core` 时顺跑 WCAG AA，缺失则标 `skipped`）。
- **L2 完整证据门**（观感交付 / 主流程改动）：同一脚本传 manifest，对关键路由出 `report.json` + DPR=2 截图（L1 全部 + 强制 axe WCAG 2.2 AA + ≥2 视口 + 数据四态 + 可选交互浮层 `overlays` 的内边距/溢出/焦点进出检查），exit 0 才算。代码变了旧 report 作废。
- **L3 design 评审文件**：L1/L2 通过后再进评审；评审者 ≠ 实现者，frontmatter 含 `roles: design`、`reviewer`、`implementer`、`report:`；`ui_evidence_check.py --validate-review <file>` exit 0。
- Gallery（组件 / 页面展示页）只证明设计系统没漂，不替代上面三项。
- 工具缺失（playwright / L2 缺 axe-core）：脚本 exit 2；写进「已做决定」说明哪项没验证。

## 交接行

交付类别是 Web UI 时，`TASK.md`「## 交接」节另写四行，由 `check_handoff.py` 核对；没有 Active Instance 时按路线写「无（adopt-only）」或「无（ui-template）」：

```text
- Active Instance 根路径：<路径 | 无（adopt-only / ui-template）>
- contract digest：<值 | 无>
- binding digest：<值 | 无>
- projection digest：<值 | 无>
```
