#!/usr/bin/env python3
"""Web UI 运行态证据门（references/ui-delivery.md「机械门」）。

给定 base URL（或启动命令）与 routes/states manifest，用真实浏览器产出可复跑证据：
  - ≥2 视口截图（默认 desktop 1280x800、mobile 375x812，两者必须在场）；
  - 注入 axe-core 跑 WCAG 2.2 AA（wcag2a/2aa/21a/21aa/22aa）；
  - 键盘 Tab 走查：记录焦点顺序与每一步焦点是否可见；
  - 逐个声明的数据态（loading / empty / error / success）截图，经 manifest 的 URL / query 或 actions 进入。
产物：<out>/<run-id>/report.json + PNG。

另：--validate-report 只核对已有 report.json；--validate-review 核对 design 评审文件
（frontmatter: roles 含 design、reviewer ≠ implementer、report 指向通过的 report.json）。

退出码：0 通过 · 1 门不通过（axe serious/critical、缺态、缺视口、焦点不可见、页面打不开）
        · 2 用法 / manifest 不合法 / 依赖缺失（playwright 或 axe-core；缺依赖是阻断，不是跳过）。

依赖：pip install playwright && playwright install chromium；axe-core 由 --axe-path、
环境变量 UI_EVIDENCE_AXE_JS，或 ./node_modules/axe-core/axe.min.js（`npm i -D axe-core`）提供。
manifest 可为 JSON；装了 PyYAML 时也接受 YAML。

manifest 示例（JSON）：
{
  "base_url": "http://127.0.0.1:5173",
  "routes": [
    {"name": "list", "path": "/items",
     "states": {
       "success": {"path": "/items"},
       "empty":   {"path": "/items?fixture=empty"},
       "error":   {"path": "/items?fixture=error"},
       "loading": {"path": "/items?fixture=slow", "wait": "domcontentloaded"}
     },
     "not_applicable": {},
     "tab_steps": 25}
  ]
}
state 的进入方式：`path`（相对 base_url）与/或 `actions` 列表，动作为
{"click": sel} / {"fill": sel, "value": v} / {"press": key} / {"wait_for": sel} / {"wait_ms": n}。
某态确实不适用时写进 route.not_applicable：{"<state>": "<理由>"}，理由会进报告供评审核对。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCHEMA = "ui-evidence/v1"
REQUIRED_STATES = ("loading", "empty", "error", "success")
DEFAULT_VIEWPORTS = [
    {"name": "desktop", "width": 1280, "height": 800},
    {"name": "mobile", "width": 375, "height": 812},
]
REQUIRED_SIZES = {(1280, 800), (375, 812)}
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
BLOCKING_IMPACTS = {"serious", "critical"}
ACTION_KEYS = {"click", "fill", "press", "wait_for", "wait_ms"}


# ---------------------------------------------------------------- manifest

def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError as e:  # pragma: no cover
            raise ValueError("YAML manifest 需要 PyYAML；或改用 JSON") from e
        return yaml.safe_load(text) or {}
    return json.loads(text)


def validate_manifest(m: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(m, dict):
        return ["manifest 顶层须为对象"]
    vps = m.get("viewports", DEFAULT_VIEWPORTS)
    if not isinstance(vps, list) or len(vps) < 2:
        errs.append("viewports 至少 2 个")
    else:
        sizes = set()
        for i, v in enumerate(vps):
            if not (isinstance(v, dict) and isinstance(v.get("width"), int) and isinstance(v.get("height"), int) and v.get("name")):
                errs.append(f"viewports[{i}] 须含 name/width/height(int)")
            else:
                sizes.add((v["width"], v["height"]))
        for s in REQUIRED_SIZES - sizes:
            errs.append(f"缺必备视口 {s[0]}x{s[1]}")
    routes = m.get("routes")
    if not isinstance(routes, list) or not routes:
        errs.append("routes 须为非空列表")
        return errs
    names = set()
    for i, r in enumerate(routes):
        tag = f"routes[{i}]"
        if not isinstance(r, dict):
            errs.append(f"{tag} 须为对象")
            continue
        name = r.get("name")
        if not name or not re.fullmatch(r"[A-Za-z0-9_.-]+", str(name)):
            errs.append(f"{tag}.name 须为 [A-Za-z0-9_.-]+")
        elif name in names:
            errs.append(f"{tag}.name 重复：{name}")
        names.add(name)
        if not isinstance(r.get("path"), str):
            errs.append(f"{tag}.path 须为字符串")
        states = r.get("states") or {}
        na = r.get("not_applicable") or {}
        if not isinstance(states, dict) or not isinstance(na, dict):
            errs.append(f"{tag}.states / not_applicable 须为对象")
            continue
        for s in REQUIRED_STATES:
            if s in states and s in na:
                errs.append(f"{tag}: 态 {s} 同时声明与豁免")
            elif s not in states and s not in na:
                errs.append(f"{tag}: 缺态 {s}（声明进入方式，或在 not_applicable 写理由）")
            elif s in na and (not isinstance(na[s], str) or len(na[s].strip()) < 4):
                errs.append(f"{tag}: not_applicable.{s} 须写理由")
        for s, spec in states.items():
            if not isinstance(spec, dict) or not (isinstance(spec.get("path"), str) or spec.get("actions")):
                errs.append(f"{tag}.states.{s} 须含 path 或 actions")
                continue
            for j, act in enumerate(spec.get("actions") or []):
                if not isinstance(act, dict) or not (set(act) - {"value"}) <= ACTION_KEYS or not (set(act) & ACTION_KEYS):
                    errs.append(f"{tag}.states.{s}.actions[{j}] 非法：{act!r}")
        ts = r.get("tab_steps", 20)
        if not isinstance(ts, int) or ts < 1:
            errs.append(f"{tag}.tab_steps 须为正整数")
    return errs


# ---------------------------------------------------------------- report

def summarize(report: dict) -> dict:
    failures: list[str] = []
    vp_names = [v["name"] for v in report["viewports"]]
    sizes = {(v["width"], v["height"]) for v in report["viewports"]}
    missing_vp = [f"{w}x{h}" for (w, h) in sorted(REQUIRED_SIZES - sizes)]
    for s in missing_vp:
        failures.append(f"缺视口 {s}")
    axe_blocking = missing_states = invisible = 0
    for r in report["routes"]:
        for s in REQUIRED_STATES:
            if s in r.get("not_applicable", {}):
                continue
            st = r["states"].get(s)
            for vp in vp_names:
                cell = (st or {}).get(vp)
                if not cell or not cell.get("screenshot") or cell.get("error"):
                    missing_states += 1
                    failures.append(f"{r['name']}/{s}/{vp}: 缺证据" + (f"（{cell['error']}）" if cell and cell.get("error") else ""))
                    continue
                for v in cell.get("axe", {}).get("violations", []):
                    if v.get("impact") in BLOCKING_IMPACTS:
                        axe_blocking += 1
                        failures.append(f"{r['name']}/{s}/{vp}: axe {v['impact']} {v['id']}（{v.get('nodes', 0)} 处）")
        for vp, walk in (r.get("focus_walk") or {}).items():
            for step in walk.get("invisible", []):
                invisible += 1
                failures.append(f"{r['name']}/{vp}: 焦点不可见 @ {step}")
    return {
        "axe_blocking": axe_blocking,
        "missing_states": missing_states,
        "missing_viewports": missing_vp,
        "focus_invisible": invisible,
        "failures": failures,
        "ok": not failures,
    }


def validate_report(rep: object) -> list[str]:
    """校验 report.json 结构（供评审 / 完成门机械核对）。"""
    errs: list[str] = []
    if not isinstance(rep, dict):
        return ["report 须为对象"]
    if rep.get("schema") != SCHEMA:
        errs.append(f"schema 须为 {SCHEMA}")
    for k in ("run_id", "base_url", "started_at", "viewports", "routes", "summary"):
        if k not in rep:
            errs.append(f"缺字段 {k}")
    if errs:
        return errs
    vp_names = []
    for v in rep["viewports"]:
        if not all(k in v for k in ("name", "width", "height")):
            errs.append("viewport 缺 name/width/height")
        vp_names.append(v.get("name"))
    for r in rep["routes"]:
        for k in ("name", "states", "focus_walk", "not_applicable"):
            if k not in r:
                errs.append(f"route 缺 {k}")
        for s, cells in (r.get("states") or {}).items():
            for vp, cell in cells.items():
                if vp not in vp_names:
                    errs.append(f"{r.get('name')}/{s}: 未声明视口 {vp}")
                if not cell.get("error") and ("screenshot" not in cell or "axe" not in cell):
                    errs.append(f"{r.get('name')}/{s}/{vp}: 缺 screenshot 或 axe")
        for vp, walk in (r.get("focus_walk") or {}).items():
            if not isinstance(walk.get("order"), list) or not isinstance(walk.get("invisible"), list):
                errs.append(f"{r.get('name')}/{vp}: focus_walk 须含 order/invisible 列表")
    s = rep["summary"]
    for k in ("axe_blocking", "missing_states", "missing_viewports", "focus_invisible", "failures", "ok"):
        if k not in s:
            errs.append(f"summary 缺 {k}")
    return errs


def validate_review(path: Path) -> list[str]:
    """design 评审文件核对：frontmatter 含 roles（含 design/uiux）、reviewer、implementer（二者不同）、
    report（指向通过的 report.json；相对评审文件所在目录或 cwd）。"""
    if not path.is_file():
        return [f"评审文件不存在：{path}"]
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ["评审文件缺 frontmatter（roles / reviewer / implementer / report）"]
    meta = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-z_]+)\s*:\s*(.*?)\s*$", line)
        if mm:
            meta[mm.group(1)] = mm.group(2).strip().strip("\"'[]")
    errs = []
    roles = {x.strip() for x in re.split(r"[,\s]+", meta.get("roles", "")) if x.strip()}
    if not roles & {"design", "uiux"}:
        errs.append("roles 须含 design（或别名 uiux）")
    rv, im = meta.get("reviewer", ""), meta.get("implementer", "")
    if not rv or not im:
        errs.append("须写 reviewer 与 implementer")
    elif rv.lower() == im.lower():
        errs.append("reviewer 不得等于 implementer（自评不算评审）")
    rp = meta.get("report")
    if not rp:
        errs.append("须写 report：指向 ui_evidence_check 的 report.json")
    else:
        cand = [path.parent / rp, Path(rp)]
        hit = next((c for c in cand if c.is_file()), None)
        if not hit:
            errs.append(f"report 不存在：{rp}")
        else:
            rep = json.loads(hit.read_text(encoding="utf-8"))
            errs += [f"report: {e}" for e in validate_report(rep)]
            if not errs and not rep["summary"]["ok"]:
                errs.append("report 结论不通过")
    if len(text[m.end():].strip()) < 40:
        errs.append("评审正文过短：须逐条写 findings 与 disposition")
    return errs


# ---------------------------------------------------------------- browser

FOCUS_JS = """() => {
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  const cs = getComputedStyle(el);
  const visible = el.matches(':focus-visible') && (
    (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) ||
    (cs.boxShadow && cs.boxShadow !== 'none') ||
    (cs.borderStyle !== 'none' && el.dataset.focusRing === 'border'));
  const label = (el.getAttribute('aria-label') || el.innerText || el.value || '').trim().slice(0, 40);
  const id = el.id ? '#' + el.id : '';
  return {desc: el.tagName.toLowerCase() + id + (label ? ' "' + label + '"' : ''), visible: !!visible};
}"""


def find_axe(cli: str | None) -> Path | None:
    for c in (cli, os.environ.get("UI_EVIDENCE_AXE_JS"), "node_modules/axe-core/axe.min.js"):
        if c and Path(c).is_file():
            return Path(c)
    return None


def wait_url(url: str, timeout: float) -> bool:
    end = time.time() + timeout
    host = urllib.parse.urlsplit(url).hostname or ""
    # 本机被测服务不走环境代理
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if host in ("127.0.0.1", "localhost", "::1") else urllib.request.build_opener()
    while time.time() < end:
        try:
            opener.open(url, timeout=2)
            return True
        except urllib.error.HTTPError:
            return True  # 有 HTTP 响应即视为已起；各页状态由逐页证据判定
        except Exception:
            time.sleep(0.5)
    return False


def join(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/") if not re.match(r"^https?://", path) else path


def do_actions(page, actions: list[dict]) -> None:
    for a in actions:
        if "click" in a:
            page.click(a["click"])
        elif "fill" in a:
            page.fill(a["fill"], str(a.get("value", "")))
        elif "press" in a:
            page.keyboard.press(a["press"])
        elif "wait_for" in a:
            page.wait_for_selector(a["wait_for"])
        elif "wait_ms" in a:
            page.wait_for_timeout(int(a["wait_ms"]))


def run(manifest: dict, base_url: str, out_root: Path, axe_js: str, run_id: str) -> dict:
    from playwright.sync_api import sync_playwright  # 依赖在 main 中预检

    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    vps = manifest.get("viewports", DEFAULT_VIEWPORTS)
    report = {
        "schema": SCHEMA, "run_id": run_id, "base_url": base_url,
        "started_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "axe_tags": AXE_TAGS, "viewports": vps, "routes": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for r in manifest["routes"]:
            rr = {"name": r["name"], "path": r["path"], "states": {}, "focus_walk": {},
                  "not_applicable": r.get("not_applicable") or {}}
            for vp in vps:
                ctx = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
                page = ctx.new_page()
                for s, spec in (r.get("states") or {}).items():
                    cell: dict = {}
                    try:
                        page.goto(join(base_url, spec.get("path", r["path"])), wait_until=spec.get("wait", "networkidle"))
                        do_actions(page, spec.get("actions") or [])
                        shot = run_dir / f"{r['name']}__{s}__{vp['name']}.png"
                        page.screenshot(path=str(shot), full_page=True)
                        cell["screenshot"] = shot.name
                        page.add_script_tag(content=axe_js)
                        res = page.evaluate("t => axe.run(document, {runOnly: {type: 'tag', values: t}})", AXE_TAGS)
                        cell["axe"] = {"violations": [
                            {"id": v["id"], "impact": v.get("impact"), "help": v.get("help"), "nodes": len(v.get("nodes", []))}
                            for v in res.get("violations", [])]}
                    except Exception as e:  # 证据缺失按失败记，不吞
                        cell["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
                    rr["states"].setdefault(s, {})[vp["name"]] = cell
                walk = {"order": [], "invisible": []}
                try:
                    start = (r.get("states") or {}).get("success", {}).get("path", r["path"])
                    page.goto(join(base_url, start), wait_until="networkidle")
                    seen = set()
                    for i in range(r.get("tab_steps", 20)):
                        page.keyboard.press("Tab")
                        f = page.evaluate(FOCUS_JS)
                        if not f:
                            continue
                        if f["desc"] in seen and walk["order"] and f["desc"] == walk["order"][0]:
                            break  # 绕回首个元素
                        seen.add(f["desc"])
                        walk["order"].append(f["desc"])
                        if not f["visible"]:
                            walk["invisible"].append(f"step {i + 1}: {f['desc']}")
                    if not walk["order"]:
                        walk["note"] = "未发现可聚焦元素"
                except Exception as e:
                    walk["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
                rr["focus_walk"][vp["name"]] = walk
                ctx.close()
            report["routes"].append(rr)
        browser.close()
    report["summary"] = summarize(report)
    (run_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["_dir"] = str(run_dir)
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Web UI 运行态证据门：多视口截图 + axe WCAG 2.2 AA + 键盘焦点走查 + 数据四态")
    ap.add_argument("manifest", nargs="?", help="routes/states manifest（JSON；有 PyYAML 时可 YAML）")
    ap.add_argument("--base-url", help="覆盖 manifest.base_url")
    ap.add_argument("--start-cmd", help="启动被测应用的命令（后台运行，结束后终止）")
    ap.add_argument("--start-timeout", type=float, default=60.0)
    ap.add_argument("--out", default="evidence/ui", help="证据根（默认 evidence/ui）")
    ap.add_argument("--run-id", help="默认按时间戳生成")
    ap.add_argument("--axe-path", help="axe.min.js 路径")
    ap.add_argument("--validate-only", action="store_true", help="只校验 manifest")
    ap.add_argument("--validate-report", metavar="REPORT", help="只校验已有 report.json 结构与结论")
    ap.add_argument("--validate-review", metavar="REVIEW", help="核对 design 评审文件（roles/reviewer≠implementer/report 通过）")
    a = ap.parse_args(argv)

    if a.validate_review:
        errs = validate_review(Path(a.validate_review))
        for e in errs:
            print(f"FAIL  {e}")
        print("PASS  design 评审文件合格" if not errs else "BLOCK design 评审文件不合格")
        return 0 if not errs else 1

    if a.validate_report:
        try:
            rep = json.loads(Path(a.validate_report).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"FAIL  report 读取失败：{e}")
            return 2
        errs = validate_report(rep)
        for e in errs:
            print(f"FAIL  {e}")
        if errs:
            return 2
        if not rep["summary"]["ok"]:
            print(f"FAIL  report 结论不通过（{len(rep['summary']['failures'])} 项）")
            return 1
        print("PASS  report 结构合法且通过")
        return 0

    if not a.manifest:
        ap.error("需要 manifest（或用 --validate-report）")
    try:
        manifest = load_manifest(Path(a.manifest))
    except Exception as e:
        print(f"USAGE manifest 读取失败：{e}", file=sys.stderr)
        return 2
    errs = validate_manifest(manifest)
    for e in errs:
        print(f"FAIL  manifest: {e}")
    if errs:
        return 2
    if a.validate_only:
        print("PASS  manifest 合法")
        return 0
    base = a.base_url or manifest.get("base_url")
    if not base:
        print("USAGE 需要 --base-url 或 manifest.base_url", file=sys.stderr)
        return 2
    try:
        import playwright.sync_api  # noqa: F401
    except ImportError:
        print("BLOCK 缺 playwright：pip install playwright && playwright install chromium（未登记前不得放行，见 references/ui-delivery.md）", file=sys.stderr)
        return 2
    axe = find_axe(a.axe_path)
    if not axe:
        print("BLOCK 缺 axe-core：npm i -D axe-core，或 --axe-path / UI_EVIDENCE_AXE_JS 指向 axe.min.js", file=sys.stderr)
        return 2

    proc = None
    if a.start_cmd:
        proc = subprocess.Popen(a.start_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        if not wait_url(base, a.start_timeout if proc else 10):
            print(f"FAIL  无法访问 {base}")
            return 1
        run_id = a.run_id or _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        rep = run(manifest, base, Path(a.out), axe.read_text(encoding="utf-8"), run_id)
    finally:
        if proc:
            try:
                os.killpg(proc.pid, 15)
            except ProcessLookupError:
                pass
    s = rep["summary"]
    for f in s["failures"]:
        print(f"FAIL  {f}")
    print(f"report: {rep['_dir']}/report.json")
    print("PASS  UI 证据门通过" if s["ok"] else f"BLOCK UI 证据门不通过（{len(s['failures'])} 项）")
    return 0 if s["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
