#!/usr/bin/env python3
"""Beautiful desktop viewer for PROGRESS.md."""

from __future__ import annotations

import argparse
import pathlib
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText


DEFAULT_FILE = pathlib.Path("/Users/annakucenko/shale-relax/PROGRESS.md")
REFRESH_MS = 2500


class ProgressViewer:
    def __init__(self, root: tk.Tk, file_path: pathlib.Path) -> None:
        self.root = root
        self.file_path = file_path
        self.last_snapshot = ""
        self.auto_refresh_enabled = tk.BooleanVar(value=True)

        self.root.title("Shale Relax - PROGRESS.md Viewer")
        self.root.geometry("1100x760")
        self.root.configure(bg="#f3f4f6")

        self._build_style()
        self._build_layout()
        self.load_and_render()
        self._schedule_refresh()

    def _build_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Top.TFrame", background="#f3f4f6")
        style.configure(
            "Title.TLabel",
            background="#f3f4f6",
            foreground="#111827",
            font=("TkDefaultFont", 16, "bold"),
        )
        style.configure(
            "Path.TLabel",
            background="#f3f4f6",
            foreground="#4b5563",
            font=("TkDefaultFont", 10),
        )
        style.configure(
            "Accent.TButton",
            background="#1d4ed8",
            foreground="#ffffff",
            borderwidth=0,
            font=("TkDefaultFont", 10, "bold"),
            padding=(12, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
            foreground=[("disabled", "#94a3b8")],
        )
        style.configure(
            "Switch.TCheckbutton",
            background="#f3f4f6",
            foreground="#1f2937",
            font=("TkDefaultFont", 10),
        )

    def _build_layout(self) -> None:
        outer = ttk.Frame(self.root, style="Top.TFrame", padding=18)
        outer.pack(fill="both", expand=True)

        top = ttk.Frame(outer, style="Top.TFrame")
        top.pack(fill="x")

        title = ttk.Label(top, text="Project Progress Dashboard", style="Title.TLabel")
        title.grid(row=0, column=0, sticky="w")

        path_label = ttk.Label(top, text=str(self.file_path), style="Path.TLabel")
        path_label.grid(row=1, column=0, sticky="w", pady=(2, 10))

        controls = ttk.Frame(top, style="Top.TFrame")
        controls.grid(row=0, column=1, rowspan=2, sticky="e")
        top.columnconfigure(0, weight=1)

        ttk.Checkbutton(
            controls,
            text="Auto refresh",
            style="Switch.TCheckbutton",
            variable=self.auto_refresh_enabled,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            controls,
            text="Refresh now",
            style="Accent.TButton",
            command=self.load_and_render,
        ).pack(side="left")

        text_container = tk.Frame(
            outer, bg="#ffffff", highlightthickness=1, highlightbackground="#d1d5db"
        )
        text_container.pack(fill="both", expand=True)

        self.text = ScrolledText(
            text_container,
            wrap="word",
            bg="#ffffff",
            fg="#111827",
            insertbackground="#111827",
            relief="flat",
            padx=24,
            pady=20,
            font=("TkTextFont", 13),
            spacing1=3,
            spacing2=2,
            spacing3=3,
        )
        self.text.pack(fill="both", expand=True)
        self.text.insert("end", "Loading file...\n")
        # Keep widget in normal state for macOS compatibility.
        # Some Tk builds render blank/white content when Text is disabled.
        self.text.bind("<Key>", lambda event: "break")
        self.text.bind("<<Paste>>", lambda event: "break")
        self.text.bind("<Button-3>", lambda event: "break")
        self._configure_tags()

    def _configure_tags(self) -> None:
        self.text.tag_configure("h1", foreground="#111827", font=("TkDefaultFont", 22, "bold"), spacing1=10, spacing3=12)
        self.text.tag_configure("h2", foreground="#1e3a8a", font=("TkDefaultFont", 17, "bold"), spacing1=8, spacing3=10)
        self.text.tag_configure("h3", foreground="#1d4ed8", font=("TkDefaultFont", 14, "bold"), spacing1=6, spacing3=8)
        self.text.tag_configure("normal", foreground="#111827", font=("TkTextFont", 13))
        self.text.tag_configure("muted", foreground="#4b5563", font=("TkTextFont", 12))
        self.text.tag_configure("check_done", foreground="#047857", font=("TkTextFont", 13))
        self.text.tag_configure("check_todo", foreground="#b45309", font=("TkTextFont", 13))
        self.text.tag_configure("table", foreground="#334155", font=("TkFixedFont", 12))
        self.text.tag_configure("divider", foreground="#94a3b8", font=("TkFixedFont", 12))

    def _schedule_refresh(self) -> None:
        self.root.after(REFRESH_MS, self._refresh_tick)

    def _refresh_tick(self) -> None:
        if self.auto_refresh_enabled.get():
            self.load_and_render(show_popup=False)
        self._schedule_refresh()

    def _insert_line(self, line: str, tag: str) -> None:
        self.text.insert("end", line + "\n", tag)

    def load_and_render(self, show_popup: bool = True) -> None:
        try:
            content = self.file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            if show_popup:
                messagebox.showerror("File not found", f"Cannot find file:\n{self.file_path}")
            return
        except OSError as exc:
            if show_popup:
                messagebox.showerror("Read error", f"Cannot open file:\n{exc}")
            return

        if content == self.last_snapshot:
            return

        self.last_snapshot = content
        self.text.delete("1.0", "end")
        try:
            self._render_markdown(content)
        except Exception as exc:
            self.text.insert(
                "end",
                "Render fallback mode.\n\n"
                f"Reason: {exc}\n\n"
                "Raw file content:\n\n",
                "muted",
            )
            self.text.insert("end", content, "normal")
        self.text.see("1.0")

    def _render_markdown(self, content: str) -> None:
        for raw_line in content.splitlines():
            line = raw_line.rstrip()

            if line.startswith("# "):
                self._insert_line(line[2:].strip(), "h1")
            elif line.startswith("## "):
                self._insert_line(line[3:].strip(), "h2")
            elif line.startswith("### "):
                self._insert_line(line[4:].strip(), "h3")
            elif line.startswith("- [x] "):
                self._insert_line("  ✓ " + line[6:], "check_done")
            elif line.startswith("- [ ] "):
                self._insert_line("  ○ " + line[6:], "check_todo")
            elif line.startswith("|") and line.endswith("|"):
                self._insert_line(line, "table")
            elif set(line) == {"-"} and len(line) >= 3:
                self._insert_line("─" * min(len(line), 72), "divider")
            elif not line.strip():
                self._insert_line("", "muted")
            elif line.startswith("Последнее обновление"):
                self._insert_line(line, "muted")
            else:
                self._insert_line(line, "normal")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Beautiful viewer for markdown progress file")
    parser.add_argument(
        "--file",
        type=pathlib.Path,
        default=DEFAULT_FILE,
        help="Path to markdown file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = tk.Tk()
    ProgressViewer(root, args.file.expanduser().resolve())
    root.mainloop()


if __name__ == "__main__":
    main()
