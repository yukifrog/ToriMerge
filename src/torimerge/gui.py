from __future__ import annotations
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from .cli import main as cli_main


def _run_cli(excel: str, template: str, outdir: str, log_widget: tk.Text, run_btn: tk.Button):
    try:
        import sys
        sys.argv = ["torimerge", "--excel", excel, "--template", template, "--output-dir", outdir]
        cli_main()
        log_widget.insert(tk.END, "Done\n")
    except SystemExit as e:
        log_widget.insert(tk.END, f"Error: {e}\n")
        messagebox.showerror("ToriMerge", str(e))
    except Exception as e:
        log_widget.insert(tk.END, f"Error: {e}\n")
        messagebox.showerror("ToriMerge", str(e))
    finally:
        run_btn.config(state=tk.NORMAL)


def main() -> None:
    root = tk.Tk()
    root.title("ToriMerge")
    root.geometry("600x400")

    excel_var = tk.StringVar()
    template_var = tk.StringVar()
    outdir_var = tk.StringVar()

    def pick_excel():
        p = filedialog.askopenfilename(title="Select Excel", filetypes=[("Excel", "*.xlsx;*.xls")])
        if p:
            excel_var.set(p)

    def pick_template():
        p = filedialog.askopenfilename(title="Select Template", filetypes=[("Text", "*.txt")])
        if p:
            template_var.set(p)

    def pick_outdir():
        p = filedialog.askdirectory(title="Select Output Folder")
        if p:
            outdir_var.set(p)

    frm = tk.Frame(root)
    frm.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

    tk.Label(frm, text="Excel").grid(row=0, column=0, sticky="w")
    tk.Entry(frm, textvariable=excel_var, width=60).grid(row=0, column=1, sticky="we")
    tk.Button(frm, text="Browse", command=pick_excel).grid(row=0, column=2)

    tk.Label(frm, text="Template (.txt)").grid(row=1, column=0, sticky="w")
    tk.Entry(frm, textvariable=template_var, width=60).grid(row=1, column=1, sticky="we")
    tk.Button(frm, text="Browse", command=pick_template).grid(row=1, column=2)

    tk.Label(frm, text="Output Folder").grid(row=2, column=0, sticky="w")
    tk.Entry(frm, textvariable=outdir_var, width=60).grid(row=2, column=1, sticky="we")
    tk.Button(frm, text="Browse", command=pick_outdir).grid(row=2, column=2)

    log = tk.Text(root, height=12)
    log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    run_btn = tk.Button(root, text="Generate Drafts")
    run_btn.pack(pady=5)

    def run():
        if not excel_var.get() or not template_var.get() or not outdir_var.get():
            messagebox.showwarning("ToriMerge", "Please select Excel, Template and Output folder.")
            return
        run_btn.config(state=tk.DISABLED)
        log.delete("1.0", tk.END)
        t = threading.Thread(target=_run_cli, args=(excel_var.get(), template_var.get(), outdir_var.get(), log, run_btn))
        t.daemon = True
        t.start()

    run_btn.config(command=run)

    root.mainloop()
