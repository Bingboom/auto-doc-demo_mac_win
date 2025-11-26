# ====================================
# Language Pack: zh_CN
# ====================================

PROJECT_TITLE = "AT 命令手册"

LABELS = {
    "command_format": "命令格式",
    "parameters": "参数",
    "examples": "命令示例",
    "note": "说明",
    "response": "响应",
    "cmd": "命令",
    "timeout_no": "序号",
    "timeout_cmd": "命令",
    "timeout_value": "超时时间（秒）",
    "timeout_title": "常用命令超时时间表",
}

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

ISSUE = "1.0"
DATE  = "2025-11-18"

COMPANY_NAME = "深圳市有方科技股份有限公司 版权所有"
COVER_TITLE_COLOR = "70AD47"

CHAPTER_NAME  = "第{number}章"
SECTION_NAME  = "节"

IS_CHINESE = True
PDF_MAIN_FONT = "SimSun"

# =========================================================
# ★ 全新章节格式
# =========================================================
CHAPTER_FORMAT = r"""
\usepackage{titlesec}
\usepackage{xcolor}

% 蓝黑色
\definecolor{chaptercolor}{RGB}{20,25,70}

% ------------------------------
% 一级标题：第X章（中号）
% ------------------------------
\titleformat{\chapter}
  {\color{chaptercolor}\bfseries\huge}
  {第\thechapter 章}
  {1em}
  {}

% =====================================================
%   页眉（Header）格式 → 中文必须保持原样
% =====================================================
\renewcommand{\chaptermark}[1]{%
  \markboth{第\thechapter 章\ #1}{}%
}

"""
