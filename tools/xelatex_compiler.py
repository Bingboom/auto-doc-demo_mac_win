import subprocess
import os

def compile_xelatex(latex_dir):
    os.chdir(latex_dir)
    tex_main = next(latex_dir.glob("*.tex"))
    for i in range(2):
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)
