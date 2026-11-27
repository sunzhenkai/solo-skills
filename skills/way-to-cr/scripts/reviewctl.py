#!/usr/bin/env python3
"""Helpers for /way-to-cr: resolve repos, inspect/preview changes, probe engines & prefs, parse MR/PR, render & write docs."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

SKIP_DIRS = {
    ".git",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    "target",
    ".tox",
}
PRIORITY_ORDER = ("P0", "P1", "P2", "P3", "P4")
ALLOWED_ENGINES = ("builtin", "claude", "codex", "ocr")
MODEL_ENGINES = ("claude", "codex", "ocr")
SENSITIVE_KEY_PARTS = ("key", "token", "secret", "password", "passwd", "auth", "credential")
DEFAULT_CLAUDE_MODELS = ("sonnet", "opus", "haiku")
DEFAULT_CODEX_MODELS = ("o3", "gpt-5.2", "gpt-5.1-codex")
GUIDELINE_CANDIDATES = (
    "AGENTS.md",
    "CLAUDE.md",
    ".cursorrules",
    "CONTRIBUTING.md",
    ".github/copilot-instructions.md",
)
LOCKFILE_NAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "Cargo.lock",
    "go.sum",
    "poetry.lock",
    "uv.lock",
    "Gemfile.lock",
    "composer.lock",
}
GENERATED_PATTERNS = ("*.min.js", "*.min.css", "*.map", "*.pb.go")
BINARY_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".tgz",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".mp3",
    ".mp4",
    ".mov",
    ".wasm",
    ".pyc",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
}
GITLAB_MR = re.compile(
    r"^https?://(?P<host>[^/]+)/(?P<project>.+?)/-/?merge_requests/(?P<iid>\d+)(?:[/?#].*)?$",
    re.I,
)
GITLAB_MR_ALT = re.compile(
    r"^https?://(?P<host>[^/]+)/(?P<project>.+?)/merge_requests/(?P<iid>\d+)(?:[/?#].*)?$",
    re.I,
)
GITHUB_PR = re.compile(
    r"^https?://(?P<host>[^/]+)/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<iid>\d+)(?:[/?#].*)?$",
    re.I,
)
P0_RE = re.compile(
    r"(sql\s*injection|xss|rce|auth(?:entication)? bypass|越权|数据丢失|secret|凭证泄露|"
    r"任意文件|路径穿越|panic\b|segfault|生产事故|P0)",
    re.I,
)
P1_RE = re.compile(
    r"(race|deadlock|nil deref|npe|空指针|正确性|逻辑错误|并发安全|数据竞争|丢事件|"
    r"broken api|崩溃|crash|P1)",
    re.I,
)
P2_RE = re.compile(
    r"(error handling|missing test|缺少测试|可维护|资源泄露|timeout|重试|P2)",
    re.I,
)
SEVERITY_TO_PRIORITY = {
    "critical": "P0",
    "high": "P1",
    "medium": "P2",
    "low": "P3",
}
GIT_DIFF_ARGS = ("--no-ext-diff", "--no-textconv", "--no-color")


class ReviewError(Exception):
    pass


def repo_root_from_script() -> Path:
    return Path.cwd()


def git(args: list[str], cwd: Path, check: bool = True, no_pager: bool = False) -> str:
    cmd = ["git", *(["--no-pager"] if no_pager else []), *args]
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise ReviewError(f"git {' '.join(args)} failed: {err}")
    return (proc.stdout or "").strip()


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        val = item.strip()
        if val and val not in seen:
            seen.add(val)
            out.append(val)
    return out


def default_prefs_path(override: str = "") -> Path:
    if override.strip():
        return Path(override).expanduser().resolve()
    env_path = os.environ.get("WAY_TO_CR_PREFS", "").strip()
    if env_path:
        return Path(env_path).expanduser().resolve()
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg).expanduser() if xdg else (Path.home() / ".config")
    return (base / "way-to-cr" / "prefs.json").resolve()


def _empty_prefs() -> dict[str, Any]:
    return {
        "version": 1,
        "default_engine": "",
        "persist_default": None,
        "engines": {
            "claude": {"model": "", "mode": ""},
            "codex": {"model": ""},
            "ocr": {"provider": "", "model": ""},
        },
        "updated_at": "",
    }


def _assert_safe_value(field: str, value: str) -> str:
    low = field.lower()
    if any(part in low for part in SENSITIVE_KEY_PARTS):
        raise ReviewError(f"refusing to store sensitive field: {field}")
    return value.strip()


def load_prefs(prefs_path: Path) -> dict[str, Any]:
    data = _empty_prefs()
    if not prefs_path.is_file():
        return data
    try:
        raw = json.loads(prefs_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"failed to read prefs {prefs_path}: {exc}") from exc
    if not isinstance(raw, dict):
        return data
    if raw.get("default_engine") in (*ALLOWED_ENGINES, ""):
        data["default_engine"] = str(raw.get("default_engine") or "")
    if isinstance(raw.get("persist_default"), bool) or raw.get("persist_default") is None:
        data["persist_default"] = raw.get("persist_default")
    raw_engines = raw.get("engines")
    if isinstance(raw_engines, dict):
        for eng in MODEL_ENGINES:
            entry = raw_engines.get(eng)
            if not isinstance(entry, dict):
                continue
            for k in data["engines"][eng]:
                if k in entry and isinstance(entry[k], str):
                    data["engines"][eng][k] = entry[k].strip()
    data["updated_at"] = str(raw.get("updated_at") or "")
    return data


def save_prefs(prefs_path: Path, data: dict[str, Any]) -> dict[str, Any]:
    clean = _empty_prefs()
    eng_default = str(data.get("default_engine") or "")
    if eng_default and eng_default not in ALLOWED_ENGINES:
        raise ReviewError(f"unsupported engine: {eng_default}")
    clean["default_engine"] = eng_default
    persist = data.get("persist_default")
    clean["persist_default"] = persist if isinstance(persist, bool) else None
    raw_engines = data.get("engines") or {}
    for eng in MODEL_ENGINES:
        src = raw_engines.get(eng) or {}
        if not isinstance(src, dict):
            continue
        for k in clean["engines"][eng]:
            val = src.get(k)
            if isinstance(val, str):
                clean["engines"][eng][k] = _assert_safe_value(k, val)
    clean["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    prefs_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".prefs-", suffix=".tmp", dir=str(prefs_path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(clean, ensure_ascii=False, indent=2) + "\n")
        os.replace(tmp_name, prefs_path)
    except Exception:
        if Path(tmp_name).exists():
            Path(tmp_name).unlink()
        raise
    return clean


def set_prefs(
    prefs_path: Path,
    *,
    engine: str = "",
    model: str = "",
    provider: str = "",
    mode: str = "",
    set_default_engine: bool = False,
    persist_default: str = "",
) -> dict[str, Any]:
    data = load_prefs(prefs_path)
    if engine:
        if engine not in ALLOWED_ENGINES:
            raise ReviewError(f"unsupported engine: {engine}")
        if set_default_engine:
            data["default_engine"] = engine
    if persist_default:
        low = persist_default.strip().lower()
        if low == "true":
            data["persist_default"] = True
        elif low == "false":
            data["persist_default"] = False
        else:
            raise ReviewError("persist-default must be true or false")
    if engine in MODEL_ENGINES:
        slot = data["engines"][engine]
        if model:
            slot["model"] = _assert_safe_value("model", model)
        if provider and "provider" in slot:
            slot["provider"] = _assert_safe_value("provider", provider)
        if mode and "mode" in slot:
            slot["mode"] = _assert_safe_value("mode", mode)
    elif model or provider or mode:
        raise ReviewError(f"engine {engine or '<none>'} does not store model/provider/mode")
    return save_prefs(prefs_path, data)


def clear_prefs(prefs_path: Path, *, engine: str = "") -> dict[str, Any]:
    data = load_prefs(prefs_path)
    if engine:
        if engine not in ALLOWED_ENGINES:
            raise ReviewError(f"unsupported engine: {engine}")
        if engine in MODEL_ENGINES:
            for k in list(data["engines"][engine]):
                data["engines"][engine][k] = ""
        if data.get("default_engine") == engine:
            data["default_engine"] = ""
    else:
        data = _empty_prefs()
    return save_prefs(prefs_path, data)


def _run_probe_cmd(cmd: list[str], timeout: int = 3) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.returncode, (proc.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def _read_claude_settings(settings_path: Path) -> tuple[str, bool]:
    if not settings_path.is_file():
        return "", False
    try:
        raw = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "", False
    if not isinstance(raw, dict):
        return "", False
    model = str(raw.get("model") or "").strip()
    plugins = raw.get("enabledPlugins")
    has_plugin = False
    if isinstance(plugins, list):
        has_plugin = any("code-review" in str(p) for p in plugins)
    elif isinstance(plugins, dict):
        has_plugin = any("code-review" in str(k) and bool(v) for k, v in plugins.items())
    return model, has_plugin


def _read_codex_config(config_path: Path) -> tuple[list[str], str]:
    if not config_path.is_file():
        return [], ""
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError:
        return [], ""
    models: list[str] = []
    provider = ""
    if tomllib is not None:
        try:
            parsed = tomllib.loads(text)
            if isinstance(parsed, dict):
                if isinstance(parsed.get("model"), str) and parsed["model"].strip():
                    models.append(parsed["model"].strip())
                if isinstance(parsed.get("model_provider"), str):
                    provider = parsed["model_provider"].strip()
                profiles = parsed.get("profiles")
                if isinstance(profiles, dict):
                    for prof in profiles.values():
                        if isinstance(prof, dict) and isinstance(prof.get("model"), str) and prof["model"].strip():
                            models.append(prof["model"].strip())
                return _dedupe(models), provider
        except Exception:
            pass
    for m in re.finditer(r'^\s*model\s*=\s*["\']([^"\']+)["\']', text, re.M):
        models.append(m.group(1).strip())
    pm = re.search(r'^\s*model_provider\s*=\s*["\']([^"\']+)["\']', text, re.M)
    if pm:
        provider = pm.group(1).strip()
    return _dedupe(models), provider


def _parse_codex_debug_models(output: str) -> list[str]:
    if not output:
        return []
    try:
        data = json.loads(output)
        items = data.get("models") if isinstance(data, dict) else data
        if isinstance(items, list):
            out = []
            for item in items:
                if isinstance(item, str):
                    out.append(item)
                elif isinstance(item, dict):
                    mid = item.get("id") or item.get("slug") or item.get("model") or item.get("name")
                    if isinstance(mid, str) and mid.strip():
                        out.append(mid.strip())
            return _dedupe(out)
    except json.JSONDecodeError:
        pass
    return []


def _parse_ocr_providers(output: str) -> list[str]:
    providers: list[str] = []
    for line in output.splitlines():
        clean = line.strip()
        if not clean or clean.startswith(("#", "-", "=", "Available", "Provider")):
            continue
        token = re.split(r"[\s:]+", clean, maxsplit=1)[0].strip("*•-")
        if token and re.match(r"^[a-zA-Z0-9._-]+$", token):
            providers.append(token)
    return _dedupe(providers)


def probe_engines(
    prefs_path: Path,
    *,
    engine: str = "",
    claude_settings: Path | None = None,
    codex_config: Path | None = None,
) -> dict[str, Any]:
    if engine and engine not in ALLOWED_ENGINES:
        raise ReviewError(f"unsupported engine: {engine}")
    prefs = load_prefs(prefs_path)
    targets = (engine,) if engine else ALLOWED_ENGINES
    results: dict[str, Any] = {}

    if "builtin" in targets:
        results["builtin"] = {
            "available": True,
            "needs_model_selection": False,
            "note": "使用当前会话模型，零额外依赖",
            "models": [],
        }

    if "claude" in targets:
        bin_path = shutil.which("claude")
        cfg_path = claude_settings or (Path.home() / ".claude" / "settings.json")
        cfg_model, has_plugin = _read_claude_settings(cfg_path)
        saved = prefs["engines"]["claude"]
        saved_model = saved.get("model", "")
        candidates = _dedupe([*DEFAULT_CLAUDE_MODELS, cfg_model, saved_model])
        results["claude"] = {
            "available": bool(bin_path),
            "binary": bin_path or "",
            "needs_model_selection": True,
            "has_code_review_plugin": has_plugin,
            "configured_model": cfg_model,
            "models": candidates,
            "models_source": "aliases+config",
            "saved_model": saved_model,
            "saved_mode": saved.get("mode", ""),
            "has_saved_model": bool(saved_model),
        }

    if "codex" in targets:
        bin_path = shutil.which("codex")
        cfg_path = codex_config or (Path.home() / ".codex" / "config.toml")
        cfg_models, cfg_provider = _read_codex_config(cfg_path)
        debug_models: list[str] = []
        if bin_path:
            code, out = _run_probe_cmd([bin_path, "debug", "models"], timeout=3)
            if code == 0:
                debug_models = _parse_codex_debug_models(out)
        saved = prefs["engines"]["codex"]
        saved_model = saved.get("model", "")
        merged = _dedupe([*cfg_models, *debug_models, saved_model])
        source = "config+debug" if (cfg_models or debug_models) else "fallback"
        if not merged:
            merged = list(DEFAULT_CODEX_MODELS)
        results["codex"] = {
            "available": bool(bin_path),
            "binary": bin_path or "",
            "needs_model_selection": True,
            "configured_provider": cfg_provider,
            "models": merged,
            "models_source": source,
            "saved_model": saved_model,
            "has_saved_model": bool(saved_model),
        }

    if "ocr" in targets:
        bin_path = shutil.which("ocr")
        version = ""
        providers: list[str] = []
        if bin_path:
            code_v, out_v = _run_probe_cmd([bin_path, "--version"], timeout=3)
            if code_v == 0:
                version = out_v
            code_p, out_p = _run_probe_cmd([bin_path, "llm", "providers"], timeout=5)
            if code_p == 0:
                providers = _parse_ocr_providers(out_p)
        saved = prefs["engines"]["ocr"]
        saved_model = saved.get("model", "")
        saved_provider = saved.get("provider", "")
        results["ocr"] = {
            "available": bool(bin_path),
            "binary": bin_path or "",
            "version": version,
            "needs_model_selection": True,
            "providers": providers,
            "models": _dedupe([saved_model]) if saved_model else [],
            "saved_provider": saved_provider,
            "saved_model": saved_model,
            "has_saved_model": bool(saved_model),
        }

    return {
        "prefs_path": str(prefs_path),
        "default_engine": prefs.get("default_engine", ""),
        "persist_default": prefs.get("persist_default"),
        "engines": results,
    }


def iter_git_roots(codes: Path, max_depth: int = 8) -> list[Path]:
    if not codes.exists():
        return []
    start = codes.resolve()
    skip_expr: list[str] = []
    for name in sorted(SKIP_DIRS - {".git"}):
        skip_expr += ["-name", name, "-o"]
    find_cmd = [
        "find",
        str(start),
        "-maxdepth",
        str(max_depth),
        "(",
        *skip_expr[:-1],
        ")",
        "-prune",
        "-o",
        "-name",
        ".git",
        "-prune",
        "-print",
    ]
    proc = subprocess.run(find_cmd, capture_output=True, text=True, check=False)
    if proc.returncode == 0 and proc.stdout.strip():
        return [Path(line).parent for line in proc.stdout.splitlines() if line.strip()]

    roots: list[Path] = []

    def walk(path: Path, depth: int) -> None:
        if (path / ".git").exists():
            roots.append(path)
        if depth >= max_depth:
            return
        try:
            entries = list(path.iterdir())
        except OSError:
            return
        for entry in entries:
            if not entry.is_dir() or entry.name in SKIP_DIRS:
                continue
            walk(entry, depth + 1)

    walk(start, 0)
    return roots


def find_git_root(path: Path) -> Path | None:
    cur = path if path.is_dir() else path.parent
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def resolve_repo(work_root: Path, raw: str) -> dict[str, Any]:
    name = raw.strip().rstrip("/")
    if not name:
        raise ReviewError("repo name is empty")

    workspace = work_root.resolve()
    if name in {"workspace", ".", str(workspace)}:
        if (workspace / ".git").exists():
            return {
                "input": name,
                "git_root": ".",
                "git_root_abs": str(workspace),
                "basename": workspace.name,
            }
        raise ReviewError("workspace root is not a Git repository; specify a repository path")

    path = Path(name).expanduser()
    if path.is_absolute():
        target = path
        if not target.exists():
            raise ReviewError(f"path does not exist: {name}")
    else:
        candidate = workspace / path
        target = candidate if candidate.exists() else None

    if target is not None:
        git_root = find_git_root(target.resolve())
        if git_root is None:
            raise ReviewError(f"no git root for: {name}")
        rel = _rel_display(work_root, git_root)
        return {
            "input": name,
            "git_root": rel,
            "git_root_abs": str(git_root),
            "basename": git_root.name,
        }

    roots = ([workspace] if (workspace / ".git").exists() else []) + iter_git_roots(workspace)
    exact = [p for p in roots if p.name == name]
    if len(exact) == 1:
        git_root = exact[0]
        return {
            "input": name,
            "git_root": _rel_display(work_root, git_root),
            "git_root_abs": str(git_root),
            "basename": git_root.name,
        }
    if len(exact) > 1:
        return {
            "input": name,
            "ambiguous": True,
            "candidates": [_rel_display(work_root, p) for p in exact],
        }

    suffix = [p for p in roots if p.as_posix().endswith("/" + name)]
    if len(suffix) == 1:
        git_root = suffix[0]
        return {
            "input": name,
            "git_root": _rel_display(work_root, git_root),
            "git_root_abs": str(git_root),
            "basename": git_root.name,
        }
    if suffix:
        return {
            "input": name,
            "ambiguous": True,
            "candidates": [_rel_display(work_root, p) for p in suffix],
        }
    raise ReviewError(f"repo not found under workspace root: {name}")


def _rel_display(work_root: Path, git_root: Path) -> str:
    try:
        rel = git_root.resolve().relative_to(work_root.resolve()).as_posix()
        return rel if rel != "." else "."
    except ValueError:
        return str(git_root)


def default_branch(git_root: Path) -> str:
    head = git(["symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"], git_root, check=False)
    if head:
        return head.replace("refs/remotes/origin/", "").strip()
    for name in ("main", "master", "develop"):
        exists = git(["rev-parse", "--verify", "--quiet", name], git_root, check=False)
        remote = git(["rev-parse", "--verify", "--quiet", f"origin/{name}"], git_root, check=False)
        if exists or remote:
            return name
    current = git(["rev-parse", "--abbrev-ref", "HEAD"], git_root, check=False)
    return current or "main"


def comparison_ref(git_root: Path, branch: str) -> str:
    remote = git(["rev-parse", "--verify", "--quiet", f"origin/{branch}"], git_root, check=False)
    if remote:
        return f"origin/{branch}"
    return branch


def detect_guidelines(git_root: Path) -> list[str]:
    return [rel for rel in GUIDELINE_CANDIDATES if (git_root / rel).is_file()]


def inspect_repo(work_root: Path, raw: str) -> dict[str, Any]:
    resolved = resolve_repo(work_root, raw)
    if resolved.get("ambiguous"):
        return resolved
    git_root = Path(resolved["git_root_abs"])
    branch = git(["rev-parse", "--abbrev-ref", "HEAD"], git_root, check=False) or "HEAD"
    porcelain = git(["status", "--porcelain"], git_root, check=False)
    dirty_paths = [line[3:] for line in porcelain.splitlines() if line.strip()]
    base = default_branch(git_root)
    cmp_ref = comparison_ref(git_root, base)
    ahead = 0
    if git(["rev-parse", "--verify", "--quiet", cmp_ref], git_root, check=False):
        count = git(["rev-list", "--count", f"{cmp_ref}..HEAD"], git_root, check=False)
        ahead = int(count or "0")
    dirty = bool(dirty_paths)
    on_default = branch == base or branch == f"origin/{base}"
    if dirty and ahead:
        recommendation = "ask"
        reason = "同时存在未提交改动和相对默认分支的提交，需用户确认审查范围"
    elif dirty:
        recommendation = "uncommitted"
        reason = "工作区有未提交改动（含 untracked）"
    elif ahead:
        recommendation = "default-branch"
        reason = f"当前分支相对 {cmp_ref} 超前 {ahead} 个提交"
    else:
        recommendation = "nothing"
        reason = "工作区干净且相对默认分支没有新提交"
    return {
        **resolved,
        "branch": branch,
        "default_branch": base,
        "comparison_ref": cmp_ref,
        "on_default": on_default,
        "dirty": dirty,
        "dirty_paths": dirty_paths,
        "ahead_of_default": ahead,
        "guidelines": detect_guidelines(git_root),
        "recommendation": recommendation,
        "reason": reason,
        "needs_confirm": True,
    }


def _exclude_reason(rel_path: str, is_binary: bool, extra_patterns: list[str]) -> str:
    name = Path(rel_path).name
    if is_binary or Path(rel_path).suffix.lower() in BINARY_EXTS:
        return "binary/media"
    if name in LOCKFILE_NAMES:
        return "lockfile"
    for pat in GENERATED_PATTERNS:
        if fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(rel_path, pat):
            return "generated"
    for pat in extra_patterns:
        if fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(name, pat):
            return f"excluded({pat})"
    return ""


def _parse_numstat(output: str) -> dict[str, tuple[int, int, bool]]:
    stats: dict[str, tuple[int, int, bool]] = {}
    for line in output.splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 3:
            continue
        add_s, del_s, path_s = parts
        if " => " in path_s:
            path_s = path_s.split(" => ")[-1].rstrip("}")
        is_bin = add_s == "-" or del_s == "-"
        ins = 0 if is_bin else int(add_s or "0")
        dels = 0 if is_bin else int(del_s or "0")
        stats[path_s] = (ins, dels, is_bin)
    return stats


def _parse_name_status(output: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        code = parts[0].strip()
        path_s = parts[-1].strip()
        statuses[path_s] = code[0] if code else "M"
    return statuses


def _is_binary_file(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return True
    return b"\x00" in chunk


def _count_lines(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return 0


def preview_changes(
    work_root: Path,
    raw_repo: str,
    *,
    mode: str,
    commit: str = "",
    from_ref: str = "",
    to_ref: str = "",
    exclude: str = "",
) -> dict[str, Any]:
    resolved = resolve_repo(work_root, raw_repo)
    if resolved.get("ambiguous"):
        return resolved
    git_root = Path(resolved["git_root_abs"])
    extra_patterns = [p.strip() for p in exclude.split(",") if p.strip()]
    entries: list[dict[str, Any]] = []
    meta_refs: dict[str, str] = {"from": "", "to": "", "commit": "", "merge_base": ""}

    if mode == "uncommitted":
        has_head = bool(git(["rev-parse", "--verify", "--quiet", "HEAD"], git_root, check=False))
        diff_target = ["HEAD"] if has_head else ["--cached"]
        ns_out = git(["diff", *GIT_DIFF_ARGS, "--numstat", *diff_target], git_root, check=False, no_pager=True)
        st_out = git(["diff", *GIT_DIFF_ARGS, "--name-status", *diff_target], git_root, check=False, no_pager=True)
        if not has_head and not ns_out:
            ns_out = git(["diff", *GIT_DIFF_ARGS, "--numstat"], git_root, check=False, no_pager=True)
            st_out = git(["diff", *GIT_DIFF_ARGS, "--name-status"], git_root, check=False, no_pager=True)
        numstats = _parse_numstat(ns_out)
        statuses = _parse_name_status(st_out)
        for p in sorted(set(numstats) | set(statuses)):
            ins, dels, is_bin = numstats.get(p, (0, 0, False))
            entries.append({"path": p, "status": statuses.get(p, "M"), "insertions": ins, "deletions": dels, "binary": is_bin})
        untracked = git(["ls-files", "--others", "--exclude-standard"], git_root, check=False, no_pager=True)
        for rel in untracked.splitlines():
            rel = rel.strip()
            if not rel:
                continue
            fp = git_root / rel
            is_bin = _is_binary_file(fp)
            lines = 0 if is_bin else _count_lines(fp)
            entries.append({"path": rel, "status": "untracked", "insertions": lines, "deletions": 0, "binary": is_bin})
    elif mode == "commit":
        if not commit.strip():
            raise ReviewError("mode=commit requires --commit <hash>")
        c_ref = commit.strip()
        meta_refs["commit"] = git(["rev-parse", "--short", c_ref], git_root, check=True)
        ns_out = git(["show", *GIT_DIFF_ARGS, "--numstat", "--format=", c_ref], git_root, check=True, no_pager=True)
        st_out = git(["show", *GIT_DIFF_ARGS, "--name-status", "--format=", c_ref], git_root, check=True, no_pager=True)
        numstats = _parse_numstat(ns_out)
        statuses = _parse_name_status(st_out)
        for p in sorted(set(numstats) | set(statuses)):
            ins, dels, is_bin = numstats.get(p, (0, 0, False))
            entries.append({"path": p, "status": statuses.get(p, "M"), "insertions": ins, "deletions": dels, "binary": is_bin})
    elif mode in ("default-branch", "range"):
        base = default_branch(git_root)
        f_ref = from_ref.strip() or comparison_ref(git_root, base)
        t_ref = to_ref.strip() or "HEAD"
        mb = git(["merge-base", f_ref, t_ref], git_root, check=False) or f_ref
        meta_refs["from"] = f_ref
        meta_refs["to"] = t_ref
        meta_refs["merge_base"] = mb
        diff_range = f"{mb}..{t_ref}"
        ns_out = git(["diff", *GIT_DIFF_ARGS, "--numstat", diff_range], git_root, check=True, no_pager=True)
        st_out = git(["diff", *GIT_DIFF_ARGS, "--name-status", diff_range], git_root, check=True, no_pager=True)
        numstats = _parse_numstat(ns_out)
        statuses = _parse_name_status(st_out)
        for p in sorted(set(numstats) | set(statuses)):
            ins, dels, is_bin = numstats.get(p, (0, 0, False))
            entries.append({"path": p, "status": statuses.get(p, "M"), "insertions": ins, "deletions": dels, "binary": is_bin})
    else:
        raise ReviewError(f"unsupported preview mode: {mode}")

    reviewable: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for item in entries:
        reason = _exclude_reason(item["path"], item["binary"], extra_patterns)
        clean = {
            "path": item["path"],
            "status": item["status"],
            "insertions": item["insertions"],
            "deletions": item["deletions"],
        }
        if reason:
            excluded.append({**clean, "reason": reason})
        else:
            reviewable.append(clean)

    return {
        **resolved,
        "mode": mode,
        **meta_refs,
        "guidelines": detect_guidelines(git_root),
        "reviewable_files": reviewable,
        "excluded_files": excluded,
        "summary": {
            "reviewable": len(reviewable),
            "excluded": len(excluded),
            "insertions": sum(f["insertions"] for f in reviewable),
            "deletions": sum(f["deletions"] for f in reviewable),
        },
    }


def parse_mr_url(url: str) -> dict[str, Any]:
    text = url.strip()
    m = GITLAB_MR.match(text) or GITLAB_MR_ALT.match(text)
    if m:
        project = m.group("project").strip("/")
        basename = project.rsplit("/", 1)[-1]
        return {
            "kind": "gitlab",
            "host": m.group("host"),
            "project": project,
            "iid": int(m.group("iid")),
            "repo_hint": basename,
            "url": text,
        }
    m = GITHUB_PR.match(text)
    if m:
        return {
            "kind": "github",
            "host": m.group("host"),
            "project": f"{m.group('owner')}/{m.group('repo')}",
            "iid": int(m.group("iid")),
            "repo_hint": m.group("repo"),
            "url": text,
        }
    raise ReviewError(f"unsupported merge request URL: {url}")


def slugify(text: str, max_len: int = 48) -> str:
    out = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (out or "change")[:max_len].rstrip("-")


def change_name(*, repo_basename: str, mode: str, branch: str = "", mr_iid: int | None = None, title: str = "", commit: str = "") -> str:
    base = slugify(repo_basename, 32)
    if mode == "mr" and mr_iid is not None:
        extra = slugify(title, 24) if title else ""
        return f"{base}-mr-{mr_iid}" + (f"-{extra}" if extra else "")
    if mode == "commit" and commit:
        return f"{base}-commit-{slugify(commit, 12)}"
    if mode == "uncommitted":
        return f"{base}-{slugify(branch or 'wip', 24)}-uncommitted"
    if mode == "default-branch":
        return f"{base}-{slugify(branch or 'branch', 24)}"
    return f"{base}-{slugify(mode or 'review', 24)}"


def classify_priority(content: str) -> str:
    if P0_RE.search(content or ""):
        return "P0"
    if P1_RE.search(content or ""):
        return "P1"
    if P2_RE.search(content or ""):
        return "P2"
    return "P3"


def _line_ref(comment: dict[str, Any]) -> str:
    start = int(comment.get("start_line") or 0)
    end = int(comment.get("end_line") or 0)
    path = comment.get("path") or "unknown"
    if start <= 0 and end <= 0:
        return path
    if end > start:
        return f"{path}:{start}-{end}"
    return f"{path}:{start or end}"


def _title(comment: dict[str, Any]) -> str:
    content = (comment.get("content") or "").strip().splitlines()
    if not content:
        return "Untitled finding"
    first = content[0].strip()
    return first[:120] + ("…" if len(first) > 120 else "")


def normalize_comments(result: dict[str, Any]) -> list[dict[str, Any]]:
    comments = list(result.get("comments") or [])
    out = []
    for item in comments:
        comment = dict(item)
        pri = str(comment.get("priority") or "").upper()
        if pri not in PRIORITY_ORDER:
            sev = str(comment.get("severity") or "").strip().lower()
            if sev in SEVERITY_TO_PRIORITY:
                comment["priority"] = SEVERITY_TO_PRIORITY[sev]
            else:
                comment["priority"] = classify_priority(str(comment.get("content") or ""))
        else:
            comment["priority"] = pri
        out.append(comment)
    out.sort(key=lambda c: (PRIORITY_ORDER.index(c["priority"]), c.get("path") or "", int(c.get("start_line") or 0)))
    return out


def counts(comments: list[dict[str, Any]]) -> dict[str, int]:
    data = {k: 0 for k in PRIORITY_ORDER}
    for comment in comments:
        data[comment["priority"]] += 1
    return data


def _extract_engine_llm(meta: dict[str, Any], result: dict[str, Any]) -> tuple[str, str, str]:
    engine = str(result.get("engine") or meta.get("engine") or "").strip()
    llm = result.get("llm") or {}
    provider = str(llm.get("provider") or meta.get("provider") or "").strip()
    model = str(llm.get("model") or meta.get("model") or "").strip()
    return engine, provider, model


def render_full(meta: dict[str, Any], result: dict[str, Any], comments: list[dict[str, Any]]) -> str:
    tally = counts(comments)
    tally_line = " / ".join(f"{k}={tally[k]}" for k in PRIORITY_ORDER if tally[k] or k in ("P0", "P1", "P2", "P3"))
    engine, provider, model = _extract_engine_llm(meta, result)
    lines = [
        "---",
        f"repo: {meta.get('repo', '')}",
        f"mode: {meta.get('mode', '')}",
        f"date: {meta.get('date', '')}",
        f"change_name: {meta.get('change_name', '')}",
        f"branch: {meta.get('branch', '')}",
        f"commit: {meta.get('commit', '')}",
        f"from: {meta.get('from', '')}",
        f"to: {meta.get('to', '')}",
        f"mr: {meta.get('mr_url', '')}",
        f"engine: {engine}",
        f"provider: {provider}",
        f"model: {model}",
        f"session_id: {result.get('session_id', '')}",
        f"status: {result.get('status', '')}",
        "---",
        "",
        f"# Code Review · {meta.get('change_name', '')}",
        "",
        "## Meta",
        "",
        f"- 仓库：`{meta.get('repo', '')}`",
        f"- 范围：`{meta.get('mode', '')}` `{meta.get('from', '')}` → `{meta.get('to', '')}`",
        f"- 分支：`{meta.get('branch', '')}`（默认 `{meta.get('default_branch', '')}`）",
    ]
    if meta.get("commit"):
        lines.append(f"- Commit：`{meta['commit']}`")
    if meta.get("mr_url"):
        lines.append(f"- Merge Request：{meta['mr_url']}")
    if engine:
        lines.append(f"- 引擎：`{engine}`")
    summary = result.get("summary") or {}
    if summary:
        lines.append(
            f"- 扫描：files={summary.get('files_reviewed', '?')} comments={summary.get('comments', len(comments))} "
            f"elapsed={summary.get('elapsed', '?')} session=`{result.get('session_id', '')}`"
        )
    if provider and model:
        lines.append(f"- LLM：`{provider}` / `{model}`")
    elif provider or model:
        lines.append(f"- LLM：`{provider or model}`")
    guidelines = meta.get("guidelines") or []
    if guidelines:
        lines.append(f"- 项目底线：{', '.join(f'`{g}`' for g in guidelines)}")
    if result.get("message"):
        lines.append(f"- Message：{result['message']}")
    lines += ["", "## 统计", "", tally_line, "", "## Findings（完整）", ""]
    if not comments:
        lines.append("No findings.")
    else:
        for pri in PRIORITY_ORDER:
            group = [c for c in comments if c["priority"] == pri]
            if not group:
                continue
            lines += [f"### {pri}", ""]
            for i, comment in enumerate(group, 1):
                lines += [
                    f"#### {i}. {_title(comment)}",
                    "",
                    f"- 位置：`{_line_ref(comment)}`",
                    f"- 优先级：{pri}",
                    "",
                    comment.get("content") or "",
                    "",
                ]
                if comment.get("existing_code"):
                    lines += ["**现有代码**", "", "```", str(comment["existing_code"]).rstrip(), "```", ""]
                if comment.get("suggestion_code"):
                    lines += ["**建议改法**", "", "```", str(comment["suggestion_code"]).rstrip(), "```", ""]
                if comment.get("thinking"):
                    lines += ["**推理**", "", str(comment["thinking"]).rstrip(), ""]
    warnings = result.get("warnings") or []
    if warnings:
        lines += ["## Warnings", ""]
        for item in warnings:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_summary(
    meta: dict[str, Any],
    comments: list[dict[str, Any]],
    doc_path: str = "",
    result: dict[str, Any] | None = None,
) -> str:
    tally = counts(comments)
    tally_line = " ".join(f"{k}={tally[k]}" for k in PRIORITY_ORDER if tally[k] or k in ("P0", "P1", "P2", "P3"))
    engine, provider, model = _extract_engine_llm(meta, result or {})
    lines = [
        f"## Review 总结 · {meta.get('change_name', '')}",
        "",
        f"范围：`{meta.get('repo', '')}` / `{meta.get('mode', '')}` `{meta.get('from', '')}` → `{meta.get('to', '')}`",
    ]
    if engine or model or provider:
        parts = [p for p in (engine, provider if provider != engine else "", model) if p]
        lines.append(f"方案：`{' / '.join(parts)}`")
    lines.append(f"结论：{tally_line}")
    if doc_path:
        lines.append(f"完整文档：`{doc_path}`")
    lines.append("")
    if not comments:
        lines.append("No findings.")
        return "\n".join(lines).rstrip() + "\n"
    for pri in PRIORITY_ORDER:
        group = [c for c in comments if c["priority"] == pri]
        if not group:
            continue
        lines.append(f"### {pri}")
        lines.append("")
        for comment in group:
            lines.append(f"- [{pri}] {_title(comment)} — `{_line_ref(comment)}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def update_index(reviews_root: Path, meta: dict[str, Any], tally: dict[str, int], doc_rel: str) -> None:
    index = reviews_root / "INDEX.md"
    header = (
        "# Code reviews\n\n"
        "| 日期 | change | 仓库 | 范围 | 引擎 | P0 | P1 | P2 | P3 | 文档 |\n"
        "|------|--------|------|------|------|----|----|----|----|------|\n"
    )
    engine = str(meta.get("engine") or "-")
    row = (
        f"| {meta.get('date', '')} | {meta.get('change_name', '')} | `{meta.get('repo', '')}` | "
        f"{meta.get('mode', '')} | {engine} | {tally.get('P0', 0)} | {tally.get('P1', 0)} | {tally.get('P2', 0)} | "
        f"{tally.get('P3', 0)} | [{meta.get('change_name', '')}]({doc_rel}) |"
    )
    if not index.exists():
        index.write_text(header + row + "\n", encoding="utf-8")
        return
    text = index.read_text(encoding="utf-8")
    lines = text.splitlines()
    key = f"| {meta.get('date', '')} | {meta.get('change_name', '')} |"
    kept = [ln for ln in lines if not ln.startswith(key)]
    if len(kept) < 3:
        index.write_text(header + row + "\n", encoding="utf-8")
        return
    kept.append(row)
    index.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")


def render_result(result: dict[str, Any], meta: dict[str, Any], fmt: str = "summary") -> dict[str, Any]:
    comments = normalize_comments(result)
    day = meta.get("date") or date.today().isoformat()
    name = meta.get("change_name") or change_name(
        repo_basename=Path(str(meta.get("repo") or "repo")).name,
        mode=str(meta.get("mode") or "review"),
        branch=str(meta.get("branch") or ""),
        mr_iid=meta.get("mr_iid"),
        title=str(meta.get("title") or ""),
        commit=str(meta.get("commit") or ""),
    )
    merged_meta = {**meta, "date": day, "change_name": name}
    tally = counts(comments)
    if fmt == "full":
        output = render_full(merged_meta, result, comments)
    else:
        output = render_summary(merged_meta, comments, "", result)
    return {
        "format": fmt,
        "change_name": name,
        "date": day,
        "counts": tally,
        "output": output,
        "summary": render_summary(merged_meta, comments, "", result),
    }


def write_review(
    work_root: Path,
    result: dict[str, Any],
    meta: dict[str, Any],
    plan_text: str = "",
) -> dict[str, Any]:
    comments = normalize_comments(result)
    day = meta.get("date") or date.today().isoformat()
    name = meta.get("change_name") or change_name(
        repo_basename=Path(str(meta.get("repo") or "repo")).name,
        mode=str(meta.get("mode") or "review"),
        branch=str(meta.get("branch") or ""),
        mr_iid=meta.get("mr_iid"),
        title=str(meta.get("title") or ""),
        commit=str(meta.get("commit") or ""),
    )
    engine, provider, model = _extract_engine_llm(meta, result)
    merged_meta = {
        **meta,
        "date": day,
        "change_name": name,
        "engine": engine,
        "provider": provider,
        "model": model,
    }
    out_dir = work_root / "docs" / "reviews" / day / name
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw.json"
    review_path = out_dir / "review.md"
    raw_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    review_path.write_text(render_full(merged_meta, result, comments), encoding="utf-8")
    doc_rel = f"docs/reviews/{day}/{name}/review.md"
    update_index(work_root / "docs" / "reviews", merged_meta, counts(comments), f"{day}/{name}/review.md")
    summary = render_summary(merged_meta, comments, doc_rel, result)
    (out_dir / "summary.md").write_text(summary, encoding="utf-8")

    plan_content = plan_text.strip() or str(meta.get("plan_markdown") or "").strip()
    plan_rel = ""
    if plan_content:
        (out_dir / "plan.md").write_text(plan_content + "\n", encoding="utf-8")
        plan_rel = f"docs/reviews/{day}/{name}/plan.md"

    payload: dict[str, Any] = {
        "out_dir": str(out_dir.relative_to(work_root)),
        "review": doc_rel,
        "raw": f"docs/reviews/{day}/{name}/raw.json",
        "summary": summary,
        "counts": counts(comments),
        "change_name": name,
        "date": day,
    }
    if plan_rel:
        payload["plan"] = plan_rel
    return payload


def _load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def emit(payload: dict[str, Any], code: int = 0) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reviewctl")
    parser.add_argument("--root", default="", help="work workspace root")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_resolve = sub.add_parser("resolve-repo")
    p_resolve.add_argument("repo")

    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("--repo", required=True)

    p_preview = sub.add_parser("preview")
    p_preview.add_argument("--repo", required=True)
    p_preview.add_argument("--mode", required=True, choices=["uncommitted", "default-branch", "commit", "range"])
    p_preview.add_argument("--commit", default="")
    p_preview.add_argument("--from", dest="from_ref", default="")
    p_preview.add_argument("--to", dest="to_ref", default="")
    p_preview.add_argument("--exclude", default="")

    p_probe = sub.add_parser("probe")
    p_probe.add_argument("--engine", default="")
    p_probe.add_argument("--prefs", default="")

    p_prefs = sub.add_parser("prefs")
    prefs_sub = p_prefs.add_subparsers(dest="prefs_cmd", required=True)
    p_pg = prefs_sub.add_parser("get")
    p_pg.add_argument("--engine", default="")
    p_pg.add_argument("--prefs", default="")
    p_ps = prefs_sub.add_parser("set")
    p_ps.add_argument("--engine", default="")
    p_ps.add_argument("--model", default="")
    p_ps.add_argument("--provider", default="")
    p_ps.add_argument("--mode", default="")
    p_ps.add_argument("--set-default-engine", action="store_true")
    p_ps.add_argument("--persist-default", default="")
    p_ps.add_argument("--prefs", default="")
    p_pc = prefs_sub.add_parser("clear")
    p_pc.add_argument("--engine", default="")
    p_pc.add_argument("--prefs", default="")

    p_mr = sub.add_parser("parse-mr")
    p_mr.add_argument("--url", required=True)

    p_name = sub.add_parser("change-name")
    p_name.add_argument("--repo-basename", required=True)
    p_name.add_argument("--mode", required=True)
    p_name.add_argument("--branch", default="")
    p_name.add_argument("--mr-iid", type=int, default=None)
    p_name.add_argument("--title", default="")
    p_name.add_argument("--commit", default="")

    p_render = sub.add_parser("render")
    p_render.add_argument("--result-json", "--ocr-json", dest="result_json", required=True)
    p_render.add_argument("--meta-json", required=True)
    p_render.add_argument("--format", default="summary", choices=["summary", "full"])

    p_write = sub.add_parser("write")
    p_write.add_argument("--result-json", "--ocr-json", dest="result_json", required=True)
    p_write.add_argument("--meta-json", required=True)
    p_write.add_argument("--plan-md", default="")

    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    try:
        if args.cmd == "resolve-repo":
            payload = resolve_repo(root, args.repo)
            if payload.get("ambiguous"):
                return emit({"ok": False, **payload}, 1)
            return emit({"ok": True, **payload})
        if args.cmd == "inspect":
            payload = inspect_repo(root, args.repo)
            if payload.get("ambiguous"):
                return emit({"ok": False, **payload}, 1)
            return emit({"ok": True, **payload})
        if args.cmd == "preview":
            payload = preview_changes(
                root,
                args.repo,
                mode=args.mode,
                commit=args.commit,
                from_ref=args.from_ref,
                to_ref=args.to_ref,
                exclude=args.exclude,
            )
            if payload.get("ambiguous"):
                return emit({"ok": False, **payload}, 1)
            return emit({"ok": True, **payload})
        if args.cmd == "probe":
            return emit({"ok": True, **probe_engines(default_prefs_path(args.prefs), engine=args.engine)})
        if args.cmd == "prefs":
            ppath = default_prefs_path(args.prefs)
            if args.prefs_cmd == "get":
                data = load_prefs(ppath)
                if args.engine:
                    if args.engine not in ALLOWED_ENGINES:
                        raise ReviewError(f"unsupported engine: {args.engine}")
                    return emit({"ok": True, "prefs_path": str(ppath), "engine": args.engine, "data": data["engines"].get(args.engine, {})})
                return emit({"ok": True, "prefs_path": str(ppath), "data": data})
            if args.prefs_cmd == "set":
                updated = set_prefs(
                    ppath,
                    engine=args.engine,
                    model=args.model,
                    provider=args.provider,
                    mode=args.mode,
                    set_default_engine=args.set_default_engine,
                    persist_default=args.persist_default,
                )
                return emit({"ok": True, "prefs_path": str(ppath), "data": updated})
            if args.prefs_cmd == "clear":
                updated = clear_prefs(ppath, engine=args.engine)
                return emit({"ok": True, "prefs_path": str(ppath), "data": updated})
        if args.cmd == "parse-mr":
            return emit({"ok": True, **parse_mr_url(args.url)})
        if args.cmd == "change-name":
            name = change_name(
                repo_basename=args.repo_basename,
                mode=args.mode,
                branch=args.branch,
                mr_iid=args.mr_iid,
                title=args.title,
                commit=args.commit,
            )
            return emit({"ok": True, "change_name": name})
        if args.cmd == "render":
            res = render_result(_load_json(args.result_json), _load_json(args.meta_json), fmt=args.format)
            return emit({"ok": True, **res})
        if args.cmd == "write":
            plan_text = Path(args.plan_md).read_text(encoding="utf-8") if args.plan_md else ""
            result = write_review(root, _load_json(args.result_json), _load_json(args.meta_json), plan_text=plan_text)
            return emit({"ok": True, **result})
        raise ReviewError(f"unknown command: {args.cmd}")
    except ReviewError as exc:
        return emit({"ok": False, "error": str(exc)}, 1)


if __name__ == "__main__":
    raise SystemExit(main())
