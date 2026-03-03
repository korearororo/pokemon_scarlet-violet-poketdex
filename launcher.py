import os
import socket
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote
import tkinter as tk


def base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def find_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def run_server(root: Path, port: int) -> ThreadingHTTPServer:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root), **kwargs)

        def log_message(self, _format: str, *_args) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def main() -> int:
    root = base_dir() / "SV_files"
    if not root.exists():
        print("SV_files 폴더를 찾을 수 없습니다:", root)
        return 1

    html_file = root / "SV_공략집.html"
    if not html_file.exists():
        html_candidates = sorted(root.glob("*.html"))
        if not html_candidates:
            print("HTML 파일을 찾을 수 없습니다.")
            return 1
        html_file = html_candidates[0]

    port = find_port()
    server = run_server(root, port)
    url = f"http://127.0.0.1:{port}/{quote(html_file.name)}"
    webbrowser.open(url)

    app = tk.Tk()
    app.title("SV 공략집 실행기")
    app.geometry("520x140")
    app.resizable(False, False)

    label = tk.Label(
        app,
        text="브라우저에서 공략집을 열었습니다.\n종료하려면 아래 버튼을 누르세요.",
        justify="left",
        font=("Malgun Gothic", 10),
    )
    label.pack(padx=16, pady=(16, 8), anchor="w")

    url_label = tk.Label(app, text=url, fg="#1d4ed8", font=("Consolas", 9))
    url_label.pack(padx=16, pady=(0, 8), anchor="w")

    def on_exit() -> None:
        try:
            server.shutdown()
            server.server_close()
        finally:
            app.destroy()

    btn_frame = tk.Frame(app)
    btn_frame.pack(fill="x", padx=16, pady=(0, 12))
    tk.Button(btn_frame, text="브라우저 다시 열기", command=lambda: webbrowser.open(url)).pack(side="left")
    tk.Button(btn_frame, text="종료", command=on_exit).pack(side="right")

    app.protocol("WM_DELETE_WINDOW", on_exit)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
