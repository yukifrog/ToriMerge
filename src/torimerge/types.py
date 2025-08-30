from pathlib import Path
from typing import TypedDict, List, Dict, Any


class RowDict(TypedDict, total=False):
    sheet: str
    key: str
    to: str
    cc: str
    bcc: str
    attach_paths: str


class GroupedEmail(TypedDict):
    key: str
    to: List[str]
    cc: List[str]
    bcc: List[str]
    attachments: List[Path]
    rows: List[Dict[str, Any]]
    context: Dict[str, Any]
