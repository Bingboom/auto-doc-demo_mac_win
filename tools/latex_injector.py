# latex_injector.py

import re
from datetime import datetime

def create_latex_block(model_name, version, doc_type, author, company="Neoway Technology", zh_font="PingFang SC", mono_font="Menlo", date_cn=None):
    """
    创建用于注入到 Sphinx 配置文件的 LaTeX 配置块

    参数:
        model_name (str): 模型名称
        version (str): 文档版本
        doc_type (str): 文档类型（例如 "AT 命令手册"）
        author (str): 作者
        company (str, 可选): 公司名称，默认是 "Neoway Technology"
        zh_font (str, 可选): 中文字体，默认是 "PingFang SC"
        mono_font (str, 可选): 单一字体，默认是 "Menlo"
        date_cn (str, 可选): 中文日期，默认为当前日期

    返回:
        str: 创建的 LaTeX 配置块
    """
    version_tag = ("V" + version.lstrip("vV")).strip()
    title = f"Neoway {model_name} {doc_type}"
    subject = f"{company} 机密 | {model_name} | {version_tag}"

    block = f"""# 自动注入时间：{datetime.now():%Y-%m-%d %H:%M:%S}
if 'latex_elements' not in globals():
    latex_elements = {{}}
latex_engine = 'xelatex'
latex_additional_files = globals().get('latex_additional_files', []) + [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png',
]
latex_documents = [
    ('index', 'Neoway_{model_name}_Manual.tex', '{title}', '{author}', 'manual')
]
latex_elements.update({{
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=24pt]{{geometry}}',
    'fontpkg': r'''
        \\usepackage{{xeCJK}}
        \\setCJKsansfont{{PingFang SC}}
        \\setCJKmonofont{{PingFang SC}}
        \\setCJKmainfont{{PingFang SC}}
        \\setmainfont{{Times New Roman}}
        \\setsansfont{{Arial}}
        \\setmonofont{{Menlo}}
    ''',
    'preamble': r'''
        \\usepackage{{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}}
        \\graphicspath{{{{./}}{{../../_common/_static/}}{{_common/_static/}}}}
        \\setlength{{\\headheight}}{{24pt}}
        \\setlength{{\\headsep}}{{12pt}}
        \\hypersetup{{
          pdftitle={{ {title} }},
          pdfauthor={{ {author} }},
          pdfsubject={{ {subject} }},
          colorlinks=true, linkcolor=blue, urlcolor=blue
        }}
        \\newcommand{{\\neowayheaderlogo}}{{\\includegraphics[scale=0.25]{{header-logo.png}}}}
    '''
}})
"""
    return block

def inject_latex(conf_path, latex_block):
    """
    将 LaTeX 配置块注入到 Sphinx 配置文件中

    参数:
        conf_path (Path): 配置文件的路径
        latex_block (str): 要注入的 LaTeX 配置块
    
    返回:
        None
    """
    # 读取 conf.py 文件
    conf_txt = conf_path.read_text(encoding="utf-8")
    
    # 定义注入标记
    marker_begin = "# >>> BEGIN: NEOWAY_LATEX_BLOCK"
    marker_end = "# <<< END:  NEOWAY_LATEX_BLOCK"

    # 移除现有的 LaTeX 配置块
    conf_txt = re.sub(rf"{re.escape(marker_begin)}.*?{re.escape(marker_end)}", "", conf_txt, flags=re.DOTALL)
    
    # 在文件末尾添加新的 LaTeX 配置块
    conf_txt = conf_txt.rstrip() + "\n\n" + latex_block + "\n"
    
    # 将修改后的内容写回 conf.py
    conf_path.write_text(conf_txt, encoding="utf-8")
