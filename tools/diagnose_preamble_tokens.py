import re
from pathlib import Path

def scan_tex(tex_file):
    tex = Path(tex_file).read_text(encoding="utf-8", errors="ignore")

    suspicious = [
        "xcolor", "VerbatimColor", "InnerLinkColor",
        "titlesec", "espTitleRed"
    ]

    print("\n===== Searching raw preamble leaks in TEX =====")
    for token in suspicious:
        for line in tex.splitlines():
            if token in line and not line.strip().startswith("\\"):
                print(f"[FOUND] Text leak: '{token}' in line → {line.strip()}")

    # 再检查是否有未闭合的大括号
    print("\n===== Checking brace balance =====")
    open_braces  = tex.count("{")
    close_braces = tex.count("}")
    print(f"{{ count = {open_braces}, }} count = {close_braces}")
    if open_braces != close_braces:
        print("⚠ 可能存在未闭合的 } 导致 token 泄漏！")

    # 定位 tokens 出现在哪个 block
    print("\n===== Detailed context (5 lines around each token) =====")
    lines = tex.splitlines()
    for i, line in enumerate(lines):
        for token in suspicious:
            if token in line:
                print(f"\n--- Token '{token}' at line {i+1} ---")
                for j in range(max(0, i-4), min(len(lines), i+5)):
                    print(f"{j+1:4d}: {lines[j]}")


if __name__ == "__main__":
    tex_file = "docs/zh_cn/N706B/build/pdf/N706B_AT.tex"
    scan_tex(tex_file)
