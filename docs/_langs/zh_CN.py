# ====================================
# Language Pack: zh_CN
# ====================================

FIELD_MAP = {
    "章节名称": "章节名称_en",
    "命令标题": "命令标题_en",
    "功能描述": "功能描述_en",
    "示例命令": "示例命令_en",
    "备注": "备注_en",
    "响应校正": "响应校正_en",
    "参数": "参数_en",
    "参数json": "参数json_en",
}

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
