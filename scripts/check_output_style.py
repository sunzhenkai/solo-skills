#!/usr/bin/env python3
"""面向人的输出风格门禁（只依赖标准库）。

规则：
1. task 族 SKILL.md（ENFORCED）≤ 8192 字节；其余 skill 超限只告警。
2. 意图复述模板（task-intent statement-template 的首个 markdown 代码块）≤ 8 行，且不含内部术语。
3. 任何以「Digest（≤10 行）」为标题的小节，其后首个代码块 ≤ 10 行。
命中 ERROR 打印 file:说明 并以 1 退出；WARN 只打印。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 8192
ENFORCED = {"taskrail", "task-explore", "taskflow", "task-intent", "role-based-reviewer"}
JARGON = re.compile(r"\b(phase|gate|Digest|worker|criterion|tier)\b", re.I)
FENCE = re.compile(r"```[a-z]*\n(.*?)```", re.S)


def nonblank(block: str) -> int:
    return len([l for l in block.splitlines() if l.strip()])


def check_sizes(skills: Path) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    for f in sorted(skills.glob("*/SKILL.md")):
        n = len(f.read_bytes())
        if n > LIMIT:
            msg = f"{f.relative_to(skills.parent)}: SKILL.md {n} B > {LIMIT} B"
            (errs if f.parent.name in ENFORCED else warns).append(msg)
    return errs, warns


def check_intent_template(path: Path) -> list[str]:
    if not path.exists():
        return []
    m = FENCE.search(path.read_text(encoding="utf-8"))
    if not m:
        return [f"{path}: 未找到复述模板代码块"]
    errs = []
    if nonblank(m.group(1)) > 8:
        errs.append(f"{path}: 复述模板超过 8 行")
    hit = JARGON.search(m.group(1))
    if hit:
        errs.append(f"{path}: 复述模板含内部术语「{hit.group(0)}」")
    return errs


def check_digest_blocks(skills: Path) -> list[str]:
    errs = []
    for f in sorted(skills.rglob("*.md")):
        if "patches" in f.parts or "evolutions" in f.parts:
            continue
        text = f.read_text(encoding="utf-8")
        for h in re.finditer(r"^#+ Digest（≤10 行）.*$", text, re.M):
            m = FENCE.search(text, h.end())
            if m and nonblank(m.group(1)) > 10:
                errs.append(f"{f.relative_to(skills.parent)}: Digest 模板超过 10 行")
    return errs


def run(skills: Path) -> tuple[list[str], list[str]]:
    errs, warns = check_sizes(skills)
    errs += check_intent_template(skills / "task-intent" / "references" / "statement-template.md")
    errs += check_digest_blocks(skills)
    return errs, warns


def main() -> int:
    errs, warns = run(ROOT / "skills")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("ERROR", e)
    if errs:
        return 1
    print(f"OK: 输出风格门禁通过（{len(warns)} 条告警）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
