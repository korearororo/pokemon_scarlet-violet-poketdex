import sys
import webbrowser
import shutil
from pathlib import Path


def base_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def runtime_data_dir() -> Path:
    local = Path.home() / "AppData" / "Local" / "SVGuideLauncher"
    local.mkdir(parents=True, exist_ok=True)
    return local


def prepare_runtime_files(src_root: Path) -> Path:
    src = src_root / "SV_files"
    dst = runtime_data_dir() / "SV_files"
    if not src.exists():
        return src
    # onefile 실행 시 _MEIPASS는 프로세스 종료와 함께 정리되므로,
    # 브라우저가 계속 읽을 수 있도록 고정 경로로 복사한다.
    shutil.copytree(src, dst, dirs_exist_ok=True)
    return dst


def main() -> int:
    root = prepare_runtime_files(base_dir())
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

    url = html_file.resolve().as_uri()
    webbrowser.open(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
