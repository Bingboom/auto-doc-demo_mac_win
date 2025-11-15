import os

def check_latex_render(latex_path):
    """
    检查 LaTeX 文件中的文本对齐问题，特别是封面部分的左对齐。
    """
    if not os.path.exists(latex_path):
        print(f"文件 {latex_path} 不存在!")
        return

    with open(latex_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 查找并检查是否使用了 `flushleft` 或 `center` 环境
    if '\\begin{flushleft}' in content and '\\end{flushleft}' in content:
        print("警告：使用了 'flushleft' 环境，确保排版没有被其他元素影响")
    elif '\\begin{center}' in content and '\\end{center}' in content:
        print("警告：使用了 'center' 环境，可能导致内容居中而不是左对齐")
    else:
        print("没有显式使用 flushleft 或 center，可能排版依赖其他布局环境")

    # 检查是否有多余的空格或换行符
    if '\\vspace' in content:
        print("警告：使用了 \\vspace，可能导致文本之间的间距不一致")
    else:
        print("没有使用 \\vspace，排版应该较为紧凑")

    # 检查是否在标题前后使用了多余的换行符
    if '\\\\' in content:
        print("警告：使用了多余的换行符 '\\\\'，可能导致行间距不一致")
    else:
        print("标题之间的行间距应该是合适的")

    # 检查字体大小是否一致
    if '\\fontsize' in content:
        print("警告：使用了 \\fontsize，可能导致字体大小不一致")
    else:
        print("字体大小应该保持一致")

def diagnose_latex_project(root_path):
    """
    扫描项目根目录中的所有 LaTeX 文件，检查封面对齐问题。
    """
    latex_files = []
    
    # 遍历根目录查找 .tex 文件
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.tex'):
                latex_files.append(os.path.join(root, file))

    if latex_files:
        for latex_file in latex_files:
            print(f"正在检查文件: {latex_file}")
            check_latex_render(latex_file)
    else:
        print("未找到 LaTeX 文件，请确保项目目录中包含 .tex 文件")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))  # 当前目录作为项目根目录
    diagnose_latex_project(project_root)
