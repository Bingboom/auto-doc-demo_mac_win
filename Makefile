.PHONY: init html pdf clean

init:
	python -m pip install -U pip
	pip install -r requirements.txt

html:
	python tools/build_docs.py

pdf:
	python tools/build_pdf.py

pdf-no-cover:
	python tools/build_pdf.py --no-cover

clean:
	rm -rf docs/**/build
