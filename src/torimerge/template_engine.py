from __future__ import annotations
from pathlib import Path
import re
from typing import Dict, Any, List, Tuple
from jinja2 import Environment, StrictUndefined


TABLE_OPEN_RE = re.compile(r"\[\[TABLE(?::([^\]]+))?\]\]", re.IGNORECASE)
TABLE_CLOSE = "[[/TABLE]]"


def parse_template(file: Path) -> Tuple[str, str]:
    text = file.read_text(encoding="utf-8")
    if "\r\n" in text:
        normalized = text.replace("\r\n", "\n")
    else:
        normalized = text.replace("\r", "\n")
    if "\n\n" in normalized:
        subject, body = normalized.split("\n\n", 1)
    else:
        subject, body = normalized.strip(), ""
    return subject.strip(), body


def _render_jinja(tpl: str, ctx: Dict[str, Any]) -> str:
    env = Environment(undefined=StrictUndefined, autoescape=False)
    return env.from_string(tpl).render(**ctx)


def _render_table_block(inner: str, rows: List[Dict[str, Any]], columns: List[str] | None) -> str:
    parts: List[str] = []
    for r in rows:
        ctx = dict(r)
        if columns:
            filtered = {k: ctx.get(k, "") for k in columns}
            ctx.update(filtered)
        parts.append(_render_jinja(inner, ctx))
    return "".join(parts)


def render(subject_tpl: str, body_tpl: str, context: Dict[str, Any], rows: List[Dict[str, Any]]) -> Tuple[str, str]:
    subject = _render_jinja(subject_tpl, context)
    body = body_tpl
    out: List[str] = []
    pos = 0
    while True:
        m = TABLE_OPEN_RE.search(body, pos)
        if not m:
            out.append(body[pos:])
            break
        start, end = m.span()
        out.append(body[pos:start])
        cols_spec = m.group(1)
        columns = None
        if cols_spec:
            columns = [c.strip() for c in cols_spec.split(",") if c.strip()]
        close_idx = body.find(TABLE_CLOSE, end)
        if close_idx == -1:
            raise ValueError("TABLE block not closed")
        inner = body[end:close_idx]
        out.append(_render_table_block(inner, rows, columns))
        pos = close_idx + len(TABLE_CLOSE)
    body_joined = "".join(out)
    body_rendered = _render_jinja(body_joined, context)
    body_rendered = body_rendered.replace("\r\n", "\n").replace("\r", "\n")
    subject = subject.replace("\r\n", "\n").replace("\r", "\n").strip()
    return subject, body_rendered
