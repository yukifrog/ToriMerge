from pathlib import Path
from torimerge.template_engine import render


def test_render_subject_body_and_table(tmp_path: Path):
    subject_tpl = "Hello {{name}}"
    body_tpl = "Start\n\n[[TABLE:val]]Row {{val}}\n[[/TABLE]]\nEnd {{name}}"
    ctx = {"name": "Alice"}
    rows = [{"val": "1"}, {"val": "2"}]
    subject, body = render(subject_tpl, body_tpl, ctx, rows)
    assert subject == "Hello Alice"
    assert "Row 1" in body and "Row 2" in body
    assert body.strip().endswith("End Alice")
