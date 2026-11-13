#!/usr/bin/env python3
"""Maintain a small, linked project atlas using only the Python standard library."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

COMMANDS = {"init", "status", "build", "check", "verify"}
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^)'\"]*['\"])?\)")
TOKEN_RE = re.compile(
    r"(`[^`]+`|!\[[^\]]*\]\([^)]+\)|\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*)"
)
HTML_URL_RE = re.compile(r"\b(href|src)=([\"'])(.*?)\2", re.IGNORECASE)


class AtlasError(Exception):
    pass


@dataclass
class Page:
    path: Path
    rel: str
    meta: dict[str, object]
    body: str
    text: str


def emit(data: dict[str, object], code: int = 0) -> int:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    return code


def read_config(root: Path) -> dict[str, object]:
    path = root / ".atlas.json"
    if not path.is_file():
        raise AtlasError(f"missing atlas config: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AtlasError(f"invalid atlas config: {exc}") from exc
    if config.get("version") != 1 or not isinstance(config.get("source"), str):
        raise AtlasError("atlas config requires version: 1 and a source path")
    return config


def source_root(root: Path) -> Path:
    config = read_config(root)
    source = Path(str(config["source"]))
    if not source.is_absolute():
        source = root / source
    source = source.resolve()
    if not source.is_dir():
        raise AtlasError(f"source directory does not exist: {source}")
    return source


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    if value in {"null", "~"}:
        return ""
    return value.strip("'\"")


def parse_page(path: Path, root: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(root).as_posix()
    if not text.startswith("---\n"):
        return Page(path, rel, {}, text, text)
    end = text.find("\n---\n", 4)
    if end < 0:
        return Page(path, rel, {}, text, text)
    meta: dict[str, object] = {}
    active_list: str | None = None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and active_list:
            value = meta.get(active_list)
            if not isinstance(value, list):
                value = []
                meta[active_list] = value
            value.append(line[4:].strip().strip("'\""))
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not match:
            continue
        key, raw = match.group(1), match.group(2) or ""
        meta[key] = parse_scalar(raw)
        active_list = key if raw == "" else None
    return Page(path, rel, meta, text[end + 5 :], text)


def load_pages(root: Path) -> tuple[list[Page], list[str]]:
    paths = []
    errors = []
    if (root / "index.md").is_file():
        paths.append(root / "index.md")
    if (root / "domains").is_dir():
        paths.extend(sorted((root / "domains").rglob("*.md")))
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if "_site" in rel.parts or "assets" in rel.parts or path in paths:
            continue
        errors.append(f"unexpected_page:{rel.as_posix()}")
    pages = [parse_page(path, root) for path in paths]
    for page in pages:
        if not page.meta:
            errors.append(f"frontmatter_missing:{page.rel}")
    return pages, errors


def expected_level(page: Page) -> int | None:
    if page.rel == "index.md":
        return 0
    parts = Path(page.rel).parts
    if len(parts) == 3 and parts[0] == "domains" and parts[2] == "index.md":
        return 1
    if len(parts) == 3 and parts[0] == "domains" and parts[2] != "index.md":
        return 2
    return None


def validate_structure(pages: list[Page], load_errors: list[str]) -> tuple[list[str], list[str]]:
    errors = list(load_errors)
    warnings = []
    by_rel = {page.rel: page for page in pages}
    if "index.md" not in by_rel:
        errors.append("missing:index.md")
    for page in pages:
        level = expected_level(page)
        if level is None:
            errors.append(f"invalid_pyramid_path:{page.rel}")
            continue
        if page.meta.get("level") != str(level):
            errors.append(f"level_mismatch:{page.rel}:expected_{level}")
        if not str(page.meta.get("title", "")).strip():
            errors.append(f"title_missing:{page.rel}")
        status = page.meta.get("status")
        if status not in {"draft", "verified"}:
            errors.append(f"status_invalid:{page.rel}")
        elif status == "draft":
            warnings.append(f"draft:{page.rel}")
        sources = page.meta.get("sources", [])
        if not isinstance(sources, list):
            errors.append(f"sources_invalid:{page.rel}")
        elif level > 0 and status == "verified" and not sources:
            errors.append(f"sources_missing:{page.rel}")
    adjacency = markdown_adjacency(pages, root=pages[0].path.parent if pages else Path("."))
    root_links = adjacency.get("index.md", set())
    for page in pages:
        level = expected_level(page)
        if level == 1:
            if page.rel not in root_links:
                errors.append(f"domain_not_linked_from_root:{page.rel}")
            if "index.md" not in adjacency.get(page.rel, set()):
                errors.append(f"parent_link_missing:{page.rel}:index.md")
        elif level == 2:
            parent = str(Path(page.rel).parent / "index.md").replace("\\", "/")
            if parent not in by_rel:
                errors.append(f"domain_index_missing:{page.rel}")
            else:
                if page.rel not in adjacency.get(parent, set()):
                    errors.append(f"topic_not_linked_from_domain:{page.rel}")
                if parent not in adjacency.get(page.rel, set()):
                    errors.append(f"parent_link_missing:{page.rel}:{parent}")
    return errors, warnings


def local_target(base: Path, raw_url: str, root: Path) -> tuple[Path | None, str]:
    parts = urlsplit(raw_url)
    if parts.scheme or parts.netloc or not parts.path:
        return None, parts.fragment
    target = (base / unquote(parts.path)).resolve()
    resolved_root = root.resolve()
    if target != resolved_root and resolved_root not in target.parents:
        raise AtlasError(f"link_escapes_atlas:{raw_url}")
    return target, parts.fragment


def markdown_adjacency(pages: list[Page], root: Path) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = {}
    for page in pages:
        linked = set()
        for raw_url in LINK_RE.findall(page.body):
            try:
                target, _ = local_target(page.path.parent, raw_url, root)
            except AtlasError:
                continue
            if target is not None and target.suffix == ".md":
                try:
                    linked.add(target.relative_to(root.resolve()).as_posix())
                except ValueError:
                    pass
        adjacency[page.rel] = linked
    return adjacency


def iter_static_html(root: Path):
    for directory in (root / "assets", root / "diagrams"):
        if directory.is_dir():
            yield from sorted(directory.rglob("*.html"))


def validate_links(pages: list[Page], root: Path) -> list[str]:
    errors = []
    sources: list[tuple[Path, str, str]] = []
    for page in pages:
        sources.extend((page.path, raw_url, page.rel) for raw_url in LINK_RE.findall(page.body))
    for path in iter_static_html(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        sources.extend((path, match.group(3), rel) for match in HTML_URL_RE.finditer(text))
    for path, raw_url, rel in sources:
        try:
            target, _ = local_target(path.parent, raw_url, root)
        except AtlasError:
            errors.append(f"link_escapes_atlas:{rel}:{raw_url}")
            continue
        if target is not None and not target.exists():
            errors.append(f"broken_link:{rel}:{raw_url}")
    return errors


def linked_archify_diagrams(page: Page, root: Path) -> list[Path]:
    diagrams = []
    diagram_root = (root / "diagrams").resolve()
    for raw_url in LINK_RE.findall(page.body):
        try:
            target, _ = local_target(page.path.parent, raw_url, root)
        except AtlasError:
            continue
        if target is None or target.suffix.lower() != ".html":
            continue
        if target == diagram_root or diagram_root in target.parents:
            diagrams.append(target)
    return diagrams


def file_sha256(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def read_receipt(path: Path, kind: str, rel: str, errors: list[str]) -> dict[str, object]:
    if not path.is_file():
        errors.append(f"diagram_{kind}_missing:{rel}")
        return {}
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError):
        errors.append(f"diagram_{kind}_invalid:{rel}")
        return {}
    if not isinstance(receipt, dict):
        errors.append(f"diagram_{kind}_invalid:{rel}")
        return {}
    return receipt


def validate_receipt_bindings(
    receipt: dict[str, object], source: Path, artifact: Path, rel: str, kind: str, errors: list[str]
) -> None:
    for key, path in (("specification", source), ("artifact", artifact)):
        binding = receipt.get(key)
        if not isinstance(binding, dict):
            errors.append(f"diagram_{kind}_{key}_missing:{rel}")
            continue
        digest, size = file_sha256(path)
        if binding.get("sha256") != digest or binding.get("bytes") != size:
            errors.append(f"diagram_{key}_mismatch:{rel}")


def validate_archify_diagrams(pages: list[Page], root: Path) -> list[str]:
    errors = []
    artifacts = {artifact for page in pages for artifact in linked_archify_diagrams(page, root)}
    for artifact in sorted(artifacts):
        rel = artifact.relative_to(root.resolve()).as_posix()
        for path, code in (
            (artifact.with_suffix(".delivery-pending.json"), "delivery_pending"),
            (artifact.with_suffix(".delivery-lock.json"), "delivery_lock"),
            (artifact.parent / ".archify-delivery-lock.json", "delivery_lock"),
        ):
            if path.exists():
                errors.append(f"diagram_{code}:{rel}")
        if not artifact.is_file():
            errors.append(f"diagram_html_missing:{rel}")
            continue
        source = artifact.with_suffix(".json")
        if not source.is_file():
            errors.append(f"diagram_source_missing:{rel}")
            continue
        delivery = read_receipt(artifact.with_suffix(".delivery.json"), "delivery", rel, errors)
        if delivery and (delivery.get("status") != "current" or delivery.get("command") != "deliver"):
            errors.append(f"diagram_delivery_invalid:{rel}")
        if delivery:
            validate_receipt_bindings(delivery, source, artifact, rel, "delivery", errors)
        summary = read_receipt(artifact.with_suffix(".finalize-summary.json"), "finalize", rel, errors)
        if summary and (summary.get("ok") is not True or summary.get("command") != "finalize"):
            errors.append(f"diagram_finalize_invalid:{rel}")
        if summary:
            validate_receipt_bindings(summary, source, artifact, rel, "finalize", errors)
    return sorted(set(errors))


def affected_archify_diagrams(pages: list[Page], states: list[dict[str, object]], root: Path) -> list[str]:
    stale = {str(state["page"]) for state in states if state["stale"]}
    return sorted(
        {
            artifact.relative_to(root.resolve()).as_posix()
            for page in pages
            if page.rel in stale
            for artifact in linked_archify_diagrams(page, root)
        }
    )


def safe_source_spec(spec: str) -> str:
    normalized = spec.replace("\\", "/").removeprefix("./")
    path = Path(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise AtlasError(f"invalid source mapping: {spec}")
    return normalized


def ignored(path: Path, source: Path, atlas: Path) -> bool:
    try:
        rel = path.relative_to(source)
    except ValueError:
        return True
    if any(part in IGNORED_DIRS for part in rel.parts):
        return True
    resolved = path.resolve()
    return resolved == atlas.resolve() or atlas.resolve() in resolved.parents


def expand_source(spec: str, source: Path, atlas: Path) -> tuple[list[Path], bool]:
    spec = safe_source_spec(spec)
    candidate = source / spec
    paths: list[Path] = []
    if any(char in spec for char in "*?["):
        matches = list(source.glob(spec))
        if not matches:
            return [], True
        for match in matches:
            if match.is_dir():
                paths.extend(p for p in match.rglob("*") if p.is_file())
            elif match.is_file():
                paths.append(match)
    elif candidate.is_dir():
        paths.extend(p for p in candidate.rglob("*") if p.is_file())
    elif candidate.is_file():
        paths.append(candidate)
    else:
        return [], True
    return [p for p in paths if not ignored(p, source, atlas)], False


def source_snapshot(page: Page, source: Path, atlas: Path) -> tuple[str, list[str], list[str]]:
    specs = page.meta.get("sources", [])
    if not isinstance(specs, list):
        return "", [], []
    files: dict[str, Path] = {}
    missing = []
    for raw_spec in specs:
        spec = str(raw_spec)
        matches, absent = expand_source(spec, source, atlas)
        if absent:
            missing.append(spec)
        for path in matches:
            files[path.relative_to(source).as_posix()] = path
    digest = hashlib.sha256()
    for rel in sorted(files):
        path = files[rel]
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    for spec in sorted(missing):
        digest.update(f"MISSING:{spec}\0".encode("utf-8"))
    return digest.hexdigest(), missing, sorted(files)


def freshness(pages: list[Page], source: Path, atlas: Path) -> list[dict[str, object]]:
    result = []
    for page in pages:
        sources = page.meta.get("sources", [])
        if not isinstance(sources, list):
            sources = []
        digest, missing, files = source_snapshot(page, source, atlas)
        recorded = str(page.meta.get("source_digest", ""))
        stale = bool(sources) and digest != recorded
        result.append(
            {
                "page": page.rel,
                "status": page.meta.get("status", "invalid"),
                "stale": stale,
                "sources": sources,
                "missing_sources": missing,
                "mapped_files": len(files),
                "current_digest": digest if sources else "",
            }
        )
    return result


def command_init(args: argparse.Namespace) -> int:
    source = Path(args.source).resolve()
    root = Path(args.root).resolve() if args.root else source / "docs" / "atlas"
    if not source.is_dir():
        raise AtlasError(f"source directory does not exist: {source}")
    if (root / ".atlas.json").exists():
        raise AtlasError(f"atlas already initialized: {root}")
    if root.exists() and any(root.iterdir()):
        raise AtlasError(f"refusing to initialize non-empty directory: {root}")
    if not args.confirm:
        return emit(
            {
                "ok": False,
                "confirmation_required": True,
                "prompt": f"Create project atlas at {root} for source {source}?",
                "confirm_args": ["init", "--root", str(root), "--source", str(source), "--confirm"],
            },
            2,
        )
    root.mkdir(parents=True, exist_ok=True)
    (root / "domains" / "core").mkdir(parents=True, exist_ok=True)
    (root / "diagrams").mkdir(parents=True, exist_ok=True)
    (root / "assets" / "diagrams").mkdir(parents=True, exist_ok=True)
    config = {"version": 1, "source": os.path.relpath(source, root)}
    (root / ".atlas.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (root / ".gitignore").write_text("_site/\n", encoding="utf-8")
    (root / "index.md").write_text(
        """---
title: 项目 Atlas
level: 0
status: draft
sources: []
source_digest:
verified_commit:
---

# 项目 Atlas

## 系统概览

用一段话说明系统服务的用户、解决的问题和外部边界。

## 领域地图

- [核心领域](domains/core/index.md)

## 主业务链路

用业务语言写出从触发到结果的主路径，并链接到下钻页面。
""",
        encoding="utf-8",
    )
    (root / "domains" / "core" / "index.md").write_text(
        """---
title: 核心领域
level: 1
status: draft
sources: []
source_digest:
verified_commit:
---

# 核心领域

## 职责与边界

说明本领域拥有什么、依赖什么，以及哪些职责属于相邻领域。

## 核心流程与规则

先写主流程，再按需要下钻为独立主题页。

## 主题

新增主题页后在这里加入链接。

## 架构图

复杂结构或流程使用 Archify 时，图源与交互图放入 `diagrams/`，在这里链接 HTML。

[返回系统总览](../../index.md)
""",
        encoding="utf-8",
    )
    (root / "diagrams" / ".gitkeep").write_text("", encoding="utf-8")
    (root / "assets" / "diagrams" / ".gitkeep").write_text("", encoding="utf-8")
    return emit({"ok": True, "root": str(root), "source": str(source), "next": "write pages, then verify and build"})


def command_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    source = source_root(root)
    pages, load_errors = load_pages(root)
    states = freshness(pages, source, root)
    return emit(
        {
            "ok": not load_errors,
            "root": str(root),
            "source": str(source),
            "stale_pages": [item["page"] for item in states if item["stale"]],
            "affected_diagrams": affected_archify_diagrams(pages, states, root),
            "draft_pages": [item["page"] for item in states if item["status"] == "draft"],
            "pages": states,
            "errors": load_errors,
        },
        1 if load_errors else 0,
    )


def git_head(source: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""
    return proc.stdout.strip()


def update_verification(page: Page, digest: str, commit: str) -> None:
    lines = page.text.splitlines(keepends=True)
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise AtlasError(f"frontmatter_missing:{page.rel}") from exc
    replacements = {"status": "verified", "source_digest": digest, "verified_commit": commit}
    seen = set()
    for i in range(1, end):
        match = re.match(r"^(status|source_digest|verified_commit):", lines[i])
        if match:
            key = match.group(1)
            lines[i] = f"{key}: {replacements[key]}\n"
            seen.add(key)
    for key in ("status", "source_digest", "verified_commit"):
        if key not in seen:
            lines.insert(end, f"{key}: {replacements[key]}\n")
            end += 1
    page.path.write_text("".join(lines), encoding="utf-8")


def command_verify(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    source = source_root(root)
    pages, load_errors = load_pages(root)
    if load_errors:
        return emit({"ok": False, "errors": load_errors}, 1)
    by_rel = {page.rel: page for page in pages}
    commit = git_head(source)
    selected = []
    digests = {}
    errors = []
    for raw in args.page:
        rel = Path(raw).as_posix()
        page = by_rel.get(rel)
        if page is None:
            errors.append(f"page_missing:{rel}")
            continue
        level = expected_level(page)
        sources = page.meta.get("sources", [])
        if level is None or level > 0 and not sources:
            errors.append(f"sources_missing:{rel}")
            continue
        digest, missing, _ = source_snapshot(page, source, root)
        if missing:
            errors.append(f"source_mapping_missing:{rel}:{','.join(missing)}")
            continue
        errors.extend(validate_archify_diagrams([page], root))
        selected.append(page)
        digests[rel] = digest
    if errors:
        return emit({"ok": False, "verified": [], "commit": commit, "errors": sorted(set(errors))}, 1)
    for page in selected:
        update_verification(page, digests[page.rel], commit)
    verified = [page.rel for page in selected]
    return emit({"ok": True, "verified": verified, "commit": commit, "errors": []})


def slugify(text: str) -> str:
    text = re.sub(r"[`*_~\[\]()]", "", text).strip().lower()
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text, flags=re.UNICODE).strip("-")
    return slug or "section"


def inline_markdown(text: str) -> str:
    output = []
    cursor = 0
    for match in TOKEN_RE.finditer(text):
        output.append(html.escape(text[cursor : match.start()]))
        token = match.group(0)
        if token.startswith("`"):
            output.append(f"<code>{html.escape(token[1:-1])}</code>")
        elif token.startswith("!["):
            parts = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", token)
            if parts:
                alt, target = parts.groups()
                output.append(f'<img src="{html.escape(target, quote=True)}" alt="{html.escape(alt, quote=True)}">')
        elif token.startswith("["):
            parts = re.match(r"\[([^\]]*)\]\(([^)]+)\)", token)
            if parts:
                label, target = parts.groups()
                target = rewrite_md_url(target)
                output.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(label)}</a>')
        else:
            output.append(f"<strong>{html.escape(token[2:-2])}</strong>")
        cursor = match.end()
    output.append(html.escape(text[cursor:]))
    return "".join(output)


def rewrite_md_url(raw_url: str) -> str:
    parts = urlsplit(raw_url)
    if parts.scheme or parts.netloc or not parts.path.lower().endswith(".md"):
        return raw_url
    return urlunsplit((parts.scheme, parts.netloc, parts.path[:-3] + ".html", parts.query, parts.fragment))


def render_markdown(body: str) -> str:
    lines = body.splitlines()
    output = []
    heading_counts: dict[str, int] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            class_attr = f' class="language-{html.escape(language, quote=True)}"' if language else ""
            output.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(code))}</code></pre>")
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            base = slugify(title)
            heading_counts[base] = heading_counts.get(base, 0) + 1
            suffix = "" if heading_counts[base] == 1 else f"-{heading_counts[base]}"
            output.append(f'<h{level} id="{base}{suffix}">{inline_markdown(title)}</h{level}>')
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([cell.strip() for cell in lines[i].strip().strip("|").split("|")])
                i += 1
            head = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in headers)
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>" for row in rows
            )
            output.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table>")
            continue
        list_match = re.match(r"^\s*([-+]|\d+\.)\s+(.+)$", line)
        if list_match:
            ordered = list_match.group(1)[0].isdigit()
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines):
                item = re.match(r"^\s*([-+]|\d+\.)\s+(.+)$", lines[i])
                if not item or item.group(1)[0].isdigit() != ordered:
                    break
                items.append(f"<li>{inline_markdown(item.group(2))}</li>")
                i += 1
            output.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6})\s+|^```|^\s*([-+]|\d+\.)\s+", lines[i]):
            if lines[i].lstrip().startswith("|"):
                break
            paragraph.append(lines[i].strip())
            i += 1
        output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
    return "\n".join(output)


STYLE = """
:root{color-scheme:light dark;--bg:#f7f7f4;--fg:#202421;--muted:#66706a;--card:#fff;--line:#dfe4df;--accent:#256f55}
@media(prefers-color-scheme:dark){:root{--bg:#151917;--fg:#e8ede9;--muted:#a7b0aa;--card:#1d2320;--line:#354039;--accent:#75c9a5}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 system-ui,-apple-system,sans-serif}
nav,main,footer{max-width:960px;margin:auto;padding:0 24px}nav{padding-top:24px;color:var(--muted)}main{margin-top:20px;margin-bottom:40px;padding-top:32px;padding-bottom:40px;background:var(--card);border:1px solid var(--line);border-radius:16px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}h1,h2,h3{line-height:1.3}h1{margin-top:0}pre{overflow:auto;padding:16px;background:var(--bg);border-radius:8px}code{font-family:ui-monospace,monospace}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}img{max-width:100%}.badge{font-size:12px;padding:3px 8px;border:1px solid var(--line);border-radius:999px;color:var(--muted)}.stale{color:#b45309}footer{color:var(--muted);font-size:13px;padding-bottom:30px}
"""


def page_breadcrumb(page: Page) -> str:
    if page.rel == "index.md":
        return "Atlas"
    domain = Path(page.rel).parts[1]
    if page.rel.endswith("/index.md"):
        return f'<a href="../../index.html">Atlas</a> / {html.escape(domain)}'
    return f'<a href="../../index.html">Atlas</a> / <a href="index.html">{html.escape(domain)}</a>'


def render_page(page: Page, stale: bool) -> str:
    title = html.escape(str(page.meta.get("title", page.rel)))
    badge = ""
    if stale:
        badge = '<span class="badge stale">待复核：源码已变化</span>'
    elif page.meta.get("status") == "draft":
        badge = '<span class="badge">草稿</span>'
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{STYLE}</style></head>
<body><nav>{page_breadcrumb(page)}</nav><main>{badge}{render_markdown(page.body)}</main><footer>由 project-atlas 生成；Markdown 为可编辑真源。</footer></body></html>
"""


def build_static_assets(root: Path, site: Path) -> int:
    assets = root / "assets"
    count = 0
    if not assets.is_dir():
        return count
    for path in sorted(assets.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        target = site / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".html":
            text = path.read_text(encoding="utf-8")
            text = HTML_URL_RE.sub(
                lambda match: f"{match.group(1)}={match.group(2)}{rewrite_md_url(match.group(3))}{match.group(2)}",
                text,
            )
            target.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, target)
        count += 1
    return count


def build_archify_diagrams(root: Path, site: Path) -> int:
    diagrams = root / "diagrams"
    count = 0
    if not diagrams.is_dir():
        return count
    for path in sorted(diagrams.rglob("*.html")):
        rel = path.relative_to(root)
        target = site / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = path.read_text(encoding="utf-8")
        text = HTML_URL_RE.sub(
            lambda match: f"{match.group(1)}={match.group(2)}{rewrite_md_url(match.group(3))}{match.group(2)}",
            text,
        )
        target.write_text(text, encoding="utf-8")
        count += 1
    return count


def command_build(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    source = source_root(root)
    pages, load_errors = load_pages(root)
    errors, warnings = validate_structure(pages, load_errors)
    errors.extend(validate_links(pages, root))
    errors.extend(validate_archify_diagrams(pages, root))
    if errors:
        return emit({"ok": False, "errors": sorted(set(errors)), "warnings": warnings}, 1)
    states = {item["page"]: item for item in freshness(pages, source, root)}
    site = root / "_site"
    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)
    for page in pages:
        target = site / Path(page.rel).with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page, bool(states[page.rel]["stale"])), encoding="utf-8")
    assets = build_static_assets(root, site)
    diagrams = build_archify_diagrams(root, site)
    stale = [rel for rel, state in states.items() if state["stale"]]
    return emit({"ok": True, "site": str(site), "pages": len(pages), "assets": assets, "diagrams": diagrams, "stale_pages": stale, "warnings": warnings})


def command_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    source = source_root(root)
    pages, load_errors = load_pages(root)
    errors, warnings = validate_structure(pages, load_errors)
    errors.extend(validate_links(pages, root))
    errors.extend(validate_archify_diagrams(pages, root))
    states = freshness(pages, source, root)
    for state in states:
        if state["stale"]:
            errors.append(f"stale:{state['page']}")
        for missing in state["missing_sources"]:
            errors.append(f"source_mapping_missing:{state['page']}:{missing}")
    errors = sorted(set(errors))
    return emit(
        {
            "ok": not errors,
            "errors": errors,
            "warnings": warnings,
            "stale_pages": [item["page"] for item in states if item["stale"]],
            "affected_diagrams": affected_archify_diagrams(pages, states, root),
        },
        1 if errors else 0,
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="atlasctl")
    sub = result.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--root")
    init.add_argument("--source", required=True)
    init.add_argument("--confirm", action="store_true")
    init.set_defaults(func=command_init)
    for name in ("status", "build", "check"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--root", default="docs/atlas")
        cmd.set_defaults(func={"status": command_status, "build": command_build, "check": command_check}[name])
    verify = sub.add_parser("verify")
    verify.add_argument("--root", default="docs/atlas")
    verify.add_argument("--page", nargs="+", required=True)
    verify.set_defaults(func=command_verify)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except (AtlasError, OSError, UnicodeError) as exc:
        return emit({"ok": False, "error": str(exc)}, 1)


if __name__ == "__main__":
    sys.exit(main())
