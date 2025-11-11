# tools/build_pdf.py
# ================================================================
# 📘 Neoway Build PDF v8.1 — 企业配套版（与 latex_inject v3.3 兼容）
# ================================================================
import os, re, shutil, subprocess, platform, sys
from pathlib import Path
from datetime import datetime

# --- 工具导入 ---
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# --- 导入模块 ---
from tools.latex_inject import inject_latex_block
from docs._common import conf_common

# === 基础项目参数 ===
LANG = "zh"
MODEL_NAME = "N706B"
VERSION = "v1.4"

DOC_TYPE_CN = "AT 命令手册"
AUTHOR_CN = "Neoway 文档工程组"

# === 元信息生成 ===
DATE_STR = conf_common.get_date_str()
VERSION_TAG = conf_common.get_version_tag(VERSION)
TITLE = f"Neoway {MODEL_NAME} {DOC_TYPE_CN}"
AUTHOR = AUTHOR_CN
SUBJECT = f"Neoway 机密 | {MODEL_NAME} | {VERSION_TAG}"

# === 自动定位目录结构 ===
PROJECT_ROOT = Path.cwd()
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / "docs" / MODEL_NAME / "source" / "conf.py").exists():
        PROJECT_ROOT = p
        break
else:
    raise FileNotFoundError(f"❌ 未找到 conf.py，请确认 docs/{MODEL_NAME}/source 目录存在")

ROOT_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)

conf_path = ROOT_DIR / "conf.py"

# === 第一步：注入 LaTeX 块 ===
print("🧩 [1/4] 注入企业版 LaTeX 样式...")
inject_latex_block(
    conf_path=conf_path,
    title=TITLE,
    author=AUTHOR,
    model_name=MODEL_NAME,
    version=VERSION,
    doc_type=DOC_TYPE_CN,
    subject_prefix="Neoway 机密"
)

# === 第二步：生成 RST ===
print("📄 [2/4] 生成 RST 文件中（CSV → RST）...")
subprocess.run(["python", "tools/render_rst.py"], check=True)
print("✅ RST 生成完成")

# === 第三步：执行 Sphinx 构建 ===
print("🏗️ [3/4] 构建 Sphinx LaTeX ...")
subprocess.run(["sphinx-build", "-b", "latex", str(ROOT_DIR), str(LATEX_DIR)], check=True)

# === 第四步：同步公共资源 ===
common_static = PROJECT_ROOT / "docs" / "_common" / "_static"
dest_common = LATEX_DIR / "_common" / "_static"
if common_static.exists():
    shutil.copytree(common_static, dest_common, dirs_exist_ok=True)
    print(f"✅ 已复制公共资源 → {dest_common}")

# === 平台字体选择 ===
sys_name = platform.system().lower()
if "darwin" in sys_name or "mac" in sys_name:
    zh_font = "PingFang SC"
    mono_font = "Menlo"
elif "win" in sys_name:
    zh_font = "Microsoft YaHei"
    mono_font = "Consolas"
else:
    zh_font = "Noto Sans CJK SC"
    mono_font = "DejaVu Sans Mono"
print(f"🖋️ 当前平台字体：{zh_font} / {mono_font}")

# === XeLaTeX 编译 ===
os.chdir(LATEX_DIR)
tex_main = next(LATEX_DIR.glob("*.tex"), None)
if not tex_main:
    raise FileNotFoundError("❌ 未找到 .tex 文件，请检查 Sphinx 输出")

print("🌀 [4/4] 编译 PDF (2 轮 XeLaTeX)...")
for i in range(2):
    print(f"   → 第 {i+1}/2 轮 ...")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

# === 输出 PDF 命名 ===
version_label = VERSION_TAG.lstrip("Vv")
output_filename = f"Neoway_{MODEL_NAME}_{DOC_TYPE_CN}_V{version_label}.pdf".replace(" ", "_")
out_pdf = PDF_DIR / output_filename

pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if pdfs:
    shutil.copy2(pdfs[0], out_pdf)
    print(f"🎉 成功生成 PDF：{out_pdf}")
else:
    print("⚠️ 未生成 PDF，请检查 LaTeX 日志。")

print("✅ 全流程完成 — Build PDF v8.1 🚀")
