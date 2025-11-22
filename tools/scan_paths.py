import re
import os
from pathlib import Path

# ============================================================
# 硬编码模式（仅匹配业务相关路径，排除第三方库中的正则）
# ============================================================

PATTERNS = [
    # 用户绝对路径
    r"/Users/[A-Za-z0-9_\-]+/",
    r"/home/[A-Za-z0-9_\-]+/",
    # Windows 绝对路径
    r"[A-Za-z]:\\\\",  # C:\\
    r"[A-Za-z]:/",     # C:/
    # 相对路径
    r"\.\./",          # ../something
    r"\.\.\\",         # ..\something
    # 项目中的显式目录引用
    r"docs/",
    r"csv-input/",
]

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    "site-packages", "dist", "build"
}

# 只扫描这些目录（你的仓库范围）
TARGET_DIRS = [
    "tools",
    "docs",
    "csv-input",
    "."
]

# 扫描文件类型
TARGET_EXT = {".py", ".rst", ".md", ".j2", ".tex", ".txt"}


def is_excluded(path: Path) -> bool:
    """排除 venv、git、site-packages 等无关目录"""
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def scan_file(file_path: Path):
    findings = []
    try:
        text = file_path.read_text(encoding="utf-8")
    except:
        return findings

    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        for pat in PATTERNS:
            if re.search(pat, line):
                findings.append((i, pat, line.strip()))
                break
    return findings


def scan_repo():
    root = Path(".").resolve()
    print(f"[SCAN] Repository root: {root}\n")

    suspicious = 0

    for target in TARGET_DIRS:
        abs_target = root / target
        if not abs_target.exists():
            continue

        print(f"[SCAN] Directory: {target}\n")

        for file in abs_target.rglob("*"):
            if file.is_dir():
                if is_excluded(file):
                    continue
                else:
                    continue

            # 文件类型过滤
            if file.suffix.lower() not in TARGET_EXT:
                continue

            if is_excluded(file):
                continue

            results = scan_file(file)
            if not results:
                continue

            suspicious += len(results)
            print(f" ⚠️  File: {file.relative_to(root)}")

            for (line_no, pat, content) in results:
                print(f"    L{str(line_no).zfill(3)}: {content}")

            print("")

    print(f"\n====== 扫描完成，共发现 {suspicious} 个可疑路径 ======")


if __name__ == "__main__":
    scan_repo()
