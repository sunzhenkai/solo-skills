#!/usr/bin/env python3
"""Deterministic lint (and optional index rebuild) for a local LLM wiki workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

TYPED_DIRS = {
    "entities": "entity",
    "concepts": "concept",
    "sources": "source",
    "synthesis": "synthesis",
    "experiences": "experience",
    "ledgers": "ledger",
    "comparisons": "comparison",
    "queries": "query",
}
TYPE_TO_DIR = {v: k for k, v in TYPED_DIRS.items()}
SYSTEM_PAGES = {"overview.md", "index.md", "log.md"}
INDEX_HEADINGS = [
    ("entities", "实体 (entities)"),
    ("concepts", "概念 (concepts)"),
    ("sources", "源摘要 (sources)"),
    ("synthesis", "综合分析 (synthesis)"),
    ("experiences", "经验 (experiences)"),
    ("ledgers", "业务台账 (ledgers)"),
    ("comparisons", "对比分析 (comparisons)"),
    ("queries", "查询归档 (queries)"),
]
ABSTRACT_KEYWORDS = (
    "方法",
    "方法论",
    "模型",
    "文化",
    "框架",
    "策略",
    "机制",
    "理论",
    "范式",
    "实践",
    "流程",
    "体系",
    "method",
    "methodology",
    "model",
    "culture",
    "framework",
    "strategy",
    "mechanism",
    "theory",
    "paradigm",
    "practice",
    "process",
    "system",
)
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
MDLINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
LOG_RE = re.compile(
    r"^## \[(\d{4}-\d{2}-\d{2})\] ([^|]+?) \| (.+)$"
)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wiki_root", type=Path, help="Workspace root containing wiki/")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    index_mode = parser.add_mutually_exclusive_group()
    index_mode.add_argument(
        "--check-index",
        action="store_true",
        help="Check wiki/index.md without writing (default)",
    )
    index_mode.add_argument(
        "--write-index",
        action="store_true",
        help="Rebuild wiki/index.md from typed pages",
    )
    return parser.parse_args(argv)


LIST_FIELDS = {"tags", "aliases", "sources", "related"}


def parse_inline_list(value: str) -> list[str] | None:
    if len(value) < 2 or not value.startswith("[") or not value.endswith("]"):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    current: list[str] = []
    quote = ""
    escaped = False
    for char in inner:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\" and quote == '"':
            current.append(char)
            escaped = True
            continue
        if quote:
            current.append(char)
            if char == quote:
                quote = ""
            continue
        if char in {'"', "'"}:
            current.append(char)
            quote = char
        elif char == ",":
            items.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if quote:
        return None
    items.append("".join(current).strip())
    parsed = []
    for item in items:
        if not item:
            return None
        if item[0] in {'"', "'"}:
            if len(item) < 2 or item[-1] != item[0]:
                return None
            item = item[1:-1]
        parsed.append(item)
    return parsed


def parse_frontmatter(text: str) -> tuple[dict[str, str], dict[str, list[str]], list[str]]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, {}, []
    fields: dict[str, str] = {}
    lists: dict[str, list[str]] = {}
    errors: list[str] = []
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line[:1].isspace() or ":" not in line:
            errors.append(f"不支持的行: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            errors.append(f"空字段名: {line}")
            continue
        if key in fields:
            errors.append(f"重复字段: {key}")
            continue
        fields[key] = value.strip("\"'")
        if key in LIST_FIELDS:
            parsed = parse_inline_list(value)
            if parsed is None:
                errors.append(f"{key} 必须是 inline list")
            else:
                lists[key] = parsed
    return fields, lists, errors


def normalize_name_key(value: str) -> str:
    chars = []
    for ch in value.strip().lower():
        if ch in {" ", "_", "-", "\u3000"}:
            continue
        chars.append(ch)
    return "".join(chars)


def title_from_filename(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").strip()


def iter_wiki_pages(wiki_dir: Path) -> list[Path]:
    if not wiki_dir.is_dir():
        return []
    pages = [
        path
        for path in wiki_dir.rglob("*.md")
        if path.is_file() and ".git" not in path.parts
    ]
    return sorted(pages)


def rel_wiki(path: Path, wiki_dir: Path) -> str:
    return path.relative_to(wiki_dir).as_posix()


def classify(rel: str) -> str:
    if rel in SYSTEM_PAGES:
        return "system"
    parts = rel.split("/")
    if parts[0] == "templates":
        return "template"
    if len(parts) >= 2 and parts[0] in TYPED_DIRS:
        return "business"
    return "misplaced"


def load_pages(wiki_dir: Path) -> list[dict]:
    pages = []
    for path in iter_wiki_pages(wiki_dir):
        rel = rel_wiki(path, wiki_dir)
        text = path.read_text(encoding="utf-8")
        fm, lists, fm_errors = parse_frontmatter(text)
        stem = path.stem
        title = fm.get("title") or title_from_filename(stem)
        kind = classify(rel)
        subdir = rel.split("/", 1)[0] if "/" in rel else ""
        pages.append(
            {
                "path": path,
                "rel": rel,
                "text": text,
                "fm": fm,
                "lists": lists,
                "fm_errors": fm_errors,
                "stem": stem,
                "title": title,
                "kind": kind,
                "subdir": subdir,
            }
        )
    return pages


def is_archived(page: dict) -> bool:
    return bool(page["fm"].get("archived_at"))


def build_resolvers(pages: list[dict]) -> tuple[dict[str, str], set[str]]:
    mapping: dict[str, str] = {}
    owners: dict[str, set[str]] = defaultdict(set)

    def add(key: str, rel: str) -> None:
        key = key.strip()
        if not key:
            return
        for variant in (key, key.lower(), normalize_name_key(key)):
            owners[variant].add(rel)
            mapping.setdefault(variant, rel)

    for page in pages:
        rel = page["rel"]
        add(rel, rel)
        add(rel[:-3] if rel.endswith(".md") else rel, rel)
        add(page["stem"], rel)
        add(page["title"], rel)
        add(title_from_filename(page["stem"]), rel)
        for alias in page["lists"].get("aliases", []):
            add(alias, rel)
        if "/" in rel:
            add(rel.split("/", 1)[1], rel)
            add(Path(rel).stem, rel)
    ambiguous = {key for key, rels in owners.items() if len(rels) > 1}
    return mapping, ambiguous


def split_wikilink(raw: str) -> str:
    # GFM tables escape wikilink aliases as [[path\|Title]]
    raw = raw.replace("\\|", "|")
    target = raw.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    return target


def wikilink_keys(target: str) -> list[str]:
    if not target:
        return []
    candidates = [
        target,
        target.lower(),
        normalize_name_key(target),
        f"{target}.md",
        f"{target.lower()}.md",
    ]
    if not target.endswith(".md") and "/" in target:
        candidates.append(f"{target}.md")
    return candidates


def is_ambiguous_wikilink(target: str, ambiguous: set[str]) -> bool:
    return any(key in ambiguous for key in wikilink_keys(target))


def resolve_wikilink(target: str, mapping: dict[str, str]) -> str | None:
    for key in wikilink_keys(target):
        if key in mapping:
            return mapping[key]
    return None


def resolve_md_link(source_rel: str, target: str, wiki_dir: Path) -> Path | None:
    href = target.strip()
    if not href or href.startswith(("#", "http://", "https://", "mailto:")):
        return None
    href = href.split("#", 1)[0]
    if not href:
        return None
    base = (wiki_dir / source_rel).parent
    dest = (base / href).resolve()
    try:
        dest.relative_to(wiki_dir.resolve())
    except ValueError:
        return dest
    return dest


def collect_incoming(
    pages: list[dict], mapping: dict[str, str], wiki_dir: Path, ambiguous: set[str]
) -> dict[str, int]:
    incoming: dict[str, int] = defaultdict(int)
    for page in pages:
        # Index/overview and archived pages do not make current pages discoverable.
        if page["kind"] in {"system", "template"} or is_archived(page):
            continue
        seen: set[str] = set()
        for match in WIKILINK_RE.finditer(page["text"]):
            target = split_wikilink(match.group(1))
            if is_ambiguous_wikilink(target, ambiguous):
                continue
            resolved = resolve_wikilink(target, mapping)
            if resolved and resolved != page["rel"] and resolved not in seen:
                incoming[resolved] += 1
                seen.add(resolved)
        for match in MDLINK_RE.finditer(page["text"]):
            dest = resolve_md_link(page["rel"], match.group(2), wiki_dir)
            if dest is None or not dest.exists() or dest.suffix != ".md":
                continue
            try:
                rel = dest.relative_to(wiki_dir.resolve()).as_posix()
            except ValueError:
                continue
            if rel != page["rel"] and rel not in seen:
                incoming[rel] += 1
                seen.add(rel)
    return incoming


def validate_source_reference(
    reference: str,
    mapping: dict[str, str],
    ambiguous: set[str],
    page_by_rel: dict[str, dict],
    wiki_dir: Path,
) -> str | None:
    value = reference.strip()
    if not value:
        return "空来源"
    is_wikilink = value.startswith("[[") and value.endswith("]]")
    target = split_wikilink(value[2:-2]) if is_wikilink else value
    if is_ambiguous_wikilink(target, ambiguous):
        return f"来源有歧义: {value}"
    resolved = resolve_wikilink(target, mapping)
    if resolved:
        target_page = page_by_rel[resolved]
        if target_page["subdir"] == "sources":
            return None
        return f"来源不是 wiki/sources 页面: {value}"
    if is_wikilink:
        return f"来源页不存在: {value}"

    root = wiki_dir.parent
    candidate = root / value if value.startswith("raw/") else root / "raw" / "sources" / value
    resolved_path = candidate.resolve()
    try:
        resolved_path.relative_to((root / "raw").resolve())
    except ValueError:
        return f"来源路径越过 raw: {value}"
    if not resolved_path.is_file():
        return f"raw 来源不存在: {value}"
    return None


def lint_issues(pages: list[dict], wiki_dir: Path) -> list[dict]:
    mapping, ambiguous = build_resolvers(pages)
    page_by_rel = {page["rel"]: page for page in pages}
    incoming = collect_incoming(pages, mapping, wiki_dir, ambiguous)
    issues: list[dict] = []

    def add(code: str, severity: str, rel: str, message: str) -> None:
        issues.append(
            {"code": code, "severity": severity, "path": f"wiki/{rel}", "message": message}
        )

    entity_names: list[tuple[str, str]] = []
    for page in pages:
        if page["kind"] != "business" or page["subdir"] != "entities":
            continue
        for display in (page["title"], page["stem"], title_from_filename(page["stem"])):
            key = normalize_name_key(display)
            if len(key) >= 3:
                entity_names.append((display, key))

    dup_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for page in pages:
        rel = page["rel"]
        kind = page["kind"]
        fm = page["fm"]

        if kind == "misplaced":
            add(
                "misplaced_wiki_page",
                "warning",
                rel,
                "业务页不在 typed 子目录",
            )

        for error in page["fm_errors"]:
            add("frontmatter_invalid", "error", rel, error)

        if kind == "business":
            required_fields = ["title", "type", "date", "confidence"]
            page_type = fm.get("type", "")
            archived = is_archived(page)
            if page_type in {"experience", "ledger"}:
                required_fields.append("status")
            if page_type == "source" and not archived:
                required_fields.extend(["origin", "captured_at"])
            missing = [field for field in required_fields if not fm.get(field)]
            origin = fm.get("origin", "")
            needs_raw_source = page_type != "source" or origin not in {
                "user-input",
                "conversation",
            }
            if not archived and needs_raw_source and not page["lists"].get("sources"):
                missing.append("sources")
            if missing or not fm:
                add(
                    "missing_frontmatter",
                    "error",
                    rel,
                    "缺少 frontmatter 字段: "
                    + (", ".join(missing) or "title, type, date, confidence"),
                )

            for reference in page["lists"].get("sources", []):
                source_error = validate_source_reference(
                    reference, mapping, ambiguous, page_by_rel, wiki_dir
                )
                if source_error:
                    add("source_invalid", "error", rel, source_error)
            content_hash = fm.get("content_hash", "")
            hash_valid = not content_hash or re.fullmatch(r"[0-9a-fA-F]{64}", content_hash)
            if not hash_valid:
                add("source_invalid", "error", rel, "content_hash 必须是 SHA-256 十六进制摘要")
            origin_path = None
            if page_type == "source" and origin and origin not in {"user-input", "conversation"}:
                origin_path = (wiki_dir.parent / origin).resolve()
                try:
                    origin_path.relative_to((wiki_dir.parent / "raw").resolve())
                except ValueError:
                    add("source_invalid", "error", rel, "origin 必须位于 raw 内")
                    origin_path = None
                if origin_path is not None and not origin_path.is_file():
                    add("source_invalid", "error", rel, f"origin 不存在: {origin}")
                    origin_path = None
            if origin_path is not None and content_hash and hash_valid:
                actual_hash = hashlib.sha256(origin_path.read_bytes()).hexdigest()
                if actual_hash != content_hash.lower():
                    add("source_invalid", "error", rel, "content_hash 与 origin 内容不匹配")
            if not archived and not fm.get("description"):
                add("description_missing", "warning", rel, "活跃业务页缺少 description")

            confidence = fm.get("confidence", "")
            if confidence and confidence not in {"high", "medium", "low"}:
                add(
                    "confidence_invalid",
                    "error",
                    rel,
                    f"confidence 必须是 high / medium / low，当前为 {confidence!r}",
                )

            archived_at = fm.get("archived_at", "")
            if archived_at and not fm.get("archive_reason"):
                add(
                    "archive_metadata_invalid",
                    "error",
                    rel,
                    "已归档页缺少 archive_reason",
                )
            if not archived_at and any(
                fm.get(field) for field in ("archive_reason", "superseded_by")
            ):
                add(
                    "archive_metadata_invalid",
                    "error",
                    rel,
                    "archive_reason / superseded_by 需要 archived_at",
                )

            parsed_dates = {}
            for field in (
                "date",
                "created",
                "last_verified",
                "review_after",
                "archived_at",
                "captured_at",
            ):
                value = fm.get(field, "")
                if not value:
                    continue
                try:
                    parsed = date.fromisoformat(value)
                    if parsed.isoformat() != value:
                        raise ValueError(value)
                    parsed_dates[field] = parsed
                except ValueError:
                    add(
                        "date_invalid",
                        "error",
                        rel,
                        f"{field} 必须是有效的 YYYY-MM-DD，当前为 {value!r}",
                    )

            if confidence == "high" and not fm.get("last_verified"):
                add(
                    "verification_missing",
                    "error",
                    rel,
                    "high confidence 需要 last_verified",
                )
            if page_type == "experience" and fm.get("status") == "validated":
                verification_fields = [
                    field for field in ("last_verified", "review_after") if not fm.get(field)
                ]
                if verification_fields:
                    add(
                        "verification_missing",
                        "error",
                        rel,
                        "validated 经验缺少: " + ", ".join(verification_fields),
                    )
            review_after = parsed_dates.get("review_after")
            if not archived and review_after and review_after < date.today():
                add(
                    "review_overdue",
                    "warning",
                    rel,
                    f"复审日期已过: {review_after.isoformat()}",
                )

            expected_dir = TYPE_TO_DIR.get(page_type)
            if page_type and expected_dir and page["subdir"] != expected_dir:
                add(
                    "type_dir_mismatch",
                    "warning",
                    rel,
                    f"type={page_type} 应位于 wiki/{expected_dir}/",
                )
            if page["subdir"] in TYPED_DIRS:
                dup_groups[(page["subdir"], normalize_name_key(page["stem"]))].append(rel)

        if kind == "business" and page["subdir"] == "concepts":
            for source in (page["title"], page["stem"]):
                coupled = match_entity_concept(source, entity_names)
                if coupled:
                    entity, suffix = coupled
                    add(
                        "entity_concept_coupling",
                        "warning",
                        rel,
                        f"概念标题绑定实体 {entity!r} 与抽象后缀 {suffix!r}",
                    )
                    break

        archived_refs: set[str] = set()
        for match in WIKILINK_RE.finditer(page["text"]):
            target = split_wikilink(match.group(1))
            if is_ambiguous_wikilink(target, ambiguous):
                add("ambiguous_link", "error", rel, f"链接有歧义 [[{target}]]，请使用路径限定")
                continue
            resolved = resolve_wikilink(target, mapping)
            if resolved is None:
                add("dead_link", "error", rel, f"死链 [[{target}]]")
                continue
            target_page = page_by_rel.get(resolved)
            if (
                kind == "business"
                and not is_archived(page)
                and target_page is not None
                and is_archived(target_page)
                and resolved != rel
                and resolved not in archived_refs
            ):
                add("archived_reference", "warning", rel, f"活跃页引用了归档页 [[{target}]]")
                archived_refs.add(resolved)

        for match in MDLINK_RE.finditer(page["text"]):
            href = match.group(2).strip()
            dest = resolve_md_link(rel, href, wiki_dir)
            if dest is None:
                continue
            if not dest.exists():
                add("dead_link", "error", rel, f"死链 ({href})")
                continue
            if dest.suffix != ".md":
                continue
            try:
                target_rel = dest.relative_to(wiki_dir.resolve()).as_posix()
            except ValueError:
                continue
            target_page = page_by_rel.get(target_rel)
            if (
                kind == "business"
                and not is_archived(page)
                and target_page is not None
                and is_archived(target_page)
                and target_rel != rel
                and target_rel not in archived_refs
            ):
                add("archived_reference", "warning", rel, f"活跃页引用了归档页 ({href})")
                archived_refs.add(target_rel)

    for (subdir, key), rels in dup_groups.items():
        if key and len(rels) > 1:
            joined = ", ".join(f"wiki/{item}" for item in rels)
            for rel in rels:
                add(
                    "duplicate_page",
                    "warning",
                    rel,
                    f"{subdir}/ 下归一化重名: {joined}",
                )

    for page in pages:
        if page["kind"] != "business" or is_archived(page):
            continue
        if page["subdir"] == "sources":
            continue
        if incoming.get(page["rel"], 0) == 0:
            add("orphan_page", "warning", page["rel"], "没有来自其它活跃 wiki 页的入链")

    log_page = next((page for page in pages if page["rel"] == "log.md"), None)
    if log_page:
        issues.extend(lint_log(log_page["text"]))

    index_page = next((page for page in pages if page["rel"] == "index.md"), None)
    index_date = index_page["fm"].get("date") if index_page else None
    expected_index = render_index(pages, index_date)
    if index_page is None or index_page["text"] != expected_index:
        add("index_stale", "error", "index.md", "索引缺失或与当前页面不一致")

    return issues


def match_entity_concept(name: str, entities: list[tuple[str, str]]) -> tuple[str, str] | None:
    key = normalize_name_key(name)
    if not key:
        return None
    for display, entity_key in entities:
        if not key.startswith(entity_key) or len(key) <= len(entity_key):
            continue
        suffix = key[len(entity_key) :]
        lowered = suffix.lower()
        if any(normalize_name_key(word) in lowered for word in ABSTRACT_KEYWORDS):
            return display, suffix
    return None


def lint_log(text: str) -> list[dict]:
    issues: list[dict] = []
    dates: list[str] = []
    for line in text.splitlines():
        if not line.startswith("## ["):
            continue
        match = LOG_RE.match(line)
        if not match:
            issues.append(
                {
                    "code": "log_format_invalid",
                    "severity": "error",
                    "path": "wiki/log.md",
                    "message": f"日志格式无效: {line}",
                }
            )
            continue
        dates.append(match.group(1))
    for prev, curr in zip(dates, dates[1:]):
        if curr < prev:
            issues.append(
                {
                    "code": "log_date_decreasing",
                    "severity": "error",
                    "path": "wiki/log.md",
                    "message": f"日期递减: {prev} → {curr}",
                }
            )
            break
    return issues


def render_index(pages: list[dict], index_date: str | None = None) -> str:
    grouped: dict[str, list[dict]] = {name: [] for name, _ in INDEX_HEADINGS}
    archived: list[dict] = []
    for page in pages:
        if page["kind"] != "business" or page["subdir"] not in grouped:
            continue
        fm = page["fm"]
        entry = {
            "subdir": page["subdir"],
            "slug": page["stem"],
            "title": page["title"],
            "type": fm.get("type", ""),
            "description": fm.get("description", ""),
            "date": fm.get("date", ""),
            "confidence": fm.get("confidence", ""),
            "status": fm.get("status", ""),
            "last_verified": fm.get("last_verified", ""),
            "review_after": fm.get("review_after", ""),
            "archived_at": fm.get("archived_at", ""),
            "archive_reason": fm.get("archive_reason", ""),
            "superseded_by": fm.get("superseded_by", ""),
        }
        if is_archived(page):
            archived.append(entry)
        else:
            grouped[page["subdir"]].append(entry)
    for entries in grouped.values():
        entries.sort(key=lambda item: (item["title"].lower(), item["slug"]))
    archived.sort(key=lambda item: (item["title"].lower(), item["slug"]))

    today = index_date or date.today().isoformat()
    lines = [
        "---",
        "title: 内容目录",
        "type: index",
        f"date: {today}",
        "---",
        "",
        "# 内容目录",
        "",
        "> 本文件由 wiki-data 维护，请勿手改业务行。",
        "",
    ]
    for dirname, heading in INDEX_HEADINGS:
        lines.extend(
            [
                f"## {heading}",
                "",
                "| 页面 | 标题 | 摘要 | 更新日期 | 置信度 | 状态 | 核实日期 | 复审日期 |",
                "|------|------|------|----------|--------|------|----------|----------|",
            ]
        )
        for entry in grouped[dirname]:
            title = escape_cell(entry["title"])
            link = f"[[{entry['subdir']}/{entry['slug']}\\|{title}]]"
            cells = [link, title]
            cells.extend(
                escape_cell(entry[field] or "-")
                for field in (
                    "description",
                    "date",
                    "confidence",
                    "status",
                    "last_verified",
                    "review_after",
                )
            )
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    lines.extend(
        [
            "## 已归档 (archived)",
            "",
            "| 页面 | 类型 | 标题 | 摘要 | 归档日期 | 归档原因 | 替代页 |",
            "|------|------|------|------|----------|----------|--------|",
        ]
    )
    for entry in archived:
        title = escape_cell(entry["title"])
        link = f"[[{entry['subdir']}/{entry['slug']}\\|{title}]]"
        cells = [link, entry["type"], title]
        cells.extend(
            escape_cell(entry[field] or "-")
            for field in ("description", "archived_at", "archive_reason", "superseded_by")
        )
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    text = "\n".join(lines)
    return text if text.endswith("\n") else text + "\n"


def rebuild_index(pages: list[dict], wiki_dir: Path) -> str:
    text = render_index(pages)
    (wiki_dir / "index.md").write_text(text, encoding="utf-8")
    return text


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def build_stats(pages: list[dict], issues: list[dict]) -> dict[str, int]:
    business = [page for page in pages if page["kind"] == "business"]
    return {
        "active": sum(not is_archived(page) for page in business),
        "archived": sum(is_archived(page) for page in business),
        "draft": sum(page["fm"].get("status") == "draft" for page in business),
        "validated": sum(page["fm"].get("status") == "validated" for page in business),
        "deprecated": sum(page["fm"].get("status") == "deprecated" for page in business),
        "review_overdue": len(
            {item["path"] for item in issues if item["code"] == "review_overdue"}
        ),
    }


def render_text(issues: list[dict], page_count: int, stats: dict[str, int]) -> str:
    errors = [item for item in issues if item["severity"] == "error"]
    warnings = [item for item in issues if item["severity"] == "warning"]
    lines = [
        f"pages: {page_count}",
        f"errors: {len(errors)}",
        f"warnings: {len(warnings)}",
    ]
    lines.extend(f"{key}: {value}" for key, value in stats.items())
    if not issues:
        lines.append("ok")
        return "\n".join(lines) + "\n"
    lines.append("")
    for item in issues:
        lines.append(f"{item['severity']}\t{item['code']}\t{item['path']}\t{item['message']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.wiki_root.expanduser().resolve()
    wiki_dir = root / "wiki"
    if not wiki_dir.is_dir():
        print(f"missing wiki directory: {wiki_dir}", file=sys.stderr)
        return 2

    pages = load_pages(wiki_dir)
    if args.write_index:
        rebuild_index(pages, wiki_dir)
        pages = load_pages(wiki_dir)

    issues = lint_issues(pages, wiki_dir)
    stats = build_stats(pages, issues)
    payload = {
        "wiki_root": str(root),
        "pages": len(pages),
        "errors": sum(1 for item in issues if item["severity"] == "error"),
        "warnings": sum(1 for item in issues if item["severity"] == "warning"),
        "stats": stats,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(render_text(issues, len(pages), stats))
    return 1 if payload["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
