# tools/check_latex_paths.py
from pathlib import Path

print("\n===== 🔍 Neoway LaTeX 路径总诊断 =====\n")

PROJECT = Path(__file__).resolve().parents[1]

paths_to_check = {
    "project_root": PROJECT,
    "expected_latex_dir": PROJECT / "docs" / "_common" / "latex",
    "expected_fonts": PROJECT / "docs" / "_common" / "latex" / "fonts.tex",
    "expected_cover_template": PROJECT / "docs" / "_common" / "latex" / "cover_template.tex.j2",
    "expected_preamble": PROJECT / "docs" / "_common" / "latex" / "base_preamble.tex",
}

for name, path in paths_to_check.items():
    print(f"[{name}] → {path}")
    if path.exists():
        print(f"  ✔ 存在")
    else:
        print(f"  ❌ 不存在")

print("\n===== 📌 分析 build_pdf.py 的实际路径 =====")

build_pdf_path = PROJECT / "tools" / "latex_cover.py"
if build_pdf_path.exists():
    text = build_pdf_path.read_text(encoding="utf-8")
    print("\n--- latex_cover.py 中的 PATHS 调用 ---")
    for line in text.splitlines():
        if "PATHS" in line:
            print(" ", line)
else:
    print("❌ latex_cover.py 不存在？")

print("\n===== 诊断输出结束 =====\n")
