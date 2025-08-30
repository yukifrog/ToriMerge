from __future__ import annotations
from typing import Dict, List, Any
from pathlib import Path
from torimerge.types import GroupedEmail
from torimerge.excel_loader import parse_recipients, parse_attachments


def group_rows(rows: List[Dict[str, Any]], key_col: str = "key") -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        k = str(r.get(key_col, "")).strip()
        if not k:
            k = "_"
        groups.setdefault(k, []).append(r)
    return groups


def build_group_emails(groups: Dict[str, List[Dict[str, Any]]]) -> List[GroupedEmail]:
    result: List[GroupedEmail] = []
    for key, rows in groups.items():
        to: List[str] = []
        cc: List[str] = []
        bcc: List[str] = []
        att: List[Path] = []
        for r in rows:
            to += parse_recipients(r.get("to", ""))
            cc += parse_recipients(r.get("cc", ""))
            bcc += parse_recipients(r.get("bcc", ""))
            att += parse_attachments(r.get("attach_paths", ""))
        to = sorted(list(dict.fromkeys(to)))
        cc = sorted(list(dict.fromkeys(cc)))
        bcc = sorted(list(dict.fromkeys(bcc)))
        att_unique: List[Path] = []
        seen = set()
        for a in att:
            if a not in seen:
                seen.add(a)
                att_unique.append(a)
        base_context: Dict[str, Any] = {}
        if rows:
            base_context.update(rows[0])
        base_context["row_count"] = len(rows)
        result.append(
            GroupedEmail(
                key=key,
                to=to,
                cc=cc,
                bcc=bcc,
                attachments=att_unique,
                rows=rows,
                context=base_context,
            )
        )
    return result
