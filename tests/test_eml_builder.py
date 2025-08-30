from pathlib import Path
from torimerge.eml_builder import build_eml


def test_eml_crlf_and_headers(tmp_path: Path):
    out = build_eml(
        to=["a@example.com"],
        cc=["c@example.com"],
        bcc=["b@example.com"],
        subject="Sub",
        body="Line1\nLine2",
        attachments=[],
        output_dir=tmp_path,
        filename_hint="test",
    )
    data = out.read_bytes()
    assert b"\r\n" in data
    assert b"Subject: Sub" in data
    assert b"To: a@example.com" in data
