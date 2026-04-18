#!/usr/bin/env python3
"""Portable macOS Markdown viewer (local web app, no external deps)."""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import socketserver
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler


DEFAULT_FILE = pathlib.Path("/Users/annakucenko/shale-relax/PROGRESS.md")
HOST = "127.0.0.1"
PORT = 8765


def inline_md(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    out: list[str] = []
    in_ul = False
    in_table = False
    table_rows: list[list[str]] = []

    def close_list() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        if table_rows:
            header = table_rows[0]
            body = table_rows[1:]
            out.append("<table><thead><tr>")
            for cell in header:
                out.append(f"<th>{inline_md(cell.strip())}</th>")
            out.append("</tr></thead><tbody>")
            for row in body:
                # Skip markdown table separator rows.
                normalized = "".join(row).replace("-", "").replace(":", "").strip()
                if not normalized:
                    continue
                out.append("<tr>")
                for cell in row:
                    out.append(f"<td>{inline_md(cell.strip())}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
        in_table = False
        table_rows = []

    for line in lines:
        raw = line.rstrip()
        stripped = raw.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            close_list()
            if not in_table:
                in_table = True
            parts = [c.strip() for c in stripped.strip("|").split("|")]
            table_rows.append(parts)
            continue
        else:
            close_table()

        if not stripped:
            close_list()
            out.append("<p class='spacer'></p>")
            continue

        if stripped == "---":
            close_list()
            out.append("<hr />")
            continue

        if stripped.startswith("### "):
            close_list()
            out.append(f"<h3>{inline_md(stripped[4:])}</h3>")
            continue
        if stripped.startswith("## "):
            close_list()
            out.append(f"<h2>{inline_md(stripped[3:])}</h2>")
            continue
        if stripped.startswith("# "):
            close_list()
            out.append(f"<h1>{inline_md(stripped[2:])}</h1>")
            continue

        if stripped.startswith("- [x] "):
            if not in_ul:
                in_ul = True
                out.append("<ul>")
            out.append(f"<li class='done'>✓ {inline_md(stripped[6:])}</li>")
            continue
        if stripped.startswith("- [ ] "):
            if not in_ul:
                in_ul = True
                out.append("<ul>")
            out.append(f"<li class='todo'>○ {inline_md(stripped[6:])}</li>")
            continue

        close_list()
        out.append(f"<p>{inline_md(raw)}</p>")

    close_list()
    close_table()
    return "\n".join(out)


def app_html(default_path: pathlib.Path) -> str:
    safe_path = html.escape(str(default_path))
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MD Viewer for macOS</title>
  <style>
    :root {{
      --bg: #0b1220;
      --panel: #111b2f;
      --panel-2: #16233f;
      --text: #e6edf6;
      --muted: #8ea0bd;
      --accent: #4f8cff;
      --ok: #36c78a;
      --warn: #f7b955;
      --line: #24385c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; background: linear-gradient(160deg, #09101d, #0f1a2f 55%, #122243);
      color: var(--text); font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      min-height: 100vh;
    }}
    .shell {{ max-width: 1100px; margin: 24px auto; padding: 0 16px; }}
    .top {{
      background: color-mix(in srgb, var(--panel), #fff 3%);
      border: 1px solid var(--line); border-radius: 14px; padding: 14px;
      display: grid; gap: 10px;
    }}
    .row {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
    .title {{ font-size: 22px; font-weight: 700; }}
    input[type="text"] {{
      flex: 1; min-width: 300px; background: #0d1629; color: var(--text);
      border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px;
    }}
    button {{
      background: var(--accent); color: white; border: 0; border-radius: 10px;
      padding: 10px 14px; cursor: pointer; font-weight: 600;
    }}
    button.secondary {{ background: #233a66; }}
    .hint {{ color: var(--muted); font-size: 13px; }}
    .card {{
      margin-top: 14px; background: color-mix(in srgb, var(--panel-2), #fff 2%);
      border: 1px solid var(--line); border-radius: 14px; padding: 24px;
      box-shadow: 0 20px 50px rgba(3, 9, 20, 0.45);
    }}
    .status {{ color: var(--muted); margin-bottom: 10px; }}
    h1, h2, h3 {{ margin: 0.9em 0 0.35em; line-height: 1.3; }}
    h1 {{ font-size: 2rem; color: #f2f6ff; }}
    h2 {{ font-size: 1.5rem; color: #cfe0ff; }}
    h3 {{ font-size: 1.2rem; color: #b9d2ff; }}
    p {{ margin: 0.25em 0; }}
    ul {{ margin: 0.35em 0 0.8em 0; padding: 0; list-style: none; }}
    li {{ margin: 0.25em 0; padding-left: 0.2em; }}
    li.done {{ color: var(--ok); }}
    li.todo {{ color: var(--warn); }}
    code {{
      background: #0d1629; border: 1px solid var(--line);
      border-radius: 6px; padding: 0.1em 0.35em;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.92em;
    }}
    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
    th, td {{ border: 1px solid var(--line); padding: 8px 10px; text-align: left; }}
    th {{ background: #172845; }}
    hr {{ border: 0; border-top: 1px solid var(--line); margin: 14px 0; }}
    .spacer {{ margin: 8px 0; }}
    .error {{ color: #ff9b9b; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <div class="shell">
    <div class="top">
      <div class="row">
        <div class="title">Markdown Viewer (macOS portable)</div>
      </div>
      <div class="row">
        <input id="path" type="text" value="{safe_path}" />
        <button onclick="loadMd()">Открыть</button>
        <button class="secondary" onclick="pickFile()">Выбрать файл</button>
        <button class="secondary" onclick="toggleAuto()" id="autoBtn">Авто: ВКЛ</button>
      </div>
      <div class="hint">Поддержка: абсолютный путь к .md или выбор файла через диалог.</div>
    </div>
    <div class="card">
      <div class="status" id="status">Загрузка...</div>
      <div id="content"></div>
    </div>
  </div>
  <script>
    let timer = null;
    let auto = true;

    function status(text) {{
      document.getElementById("status").textContent = text;
    }}

    async function loadMd() {{
      const path = document.getElementById("path").value.trim();
      if (!path) {{
        status("Укажите путь к файлу.");
        return;
      }}
      status("Читаю файл...");
      const res = await fetch("/api/render?path=" + encodeURIComponent(path));
      const data = await res.json();
      const content = document.getElementById("content");
      if (!data.ok) {{
        content.innerHTML = "<div class='error'>" + data.error + "</div>";
        status("Ошибка чтения.");
        return;
      }}
      content.innerHTML = data.html;
      status("Готово: " + data.path);
    }}

    async function pickFile() {{
      const res = await fetch("/api/pick-file");
      const data = await res.json();
      if (!data.ok) {{
        status(data.error || "Не удалось выбрать файл.");
        return;
      }}
      document.getElementById("path").value = data.path;
      await loadMd();
    }}

    function tick() {{
      if (auto) loadMd();
      timer = setTimeout(tick, 2500);
    }}

    function toggleAuto() {{
      auto = !auto;
      document.getElementById("autoBtn").textContent = auto ? "Авто: ВКЛ" : "Авто: ВЫКЛ";
    }}

    loadMd();
    tick();
  </script>
</body>
</html>"""


class ViewerHandler(BaseHTTPRequestHandler):
    default_file = DEFAULT_FILE

    def log_message(self, _format: str, *args) -> None:
        return

    def _send_json(self, status: int, body: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _send_html(self, status: int, body: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/":
            self._send_html(200, app_html(self.default_file))
            return

        if parsed.path == "/api/render":
            requested = query.get("path", [""])[0]
            if not requested:
                self._send_json(400, '{"ok":false,"error":"Path is empty"}')
                return

            path = pathlib.Path(requested).expanduser().resolve()
            try:
                text = path.read_text(encoding="utf-8")
            except Exception as exc:
                msg = json_escape(f"Cannot read file: {exc}")
                self._send_json(200, f'{{"ok":false,"error":"{msg}"}}')
                return

            rendered = markdown_to_html(text)
            safe_path = json_escape(str(path))
            safe_html = json_escape(rendered)
            self._send_json(200, f'{{"ok":true,"path":"{safe_path}","html":"{safe_html}"}}')
            return

        if parsed.path == "/api/pick-file":
            path = pick_file_dialog()
            if not path:
                self._send_json(200, '{"ok":false,"error":"Selection cancelled"}')
                return
            safe_path = json_escape(path)
            self._send_json(200, f'{{"ok":true,"path":"{safe_path}"}}')
            return

        self._send_html(404, "<h1>Not found</h1>")


def json_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "")
        .replace("\t", "\\t")
    )


def pick_file_dialog() -> str | None:
    script = (
        'set selectedFile to choose file with prompt "Выберите Markdown файл" '
        'of type {"md","markdown","txt"}\n'
        "POSIX path of selectedFile"
    )
    import subprocess

    try:
        proc = subprocess.run(
            ["osascript", "-e", script], check=True, capture_output=True, text=True
        )
        return proc.stdout.strip() or None
    except Exception:
        return None


def run_server(default_file: pathlib.Path, open_browser: bool, port: int) -> None:
    ViewerHandler.default_file = default_file

    class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    chosen_port = port
    server = None
    for p in range(port, port + 20):
        try:
            server = ThreadingServer((HOST, p), ViewerHandler)
            chosen_port = p
            break
        except OSError:
            continue
    if server is None:
        raise OSError(f"Cannot bind to ports {port}..{port+19}")

    with server as httpd:
        url = f"http://{HOST}:{chosen_port}/"
        print(f"MD Viewer is running: {url}", flush=True)
        if open_browser:
            threading.Timer(0.25, lambda: webbrowser.open(url)).start()
        httpd.serve_forever()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Portable Markdown viewer for macOS")
    parser.add_argument("--file", type=pathlib.Path, default=DEFAULT_FILE, help="Default markdown file")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    parser.add_argument("--port", type=int, default=PORT, help="Preferred local port")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_server(
        args.file.expanduser().resolve(),
        open_browser=not args.no_browser,
        port=args.port,
    )


if __name__ == "__main__":
    main()
