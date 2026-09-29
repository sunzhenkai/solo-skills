#!/usr/bin/env python3
"""goal_transition.py — 状态迁移查表 + 状态文件读写 + 生产者戳解析。

数据来源：references/state-machine.md 的迁移网格（唯一真源）。
状态文件：只存计数器（state / exit_point / autocontinue_count /
last_input_event / blocked / handoff_summary），不存迁移规则。

用法：
    # 一次性查表（不写文件）
    python3 goal_transition.py --state 已停 --event "goal 自动续跑" --autocontinue-count 3

    # 基于状态文件查表并回写
    python3 goal_transition.py --state-file /path/to/state.yaml --event "goal 自动续跑" --write

    # 吃生产者戳（goal-event: auto-continue）
    python3 goal_transition.py --state-file /path/to/state.yaml --event-tag auto-continue --write

输出 JSON：
    {state, event, defined, next_state, action, reply_shape, note,
     state_file, wrote_back, count}
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

# goal-event 戳 → 事件名。生产者在每轮 prompt 开头盖戳时，tag 取左列。
EVENT_TAGS = {
    "auto-continue": "goal 自动续跑",
    "user-authorize": "用户授权",
    "user-continue": "用户继续",
    "user-redirect": "用户改向",
    "user-info": "用户补充信息",
    "review-converged": "审阅收敛",
    "review-diverged": "审阅未收敛",
    "exit-point-hit": "退出点命中",
    "criterion-met": "判据成立",
    "step-progress": "步骤推进",
    "external-fact": "外部新事实到达",
}

EMPTY_MARKERS = {"", "—", "-"}

STATE_FILE_FIELDS = ("state", "exit_point", "autocontinue_count", "last_input_event", "blocked", "handoff_summary")


def _split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _parse_grid(text: str) -> dict[str, dict[str, str]]:
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


# ---------- state-file ----------

def read_state_file(path: Path) -> dict:
    """Read a minimal YAML state file. Fields are a closed set; values are scalars."""
    if not path.is_file():
        return {}
    out: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key not in STATE_FILE_FIELDS:
            continue
        if val in ("", "null", "~"):
            out[key] = None
        elif val.lower() in ("true", "yes"):
            out[key] = True
        elif val.lower() in ("false", "no"):
            out[key] = False
        elif re.fullmatch(r"-?\d+", val):
            out[key] = int(val)
        else:
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            out[key] = val
    return out


def write_state_file(path: Path, data: dict) -> None:
    """Write the state file. Only known fields; stable order; one scalar per line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for key in STATE_FILE_FIELDS:
        if key not in data:
            continue
        val = data[key]
        if val is None:
            rendered = "null"
        elif isinstance(val, bool):
            rendered = "true" if val else "false"
        elif isinstance(val, int):
            rendered = str(val)
        else:
            s = str(val)
            if any(c in s for c in (":", "#", "\n")) or s != s.strip():
                s = '"' + s.replace('"', '\\"') + '"'
            rendered = s
        lines.append(f"{key}: {rendered}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- core decide ----------

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

    action = cell
    if ev == "goal 自动续跑" and state == "已停":
        if autocontinue_count is None:
            return {
                "state": state, "event": ev, "defined": False,
                "next_state": None, "action": "",
                "reply_shape": "",
                "note": "已停 × goal 自动续跑 需要 --autocontinue-count N 或 state-file 里有 autocontinue_count",
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


# ---------- main ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="goal 状态迁移查表 + 状态文件读写")
    parser.add_argument("--state", help="当前状态（与 --state-file 互斥，且优先级低）")
    parser.add_argument("--state-file", help="状态文件路径；存在则读 state/count")
    parser.add_argument("--event", help="事件名（与 --event-tag 互斥，且优先级低）")
    parser.add_argument("--event-tag", help="生产者戳（goal-event: <tag>）")
    parser.add_argument("--autocontinue-count", type=int, default=None,
                        help="连续第几次自动续跑；state-file 有值时被覆盖")
    parser.add_argument("--write", action="store_true", help="迁移判定后回写 state-file")
    args = parser.parse_args()

    file_data: dict = {}
    state_file: Path | None = None
    if args.state_file:
        state_file = Path(args.state_file)
        file_data = read_state_file(state_file)

    state = file_data.get("state") or args.state
    if not state:
        parser.error("--state-file 无 state 字段时必须给 --state")

    event = args.event
    if args.event_tag:
        if args.event_tag not in EVENT_TAGS:
            parser.error(f"未知 event-tag {args.event_tag!r}；合法值：{list(EVENT_TAGS)}")
        event = EVENT_TAGS[args.event_tag]
    if not event:
        parser.error("必须给 --event 或 --event-tag")

    count = file_data.get("autocontinue_count")
    if count is None:
        count = args.autocontinue_count

    # 计数语义：decide() 期望「这次是连续第 N 次自动续跑」。
    # - state-file 里存的是「已连续发生 N 次」，本轮再来一次就是第 N+1 次。
    # - --autocontinue-count 一次性调用时，调用方传的就是「这次是第 N 次」。
    effective_count = count
    if event == "goal 自动续跑" and file_data.get("autocontinue_count") is not None:
        effective_count = file_data["autocontinue_count"] + 1

    out = decide(state, event, effective_count)
    out["state_file"] = str(state_file) if state_file else None
    out["count"] = count

    wrote = False
    if args.write and state_file is not None:
        new_data = dict(file_data)
        if out["defined"]:
            new_data["state"] = out["next_state"]
            new_data["last_input_event"] = out["event"]
            if out["event"] == "goal 自动续跑":
                new_data["autocontinue_count"] = effective_count
            else:
                new_data["autocontinue_count"] = 0
            if "blocked" in out["action"]:
                new_data["blocked"] = True
                new_data.setdefault("handoff_summary", None)
            else:
                new_data["blocked"] = False
        else:
            new_data["last_input_event"] = out["event"]
        write_state_file(state_file, new_data)
        wrote = True
    out["wrote_back"] = wrote

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if out["defined"] else 1


if __name__ == "__main__":
    sys.exit(main())
