import subprocess

def build_latex_from_sphinx(project_dir, latex_dir):
    subprocess.run(["sphinx-build", "-b", "latex", str(project_dir), str(latex_dir)], check=True)
