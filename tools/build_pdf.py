# -*- coding: utf-8 -*-
"""
📘 build_pdf.py – 模块化 PDF 构建器（集成 LaTeX 样式注入）
Usage:
  python tools/build_pdf.py
"""

from pathlib import Path
from datetime import datetime
import subprocess
import argparse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

# 导入 LaTeX 注入模块
from tools.latex_inject import inject_latex_style, CONF_PATH

# ====== 基本路径 ======
BASE = Path(__file__).resolve().parents[1]
COMMON = BASE / "docs" / "_common"
TEMPLATE_DIR = COMMON / "templates" / "pdf"
STATIC_DIR = COMMON / "_static"
OUTPUT_DIR = BASE / "docs" / "N706B" / "build" / "pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HTML_SOURCE = BASE / "docs" / "N706B" / "build" / "html" / "index.html"

# ====== 元信息配置 ======
META = {
    "project_name": "Neoway N706B AT 命令手册",
    "subtitle": "AT Command Manual – V1.4",
    "author": "文档工程组",
    "version": "V1.4",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "year": datetime.now().year,
    "company": "深圳市有方科技股份有限公司",
    "logo_path": str((STATIC_DIR / "header-logo.png").resolve()),
    "history": ["V1.0 初版", "V1.2 增加 NB 命令", "V1.4 优化章节结构"],
}

# ====== 构建函数 ======
def render_template(name: str, context: dict) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    return env.get_template(name).render(**context)


def build_pdf(include_cover=True, include_version=True, include_license=True):
    print("🧩 Step 1: 注入 LaTeX 样式 …")
    inject_latex_style(CONF_PATH)
    print("✅ LaTeX 样式注入完成。")

    print("🧩 Step 2: 构建 Sphinx → LaTeX …")
    PROJECT_DIR = BASE / "docs" / "N706B" / "source"
    LATEX_DIR = BASE / "docs" / "N706B" / "build" / "latex"
    subprocess.run(
        ["sphinx-build", "-b", "latex", str(PROJECT_DIR), str(LATEX_DIR)],
        check=True,
    )

    print("🧩 Step 3: 生成 PDF 成品 …")

    html_content = HTML_SOURCE.read_text(encoding="utf-8")
    parts = []
    if include_cover:
        parts.append(render_template("cover_page.j2", META))
    if include_version:
        parts.append(render_template("version_page.j2", META))
    if include_license:
        parts.append(render_template("license_page.j2", META))
    parts.append(html_content)

    final_html = "\n".join(parts)
    css_path = STATIC_DIR / "pdf_style.css"
    output_file = OUTPUT_DIR / f"Neoway_N706B_AT_命令手册_{META['version']}.pdf"

    HTML(string=final_html, base_url=str(BASE)).write_pdf(
        str(output_file), stylesheets=[CSS(filename=str(css_path))]
    )
    print(f"✅ PDF 生成成功：{output_file}")


# ====== CLI ======
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--no-cover", action="store_true")
    p.add_argument("--no-version", action="store_true")
    p.add_argument("--no-license", action="store_true")
    args = p.parse_args()

    build_pdf(
        include_cover=not args.no_cover,
        include_version=not args.no_version,
        include_license=not args.no_license,
    )
