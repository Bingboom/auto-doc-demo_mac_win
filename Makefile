.PHONY: pdf all

pdf:
	python tools/build_docs.py N706B zh_CN

all:
	python tools/build_docs.py N706B zh_CN
	python tools/build_docs.py N725 zh_CN
