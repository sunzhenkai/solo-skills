#!/usr/bin/env python3
"""Web UI 运行态证据门（references/ui-delivery.md「机械门」）。

支持两档运行态检查：
  - L1 快检（--quick --base-url <url> [--routes /,/settings]）：免手写 manifest，面向所有 UI 改动。
    捕获 pageerror / console.error / 资源 4xx-5xx、裂图、横向溢出、外扩环被裁、极小热区(<24px)、
    键盘焦点可见与不被 sticky/fixed 遮挡；找到 axe-core 时顺跑 WCAG 2.2 AA，缺失时标 skipped。
  - L2 完整门（传 manifest）：L1 全部（axe-core 强制）+ ≥2 必备视口 + 数据四态（loading/empty/error/success）
    + 可选交互浮层 overlays 检查（打开可见、内边距防贴边、无溢出、焦点进入与 Esc 归还）+ DPR=2 截图。

产物：<out>/<run-id>/report.json + PNG。
另：--validate-report 核对已有 report.json；--validate-review 核对 design 评审文件
（frontmatter: roles 含 design、reviewer ≠ implementer、report 指向通过的 report.json）。

退出码：0 通过 · 1 门不通过（运行时报错、裂图、溢出/环被裁/极小热区、axe serious/critical、
        缺态、缺视口、焦点不可见/被遮挡、浮层不通过、页面打不开）
        · 2 用法 / manifest 不合法 / 依赖缺失（playwright；完整门缺 axe-core 也为 2）。

依赖：pip install playwright && playwright install chromium；axe-core 由 --axe-path、
环境变量 UI_EVIDENCE_AXE_JS，或 ./node_modules/axe-core/axe.min.js（`npm i -D axe-core`）提供。
manifest 可为 JSON；装了 PyYAML 时也接受 YAML。
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


def build_quick_manifest(base_url: str, routes_arg: str) -> dict:
    raw = [x.strip() for x in routes_arg.split(",") if x.strip()] or ["/"]
    routes = []
    seen: set[str] = set()
    for idx, p in enumerate(raw):
        norm = p if p.startswith("/") or re.match(r"^https?://", p) else "/" + p
        slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", norm.strip("/")) or "home"
        name = slug if slug not in seen else f"{slug}_{idx + 1}"
        seen.add(name)
        routes.append({
            "name": name,
            "path": norm,
            "states": {"default": {"path": norm}},
            "not_applicable": {},
            "tab_steps": 20,
        })
    return {"base_url": base_url, "viewports": list(DEFAULT_VIEWPORTS), "routes": routes}


def _validate_actions(actions: object, prefix: str, errs: list[str]) -> None:
    if not isinstance(actions, list):
        errs.append(f"{prefix} 须为列表")
        return
    for j, act in enumerate(actions):
        if not isinstance(act, dict) or not (set(act) - {"value"}) <= ACTION_KEYS or not (set(act) & ACTION_KEYS):
            errs.append(f"{prefix}[{j}] 非法：{act!r}")


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
            if spec.get("actions") is not None:
                _validate_actions(spec.get("actions"), f"{tag}.states.{s}.actions", errs)
        overlays = r.get("overlays")
        if overlays is not None:
            if not isinstance(overlays, list):
                errs.append(f"{tag}.overlays 须为列表")
            else:
                ov_names = set()
                for k, ov in enumerate(overlays):
                    otag = f"{tag}.overlays[{k}]"
                    if not isinstance(ov, dict):
                        errs.append(f"{otag} 须为对象")
                        continue
                    oname = ov.get("name")
                    if not oname or not re.fullmatch(r"[A-Za-z0-9_.-]+", str(oname)):
                        errs.append(f"{otag}.name 须为 [A-Za-z0-9_.-]+")
                    elif oname in ov_names:
                        errs.append(f"{otag}.name 重复：{oname}")
                    ov_names.add(oname)
                    if not isinstance(ov.get("container"), str) or not ov["container"].strip():
                        errs.append(f"{otag}.container 须为非空 CSS 选择器")
                    trig = ov.get("trigger")
                    if isinstance(trig, dict):
                        _validate_actions([trig], f"{otag}.trigger", errs)
                    elif isinstance(trig, list) and trig:
                        _validate_actions(trig, f"{otag}.trigger", errs)
                    else:
                        errs.append(f"{otag}.trigger 须为单个动作或非空动作列表")
        ts = r.get("tab_steps", 20)
        if not isinstance(ts, int) or ts < 1:
            errs.append(f"{tag}.tab_steps 须为正整数")
    return errs


# ---------------------------------------------------------------- report

def summarize(report: dict) -> dict:
    failures: list[str] = []
    warnings: list[str] = []
    mode = report.get("mode", "full")
    vp_names = [v["name"] for v in report["viewports"]]
    sizes = {(v["width"], v["height"]) for v in report["viewports"]}
    missing_vp = [f"{w}x{h}" for (w, h) in sorted(REQUIRED_SIZES - sizes)]
    for s in missing_vp:
        failures.append(f"缺视口 {s}")

    axe_blocking = missing_states = invisible = obscured = 0
    runtime_errors = broken_images = layout_blocking = overlay_failures = 0

    for r in report["routes"]:
        states_map = r.get("states") or {}
        target_states = list(states_map.keys()) if mode == "quick" else list(REQUIRED_STATES)
        for s in target_states:
            if mode != "quick" and s in r.get("not_applicable", {}):
                continue
            st = states_map.get(s)
            for vp in vp_names:
                cell = (st or {}).get(vp)
                loc = f"{r['name']}/{s}/{vp}"
                if not cell or not cell.get("screenshot") or cell.get("error"):
                    missing_states += 1
                    failures.append(f"{loc}: 缺证据" + (f"（{cell['error']}）" if cell and cell.get("error") else ""))
                    continue

                # axe
                for v in (cell.get("axe") or {}).get("violations", []):
                    if v.get("impact") in BLOCKING_IMPACTS:
                        axe_blocking += 1
                        failures.append(f"{loc}: axe {v['impact']} {v['id']}（{v.get('nodes', 0)} 处）")

                # runtime errors
                rt = cell.get("runtime") or {}
                for e in rt.get("page_errors") or []:
                    runtime_errors += 1
                    failures.append(f"{loc}: pageerror {e}")
                if not cell.get("allow_console_errors"):
                    for e in rt.get("console_errors") or []:
                        runtime_errors += 1
                        failures.append(f"{loc}: console.error {e}")
                if s != "error" and not cell.get("allow_http_errors"):
                    for e in rt.get("http_errors") or []:
                        runtime_errors += 1
                        failures.append(f"{loc}: HTTP 错误 {e}")
                    for e in rt.get("request_failed") or []:
                        runtime_errors += 1
                        failures.append(f"{loc}: 请求失败 {e}")

                # dom checks
                dom = cell.get("dom") or {}
                ho = dom.get("horizontal_overflow") or {}
                if ho.get("overflow"):
                    layout_blocking += 1
                    culprits = "、".join((ho.get("culprits") or [])[:3])
                    extra = f"（元凶：{culprits}）" if culprits else ""
                    failures.append(f"{loc}: 横向溢出 {ho.get('scroll_width')} > {ho.get('inner_width')}{extra}")
                for img in dom.get("broken_images") or []:
                    broken_images += 1
                    failures.append(f"{loc}: 裂图 {img}")
                for ring in dom.get("clipped_rings") or []:
                    layout_blocking += 1
                    failures.append(f"{loc}: 环被裁 {ring}")
                for t in dom.get("tiny_targets_blocking") or []:
                    layout_blocking += 1
                    failures.append(f"{loc}: 点击热区过小(<24px) {t}")

                # warnings (non-blocking)
                for w in dom.get("tiny_targets_warn") or []:
                    warnings.append(f"{loc}: 移动端热区偏小(<40px) {w}")
                for w in dom.get("long_lines") or []:
                    warnings.append(f"{loc}: 行太长 {w}")
                for w in dom.get("small_text") or []:
                    warnings.append(f"{loc}: 字太小 {w}")
                for w in dom.get("tight_line_height") or []:
                    warnings.append(f"{loc}: 行高过紧 {w}")

        for vp, walk in (r.get("focus_walk") or {}).items():
            for step in walk.get("invisible", []):
                invisible += 1
                failures.append(f"{r['name']}/{vp}: 焦点不可见 @ {step}")
            for step in walk.get("obscured", []):
                obscured += 1
                failures.append(f"{r['name']}/{vp}: 焦点被浮层遮挡 @ {step}")

        for ov_name, vp_cells in (r.get("overlays") or {}).items():
            for vp, ov in vp_cells.items():
                oloc = f"{r['name']}/overlay:{ov_name}/{vp}"
                if ov.get("error"):
                    overlay_failures += 1
                    failures.append(f"{oloc}: 打开/检查失败（{ov['error']}）")
                    continue
                if not ov.get("visible"):
                    overlay_failures += 1
                    failures.append(f"{oloc}: 触发后浮层不可见")
                if ov.get("padding_clipped"):
                    overlay_failures += 1
                    failures.append(f"{oloc}: 内容贴边（内边距不足）")
                if ov.get("overflow"):
                    overlay_failures += 1
                    failures.append(f"{oloc}: 浮层内部横向溢出")
                if ov.get("focus_entered") is False:
                    overlay_failures += 1
                    failures.append(f"{oloc}: 打开后焦点未进入浮层")
                if ov.get("closed") is False:
                    overlay_failures += 1
                    failures.append(f"{oloc}: 按关闭键后浮层未关闭")
                if ov.get("focus_restored") is False:
                    overlay_failures += 1
                    failures.append(f"{oloc}: 关闭后焦点未归还触发区")

    return {
        "axe_blocking": axe_blocking,
        "missing_states": missing_states,
        "missing_viewports": missing_vp,
        "focus_invisible": invisible,
        "focus_obscured": obscured,
        "runtime_errors": runtime_errors,
        "broken_images": broken_images,
        "layout_blocking": layout_blocking,
        "overlay_failures": overlay_failures,
        "warnings": warnings,
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
    mode = rep.get("mode", "full")
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
                if not cell.get("error"):
                    if "screenshot" not in cell:
                        errs.append(f"{r.get('name')}/{s}/{vp}: 缺 screenshot")
                    if mode != "quick" and "axe" not in cell:
                        errs.append(f"{r.get('name')}/{s}/{vp}: 缺 axe")
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
  const desc = el.tagName.toLowerCase() + id + (label ? ' "' + label + '"' : '');
  let obscured = false;
  let obscuredBy = '';
  const rect = el.getBoundingClientRect();
  if (rect.width > 0 && rect.height > 0) {
    const cx = Math.min(Math.max(rect.left + rect.width / 2, 1), window.innerWidth - 1);
    const cy = Math.min(Math.max(rect.top + rect.height / 2, 1), window.innerHeight - 1);
    const hit = document.elementFromPoint(cx, cy);
    if (hit && hit !== el && !el.contains(hit) && !hit.contains(el)) {
      let p = hit;
      while (p && p !== document.body && p !== document.documentElement) {
        const ps = getComputedStyle(p);
        if (ps.position === 'fixed' || ps.position === 'sticky') {
          obscured = true;
          obscuredBy = p.tagName.toLowerCase() + (p.id ? '#' + p.id : '') +
            (p.className && typeof p.className === 'string' && p.className.trim() ? '.' + p.className.trim().split(/\\s+/)[0] : '');
          break;
        }
        p = p.parentElement;
      }
    }
  }
  return {desc, visible: !!visible, obscured, obscuredBy};
}"""

DOM_CHECK_JS = """(isMobile) => {
  const px = (v) => parseFloat(v) || 0;
  const name = (x) => x.tagName.toLowerCase() + (x.id ? '#' + x.id : '') +
    (x.getAttribute('class') ? '.' + x.getAttribute('class').trim().split(/\\s+/)[0] : '');
  const isVisible = (el) => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const out = (s) => {
    let m = s.outlineStyle === 'none' ? 0 : px(s.outlineWidth) + px(s.outlineOffset);
    for (const seg of (s.boxShadow === 'none' ? '' : s.boxShadow).split(/,(?![^(]*\\))/)) {
      const len = seg.match(/-?[\\d.]+px/g) || [];
      if (!/inset/.test(seg) && len.length >= 4) m = Math.max(m, px(len[3]));
    }
    return m;
  };

  // 1. 横向溢出及元凶
  const sw = document.documentElement.scrollWidth;
  const iw = window.innerWidth;
  const culprits = [];
  if (sw > iw + 1) {
    for (const el of document.querySelectorAll('body *')) {
      if (!isVisible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > iw + 1) {
        culprits.push(name(el) + ' (right=' + Math.round(r.right) + ')');
        if (culprits.length >= 5) break;
      }
    }
  }

  // 2. 裂图
  const broken_images = [];
  for (const img of document.querySelectorAll('img')) {
    if (!isVisible(img)) continue;
    if (img.complete && img.naturalWidth === 0) {
      broken_images.push(img.getAttribute('src') || img.getAttribute('alt') || '<img>');
    }
  }

  // 3. 排版量测（warning）
  const long_lines = [], small_text = [], tight_line_height = [];
  for (const el of document.querySelectorAll('p, li, dd, blockquote, td')) {
    const t = (el.textContent || '').trim();
    if (t.length < 30 || !el.offsetWidth) continue;
    const s = getComputedStyle(el), size = parseFloat(s.fontSize);
    const zh = /[\\u4e00-\\u9fff]/.test(t), w = el.getBoundingClientRect().width;
    const perLine = Math.round(zh ? w / size : w / (size * 0.5));
    const lh = s.lineHeight === 'normal' ? 1.2 : parseFloat(s.lineHeight) / size;
    const tag = el.tagName.toLowerCase() + '「' + t.slice(0, 12) + '」';
    if (perLine > (zh ? 46 : 95)) long_lines.push(tag + ' 约 ' + perLine + (zh ? ' 字' : ' 字符'));
    if (size < 12.5) small_text.push(tag + ' ' + size + 'px');
    if (lh < (zh ? 1.5 : 1.4)) tight_line_height.push(tag + ' ' + lh.toFixed(2));
  }

  // 4. 外扩环被祖先 overflow 裁切
  const clipped_rings = [];
  for (const el of document.querySelectorAll('*')) {
    const d = out(getComputedStyle(el));
    if (d <= 0 || !el.offsetWidth) continue;
    let a = el.parentElement;
    for (; a; a = a.parentElement) {
      const s = getComputedStyle(a);
      if (s.overflowX !== 'visible' || s.overflowY !== 'visible') break;
    }
    if (!a) continue;
    const e = el.getBoundingClientRect(), b = a.getBoundingClientRect(), s = getComputedStyle(a);
    const sx = a.scrollWidth > a.clientWidth, sy = a.scrollHeight > a.clientHeight, edge = [];
    if (e.left - d < b.left + px(s.borderLeftWidth) - 0.5 && !sx) edge.push('左');
    if (e.right + d > b.right - px(s.borderRightWidth) + 0.5 && !sx) edge.push('右');
    if (e.top - d < b.top + px(s.borderTopWidth) - 0.5 && !sy) edge.push('上');
    if (e.bottom + d > b.bottom - px(s.borderBottomWidth) + 0.5 && !sy) edge.push('下');
    if (edge.length) clipped_rings.push(name(el) + ' 被裁' + edge.join('') + '，裁它：' + name(a));
  }

  // 5. 可交互目标热区尺寸（不含正文行内链接）
  const tiny_targets_blocking = [], tiny_targets_warn = [];
  for (const el of document.querySelectorAll('button, [role="button"], input:not([type="hidden"]), select, textarea')) {
    if (!isVisible(el) || el.disabled) continue;
    const r = el.getBoundingClientRect();
    const minSide = Math.min(r.width, r.height);
    if (minSide < 24) {
      tiny_targets_blocking.push(name(el) + ' (' + Math.round(r.width) + 'x' + Math.round(r.height) + ')');
    } else if (isMobile && minSide < 40) {
      tiny_targets_warn.push(name(el) + ' (' + Math.round(r.width) + 'x' + Math.round(r.height) + ')');
    }
  }

  return {
    horizontal_overflow: {overflow: sw > iw + 1, scroll_width: sw, inner_width: iw, culprits},
    broken_images,
    clipped_rings,
    tiny_targets_blocking,
    tiny_targets_warn,
    long_lines,
    small_text,
    tight_line_height,
  };
}"""

OVERLAY_CHECK_JS = """([selector, minPad]) => {
  const el = document.querySelector(selector);
  if (!el) return {visible: false};
  const s = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  const visible = s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0 && r.width > 0 && r.height > 0;
  if (!visible) return {visible: false};
  const px = (v) => parseFloat(v) || 0;
  const padMin = Math.min(px(s.paddingLeft), px(s.paddingRight), px(s.paddingTop), px(s.paddingBottom));
  let padding_clipped = false;
  if (padMin < minPad) {
    // 若容器本身无 padding，检查直接子元素是否贴着容器左/右/上边缘
    const kids = Array.from(el.children).filter(c => {
      const cr = c.getBoundingClientRect();
      return cr.width > 0 && cr.height > 0;
    });
    if (kids.length) {
      const k = kids[0].getBoundingClientRect();
      const ks = getComputedStyle(kids[0]);
      const gapL = (k.left - r.left) + px(ks.paddingLeft);
      const gapR = (r.right - k.right) + px(ks.paddingRight);
      const gapT = (k.top - r.top) + px(ks.paddingTop);
      if (Math.min(gapL, gapR, gapT) < minPad) padding_clipped = true;
    }
  }
  const overflow = el.scrollWidth > el.clientWidth + 1;
  const active = document.activeElement;
  const focus_entered = !!(active && (active === el || el.contains(active)));
  return {visible: true, padding_clipped, overflow, focus_entered};
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


def run(
    manifest: dict,
    base_url: str,
    out_root: Path,
    axe_js: str | None,
    run_id: str,
    *,
    mode: str = "full",
    dpr: float = 2.0,
    with_fold: bool = False,
) -> dict:
    from playwright.sync_api import sync_playwright  # 依赖在 main 中预检

    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    vps = manifest.get("viewports", DEFAULT_VIEWPORTS)
    report: dict = {
        "schema": SCHEMA,
        "mode": mode,
        "run_id": run_id,
        "base_url": base_url,
        "dpr": dpr,
        "started_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "axe_tags": AXE_TAGS if axe_js else [],
        "axe_skipped": axe_js is None,
        "viewports": vps,
        "routes": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for r in manifest["routes"]:
            rr: dict = {
                "name": r["name"],
                "path": r["path"],
                "states": {},
                "focus_walk": {},
                "overlays": {},
                "not_applicable": r.get("not_applicable") or {},
            }
            for vp in vps:
                is_mobile = vp["width"] <= 480
                ctx = browser.new_context(
                    viewport={"width": vp["width"], "height": vp["height"]},
                    device_scale_factor=dpr,
                )
                page = ctx.new_page()

                rt_buf: dict[str, list[str]] = {
                    "page_errors": [],
                    "console_errors": [],
                    "http_errors": [],
                    "request_failed": [],
                }
                page.on("pageerror", lambda err: rt_buf["page_errors"].append(str(err).splitlines()[0][:200]))
                page.on("console", lambda msg: rt_buf["console_errors"].append(msg.text[:200]) if msg.type == "error" else None)
                page.on("response", lambda res: rt_buf["http_errors"].append(f"{res.status} {res.url[:120]}") if res.status >= 400 else None)
                page.on("requestfailed", lambda req: rt_buf["request_failed"].append(f"{req.url[:120]} ({req.failure})") if req.failure else None)

                for s, spec in (r.get("states") or {}).items():
                    for k in rt_buf:
                        rt_buf[k].clear()
                    cell: dict = {}
                    if spec.get("allow_console_errors"):
                        cell["allow_console_errors"] = True
                    if spec.get("allow_http_errors"):
                        cell["allow_http_errors"] = True
                    try:
                        page.goto(join(base_url, spec.get("path", r["path"])), wait_until=spec.get("wait", "networkidle"))
                        do_actions(page, spec.get("actions") or [])
                        shot = run_dir / f"{r['name']}__{s}__{vp['name']}.png"
                        page.screenshot(path=str(shot), full_page=True)
                        cell["screenshot"] = shot.name
                        if with_fold:
                            fshot = run_dir / f"{r['name']}__{s}__{vp['name']}__fold.png"
                            page.screenshot(path=str(fshot), full_page=False)
                            cell["screenshot_fold"] = fshot.name
                        cell["runtime"] = {k: list(v) for k, v in rt_buf.items()}
                        cell["dom"] = page.evaluate(DOM_CHECK_JS, is_mobile)
                        if axe_js:
                            page.add_script_tag(content=axe_js)
                            res = page.evaluate("t => axe.run(document, {runOnly: {type: 'tag', values: t}})", AXE_TAGS)
                            cell["axe"] = {"violations": [
                                {"id": v["id"], "impact": v.get("impact"), "help": v.get("help"), "nodes": len(v.get("nodes", []))}
                                for v in res.get("violations", [])]}
                    except Exception as e:  # 证据缺失按失败记，不吞
                        cell["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
                    rr["states"].setdefault(s, {})[vp["name"]] = cell

                # 键盘焦点走查（含 sticky/fixed 遮挡检查）
                walk: dict = {"order": [], "invisible": [], "obscured": []}
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
                        if f.get("obscured"):
                            walk["obscured"].append(f"step {i + 1}: {f['desc']} 被 {f.get('obscuredBy') or 'fixed/sticky'} 遮挡")
                    if not walk["order"]:
                        walk["note"] = "未发现可聚焦元素"
                except Exception as e:
                    walk["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
                rr["focus_walk"][vp["name"]] = walk

                # 交互浮层检查（manifest.routes[].overlays）
                for ov in r.get("overlays") or []:
                    ov_res: dict = {}
                    try:
                        start = (r.get("states") or {}).get("success", {}).get("path", r["path"])
                        page.goto(join(base_url, start), wait_until="networkidle")
                        trig = ov["trigger"]
                        do_actions(page, trig if isinstance(trig, list) else [trig])
                        page.wait_for_selector(ov["container"], state="visible", timeout=5000)
                        ov_shot = run_dir / f"{r['name']}__overlay_{ov['name']}__{vp['name']}.png"
                        page.screenshot(path=str(ov_shot), full_page=False)
                        ov_res["screenshot"] = ov_shot.name
                        ov_res.update(page.evaluate(OVERLAY_CHECK_JS, [ov["container"], ov.get("min_padding", 8)]))
                        close_key = ov.get("close_key", "Escape")
                        if close_key:
                            page.keyboard.press(close_key)
                            page.wait_for_timeout(150)
                            still = page.evaluate(
                                "sel => { const e = document.querySelector(sel); if (!e) return false; "
                                "const s = getComputedStyle(e); const r = e.getBoundingClientRect(); "
                                "return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0; }",
                                ov["container"],
                            )
                            ov_res["closed"] = not still
                            ov_res["focus_restored"] = bool(page.evaluate(
                                "() => { const a = document.activeElement; return !!(a && a !== document.body && a !== document.documentElement); }"
                            ))
                    except Exception as e:
                        ov_res["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
                    rr["overlays"].setdefault(ov["name"], {})[vp["name"]] = ov_res

                ctx.close()
            report["routes"].append(rr)
        browser.close()
    report["summary"] = summarize(report)
    (run_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["_dir"] = str(run_dir)
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Web UI 运行态证据门：L1 快检（--quick）与 L2 完整门（manifest）")
    ap.add_argument("manifest", nargs="?", help="routes/states manifest（JSON；有 PyYAML 时可 YAML）")
    ap.add_argument("--quick", action="store_true", help="L1 快检模式：免 manifest，按 --routes 扫运行时错误、裂图、布局溢出、环被裁与焦点")
    ap.add_argument("--routes", default="/", help="配合 --quick：逗号分隔的路由路径（默认 /）")
    ap.add_argument("--base-url", help="覆盖 manifest.base_url（--quick 模式下必填）")
    ap.add_argument("--start-cmd", help="启动被测应用的命令（后台运行，结束后终止）")
    ap.add_argument("--start-timeout", type=float, default=60.0)
    ap.add_argument("--out", default="evidence/ui", help="证据根（默认 evidence/ui）")
    ap.add_argument("--run-id", help="默认按时间戳生成")
    ap.add_argument("--axe-path", help="axe.min.js 路径")
    ap.add_argument("--dpr", type=float, default=2.0, help="截图设备像素比（默认 2.0，用于 1px 细线校验）")
    ap.add_argument("--with-fold", action="store_true", help="除整页外额外保存首屏截图（*__fold.png）")
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

    mode = "quick" if a.quick else "full"
    if a.quick:
        if not a.base_url:
            print("USAGE --quick 模式需要 --base-url", file=sys.stderr)
            return 2
        manifest = build_quick_manifest(a.base_url, a.routes)
        base = a.base_url
    else:
        if not a.manifest:
            ap.error("需要 manifest（或用 --quick / --validate-report）")
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
    if not axe and mode == "full":
        print("BLOCK 缺 axe-core：npm i -D axe-core，或 --axe-path / UI_EVIDENCE_AXE_JS 指向 axe.min.js", file=sys.stderr)
        return 2
    axe_js = axe.read_text(encoding="utf-8") if axe else None

    proc = None
    if a.start_cmd:
        proc = subprocess.Popen(a.start_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        if not wait_url(base, a.start_timeout if proc else 10):
            print(f"FAIL  无法访问 {base}")
            return 1
        run_id = a.run_id or _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        rep = run(manifest, base, Path(a.out), axe_js, run_id, mode=mode, dpr=a.dpr, with_fold=a.with_fold)
    finally:
        if proc:
            try:
                os.killpg(proc.pid, 15)
            except ProcessLookupError:
                pass
    s = rep["summary"]
    for f in s["failures"]:
        print(f"FAIL  {f}")
    for w in s.get("warnings") or []:
        print(f"WARN  {w}")
    if rep.get("axe_skipped"):
        print("WARN  quick 模式未找到 axe-core，WCAG 检查已跳过")
    print(f"report: {rep['_dir']}/report.json")
    print("PASS  UI 证据门通过" if s["ok"] else f"BLOCK UI 证据门不通过（{len(s['failures'])} 项）")
    return 0 if s["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
