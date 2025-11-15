# tools/toc_mark_scanner_v7.py
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEX_DIR = ROOT / "docs" / "N706B" / "build" / "pdf" / "latex"

TARGET_PATTERNS = [
    r"\\markboth\{.*?\}",
    r"\\markright\{.*?\}",
    r"\\chaptermark",
    r"\\sectionmark",
    r"第\s*0\s*章",
]

def scan_file(path: Path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    findings = []

    for p in TARGET_PATTERNS:
        for m in re.finditer(p, txt):
            line_no = txt.count("\n", 0, m.start()) + 1
            snippet = txt[m.start():m.end()]
            findings.append((line_no, snippet))

    return findings


def main():
    print("===== 🔍 Neoway TOC 页眉污染源 深度扫描器 v7 =====")
    print(f"扫描目录：{LATEX_DIR}")
    print("--------------------------------------------------")

    if not LATEX_DIR.exists():
        print("❌ LaTeX 目录不存在，请先执行 build pdf")
        return

    tex_files = list(LATEX_DIR.glob("*.tex"))
    if not tex_files:
        print("❌ 未找到 .tex 文件")
        return

    all_hits = {}

    for f in tex_files:
        hits = scan_file(f)
        if hits:
            all_hits[f] = hits

    if not all_hits:
        print("✔ 未发现任何标记污染源，TOC 页眉应当纯净")
        return

    print("\n===== 🎯 扫描结果 =====")
    for path, hits in all_hits.items():
        print(f"\n📄 文件：{path.name}")
        for line, snip in hits:
            print(f"  - 第 {line} 行: {snip}")

    print("\n===== 分析指引 =====")
    print("""
1. 如果在 Neoway_N706B_Manual.tex 里出现:
       \\markboth{Contents}{Contents}
       或  \\markboth{}{Something}
       或  \\chaptermark
   → 这是目录页附带的隐式标记，会导致 “第 0 章” 再生。

2. 如果发现:
       第 0 章
   → 说明某段代码重新触发了章节计数（例如未完全替换 \\chapter*）

3. 如果来源来自:
       sphinxmanual.cls / sphinxlatexstylepage.sty
   → 说明你的 patch 注入顺序不够靠后，需要把 patch 放进最末尾 preamble。
""")

    print("\n===== 结束 =====")


if __name__ == "__main__":
    main()
