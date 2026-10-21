#!/usr/bin/env python3
"""静态检查生成的 HTML 页面：本地链接、页面基本信息、联网依赖，以及常见的默认样貌提示。

  python3 check_page.py docs/pretty-ui --offline
  python3 check_page.py page.html other.html

报错（退出码 1）：
  - 本地 href / src / srcset / CSS url() 从所在文件的目录解析不到目标
  - 站点根路径（/…）、file:// 或绝对磁盘路径的本地链接
  - 缺 <html lang>、viewport 或 <title>
  - 加 --offline 时，依赖联网加载的脚本、样式、字体、图片或模块
提示（不影响退出码，方括号里是 references/rules.md 的规则号）：
  渐变文字、表情符号当图标、去掉焦点轮廓却没有 :focus-visible、有动效却没有
  prefers-reduced-motion、小于 12px 的字号、没走 CSS 变量的颜色、中文页面里的大写变换、
  链接指向目录或检查目录之外。

输入是目录时检查其中全部 .html。只依赖 Python 3 标准库。
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote

SKIP_SCHEMES = ("mailto:", "tel:", "data:", "javascript:", "blob:", "about:", "sms:")
RESOURCE_LINK_RELS = {"stylesheet", "icon", "shortcut", "apple-touch-icon", "preload", "modulepreload", "manifest", "prefetch"}
RESOURCE_TAGS = {"script", "img", "source", "video", "audio", "iframe", "embed", "track", "input"}
EMOJI_CONTEXTS = {"h1", "h2", "h3", "h4", "h5", "h6", "button", "a", "label", "summary", "th", "dt"}
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u2604\u2607-\u260F\u2613-\u26FF"
    "\u2705\u2728\u274C\u2753-\u2757\u2795-\u2797\u2B50\u2B55\u231A\u231B\u23E9-\u23F3\u23F8-\u23FA]"
)
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)
CSS_IMPORT_RE = re.compile(r"@import\s+['\"]([^'\"]+)['\"]", re.I)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
JS_REMOTE_IMPORT_RE = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s+)['"]((?:https?:)?//[^'"]+)['"]""")
COLOR_LITERAL_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\(")
FONT_SIZE_RE = re.compile(r"font-size\s*:\s*([\d.]+)(px|rem)\b", re.I)
BLOCK_RE = re.compile(r"\{([^{}]*)\}")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.has_viewport = False
        self.title_parts: list[str] = []
        self.has_title_tag = False
        self.refs: list[tuple[str, str, bool]] = []  # (url, 来源描述, 是否属于页面资源)
        self.css: list[str] = []
        self.scripts: list[str] = []
        self.emoji_hits: list[str] = []
        self._raw: str | None = None  # 正在读取的 style / script / title
        self._ctx: dict[str, int] = {}

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): (v or "") for k, v in attrs_list}
        if tag == "html":
            self.lang = attrs.get("lang", "").strip() or None
        elif tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.has_viewport = True
        elif tag in ("title", "style", "script"):
            self._raw = tag
            if tag == "title":
                self.has_title_tag = True
        if tag in EMOJI_CONTEXTS:
            self._ctx[tag] = self._ctx.get(tag, 0) + 1
        if "style" in attrs:
            self.css.append(attrs["style"])

        if tag == "link":
            rels = set(attrs.get("rel", "").lower().split())
            if attrs.get("href"):
                self.refs.append((attrs["href"], "<link href>", bool(rels & RESOURCE_LINK_RELS)))
        elif tag == "a" or tag == "area":
            if attrs.get("href"):
                self.refs.append((attrs["href"], f"<{tag} href>", False))
        else:
            for key in ("src", "href", "xlink:href", "poster", "data"):
                if attrs.get(key):
                    resource = tag in RESOURCE_TAGS or key in ("src", "poster", "data") or tag in ("image", "use", "object")
                    self.refs.append((attrs[key], f"<{tag} {key}>", resource))
            if attrs.get("srcset"):
                for part in attrs["srcset"].split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.refs.append((url, f"<{tag} srcset>", True))

    def handle_endtag(self, tag: str) -> None:
        if tag == self._raw:
            self._raw = None
        if self._ctx.get(tag):
            self._ctx[tag] -= 1

    def handle_data(self, data: str) -> None:
        if self._raw == "style":
            self.css.append(data)
        elif self._raw == "script":
            self.scripts.append(data)
        elif self._raw == "title":
            self.title_parts.append(data)
        elif any(self._ctx.values()) and EMOJI_RE.search(data):
            self.emoji_hits.append(data.strip()[:20])


def classify(url: str) -> str:
    u = url.strip()
    low = u.lower()
    if not u or u.startswith("#") or low.startswith(SKIP_SCHEMES):
        return "skip"
    if low.startswith(("http://", "https://", "//")):
        return "remote"
    if low.startswith("file:"):
        return "file"
    if re.match(r"^[a-zA-Z]:[\\/]", u) or u.startswith("\\\\"):
        return "abs"
    if u.startswith("/"):
        return "root"
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", u):
        return "skip"
    return "local"


def css_blocks(fragments: list[str]) -> list[str]:
    """样式表取最内层的声明块；style 属性没有花括号，整段算一个块。"""
    blocks: list[str] = []
    for frag in fragments:
        frag = CSS_COMMENT_RE.sub("", frag)
        blocks += BLOCK_RE.findall(frag) if "{" in frag else [frag]
    return blocks


def css_declarations(blocks: list[str]) -> list[tuple[str, str]]:
    out = []
    for block in blocks:
        for decl in block.split(";"):
            if ":" in decl:
                prop, value = decl.split(":", 1)
                out.append((prop.strip().lower(), value.strip()))
    return out


def check_file(path: str, root: str | None, offline: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    hints: list[str] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    p = PageParser()
    p.feed(text)
    p.close()
    base = os.path.dirname(os.path.abspath(path))
    css = CSS_COMMENT_RE.sub("", "\n".join(p.css))
    blocks = css_blocks(p.css)
    scripts = "\n".join(p.scripts)

    if not p.lang:
        errors.append("<html> 缺 lang 属性")
    if not p.has_viewport:
        errors.append('缺 <meta name="viewport">')
    if not p.has_title_tag or not "".join(p.title_parts).strip():
        errors.append("缺 <title> 或标题为空")

    refs = list(p.refs)
    refs += [(m.group(2), "CSS url()", True) for m in CSS_URL_RE.finditer(css)]
    refs += [(m.group(1), "CSS @import", True) for m in CSS_IMPORT_RE.finditer(css)]
    refs += [(m.group(1), "<script> import", True) for m in JS_REMOTE_IMPORT_RE.finditer(scripts)]

    remote: list[str] = []
    dir_links: list[str] = []
    outside: list[str] = []
    seen: set[tuple[str, str]] = set()
    for url, where, resource in refs:
        if (url, where) in seen:
            continue
        seen.add((url, where))
        kind = classify(url)
        if kind == "skip":
            continue
        if kind == "remote":
            if resource:
                remote.append(f"{url}（{where}）")
            continue
        if kind == "file":
            errors.append(f"file:// 链接换目录后失效：{url}（{where}）")
            continue
        if kind == "abs":
            errors.append(f"绝对磁盘路径换机器后失效：{url}（{where}）")
            continue
        if kind == "root":
            errors.append(f"站点根路径离开当前目录就失效，改成相对当前文件的路径：{url}（{where}）")
            continue
        rel = unquote(re.split(r"[?#]", url, maxsplit=1)[0])
        if not rel:
            continue
        target = os.path.normpath(os.path.join(base, rel))
        if not os.path.exists(target):
            errors.append(f"本地链接目标不存在：{url}（{where}，从 {os.path.relpath(base)} 解析）")
            continue
        if os.path.isdir(target):
            dir_links.append(url)
        if root and os.path.commonpath([os.path.abspath(root), target]) != os.path.abspath(root):
            outside.append(url)

    if remote:
        msg = f"依赖联网资源 {len(remote)} 处，离线打不开：" + "；".join(remote[:3])
        (errors if offline else hints).append(msg)
    if dir_links:
        hints.append("链接指向目录，直接打开文件时不会自动补 index.html，写全 …/index.html：" + "、".join(dir_links[:3]))
    if outside:
        hints.append("链接指向检查目录之外：" + "、".join(outside[:3]))

    gradient_text = sum(1 for b in blocks if re.search(r"background-clip\s*:\s*text", b, re.I) and "gradient" in b.lower())
    if gradient_text:
        hints.append(f"[X2] 渐变文字 {gradient_text} 处")
    if len(p.emoji_hits) >= 2:
        hints.append(f"[X5] 标题、按钮、链接里的表情符号 {len(p.emoji_hits)} 处：" + "、".join(p.emoji_hits[:3]))
    if re.search(r"outline\s*:\s*(none|0)\b", css, re.I) and ":focus-visible" not in css:
        hints.append("[F7] 去掉了焦点轮廓，却没有 :focus-visible 样式")
    if re.search(r"@keyframes|\banimation\s*:|\btransition\s*:", css, re.I) and "prefers-reduced-motion" not in css:
        hints.append("[M4] 有动效，却没有 prefers-reduced-motion 的处理")
    small = []
    for value, unit in FONT_SIZE_RE.findall(css):
        px = float(value) * (16 if unit.lower() == "rem" else 1)
        if px < 12:
            small.append(f"{value}{unit}")
    if small:
        hints.append(f"[T4] 小于 12px 的字号 {len(small)} 处：" + "、".join(sorted(set(small))[:5]))
    literals = []
    for prop, value in css_declarations(blocks):
        if not prop.startswith("--") and COLOR_LITERAL_RE.search(value):
            literals.append(f"{prop}: {value[:32]}")
    if literals:
        hints.append(f"[C1] 没走 CSS 变量的颜色 {len(literals)} 处：" + "；".join(literals[:3]))
    if (p.lang or "").lower().startswith("zh"):
        upper = len(re.findall(r"text-transform\s*:\s*uppercase", css, re.I))
        if upper:
            hints.append(f"[X12] 中文页面里的大写变换 {upper} 处")
    return errors, hints


def collect(paths: list[str]) -> list[tuple[str, str | None]]:
    files: list[tuple[str, str | None]] = []
    for item in paths:
        if os.path.isdir(item):
            for dirpath, dirnames, filenames in os.walk(item):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                for name in sorted(filenames):
                    if name.lower().endswith((".html", ".htm")):
                        files.append((os.path.join(dirpath, name), item))
        elif os.path.isfile(item):
            files.append((item, None))
        else:
            print(f"找不到：{item}", file=sys.stderr)
            raise SystemExit(2)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="HTML 文件或目录")
    ap.add_argument("--offline", action="store_true", help="页面必须离线可用：联网资源算报错")
    a = ap.parse_args()

    files = collect(a.paths)
    if not files:
        print("没有找到 .html 文件", file=sys.stderr)
        return 2
    n_err = n_hint = 0
    for path, root in files:
        errors, hints = check_file(path, root, a.offline)
        shown = os.path.relpath(path)
        for e in errors:
            print(f"ERROR {shown}: {e}")
        for h in hints:
            print(f"WARN  {shown}: {h}")
        n_err += len(errors)
        n_hint += len(hints)
    print(f"检查 {len(files)} 个文件：{n_err} 个报错，{n_hint} 条提示")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
