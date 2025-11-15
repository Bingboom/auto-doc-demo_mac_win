#!/usr/bin/env python3
# tools/build_pdf.py

import sys
import shutil
import subprocess
from pathlib import Path

# === 自动加入项目根目录 ===
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paths import PATHS
from tools.latex_cover import render_cover
from tools.latex_styles import load_latex_styles
from tools.latex_injector import inject_latex_block


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
    绝不保留任何旧的 tex/aux/log/index 文件。
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
    target = PATHS["build_pdf"] / "latex"
    target.mkdir(parents=True, exist_ok=True)

    latex_dir = PATHS["latex"]
    static_dir = PATHS["images"]

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
    cover_path = render_cover(model, version, doc_type)
    print("✔ 已生成封面：", cover_path)

    # ② 加载 LaTeX 样式（字体、公司名等）
    styles = load_latex_styles()

    # ③ 注入 LaTeX block 到 conf.py
    conf_path = PATHS["rst_source"] / "conf.py"
    inject_latex_block(conf_path, model, version, doc_type, author, styles)
    print("✔ 已完成 LaTeX 样式注入")

    # ④ 构建 latex build 目录
    latex_build_dir = PATHS["build_pdf"] / "latex"
    latex_build_dir.mkdir(parents=True, exist_ok=True)

    # 🔥 清理所有旧 latex 文件，确保目录干净
    clean_latex_dir(latex_build_dir)

    # 拷贝字体 + 图片资源（不复制 .tex）
    copy_static_assets()
    print("✔ 已自动复制字体与图片资源")

    # ⑤ 使用 Sphinx 构建 LaTeX
    run_cmd(
        [
            "sphinx-build",
            "-b", "latex",
            str(PATHS["rst_source"]),
            str(latex_build_dir),
        ]
    )

    # ⑥ 明确锁定主 tex 文件：Neoway_{model}_Manual.tex
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

    # =========== ⑦ 三次编译 ===========
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

    # ⑧ 复制最终 PDF
    final_pdf = tex_file.with_suffix(".pdf")
    output_pdf = PATHS["build_pdf"] / f"Neoway_{model}_{doc_type.replace(' ', '_')}.pdf"
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
