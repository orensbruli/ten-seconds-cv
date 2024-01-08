SHELL   = /bin/sh

FILE0   = main
TEX_TEMPLATE = $(FILE0).template.tex
TEX     = $(FILE0).tex
PDF     = $(FILE0).pdf

all: pdf

pdf:
	mkdir -p build/pdf/
	cp latex/* build/pdf/
	cp data.md build/pdf/
	wget --output-document=build/pdf/img.jpg $$(yq e '.image' data.md | grep https)

	cd build/pdf/; \
	pandoc data.md --pdf-engine xelatex --template page1sidebar.template.tex -o page1sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template page2sidebar.template.tex -o page2sidebar.tex ; \
	pandoc data.md --pdf-engine xelatex --template $(TEX_TEMPLATE) -o $(TEX) ; \
	xelatex -shell-escape -output-driver="xdvipdfmx -z 0" $(TEX)

	cp build/pdf/$(PDF) ./rendered.pdf

clean-pdf:
	rm -rf build/pdf/

clean:
	rm -rf build/

