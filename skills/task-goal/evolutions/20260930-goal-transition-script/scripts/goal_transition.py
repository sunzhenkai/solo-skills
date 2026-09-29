#!/usr/bin/env python3
"""goal_transition.py — 状态迁移查表。

输入状态 + 事件，输出下一状态 / 允许动作 / 回复形状。
数据从 references/state-machine.md 的网格行解析，不另存副本。

用法：
    python3 goal_transition.py --state 已停 --event "goal 自动续跑" --autocontinue-count 3
    python3 goal_transition.py --state 执行中 --event "审阅收敛"

输出 JSON：
    {
      "state": "...", "event": "...",
      "defined": true|false,
      "next_state": "..." | null,
      "action": "...",            # 单元格原文
      "reply_shape": "...",       # 从 action 提取的回复形状提示
      "note": "..."
    }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
STATE_MACHINE_MD = SKILL_ROOT / "references" / "state-machine.md"

STATES = ("执行中", "已停", "已交接", "已完成")

EVENTS = (
    "用户授权",
    "用户继续",
    "用户改向",
    "goal 自动续跑",
    "审阅收敛",
    "审阅未收敛",
    "退出点命中",
    "判据成立",
    "步骤推进",
    "外部新事实到达",
    "用户补充信息",
)

EMPTY_MARKERS = {"", "—", "-"}


def _split_cells(line: str) -> list[str]:
    """Split a markdown table row into stripped cells (drop leading/trailing pipes)."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _parse_grid(text: str) -> dict[str, dict[str, str]]:
    """Parse the transition grid into {state: {event: cell}}."""
    grid: dict[str, dict[str, str]] = {}
    header_events: list[str] = []
    in_grid = False
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = _split_cells(line)
        if not cells:
            continue
        first = cells[0]
        if first.startswith("状态"):
            header_events = [c.lstrip("＼").strip() for c in cells[1:]]
            in_grid = True
            continue
        if set(first) <= {"-", ":"}:
            continue
        if not in_grid:
            continue
        state = first.strip("*").strip()
        if state not in STATES:
            continue
        row: dict[str, str] = {}
        for ev, cell in zip(header_events, cells[1:]):
            row[ev] = cell
        grid[state] = row
    return grid


def _find_event(query: str, events: list[str]) -> str | None:
    """Exact match, then prefix, then unique substring (so「自动续跑」matches「goal 自动续跑」)."""
    if query in events:
        return query
    prefix = [e for e in events if e.startswith(query) or query.startswith(e)]
    if len(prefix) == 1:
        return prefix[0]
    sub = [e for e in events if query in e]
    if len(sub) == 1:
        return sub[0]
    return None


def _extract_reply_shape(action: str) -> str:
    """Pull the reply-shape hint out of a cell, best-effort."""
    if "blocked" in action:
        return "交接摘要（已完成、未完成、证据、下一步）"
    if "重申" in action:
        return "重申仍停，不写成选项列表"
    if "只读" in action:
        return "只读环境查证 / 外部原文取证 / 证据固化"
    if "路由写授权" in action or "路由写成需要的授权" in action:
        return "写明退出点与需要的授权"
    if "选项列表" in action:
        return "不写成选项列表"
    return ""


def decide(state: str, event: str, autocontinue_count: int | None) -> dict:
    if state not in STATES:
        return {
            "state": state, "event": event, "defined": False,
            "next_state": None, "action": "",
            "reply_shape": "",
            "note": f"未知状态 {state!r}；合法值：{list(STATES)}",
        }

    text = STATE_MACHINE_MD.read_text(encoding="utf-8")
    grid = _parse_grid(text)
    if state not in grid:
        return {
            "state": state, "event": event, "defined": False,
            "next_state": None, "action": "",
            "reply_shape": "",
            "note": f"网格缺 {state} 行 → 走无进展轮",
        }

    events = list(grid[state].keys())
    ev = _find_event(event, events)
    if ev is None:
        return {
            "state": state, "event": event, "defined": False,
            "next_state": None, "action": "",
            "reply_shape": "",
            "note": f"事件 {event!r} 不在封闭枚举内 → 走无进展轮；合法事件：{events}",
        }

    cell = grid[state].get(ev, "")
    if cell.strip() in EMPTY_MARKERS:
        return {
            "state": state, "event": ev, "defined": False,
            "next_state": None, "action": "",
            "reply_shape": "",
            "note": "未定义组合 → 走无进展轮",
        }

    # Specialise the autocontinue cell by count.
    action = cell
    if ev == "goal 自动续跑" and state == "已停":
        if autocontinue_count is None:
            return {
                "state": state, "event": ev, "defined": False,
                "next_state": None, "action": "",
                "reply_shape": "",
                "note": "已停 × goal 自动续跑 需要 --autocontinue-count N",
            }
        if autocontinue_count >= 3:
            action = "已停（blocked 交接：已完成、未完成、证据、下一步）"
        else:
            action = f"已停（第 {autocontinue_count} 次：只读查证/取证/固化）"

    m = re.match(r"^(执行中|已停|已交接|已完成)", action)
    next_state = m.group(1) if m else state

    return {
        "state": state,
        "event": ev,
        "defined": True,
        "next_state": next_state,
        "action": action,
        "reply_shape": _extract_reply_shape(action),
        "note": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="goal 状态迁移查表")
    parser.add_argument("--state", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--autocontinue-count", type=int, default=None)
    args = parser.parse_args()

    out = decide(args.state, args.event, args.autocontinue_count)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if out["defined"] else 1


if __name__ == "__main__":
    sys.exit(main())
