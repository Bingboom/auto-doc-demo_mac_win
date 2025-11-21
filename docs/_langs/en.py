# ======================================
# 英文语言包
# ======================================

# 字段映射：使用 *_n 字段，如果不存在，render_rst.py 会 fallback
FIELD_MAP = {
    "章节名称": "章节名称",
    "命令标题": "命令标题",
    "功能描述": "功能描述",
    "示例命令": "示例命令",
    "备注": "备注",
    "响应校正": "响应校正",
    "参数": "参数",
    "参数json": "参数json",
}

PROJECT_TITLE = "AT Commands Manual"
ISSUE = "1.0"
DATE = "2025-11-18"

COMPANY_NAME = "Neoway Technology Co., Ltd. All Rights Reserved."
COVER_TITLE_COLOR = "1F4E78"

CHAPTER_NAME = "Chapter"
SECTION_NAME = "Section"

IS_CHINESE = False
PDF_MAIN_FONT = "Times New Roman"

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
