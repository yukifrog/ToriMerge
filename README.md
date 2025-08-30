# ToriMerge

Windows tool to generate Thunderbird .eml drafts from Excel data and a text template.

- Excel: multiple sheets, grouping by key column, recipients in columns.
- Template: .txt only. 1st line is subject, blank line, then body. Placeholders: {{column_name}}. Repeating block: [[TABLE]]...[[/TABLE]] or [[TABLE:col1,col2]]...[[/TABLE]].
- Output: UTF-8 .eml files with CRLF, To/CC/BCC, multiple attachments.
- Interfaces prepared for future Oracle address book.

## Excel format
Required columns:
- key: groups multiple rows into one email
- to: one or more addresses separated by comma or semicolon
Optional columns:
- cc, bcc, attach_paths (comma/semicolon separated file paths), plus any data columns referenced in templates

## Usage (CLI)
torimerge --excel data.xlsx --template template.txt --output-dir out

## GUI
torimerge-gui

## Build (Windows)
Use PyInstaller spec in repository to build torimerge.exe and torimerge-gui.exe.
