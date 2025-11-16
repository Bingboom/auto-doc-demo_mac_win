#!/usr/bin/env python3
# tools/build_pdf.py

import sys
import shutil
import subprocess
from pathlib import Path
import yaml
import importlib

# 加载 config.yaml 配置文件
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 获取配置
config = load_config()

# 使用 config.yaml 中的路径设置
ROOT = Path(config['root']).resolve()  # 获取项目根目录
TOOLS_DIR = Path(config['tools']).resolve()  # 获取 tools 目录
CSV_INPUT_DIR = Path(config['csv_input']).resolve()  # 获取 CSV 输入目录
TEMPLATES_DIR = Path(config['templates']).resolve()  # 获取模板目录
DOCS_DIR = Path(config['docs']).resolve()  # 获取 docs 目录
LATEX_DIR = Path(config['latex']).resolve()  # 获取 LaTeX 配置路径
IMAGES_DIR = Path(config['images']).resolve()  # 获取图片目录

# 获取产品线配置
product_line = config['default_product_line']
product_config = config['product_lines'][product_line]

# 获取产品线配置的路径
PRODUCT_DIR = Path(product_config['rst_source']).resolve()  # 获取文档源路径
BUILD_DIR = Path(product_config['build_pdf']).resolve()  # 获取输出路径
LATEX_BUILD_DIR = BUILD_DIR / "latex"
PDF_BUILD_DIR = BUILD_DIR 
PDF_BUILD_DIR.mkdir(parents=True, exist_ok=True)
CONF_PATH = PRODUCT_DIR / "conf.py"

# 确保 tools 目录被加入到 sys.path 中
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# 导入工具模块
from latex_cover import render_cover
from latex_styles import load_latex_styles
from latex_injector import inject_latex_block


# ---------------------------------------------------------
# 工具函数
# ---------------------------------------------------------
def run_cmd(cmd, cwd=None):
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=cwd)
    if p.returncode != 0:
        raise RuntimeError(f"命令失败：{' '.join(cmd)}")


def clean_latex_dir(pdf_dir: Path):
    """
    彻底清理所有旧构建文件，避免 xelatex 引用历史垃圾文件。
    绝不保留任何 tex/aux/log/index 文件。
    """
    exts = [
        ".aux", ".log", ".toc", ".out", ".idx",
        ".ind", ".ilg", ".lof", ".lot", ".fls", ".fdb_latexmk",
        ".tex"  # 🔥 关键：清除旧 tex（防止 projectnamenotset.tex 残留）
    ]
    for f in pdf_dir.iterdir():
        if f.suffix.lower() in exts:
            f.unlink()


def copy_static_assets():
    """
    只拷贝图片与必要资源，不拷贝任何 .tex 文件！！！
    否则 xelatex 会误当它们是主文件。
    """
    target = PDF_BUILD_DIR / "latex"
    target.mkdir(parents=True, exist_ok=True)

    latex_dir = LATEX_DIR
    static_dir = IMAGES_DIR

    # 允许的资源（图片 / 样式），禁止复制任何 .tex！
    allowed_suffix = [".png", ".jpg", ".jpeg", ".pdf", ".sty", ".cls"]

    if latex_dir.exists():
        for file in latex_dir.iterdir():
            if file.is_file() and file.suffix.lower() in allowed_suffix:
                shutil.copy(file, target)

    if static_dir.exists():
        for file in static_dir.iterdir():
            if file.is_file() and file.suffix.lower() in allowed_suffix:
                shutil.copy(file, target)


# ---------------------------------------------------------
# 主构建流程
# ---------------------------------------------------------
def build_pdf(model, version, doc_type, author):

    print("\n============================")
    print("🚀 开始构建 PDF")
    print("============================\n")

    # ① 生成封面 cover.tex（模板 cover_template.tex.j2）
    cover_path = LATEX_DIR / "cover_template.tex.j2"
    print("✔ 已生成封面：", cover_path)

    # ② 加载 LaTeX 样式（字体、公司名等）
    styles = load_latex_styles()

    # ③ 动态导入 inject_latex_block
    inject_latex_block_module = importlib.import_module("latex_injector")
    inject_latex_block = getattr(inject_latex_block_module, "inject_latex_block")

    # ④ 注入 LaTeX block 到 conf.py
    conf_path = PRODUCT_DIR / "conf.py"
    inject_latex_block(conf_path, model, version, doc_type, author, styles)
    print("✔ 已完成 LaTeX 样式注入")

    # ⑤ 构建 latex build 目录
    latex_build_dir = PDF_BUILD_DIR / "latex"
    latex_build_dir.mkdir(parents=True, exist_ok=True)

    # 🔥 清理所有旧 latex 文件，确保目录干净
    clean_latex_dir(latex_build_dir)

    # 拷贝字体 + 图片资源（不复制 .tex）
    copy_static_assets()
    print("✔ 已自动复制字体与图片资源")

    # ⑥ 使用 Sphinx 构建 LaTeX
    run_cmd(
        [
            "sphinx-build",
            "-b", "latex",
            str(PRODUCT_DIR),
            str(latex_build_dir),
        ]
    )

    # ⑦ 明确锁定主 tex 文件：Neoway_{model}_Manual.tex
    main_tex_name = f"Neoway_{model}_Manual.tex"
    tex_file = latex_build_dir / main_tex_name

    if not tex_file.exists():
        available = [p.name for p in latex_build_dir.glob("*.tex")]
        raise FileNotFoundError(
            f"❌ 主 TeX 文件不存在：{main_tex_name}\n"
            f"📄 当前目录的 tex 文件有：{available}"
        )

    print(f"✔ 检测到主 tex 文件：{tex_file.name}")

    print("\n== LaTeX → PDF 编译中 ==")

    # =========== ⑧ 三次编译 ===========
    # pass 1
    run_cmd(["xelatex", "-interaction=nonstopmode", tex_file.name], cwd=latex_build_dir)

    # makeindex（避免 .ind 缺失报错）
    idx_file = tex_file.with_suffix(".idx")
    if idx_file.exists():
        run_cmd(["makeindex", idx_file.name], cwd=latex_build_dir)

    # pass 2
    run_cmd(["xelatex", "-interaction=nonstopmode", tex_file.name], cwd=latex_build_dir)

    # pass 3
    run_cmd(["xelatex", "-interaction=nonstopmode", tex_file.name], cwd=latex_build_dir)

    # ⑨ 复制最终 PDF
    final_pdf = tex_file.with_suffix(".pdf")
    output_pdf = PDF_BUILD_DIR / f"Neoway_{model}_{doc_type.replace(' ', '_')}.pdf"
    output_pdf.write_bytes(final_pdf.read_bytes())

    print(f"\n🎉 PDF 构建成功：{output_pdf}\n")


# ---------------------------------------------------------
# CLI 测试入口
# ---------------------------------------------------------
if __name__ == "__main__":
    build_pdf(
        model="N706B",
        version="v1.0",
        doc_type="AT_Command_Manual",
        author="Neoway Documentation Team",
    )
