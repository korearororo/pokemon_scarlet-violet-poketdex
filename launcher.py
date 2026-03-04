import os
import shutil
import subprocess
import sys
import traceback
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

APP_NAME = "SVGuideLauncher"


def base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def runtime_root() -> Path:
    local_app_data = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    root = local_app_data / APP_NAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def log_path() -> Path:
    return runtime_root() / "launcher.log"


def write_log(message: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with log_path().open("a", encoding="utf-8") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        pass


def current_bundle_id() -> str:
    try:
        if getattr(sys, "frozen", False):
            exe = Path(sys.executable)
            stat = exe.stat()
            return f"exe:{stat.st_size}:{stat.st_mtime_ns}"
        src = base_dir() / "SV_files"
        stat = src.stat()
        return f"src:{stat.st_size}:{stat.st_mtime_ns}"
    except Exception:
        return "unknown"


def runtime_data_dir() -> Path:
    dst = runtime_root() / "SV_files"
    marker = runtime_root() / ".bundle_id"
    src = base_dir() / "SV_files"

    if not src.exists():
        write_log(f"Source SV_files not found: {src}")
        return src

    bundle_id = current_bundle_id()
    marker_id = marker.read_text(encoding="utf-8").strip() if marker.exists() else ""

    if dst.exists() and (dst / "SV_공략집.html").exists() and marker_id == bundle_id:
        write_log("Using cached runtime data")
        return dst

    write_log(f"Sync runtime data: src={src} -> dst={dst}")
    shutil.copytree(src, dst, dirs_exist_ok=True)
    marker.write_text(bundle_id, encoding="utf-8")
    return dst


def pick_html(root: Path) -> Optional[Path]:
    candidates = sorted(root.glob("*.html"))
    if not candidates:
        return None

    exact = [p for p in candidates if p.stem == "SV_공략집"]
    if exact:
        return exact[0]

    preferred = [p for p in candidates if "공략" in p.stem]
    if preferred:
        return preferred[0]

    preferred = [p for p in candidates if "guide" in p.stem.lower()]
    if preferred:
        return preferred[0]

    return candidates[0]


def find_app_browser() -> Optional[str]:
    candidates = [
        shutil.which("msedge"),
        shutil.which("chrome"),
        shutil.which("brave"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]
    for item in candidates:
        if not item:
            continue
        p = Path(item)
        if p.exists():
            return str(p)
    return None


def open_html_app_window(html_file: Path) -> bool:
    browser = find_app_browser()
    if not browser:
        write_log("No app-capable browser found")
        return False

    url = html_file.resolve().as_uri()
    args = [
        browser,
        "--app=" + url,
        "--new-window",
        "--window-size=1360,900",
        "--disable-features=msEdgeSidebarV2",
    ]
    try:
        subprocess.Popen(args, close_fds=True)
        write_log(f"Opened via app-window browser: {browser}")
        return True
    except Exception as exc:
        write_log(f"app-window open failed: {exc}")
        return False


def open_html(html_file: Path) -> bool:
    url = html_file.resolve().as_uri()
    write_log(f"Opening html: {html_file}")

    # 0) Standalone app-like window (preferred)
    if open_html_app_window(html_file):
        return True

    # 1) Standard browser open
    try:
        if webbrowser.open(url, new=2):
            write_log("Opened via webbrowser.open")
            return True
    except Exception as exc:
        write_log(f"webbrowser.open failed: {exc}")

    # 2) Windows shell open file association
    try:
        os.startfile(str(html_file))  # type: ignore[attr-defined]
        write_log("Opened via os.startfile")
        return True
    except Exception as exc:
        write_log(f"os.startfile failed: {exc}")

    # 3) cmd start fallback
    try:
        subprocess.Popen(["cmd", "/c", "start", "", str(html_file)], close_fds=True)
        write_log("Opened via cmd start")
        return True
    except Exception as exc:
        write_log(f"cmd start failed: {exc}")

    return False


def show_error(message: str) -> None:
    write_log(f"ERROR: {message}")
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, message, "SV Guide Launcher", 0x10)
    except Exception:
        pass


def main() -> int:
    try:
        root = runtime_data_dir()
        if not root.exists():
            show_error(f"SV_files folder not found:\n{root}")
            return 1

        html_file = pick_html(root)
        if html_file is None:
            show_error(f"No html file found in:\n{root}")
            return 1

        if not open_html(html_file):
            show_error(
                "Could not open the guide page.\n"
                "Check browser availability, then retry.\n\n"
                f"Path: {html_file}\n"
                f"Log: {log_path()}"
            )
            return 1

        return 0
    except Exception:
        write_log(traceback.format_exc())
        show_error(
            "Launcher crashed unexpectedly.\n\n"
            f"Log: {log_path()}"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
