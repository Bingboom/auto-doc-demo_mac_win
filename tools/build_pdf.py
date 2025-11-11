# ================================================================
# 📘 Neoway Build PDF v8.0 — 企业集成版
# ================================================================
import subprocess, platform, shutil, os, sys
from pathlib import Path
from datetime import datetime

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.latex_inject import inject_latex_block
from docs._common import conf_common

MODEL = "N706B"
VERSION = "v1.4"
DOC_TYPE = "AT 命令手册"
AUTHOR = "Neoway 文档工程组"

PROJECT_DIR = PROJECT_ROOT / f"docs/{MODEL}/source"
BUILD_DIR = PROJECT_ROOT / f"docs/{MODEL}/build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
CONF_PATH = PROJECT_DIR / "conf.py"

print("🧩 Step 1: 注入 LaTeX 样式 …")
inject_latex_block(
    conf_path=CONF_PATH,
    model_name=MODEL,
    version=VERSION,
    doc_type=DOC_TYPE,
    author=AUTHOR,
    company=conf_common.COMPANY_NAME,
    zh_font=conf_common.get_fonts()["zh_font"],
    mono_font=conf_common.get_fonts()["mono_font"],
    date_cn=conf_common.get_date_cn(),
)
print("✅ LaTeX 样式注入完成。")

print("🧩 Step 2: 构建 Sphinx → LaTeX …")
subprocess.run(["sphinx-build", "-b", "latex", str(PROJECT_DIR), str(LATEX_DIR)], check=True)

print("🧩 Step 3: 编译 XeLaTeX …")
os.chdir(LATEX_DIR)
tex_main = next(LATEX_DIR.glob("*.tex"))
for i in range(2):
    print(f"🌀 XeLaTeX 第 {i+1}/2 轮 …")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

print("🧩 Step 4: 拷贝 PDF …")
version_label = VERSION.lstrip("vV")
out_pdf = PDF_DIR / f"Neoway_{MODEL}_{DOC_TYPE}_V{version_label}.pdf".replace(" ", "_")
pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if pdfs:
    shutil.copy2(pdfs[0], out_pdf)
    print(f"🎉 成功生成 PDF：{out_pdf}")
else:
    print("❌ 未生成 PDF，请检查 LaTeX 日志。")
