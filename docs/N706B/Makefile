# ===============================================
#  Sphinx Makefile for Neoway Auto-Doc Project
# ===============================================

# 当前目录
SPHINX_PROJ = N706B
SOURCEDIR = source
BUILDDIR = build

# Python 环境
PYTHON ?= python3

# Sphinx 命令
SPHINXBUILD   = $(PYTHON) -m sphinx
SPHINXOPTS    =

.PHONY: help clean html latexpdf

help:
	@echo "Available targets:"
	@echo "   make html       - Build HTML documentation"
	@echo "   make latexpdf   - Build LaTeX and PDF"
	@echo "   make clean      - Clean all build output"

clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

latexpdf:
	$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS)
	@echo "===> Running xelatex..."
	@cd "$(BUILDDIR)/latex" && xelatex -interaction=nonstopmode *.tex && xelatex -interaction=nonstopmode *.tex
	@echo "✔ PDF 生成完成，输出路径:"
	@ls -1 "$(BUILDDIR)/latex"/*.pdf
