#!/usr/bin/env python3
"""taskflow 入口门：建 driver / 派实现前机械核对 handoff 是否成立。

用法：
  check_handoff.py <workspace-root> <slug> [--json]

核对项（全部满足才 exit 0）：
  1. tasks/ongoing/<slug>/TASK.md 存在（子任务用 <parent>/subtasks/<sub> 作 slug）；
  2. 元信息 status = handed-off，phase ∈ propose / apply / archive / done；
  3. 已批准：approve/APPROVED.md 存在；元信息 criterion 非空；driver = <slug 末段>-driver；
  4. TASK.md「## 交接」节存在，且载荷含「交付类别」与「适用门包」两行（非空）；
  5. 交付类别含 Web UI 时，交接节另含 Active Instance 根路径与 contract / binding / projection 三条 digest。

逃生口：元信息 `gate_bypass:` 值含 `user-confirmed` 且写明理由时，以 BYPASS 放行（exit 0，
输出醒目警告）；只在用户原话明确要求跳过时写入，理由照录用户原话。

退出码：0 通过（或已登记 BYPASS）· 1 不通过 · 2 用法错误。
仅标准库，只读。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_PHASES = ("propose", "apply", "archive", "done")
REDIRECT = "拒绝建 driver / 派实现：先回 taskrail 走完 approve → handoff（taskrail references/handoff.md）。"


def parse_meta(text: str) -> dict[str, str]:
    """读 TASK.md 元信息：优先 `---` frontmatter，其次首个 ```yaml 块，再退到全文顶层 key: value（兼容 `- key: value` 列表行）。"""
    block = None
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if m:
        block = m.group(1)
    else:
        m = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.S)
        block = m.group(1) if m else text
    meta: dict[str, str] = {}
    for line in block.splitlines():
        mm = re.match(r"^[-*]?\s*([a-z_]+)\s*:\s*(.*?)\s*$", line)
        if mm and mm.group(1) not in meta:
            meta[mm.group(1)] = mm.group(2).strip().strip("\"'")
    return meta


def section(text: str, title: str) -> str | None:
    m = re.search(rf"^##\s+{re.escape(title)}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def field(body: str, name: str) -> str | None:
    m = re.search(rf"^\s*[-*]?\s*{re.escape(name)}\s*[:：]\s*(.*?)\s*$", body, re.M)
    if not m:
        return None
    return m.group(1).strip() or None


def check(root: Path, slug: str) -> dict:
    task_md = root / "tasks" / "ongoing" / slug / "TASK.md"
    res: dict = {"task_md": str(task_md), "slug": slug, "errors": [], "warnings": [], "bypass": None}
    if not task_md.is_file():
        res["errors"].append(f"TASK.md 不存在：{task_md}")
        return res
    text = task_md.read_text(encoding="utf-8")
    meta = parse_meta(text)
    res["status"], res["phase"] = meta.get("status"), meta.get("phase")

    bypass = meta.get("gate_bypass", "")
    if bypass and bypass.lower() not in ("null", "none", "~"):
        if "user-confirmed" in bypass and len(bypass.replace("user-confirmed", "").strip(" :：-")) >= 4:
            res["bypass"] = bypass
            res["warnings"].append("BYPASS：入口门由用户确认豁免（TASK.md gate_bypass），门包未经机械核对，没验证到的项按 done.md 第 6 条记进「已做决定」。")
            return res
        res["errors"].append("gate_bypass 须含 `user-confirmed` 与用户原话。")

    if meta.get("status") != "handed-off":
        res["errors"].append(f"status 须为 handed-off，实为 {meta.get('status')!r}")
    if meta.get("phase") not in ALLOWED_PHASES:
        res["errors"].append(f"phase 须为 {'/'.join(ALLOWED_PHASES)}（approve 之后），实为 {meta.get('phase')!r}")
    if not (task_md.parent / "approve" / "APPROVED.md").is_file():
        res["errors"].append("缺 approve/APPROVED.md（方案未经 approve 冻结）")
    if not meta.get("criterion"):
        res["errors"].append("元信息缺 criterion（完成判据原文）")
    want_driver = f"{slug.rstrip('/').rsplit('/', 1)[-1]}-driver"
    if meta.get("driver") != want_driver:
        res["errors"].append(f"driver 须为 {want_driver!r}，实为 {meta.get('driver')!r}")

    body = section(text, "交接")
    if body is None:
        res["errors"].append("缺「## 交接」节（handoff 载荷）")
        return res
    cls = field(body, "交付类别")
    packs = field(body, "适用门包")
    res["delivery_class"], res["gate_packs"] = cls, packs
    if not cls:
        res["errors"].append("交接载荷缺「交付类别」（无交付产出写「不适用」）")
    if not packs:
        res["errors"].append("交接载荷缺「适用门包」（不适用写「无」）")
    if cls and re.search(r"web\s*-?\s*ui", cls, re.I):
        for name in ("Active Instance 根路径", "contract digest", "binding digest", "projection digest"):
            if not field(body, name):
                res["errors"].append(f"Web UI 交接载荷缺「{name}」")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="taskflow 入口门：核对方案已批准、handoff 已成立且载荷带交付类别与门包")
    ap.add_argument("workspace_root", help="含 tasks/ 的工作区根")
    ap.add_argument("slug", help="任务 slug（子任务写 parent/sub）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args(argv)
    root = Path(a.workspace_root)
    if not root.is_dir():
        print(f"USAGE: workspace_root 不是目录：{root}", file=sys.stderr)
        return 2
    res = check(root, a.slug)
    ok = not res["errors"]
    res["ok"] = ok
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for w in res["warnings"]:
            print(f"WARN  {w}")
        for e in res["errors"]:
            print(f"FAIL  {e}")
        print("PASS  handoff 成立" if ok else f"BLOCK {REDIRECT}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
