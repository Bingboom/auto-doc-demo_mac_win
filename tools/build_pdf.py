# tools/build_pdf.py
# ================================================================
# 📘 Neoway Build PDF v7.7 — 调用 latex_inject（稳定版）
# ================================================================
import os, shutil, subprocess, sys, platform
from pathlib import Path
from datetime import datetime

# 项目信息
LANG = "zh"
MODEL_NAME = "N706B"
VERSION = "v1.4"
DOC_TYPE = "AT 命令手册"
AUTHOR = "Neoway 文档工程组"

# 路径
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.render_rst import *  # 生成 RST
from tools.latex_inject import inject_latex_block

# 寻找 conf.py
PROJECT_ROOT = Path.cwd()
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / "docs" / MODEL_NAME / "source" / "conf.py").exists():
        PROJECT_ROOT = p
        break
else:
    raise FileNotFoundError("❌ 未找到 docs/{MODEL_NAME}/source/conf.py")

ROOT_DIR  = PROJECT_ROOT / "docs" / MODEL_NAME / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR   = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
conf_path = ROOT_DIR / "conf.py"

# 1) 生成 RST
print("🧩 生成 RST 文件中（CSV → RST）...")
subprocess.run([sys.executable, str(PROJECT_ROOT / "tools" / "render_rst.py")], check=True)
print("✅ RST 生成完成，准备注入 LaTeX。")

# 2) 注入 LaTeX 样式（幂等）
inject_latex_block(
    conf_path=conf_path,
    title=f"Neoway {MODEL_NAME} {DOC_TYPE}",
    author=AUTHOR,
    model_name=MODEL_NAME,
    version=VERSION,
    doc_type=DOC_TYPE
)
print("✅ LaTeX 样式注入完成。")

# 3) 构建 LaTeX
subprocess.run(["sphinx-build", "-b", "latex", str(ROOT_DIR), str(LATEX_DIR)], check=True)

# 4) 同步公共资源
common_static = PROJECT_ROOT / "docs" / "_common" / "_static"
dest_common   = LATEX_DIR / "_common" / "_static"
if common_static.exists():
    shutil.copytree(common_static, dest_common, dirs_exist_ok=True)
    print(f"✅ 已复制公共资源到：{dest_common}")

# 5) 编译 PDF（XeLaTeX 两轮）
os.chdir(LATEX_DIR)
tex_main = next(LATEX_DIR.glob("*.tex"))
for i in range(2):
    print(f"🌀 XeLaTeX 第 {i+1}/2 轮 …")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

# 6) 输出 PDF
version_tag = "V" + VERSION.lstrip("vV")
out_name = f"Neoway_{MODEL_NAME}_{DOC_TYPE}_{version_tag}.pdf".replace(" ", "_")
pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if not pdfs:
    raise SystemExit("❌ 未生成 PDF，请检查 LaTeX 日志。")
out_pdf = PDF_DIR / out_name
shutil.copy2(pdfs[0], out_pdf)
print(f"🎉 成功生成 PDF：{out_pdf}")
