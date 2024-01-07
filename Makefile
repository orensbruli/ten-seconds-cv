SHELL   = /bin/sh

FILE0   = main
TEX_TEMPLATE = $(FILE0).template.tex
TEX     = $(FILE0).tex
XDV     = $(FILE0).xdv
PDF     = $(FILE0).pdf
PDFOUT  = $(FILE0)-encrypted.pdf


all:
	make tex

tex:
	xelatex -no-pdf $(TEX)
	xelatex -no-pdf $(TEX)
	#xdvipdfmx.exe $(XDV)
	xelatex $(TEX)
	make clean
pw:
	pdftk $(PDF) output $(PDFOUT) owner_pw ownerpasswd user_pw userpasswd compress encrypt_128bit

help:
	echo "USAGE: make [all/tex/handout/pw/clean]"

clean:
	rm -f *.aux *.dvi *.idx *.ilg *.ind *.log *.nav *.out *.snm *.xdv *.toc *.synctex.gz *~

pdf:
	mkdir -p build/pdf/
	cp latex/* build/pdf/
	cp data.md build/pdf/
	wget --output-document=build/pdf/img.jpg  https://lh3.googleusercontent.com/u/0/drive-viewer/AEYmBYRh5Ban9xwmHesxqfizee_30j4WBP55CTzwW_GOZOMLVlTaA3wK_kPcIFl4j0SaqsuJB5IlPMl5xCuj-itvlzjLBiYp
	cd build/pdf && pandoc data.md --pdf-engine xelatex --template $(TEX_TEMPLATE) -o $(TEX)
	cd build/pdf && pandoc data.md --pdf-engine xelatex --template page1sidebar.template.tex -o page1sidebar.tex
	cd build/pdf && pandoc data.md --pdf-engine xelatex --template page2sidebar.template.tex -o page2sidebar.tex
	cd build/pdf && xelatex -no-pdf $(TEX)
	cd build/pdf && xelatex $(TEX)
	cp build/pdf/$(PDF) ./rendered.pdf
	make clean

clean-pdf:
	rm -rf build/pdf

