SHELL   = /bin/sh

FILE0   = main
TEX_TEMPLATE = $(FILE0).template.tex
TEX     = $(FILE0).tex
PDF     = $(FILE0).pdf


all:
	make pdf

pdf:
	mkdir -p build/pdf/
	cp latex/* build/pdf/
	cp data.md build/pdf/
	wget --output-document=build/pdf/img.jpg $$(yq e '.image' data.md | grep https)

	cd build/pdf/; \
	pandoc data.md --pdf-engine xelatex --template page1sidebar.template.tex -o page1sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template page2sidebar.template.tex -o page2sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template $(TEX_TEMPLATE) -o $(TEX) ; \
	xelatex $(TEX)

	cp build/pdf/$(PDF) ./rendered.pdf
	make clean-pdf

clean-pdf:
	rm -rf build/pdf

