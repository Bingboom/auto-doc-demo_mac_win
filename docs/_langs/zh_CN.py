# ====================================
# Language Pack: zh_CN
# ====================================

PROJECT_TITLE = "AT命令手册"
ISSUE = "1.0"
DATE  = "2025-11-18"

COMPANY_NAME = "深圳市有方科技股份有限公司 版权所有"
COVER_TITLE_COLOR = "70AD47"

CHAPTER_NAME  = "第{number}章"
SECTION_NAME  = "节"

IS_CHINESE = True
PDF_MAIN_FONT = "SimSun"

# 中文章节首页 & 页眉控制
CHAPTER_FORMAT = r"""
\renewcommand{\chaptername}{}
\renewcommand{\thechapter}{\arabic{chapter}}

\titleformat{\chapter}
  {\Huge\bfseries}
  {第\thechapter 章}
  {1em}
  {}

\renewcommand{\chaptermark}[1]{%
  \markboth{第\thechapter 章\ #1}{}%
}
"""
