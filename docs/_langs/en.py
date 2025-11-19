# ====================================
# Language Pack: en
# ====================================

PROJECT_TITLE = "AT Commands Manual"
ISSUE = "1.0"
DATE  = "2025-11-18"

COMPANY_NAME = "Neoway Technology Co., Ltd. All Rights Reserved."
COVER_TITLE_COLOR = "1F4E78"

CHAPTER_NAME = "Chapter"
SECTION_NAME = "Section"

IS_CHINESE = False
PDF_MAIN_FONT = "Times New Roman"

# 英文保持 Chapter，但数字统一阿拉伯数字
CHAPTER_FORMAT = r"""
\renewcommand{\chaptername}{Chapter}
\renewcommand{\thechapter}{\arabic{chapter}}

\titleformat{\chapter}
  {\Huge\bfseries}
  {\chaptername\ \thechapter}
  {1em}
  {}

\renewcommand{\chaptermark}[1]{%
  \markboth{\chaptername\ \thechapter\ #1}{}%
}
"""
