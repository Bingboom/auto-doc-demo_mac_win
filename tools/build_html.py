#!/usr/bin/env python3
"""
📘 Neoway Build HTML v1.3 — 快速构建 Sphinx HTML
仅执行 Sphinx HTML 构建，不重新渲染 RST。
"""

import subprocess
import sys
from pathlib import Path
import shutil
import webbrowser

def build_html(model: str = "N706B", clean: bool = False, open_browser: bool = False):
    # === 路径定义 ===
    root = Path(__file__).resolve().parents[1]
    conf_dir = root / "docs" / model / "source"
    src_dir = conf_dir
    build_dir = root / "docs" / model / "build" / "html"

    # === 清理旧构建 ===
    if clean and build_dir.exists():
        print(f"🧹 清理旧 HTML 构建目录：{build_dir}")
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    # === 执行 sphinx-build ===
    print(f"🌐 构建 {model} HTML 文档中...")
    subprocess.run([
        "sphinx-build",
        "-b", "html",
        "-c", str(conf_dir),   # 指定 conf.py 所在目录
        str(src_dir),
        str(build_dir)
    ], check=True)

    print(f"✅ 构建完成：{build_dir}/index.html")

    if open_browser:
        webbrowser.open_new_tab(str(build_dir / "index.html"))
        print("🌈 已在浏览器中打开。")


if __name__ == "__main__":
    args = sys.argv[1:]
    model = args[0] if args and not args[0].startswith("--") else "N706B"
    clean = "--clean" in args
    open_browser = "--open" in args
    build_html(model, clean, open_browser)
