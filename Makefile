PYTHON = python3

help:
	@echo "make all        # 构建全部 model × 全语言"
	@echo "make html       # 同上"
	@echo "make pdf        # 同上"

all:
	$(PYTHON) tools/build_docs.py

html:
	$(PYTHON) tools/build_docs.py

pdf:
	$(PYTHON) tools/build_docs.py

# 单产品单语言调试命令
# 例如：
#    make build PRODUCT=N706B LANG=zh_CN
build:
	$(PYTHON) tools/build_docs.py $(PRODUCT) $(LANG)
