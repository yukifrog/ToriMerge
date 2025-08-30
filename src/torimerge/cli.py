from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
from typing import List
from .excel_loader import load_excel, required_columns_present
from .group_merge import group_rows, build_group_emails
from .template_engine import parse_template, render
from .eml_builder import build_eml


def main() -> None:
    ap = ArgumentParser(prog="torimerge")
    ap.add_argument("--excel", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--key-col", default="key")
    args = ap.parse_args()

    excel_path = Path(args.excel)
    template_path = Path(args.template)
    out_dir = Path(args.output_dir)

    rows = load_excel(excel_path)
    if not required_columns_present(rows, ["key", "to"]):
        raise SystemExit("Excel must include at least 'key' and 'to' columns")
    groups = group_rows(rows, key_col=args.key_col)
    grouped = build_group_emails(groups)
    subj_tpl, body_tpl = parse_template(template_path)
    count = 0
    outputs: List[Path] = []
    for g in grouped:
        subject, body = render(subj_tpl, body_tpl, g["context"], g["rows"])
        fname_hint = f"{g['key']}"
        p = build_eml(g["to"], g["cc"], g["bcc"], subject, body, g["attachments"], out_dir, fname_hint)
        outputs.append(p)
        count += 1
    print(f"Generated {count} draft(s)")
    for p in outputs:
        print(p.as_posix())
