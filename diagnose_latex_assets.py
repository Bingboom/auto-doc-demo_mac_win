#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
一键诊断 LaTeX 资源丢失问题：
- background.png 找不到
- header-logo.png 找不到
- cover.tex 中路径是否正确
- latex_injector 注入是否成功
- path_utils 计算 ROOT 是否正确
- build/latex 中资源是否被复制
"""

import subprocess, re, sys
from pathlib import Path

print("===== 📘 LaTeX Resource Diagnostic Tool =====")

ROOT = Path(__file__).resolve().parent
print(f"📌 仓库根目录: {ROOT}")

# -------------------------------
# 1. 获取产品线
# -------------------------------
def get_product():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    # fallback from config.yaml
    cfg = (ROOT / "config.yaml").read_text(encoding="utf-8")
    m = re.search(r"default_product:\s*\"([^\"]+)\"", cfg)
    return m.group(1)

product = get_product()
print(f"📦 产品线: {product}")

# -------------------------------
# 2. 构建目录
# -------------------------------
build_latex = ROOT / f"docs/{product}/build/latex"
source_latex_common = ROOT / "docs/_common/_static"

print(f"📁 latex build 目录: {build_latex}")

if not build_latex.exists():
    print("❌ 未找到 build/latex，请先执行 make latexpdf")
    sys.exit(1)

# -------------------------------
# 3. 检查关键文件是否存在
# -------------------------------
background = source_latex_common / "background.png"
logo = source_latex_common / "header-logo.png"

print("\n===== 🔍 检查 _static 下资源 =====")
print(f"background.png: {'✔ 存在' if background.exists() else '❌ 不存在'}")
print(f"header-logo.png: {'✔ 存在' if logo.exists() else '❌ 不存在'}")

# -------------------------------
# 4. 检查 build/latex 中是否被复制
# -------------------------------
print("\n===== 🔍 检查 build/latex 资源复制 =====")
bg_build = build_latex / "background.png"
logo_build = build_latex / "header-logo.png"

print(f"build/background.png: {'✔ 存在' if bg_build.exists() else '❌ 不存在'}")
print(f"build/header-logo.png: {'✔ 存在' if logo_build.exists() else '❌ 不存在'}")

# -------------------------------
# 5. 检查 cover.tex 路径是否正确
# -------------------------------
cover_path = build_latex / "cover.tex"
print("\n===== 🔍 检查 cover.tex =====")
if not cover_path.exists():
    print("❌ cover.tex 未复制到 build/latex")
else:
    txt = cover_path.read_text(encoding="utf-8")
    print("✔ cover.tex 已复制")
    m_bg = re.search(r"\{(.+background\.png)\}", txt)
    print("→ cover.tex 中 background.png 路径: ", m_bg.group(1) if m_bg else "❌ 未找到引用")

# -------------------------------
# 6. 检查 headerfooter.tex 路径
# -------------------------------
header_path = build_latex / "headerfooter.tex"
print("\n===== 🔍 检查 headerfooter.tex =====")
if not header_path.exists():
    print("❌ headerfooter.tex 未复制")
else:
    txt = header_path.read_text(encoding="utf-8")
    m_logo = re.search(r"\{(.+header-logo\.png)\}", txt)
    print("✔ headerfooter.tex 已复制")
    print("→ header-logo.png 路径: ", m_logo.group(1) if m_logo else "❌ 未找到引用")

# -------------------------------
# 7. 检查 path_utils 计算 ROOT 是否正确
# -------------------------------
print("\n===== 🔍 检查 path_utils ROOT 解析 =====")
try:
    import tools.utils.path_utils as PU
    print("path_utils.ROOT =", PU.ROOT)
    print("path_utils.static_images_path =", PU.static_images_path())
    print("path_utils.latex_common_path =", PU.latex_common_path())
except Exception as e:
    print("❌ 无法导入 path_utils:", e)

# -------------------------------
# 8. 检查 latex_injector 注入块是否_
