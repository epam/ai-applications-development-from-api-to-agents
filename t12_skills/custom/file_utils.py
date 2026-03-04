from pathlib import Path


def get_file_content(path: Path) -> str:
    if not path.exists():
        return f"ERROR: File not found: {path}"

    if not path.is_file():
        return f"ERROR: Not a file: {path}"

    return path.read_text(encoding="utf-8")
