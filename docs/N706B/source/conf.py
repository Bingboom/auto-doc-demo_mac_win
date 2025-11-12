# -- Path setup --------------------------------------------------------------

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# -- Project information -----------------------------------------------------

project = 'Neoway N706B AT Command Manual'
author = 'Neoway Documentation Team'
version = 'v1.4'
release = version

# -- General configuration ---------------------------------------------------

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
]

# Templates path
templates_path = ['_templates']

# Source file suffix
source_suffix = '.rst'

# Master document
master_doc = 'index'

# -- LaTeX configuration ----------------------------------------------------

latex_elements = {
    'papersize': 'letter',
    'pointsize': '10pt',

    # LaTeX preamble for additional package inclusions
    'preamble': r'''
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{fontspec}
\setmainfont{Times New Roman}
''',

    # Add MakeIndex package for generating index
    'makeindex': r'\usepackage{makeidx}\makeindex',
    
    # Customize the document class (you can change 'report' to any other class)
    'docclass': 'report',
}

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for PDF output --------------------------------------------------

latex_documents = [
    (master_doc, 'Neoway_N706B_Manual.tex', 'Neoway N706B AT Command Manual', author, 'manual'),
]

# -- Miscellaneous -----------------------------------------------------------

# A list of directories, relative to source, to exclude when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# 自动注入时间：2025-11-13 00:19:31
if 'latex_elements' not in globals():
    latex_elements = {}
latex_engine = 'xelatex'
latex_additional_files = globals().get('latex_additional_files', []) + [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png',
]
latex_documents = [
    ('index', 'Neoway_N706B_Manual.tex', 'Neoway N706B AT 命令手册', 'Neoway 文档工程组', 'manual')
]
latex_elements.update({
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=24pt]{geometry}',
    'fontpkg': r'''
        \usepackage{xeCJK}
        \setCJKsansfont{PingFang SC}
        \setCJKmonofont{PingFang SC}
        \setCJKmainfont{PingFang SC}
        \setmainfont{Times New Roman}
        \setsansfont{Arial}
        \setmonofont{Menlo}
    ''',
    'preamble': r'''
        \usepackage{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}
        \graphicspath{{./}{../../_common/_static/}{_common/_static/}}
        \setlength{\headheight}{24pt}
        \setlength{\headsep}{12pt}
        \hypersetup{
          pdftitle={ Neoway N706B AT 命令手册 },
          pdfauthor={ Neoway 文档工程组 },
          pdfsubject={ Neoway Technology 机密 | N706B | V1.4 },
          colorlinks=true, linkcolor=blue, urlcolor=blue
        }
        \newcommand{\neowayheaderlogo}{\includegraphics[scale=0.25]{header-logo.png}}
    '''
})

