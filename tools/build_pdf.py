# ================================================================
# 📘 Neoway Build PDF v7.6 修正版 — 调用 latex_inject
# ================================================================
import os, subprocess, platform, sys, shutil
from pathlib import Path
from datetime import datetime

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.render_rst import *
from tools.latex_inject import inject_latex_block  # ✅ 现在定义存在

LANG = "zh"
MODEL_NAME = "N706B"
VERSION = "v1.4"
DOC_TYPE = "AT 命令手册"
AUTHOR = "Neoway 文档工程组"

PROJECT_ROOT = Path.cwd()
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / "docs" / MODEL_NAME / "source" / "conf.py").exists():
        PROJECT_ROOT = p
        break

ROOT_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
conf_path = ROOT_DIR / "conf.py"

print("🧩 生成 RST 文件中（CSV → RST）...")
subprocess.run([sys.executable, "tools/render_rst.py"], check=True)
print("✅ RST 生成完成，准备构建 PDF。")

inject_latex_block(conf_path, f"Neoway {MODEL_NAME} {DOC_TYPE}", AUTHOR, MODEL_NAME, VERSION)

subprocess.run(["sphinx-build", "-b", "latex", str(ROOT_DIR), str(LATEX_DIR)], check=True)
common_static = PROJECT_ROOT / "docs" / "_common" / "_static"
dest_common = LATEX_DIR / "_common" / "_static"
if common_static.exists():
    shutil.copytree(common_static, dest_common, dirs_exist_ok=True)
    print(f"✅ 已复制背景图到 {dest_common}")

os.chdir(LATEX_DIR)
tex_main = next(LATEX_DIR.glob("*.tex"))
for i in range(2):
    print(f"🌀 XeLaTeX 第 {i+1}/2 轮 …")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
out_pdf = PDF_DIR / f"Neoway_{MODEL_NAME}_{DOC_TYPE}_{VERSION}.pdf".replace(" ", "_")
if pdfs:
    shutil.copy2(pdfs[0], out_pdf)
    print(f"🎉 成功生成 PDF：{out_pdf}")
else:
    print("❌ 未生成 PDF。")
