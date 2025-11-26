# ======================================
# 英文语言包
# ======================================

PROJECT_TITLE = "AT Commands Manual"

LABELS = {
    "command_format": "Command Format",
    "parameters": "Parameters",
    "examples": "Examples",
    "note": "Notes",
    "response": "Response",
    "cmd": "Command",
    "timeout_no": "No.",
    "timeout_cmd": "Command",
    "timeout_value": "Timeout (s)",
    "timeout_title": "Command Timeout Table",
}

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

ISSUE = "1.0"
DATE = "2025-11-18"

COMPANY_NAME = "Neoway Technology Co., Ltd. All Rights Reserved."
COVER_TITLE_COLOR = "1F4E78"

CHAPTER_NAME = "Chapter"
SECTION_NAME = "Section"

IS_CHINESE = False
PDF_MAIN_FONT = "Times New Roman"

# =========================================================
# ★ 全新章节格式
# =========================================================
CHAPTER_FORMAT = r"""
\renewcommand{\chaptername}{}
\renewcommand{\thechapter}{\arabic{chapter}}

\definecolor{chaptercolor}{RGB}{20,25,70}

% ------------------------------
% 一级标题：Chapter X
% ------------------------------
\titleformat{\chapter}
  {\color{chaptercolor}\bfseries\huge}
  {Chapter\ \thechapter}
  {1em}
  {}

% 英文页眉
\renewcommand{\chaptermark}[1]{%
  \markboth{Chapter\ \thechapter\ #1}{}%
}

"""
