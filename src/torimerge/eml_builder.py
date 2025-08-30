from __future__ import annotations
from email.message import EmailMessage
from email.policy import SMTP
from pathlib import Path
from typing import List


def build_eml(
    to: List[str],
    cc: List[str],
    bcc: List[str],
    subject: str,
    body: str,
    attachments: List[Path],
    output_dir: Path,
    filename_hint: str,
) -> Path:
    msg = EmailMessage()
    if to:
        msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject
    msg.set_content(body, subtype="plain", charset="utf-8")
    for p in attachments:
        try:
            data = p.read_bytes()
        except Exception:
            continue
        msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=p.name)
    raw = msg.as_bytes(policy=SMTP)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in filename_hint) or "mail"
    out_path = output_dir / f"{safe_name}.eml"
    idx = 1
    while out_path.exists():
        out_path = output_dir / f"{safe_name}_{idx}.eml"
        idx += 1
    out_path.write_bytes(raw)
    return out_path
