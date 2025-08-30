from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd


def _norm_col(name: str) -> str:
    return str(name).strip().replace(" ", "_").lower()


def _split_multi(s: str) -> List[str]:
    if not s:
        return []
    parts = []
    for part in str(s).replace(";", ",").split(","):
        p = part.strip()
        if p:
            parts.append(p)
    return parts


def load_excel(path: Path) -> List[Dict[str, Any]]:
    x = pd.read_excel(path, sheet_name=None, dtype=str)
    rows: List[Dict[str, Any]] = []
    for sheet, df in x.items():
        df = df.fillna("").astype(str)
        df.columns = [_norm_col(c) for c in df.columns]
        for _, row in df.iterrows():
            d = {k: v.strip() for k, v in row.to_dict().items()}
            d["sheet"] = sheet
            rows.append(d)
    return rows


def parse_recipients(val: str) -> List[str]:
    return _split_multi(val)


def parse_attachments(val: str) -> List[Path]:
    return [Path(p).expanduser() for p in _split_multi(val)]


def required_columns_present(rows: List[Dict[str, Any]], required: List[str]) -> bool:
    if not rows:
        return False
    cols = set(rows[0].keys())
    return all(r in cols for r in required)
