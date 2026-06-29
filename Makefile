SHELL   = /bin/sh

FILE0   = main
FORMAT ?= two-columns
TEX_DIR = latex/$(FORMAT)
TEX_TEMPLATE = $(FILE0).template.tex
TEX     = $(FILE0).raw.tex
PDF     = $(FILE0).pdf
COVER   = cover.png
RAW_PDF = $(FILE0).raw.pdf

all: pdf

pdf:
	mkdir -p build/pdf/$(FORMAT)
	cp $(TEX_DIR)/* build/pdf/$(FORMAT)/
	cp data.md build/pdf/$(FORMAT)/
	wget --output-document=build/pdf/$(FORMAT)/img.jpg $$(yq e '.image' data.md | grep https)

	python3 heatmap.py

	mv heatmap.eps build/pdf/$(FORMAT)/

	cd build/pdf/$(FORMAT)/; \
	pandoc data.md --pdf-engine xelatex --template sidebar.template.tex -o sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template $(TEX_TEMPLATE) -o $(TEX) ; \
	xelatex -shell-escape -output-driver="xdvipdfmx -z 0" $(TEX) ; \
    echo "Compresing PDF..."; \
    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -dPrinted=false -sOutputFile=$(PDF) $(RAW_PDF); \
    gs -sDEVICE=png16m -sOutputFile=cover.png -r144 $(RAW_PDF);
	cp build/pdf/$(FORMAT)/$(PDF) ./cv-esteban-martinena-$(FORMAT).pdf
	cp build/pdf/$(FORMAT)/$(COVER) ./cover-$(FORMAT).png

clean-pdf:
	rm -rf build/pdf/

clean:
	rm -rf build/

