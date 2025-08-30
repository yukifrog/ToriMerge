from torimerge.group_merge import group_rows, build_group_emails


def test_grouping_and_aggregation():
    rows = [
        {"key": "A", "to": "a@example.com", "cc": "", "bcc": "", "attach_paths": ""},
        {"key": "A", "to": "b@example.com", "cc": "c@example.com", "bcc": "", "attach_paths": ""},
        {"key": "B", "to": "x@example.com;y@example.com", "cc": "", "bcc": "z@example.com", "attach_paths": ""},
    ]
    groups = group_rows(rows)
    grouped = build_group_emails(groups)
    gA = [g for g in grouped if g["key"] == "A"][0]
    assert set(gA["to"]) == {"a@example.com", "b@example.com"}
    assert set(gA["cc"]) == {"c@example.com"}
    gB = [g for g in grouped if g["key"] == "B"][0]
    assert set(gB["to"]) == {"x@example.com", "y@example.com"}
    assert set(gB["bcc"]) == {"z@example.com"}
