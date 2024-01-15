SHELL   = /bin/sh

FILE0   = main
TEX_TEMPLATE = $(FILE0).template.tex
TEX     = $(FILE0).raw.tex
PDF     = $(FILE0).pdf
RAW_PDF = $(FILE0).raw.pdf

all: pdf

pdf:
	mkdir -p build/pdf/
	cp latex/* build/pdf/
	cp data.md build/pdf/
	wget --output-document=build/pdf/img.jpg $$(yq e '.image' data.md | grep https)

	python3 heatmap.py

	mv heatmap.eps build/pdf/

	cd build/pdf/; \
	pandoc data.md --pdf-engine xelatex --template sidebar.template.tex -o sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template $(TEX_TEMPLATE) -o $(TEX) ; \
	xelatex -shell-escape -output-driver="xdvipdfmx -z 0" $(TEX) ; \
    echo "Compresing PDF..."; \
    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -dPrinted=false -sOutputFile=$(PDF) $(RAW_PDF)
	cp build/pdf/$(PDF) ./rendered.pdf

clean-pdf:
	rm -rf build/pdf/

clean:
	rm -rf build/

