#!/usr/bin/env python3
"""roster 数据位置的公共解析：读 ~/.config/agent-roster/config.yaml 的 data_root。

只解析单行 `data_root: <path>`（不支持任意 YAML），缺文件或缺键时给出可操作的报错。
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

CONFIG = Path.home() / ".config" / "agent-roster" / "config.yaml"


def data_root() -> Path:
    if not CONFIG.exists():
        print(f"error: 找不到 {CONFIG}——先建立并写明 data_root", file=sys.stderr)
        raise SystemExit(2)
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*data_root\s*:\s*(\S+)", line)
        if m and not line.strip().startswith("#"):
            return Path(os.path.expanduser(m.group(1)))
    print(f"error: {CONFIG} 里没有 data_root 键", file=sys.stderr)
    raise SystemExit(2)


def agents_dir() -> Path:
    return data_root() / "agents"


def traces_dir() -> Path:
    return agents_dir() / "traces"
