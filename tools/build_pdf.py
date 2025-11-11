# ================================================================
# 📘 Neoway Build PDF v8.0 — 企业集成版
#    - 自动生成 RST
#    - 注入企业 LaTeX 样式（via latex_inject）
#    - 执行 XeLaTeX 双轮构建并输出版本化 PDF
# ================================================================
import os, shutil, subprocess, platform, sys
from pathlib import Path
from datetime import datetime

# === 环境初始化 ===
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# === 导入模块 ===
from tools.render_rst import *  # CSV → RST
from tools.latex_inject import inject_latex_block
from docs._common import conf_common as cfg

# === 基本信息（可修改） ===
LANG = "zh"
MODEL_NAME = "N706B"
VERSION = "v1.4"
DOC_TYPE = "AT 命令手册"
AUTHOR = cfg.PROJECT_AUTHOR

# === 路径定义 ===
PROJECT_ROOT = Path.cwd()
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / "docs" / MODEL_NAME / "source" / "conf.py").exists():
        PROJECT_ROOT = p
        break
else:
    raise FileNotFoundError("❌ 未找到 conf.py，请检查项目结构。")

ROOT_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
CONF_PATH = ROOT_DIR / "conf.py"

# ================================================================
# 🧩 STEP 1. 自动生成 RST 文件
# ================================================================
print("🧩 生成 RST 文件中（CSV → RST）...")
subprocess.run([sys.executable, "tools/render_rst.py"], check=True)
print("✅ RST 生成完成。")

# ================================================================
# 🧩 STEP 2. 注入企业 LaTeX 样式
# ================================================================
print("🧱 注入企业 LaTeX 样式块中…")
inject_latex_block(
    conf_path=CONF_PATH,
    title=f"Neoway {MODEL_NAME} {DOC_TYPE}",
    author=AUTHOR,
    model_name=MODEL_NAME,
    version=VERSION,
)
print("✅ LaTeX 样式注入完成。")

# ================================================================
# 🧩 STEP 3. 构建 Sphinx LaTeX
# ================================================================
print("📦 构建 Sphinx LaTeX 源文件中…")
subprocess.run(["sphinx-build", "-b", "latex", str(ROOT_DIR), str(LATEX_DIR)], check=True)
print("✅ LaTeX 源文件构建完成。")

# ================================================================
# 🧩 STEP 4. 复制公共静态资源
# ================================================================
common_static = PROJECT_ROOT / "docs" / "_common" / "_static"
dest_common = LATEX_DIR / "_common" / "_static"
if common_static.exists():
    shutil.copytree(common_static, dest_common, dirs_exist_ok=True)
    print(f"✅ 已复制公共资源 → {dest_common}")
else:
    print("⚠️ 未找到公共资源目录：docs/_common/_static")

# ================================================================
# 🧩 STEP 5. XeLaTeX 双轮编译
# ================================================================
os.chdir(LATEX_DIR)
tex_files = list(LATEX_DIR.glob("*.tex"))
if not tex_files:
    raise FileNotFoundError("❌ 未生成 .tex 文件，请检查 LaTeX 构建输出。")

tex_main = tex_files[0]
for i in range(2):
    print(f"🌀 XeLaTeX 第 {i+1}/2 轮编译：{tex_main.name}")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

# ================================================================
# 🧩 STEP 6. 输出最终 PDF
# ================================================================
version_tag = cfg.get_version_tag(VERSION)
out_pdf = PDF_DIR / f"Neoway_{MODEL_NAME}_{DOC_TYPE}_{version_tag}.pdf".replace(" ", "_")

pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if pdfs:
    shutil.copy2(pdfs[0], out_pdf)
    print(f"🎉 成功生成 PDF：{out_pdf}")
else:
    print("❌ 未生成 PDF，请检查 LaTeX 日志。")

# ================================================================
# 🧩 STEP 7. 日志 & 提示
# ================================================================
print("\n📘 构建流程完成")
print(f"  📂 源文件目录：{ROOT_DIR}")
print(f"  📄 输出 PDF：{out_pdf}")
print(f"  🕒 构建时间：{datetime.now():%Y-%m-%d %H:%M:%S}")
