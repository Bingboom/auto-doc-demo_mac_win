#!/usr/bin/env python3
from tools.render_rst import *
import subprocess
from pathlib import Path
import sys
from render_rst import render_rst_for_model

def build_docs(model: str = "N706B", lang: str = "zh_CN"):
    root = Path(__file__).resolve().parents[1]
    render_rst_for_model(root, model)

    conf_dir = root / "docs" / model
    src_dir = conf_dir / "source"
    build_dir = conf_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    print(f"📘 正在构建 {model} PDF ...")
    subprocess.run([
        "sphinx-build",
        "-b", "pdf",
        "-c", str(conf_dir),
        str(src_dir),
        str(build_dir)
    ], check=True)
    print(f"🎉 构建完成: {build_dir}/Neoway_{model}_AT_Commands_Manual.pdf")

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "N706B"
    lang = sys.argv[2] if len(sys.argv) > 2 else "zh_CN"
    build_docs(model, lang)
